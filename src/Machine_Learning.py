import numpy as np
import pandas as pd
import sys, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

src = os.path.dirname(os.path.realpath(__file__))
root = os.path.dirname(src)
sys.path.append(src)
sys.path.append(root)
data_file = os.path.abspath(os.path.join(root, 'data','train.csv'))
MIN_PROB=0.4
N_CLUSTERS = 5  

def predict_on_database(df, train_csv_path=data_file):
    """
    Predicts fake news labels and probabilities for articles in a database using a trained model.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the articles to predict.
    - train_csv_path (str): Path to the CSV file containing the training dataset.
    """
    global MIN_PROB
    train_df = pd.read_csv(train_csv_path)
    y_train = train_df.fake_value
    x_train = train_df["text"]
    tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_df=0.8)
    tfidf_train = tfidf_vectorizer.fit_transform(x_train)
    pac = PassiveAggressiveClassifier(max_iter=500)
    pac.fit(tfidf_train, y_train)
    x_test = df["text"]
    tfidf_test = tfidf_vectorizer.transform(x_test)
    y_pred = pac.predict(tfidf_test)
    y_prob = pac.decision_function(tfidf_test)
    probabilities = 1 / (1 + np.exp(-y_prob))
    df["fake_value"] = y_pred
    df["confidence"] = probabilities
    for i, conf in enumerate(df["confidence"]):
        if conf < MIN_PROB and  df.iloc[i,-2]=="FAKE":
            df.iloc[i,-2]="REAL"
    
    real_count = np.sum(df["fake_value"] == "REAL")
    print("REAL Count =", real_count)
    fake_count = np.sum(df["fake_value"] == "FAKE")
    print("FAKE Count =", fake_count)

    return df



def predict_on_database_semi_sup(df, train_csv_path=data_file):
    """
    Predicts fake news labels for articles in a database using both supervised and unsupervised models.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the articles to predict.
    - train_csv_path (str): Path to the CSV file containing the training dataset.
    """
    global MIN_PROB

    # Load training data
    train_df = pd.read_csv(train_csv_path)
    y_train = train_df.fake_value
    x_train = train_df["text"]

    # Split the training data for validation
    x_train_split, x_val_split, y_train_split, y_val_split = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

    # TF-IDF Vectorizer for supervised learning
    tfidf_vectorizer_supervised = TfidfVectorizer(stop_words="english", max_df=0.8)
    tfidf_train_supervised = tfidf_vectorizer_supervised.fit_transform(x_train_split)
    tfidf_val_supervised = tfidf_vectorizer_supervised.transform(x_val_split)

    # Passive Aggressive Classifier for supervised learning
    pac_supervised = PassiveAggressiveClassifier(max_iter=500)
    pac_supervised.fit(tfidf_train_supervised, y_train_split)

    # Predict fake news labels using supervised model on validation set
    y_pred_val_supervised = pac_supervised.predict(tfidf_val_supervised)

    # TF-IDF Vectorizer for unsupervised learning
    tfidf_vectorizer_unsupervised = TfidfVectorizer(stop_words="english", max_df=0.8)
    tfidf_train_unsupervised = tfidf_vectorizer_unsupervised.fit_transform(x_train_split)

    # K-means clustering for unsupervised learning
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42)
    pipeline = make_pipeline(tfidf_vectorizer_unsupervised, kmeans)
    train_clusters = pipeline.fit_predict(x_train_split)

    # Add cluster information to the training data
    train_df_split = train_df.loc[train_df.index.isin(y_val_split.index)]
    train_df_split['cluster'] = train_clusters

    # Combine predictions using stacking with Logistic Regression as meta-model
    X_stack = np.column_stack((y_pred_val_supervised, train_clusters))
    meta_model = LogisticRegression()
    meta_model.fit(X_stack, y_val_split)

    # Apply clustering to test data
    x_test = df["text"]
    tfidf_test_supervised = tfidf_vectorizer_supervised.transform(x_test)
    tfidf_test_unsupervised = tfidf_vectorizer_unsupervised.transform(x_test)

    # Predict fake news labels using supervised model on test set
    y_pred_test_supervised = pac_supervised.predict(tfidf_test_supervised)

    # Predict cluster labels using unsupervised model
    test_clusters = pipeline.predict(x_test)

    # Combine predictions using stacking with Logistic Regression as meta-model
    X_test_stack = np.column_stack((y_pred_test_supervised, test_clusters))
    df["fake_value_combined"] = meta_model.predict(X_test_stack)

    # Print counts for each label
    real_count = np.sum(df["fake_value_combined"] == "REAL")
    print("REAL Count =", real_count)
    fake_count = np.sum(df["fake_value_combined"] == "FAKE")
    print("FAKE Count =", fake_count)

    return df