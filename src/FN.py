import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import data

def predict_on_database(df, train_csv_path="./data/train.csv"):
    """
    Predicts fake news labels and probabilities for articles in a database using a trained model.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the articles to predict.
    - train_csv_path (str): Path to the CSV file containing the training dataset.
    """
    # Load the training dataset
    train_df = pd.read_csv(train_csv_path)

    # Get the labels for training
    y_train = train_df.fake_value

    # Use the entire training dataset
    x_train = train_df["text"]

    # Initialize a TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_df=0.8)

    # Fit and transform the train set
    tfidf_train = tfidf_vectorizer.fit_transform(x_train)

    # Initialize a PassiveAggressiveClassifier
    pac = PassiveAggressiveClassifier(max_iter=500)
    pac.fit(tfidf_train, y_train)

    # Predict on the database
    x_test = df["text"]
    tfidf_test = tfidf_vectorizer.transform(x_test)
    y_pred = pac.predict(tfidf_test)
    y_prob = pac.decision_function(tfidf_test)

    # Convert decision function scores to probabilities using the logistic function
    probabilities = 1 / (1 + np.exp(-y_prob))

    # Update the database with predictions and probabilities
    df["fake_value"] = y_pred
    df["confidence"] = probabilities # Use the probability for the "FAKE" class

    # Convert 'confidence' column to numeric
    df["confidence"] = pd.to_numeric(df["confidence"])
    print(df)
    for i,conf in enumerate(df["confidence"]):
        if pd.to_numeric(conf) < 0.4 and  df["fake_value"].iloc[i]=="FAKE":
            df.iloc[i, -2]="REAL"
    # Set "fake" value to True for rows where confidence is smaller than 0.2
    

    # Display the count of REAL and FAKE instances
    real_count = np.sum(y_pred == "REAL")
    print("REAL Count =", real_count)
    fake_count = np.sum(y_pred == "FAKE")
    print("FAKE Count =", fake_count)

    # Display the updated database with confidence
    # print("Updated Database with Confidence:")
    # print(df)

    return df

# Example usage
# df_to_predict = ...  # Provide the DataFrame you want to predict on
# predicted_df = predict_on_database(df_to_predict)