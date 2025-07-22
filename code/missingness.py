"""
Missingness Analysis Module

This script analyzes each column of a pandas DataFrame (or CSV file) and generates a report where each row is a column from the dataframe, and the columns are: Column Name, % Missing, Imputation Method, Data Type, Reason.
"""

import pandas as pd
import sys
import os


def analyze_missingness(df: pd.DataFrame) -> str:
    """Generate a markdown report where each row is a column from the dataframe, with headers: Column Name, % Missing, Imputation Method, Data Type, Reason."""
    percent_missing = df.isnull().mean() * 100
    headers = ["Column Name", "% Missing", "Imputation Method", "Data Type", "Reason"]
    rows = []
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_float_dtype(dtype):
            method = "mean"
            reason = "Mean is best for continuous numeric data."
        elif pd.api.types.is_integer_dtype(dtype):
            method = "median"
            reason = "Median is robust for integer data with outliers."
        elif pd.api.types.is_object_dtype(dtype) or pd.api.types.is_categorical_dtype(dtype):
            method = "mode"
            reason = "Mode is best for categorical or text data."
        else:
            method = "mode"
            reason = "Mode is safest for unknown or mixed types."
        rows.append([
            col,
            f"{percent_missing[col]:.2f}%",
            method,
            str(dtype),
            reason
        ])
    # Markdown table
    md = "| " + " | ".join(headers) + " |\n"
    md += "|" + "---|" * len(headers) + "\n"
    for row in rows:
        md += "| " + " | ".join(row) + " |\n"
    return md


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze missingness in a CSV file or DataFrame.")
    parser.add_argument("data", help="CSV file path")
    parser.add_argument("--output", default="missingness_report.md", help="Output markdown file path")
    args = parser.parse_args()
    if os.path.exists(args.data):
        df = pd.read_csv(args.data)
    else:
        print(f"File not found: {args.data}")
        sys.exit(1)
    md = analyze_missingness(df)
    with open(args.output, "w") as f:
        f.write(md)
    print(f"Missingness report written to {args.output}")

if __name__ == "__main__":
    main()
