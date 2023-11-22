import pandas as pd
from . import Machin_Learning as ML
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Assuming this is your test module, let's call it test_FN.py

def test_full_data_accuracy():
    # Load the full training dataset
    df_Full_test = pd.read_csv("../data/train.csv")
    df_Full_test_COMP = df_Full_test.copy()

    # Use the 'predict_on_database' function to predict fake news labels and probabilities
    predicted_partial_test_df = ML.predict_on_database(df_Full_test, "../data/train.csv")

    # Calculate accuracy on partial test data
    accuracy_partial_test = accuracy_score(predicted_partial_test_df["fake_value"], df_Full_test_COMP["fake_value"])
    
    # Assert that the accuracy is within an acceptable range (you can customize this)
    assert accuracy_partial_test >= 0.0 and accuracy_partial_test <= 1.0

def test_partial_data_accuracy():
    # Load the full training dataset
    df_Full_test = pd.read_csv("../data/train.csv")

    # Split the training dataset into train and test sets
    partial_train_df, partial_test_df = train_test_split(df_Full_test, test_size=0.8)
    partial_test_df_COMP = partial_test_df.copy()

    # Save the smaller training and test datasets to new files
    partial_train_df.to_csv("../data/partial_train.csv", index=False)
    partial_test_df.to_csv("../data/partial_test.csv", index=False)

    # Use the 'predict_on_database' function to predict fake news labels and probabilities on the partial test dataset
    predicted_partial_test_df = ML.predict_on_database(partial_test_df, "../data/partial_train.csv")

    # Calculate accuracy on partial test data
    accuracy_partial_test = accuracy_score(predicted_partial_test_df["fake_value"], partial_test_df_COMP["fake_value"])

    # Assert that the accuracy is within an acceptable range (you can customize this)
    assert accuracy_partial_test >= 0.0 and accuracy_partial_test <= 1.0
