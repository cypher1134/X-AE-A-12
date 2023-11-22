import FN
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Test on the same database of training should get a 100% accuracy
predicted_full_train_df = FN.predict_on_database("../data/train.csv", "../data/train.csv")

# Calculate accuracy on full training data
accuracy_full_train = accuracy_score(predicted_full_train_df["fake_value"], pd.read_csv("../data/train.csv",10000)["fake_value"])
print(f"Accuracy on full training data: {accuracy_full_train * 100:.2f}%")

# Load the full training dataset
full_train_df = pd.read_csv("../data/train.csv")

# Split the training dataset into train and test sets
partial_train_df, partial_test_df = train_test_split(full_train_df, test_size=0.4, random_state=42)

# Save the smaller training and test datasets to new files
partial_train_df.to_csv("../data/partial_train.csv", index=False)
partial_test_df.to_csv("../data/partial_test.csv", index=False)

# Test on the partial test dataset
predicted_partial_test_df = FN.predict_on_database("../data/partial_test.csv", "../data/partial_train.csv")

# Calculate accuracy on partial test data
accuracy_partial_test = accuracy_score(predicted_partial_test_df["fake_value"], pd.read_csv("../data/partial_test.csv")["fake_value"])
print(f"Accuracy on partial test data: {accuracy_partial_test * 100:.2f}%")
