from flask import Flask, request, jsonify
import ast
import joblib
import pandas as pd
from src.feature_extractor import get_function_features, get_max_depth
import tempfile
import os

app = Flask(__name__)

# Load trained model
model = joblib.load("models/rf_model.pkl")


def extract_features_from_code(code):
    try:
        tree = ast.parse(code)
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        extracted = []
        for func in functions:
            feats = get_function_features(func)
            feats["file"] = "submitted_code"
            extracted.append(feats)
        return extracted
    except Exception as e:
        return str(e)


@app.route("/analyze", methods=["POST"])
def analyze():
    content = request.get_json()
    code = content.get("code")

    if not code:
        return jsonify({"error": "Missing code"}), 400

    features = extract_features_from_code(code)
    if isinstance(features, str):
        return jsonify({"error": features}), 500

    df = pd.DataFrame(features)
    X = df.drop(columns=["name", "file"], errors='ignore')
    df["risk_prediction"] = model.predict(X)

    return jsonify(df[["name", "risk_prediction"]].to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
