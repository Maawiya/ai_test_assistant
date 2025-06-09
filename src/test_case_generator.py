import pandas as pd
import os


def generate_test_case(func_name, num_args):
    """
    Generate simple unit test cases based on function name and argument count.
    """
    arg_list = [f"arg{i}" for i in range(num_args)]
    call = f"{func_name}({', '.join(arg_list)})"

    return f"""
    def test_{func_name}(self):
        # TODO: Replace placeholder arguments and expected value
        result = {call}
        self.assertIsNotNone(result)  # Replace with actual checks
    """


def generate_tests_from_csv(csv_path="data/function_features.csv", output_path="tests/test_generated.py"):
    df = pd.read_csv(csv_path)

    test_code = [
        "import unittest",
        "from target_module import *  # Replace with your module"
    ]

    test_code.append("\nclass GeneratedTests(unittest.TestCase):")

    for _, row in df.iterrows():
        func_name = row.get("name")
        num_args = int(row.get("num_args", 0))
        if isinstance(func_name, str) and func_name.isidentifier():
            test_code.append(generate_test_case(func_name, num_args))

    # Ensure test directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write to test file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(test_code))

    print(f"Test cases generated and saved to {output_path}")


if __name__ == "__main__":
    generate_tests_from_csv()
