import ast
import os
import pandas as pd


def get_function_features(function_node):
    """
    Extract structural features from a Python function node (AST).
    """
    features = {
        "name": function_node.name,
        "length": len(function_node.body),
        "num_args": len(function_node.args.args),
        "num_returns": sum(isinstance(n, ast.Return) for n in ast.walk(function_node)),
        "num_if": sum(isinstance(n, ast.If) for n in ast.walk(function_node)),
        "num_for": sum(isinstance(n, ast.For) for n in ast.walk(function_node)),
        "num_while": sum(isinstance(n, ast.While) for n in ast.walk(function_node)),
        "max_depth": get_max_depth(function_node)
    }
    return features


def get_max_depth(node, level=0):
    """
    Recursively computes the maximum nesting depth of a function.
    """
    if not hasattr(node, "body") or not isinstance(node.body, list):
        return level
    return max([get_max_depth(n, level + 1) for n in node.body] + [level])


def analyze_file(file_path):
    """
    Analyze one Python file and return a list of features for each function.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    return [get_function_features(func) for func in functions]


def analyze_directory(directory):
    """
    Analyze all Python files in the given directory and export features to CSV.
    """
    all_features = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                try:
                    funcs = analyze_file(full_path)
                    for func in funcs:
                        func["file"] = file
                        all_features.append(func)
                except Exception as e:
                    print(f"[ERROR] {file}: {e}")

    if all_features:
        df = pd.DataFrame(all_features)
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/function_features.csv", index=False)
        print("Features extracted and saved to data/function_features.csv")
    else:
        print("No functions found to analyze.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract features from Python files.")
    parser.add_argument("--src", type=str, default="data/raw_code", help="Path to directory with .py files")
    args = parser.parse_args()

    analyze_directory(args.src)
