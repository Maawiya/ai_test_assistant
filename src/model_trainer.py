import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os


def train_model(csv_path="data/function_features.csv", model_output="models/rf_model.pkl"):
    # Load the dataset
    df = pd.read_csv(csv_path)

    # Drop non-numeric columns (e.g., 'name', 'file')
    X = df.drop(columns=["name", "file"], errors='ignore')
    y = df["label"] if "label" in df.columns else None

    if y is None:
        raise ValueError("The dataset must contain a 'label' column (0 = OK, 1 = buggy).")

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate the model
    y_pred = clf.predict(X_test)
    print("\n Classification Report:\n")
    print(classification_report(y_test, y_pred))

    # Save the model
    os.makedirs(os.path.dirname(model_output), exist_ok=True)
    joblib.dump(clf, model_output)
    print(f"\n Model saved to {model_output}")


if __name__ == "__main__":
    train_model()
