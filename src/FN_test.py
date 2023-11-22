import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import FN  # Assuming this is a module you've defined


# Load the full training dataset
df_Full_test = pd.read_csv("../data/train.csv")

# Split the training dataset into train and test sets
partial_train_df, partial_test_df = train_test_split(df_Full_test, test_size=0.8 )
partial_test_df_cmp=partial_test_df.copy()

# Save the smaller training and test datasets to new files
partial_train_df.to_csv("../data/partial_train.csv", index=False)
partial_test_df.to_csv("../data/partial_test.csv", index=False)

# Test on the partial test dataset
predicted_partial_test_df = FN.predict_on_database(partial_test_df, "../data/partial_train.csv")

# Calculate accuracy on partial test data
accuracy_partial_test = accuracy_score(predicted_partial_test_df["fake_value"], partial_test_df_cmp["fake_value"])
print(f"Accuracy on partial test data: {accuracy_partial_test * 100:.2f}%")