import numpy as np
import pandas as pd
import sys,os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
src = os.path.dirname(os.path.realpath(__file__))
root = os.path.dirname(src)
sys.path.append(src)
sys.path.append(root)
data_file = os.path.abspath(os.path.join(root, 'data','train.csv'))
MIN_PROB=0.4

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

