import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import data


def predict_on_database(db_path="../data/scrap.db", train_csv_path="../data/train.csv"):
    """
    Predicts fake news labels for articles in a database using a trained model.

    Parameters:
    - db_path (str): Path to the database file.
    - train_csv_path (str): Path to the CSV file containing the training dataset.
    """
    # Load the database
    data.db_thread(db_path)

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
    test_df = data.raw_data
    x_test = test_df["text"]
    tfidf_test = tfidf_vectorizer.transform(x_test)
    y_pred = pac.predict(tfidf_test)

    # Update the database with predictions
    test_df["fake_value"] = y_pred

    # Display the count of REAL instances
    real_count = np.sum(y_pred == "REAL")
    print("REAL Count =", real_count)
    fake_count = np.sum(y_pred == "FAKE")
    print("FAKE Count =", fake_count)

    # Display the updated database
    # print("Updated Database:")
    # print(test_df)
    return test_df

# Call the function to make predictions on the database
predict_on_database()
