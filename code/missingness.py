"""
Missingness Analysis Module

This script analyzes each column of a pandas DataFrame (or CSV file) and generates a report where each row is a column from the dataframe, and the columns are: Column Name, % Missing, Imputation Method, Data Type, Reason.
"""

import pandas as pd
import sys
import os
import re

def infer_gender_from_name(name: str) -> str:
    """
    Infer gender from a first name using common name patterns.
    Returns 'M', 'F', or 'Other' based on the name.
    """
    if pd.isna(name) or not isinstance(name, str):
        return "Other"
    
    # Clean the name
    name = name.strip().lower()
    
    # Common male names (high confidence)
    male_names = {
        'james', 'robert', 'john', 'michael', 'david', 'william', 'richard', 'joseph', 'thomas', 'christopher',
        'charles', 'daniel', 'matthew', 'anthony', 'mark', 'donald', 'steven', 'paul', 'andrew', 'joshua',
        'kenneth', 'kevin', 'brian', 'george', 'timothy', 'ronald', 'jason', 'edward', 'jeffrey', 'ryan',
        'jacob', 'gary', 'nicholas', 'eric', 'jonathan', 'stephen', 'larry', 'justin', 'scott', 'brandon',
        'benjamin', 'frank', 'gregory', 'raymond', 'samuel', 'patrick', 'alexander', 'jack', 'dennis', 'jerry',
        'mike', 'joe', 'jim', 'bob', 'tom', 'dave', 'chris', 'steve', 'tony', 'jimmy', 'bobby', 'tommy'
    }
    
    # Common female names (high confidence)
    female_names = {
        'mary', 'patricia', 'jennifer', 'linda', 'elizabeth', 'barbara', 'susan', 'jessica', 'sarah', 'karen',
        'nancy', 'lisa', 'betty', 'helen', 'sandra', 'donna', 'carol', 'ruth', 'sharon', 'michelle',
        'laura', 'emily', 'kimberly', 'deborah', 'dorothy', 'julie', 'amy', 'angela', 'anna', 'rebecca',
        'virginia', 'kathleen', 'pamela', 'martha', 'debra', 'amanda', 'stephanie', 'carolyn', 'christine', 'marie',
        'janet', 'catherine', 'frances', 'ann', 'joyce', 'diane', 'alice', 'julie', 'heather', 'teresa',
        'doris', 'gloria', 'evelyn', 'jean', 'cheryl', 'mildred', 'katherine', 'joan', 'ashley', 'kelly'
    }
    
    # Check for exact matches
    if name in male_names:
        return "M"
    elif name in female_names:
        return "F"
    
    # Check for name endings that are typically gender-specific
    if name.endswith(('a', 'ia', 'ina', 'ella', 'ette', 'ine', 'ina', 'ana', 'ena')):
        return "F"
    elif name.endswith(('o', 'us', 'er', 'or', 'an', 'en', 'in', 'on')):
        return "M"
    
    # Check for common unisex names
    unisex_names = {
        'alex', 'alexis', 'casey', 'drew', 'jordan', 'morgan', 'pat', 'patricia', 'robin', 'sam', 'samuel',
        'taylor', 'tracy', 'jamie', 'jessie', 'jesse', 'kris', 'chris', 'kelly', 'dana', 'dane', 'lee',
        'leslie', 'lesley', 'avery', 'riley', 'quinn', 'blake', 'hayden', 'logan', 'parker', 'reese'
    }
    
    if name in unisex_names:
        return "Other"
    
    # If we can't determine, return "Other"
    return "Other"

def intelligent_imputation(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Perform intelligent imputation for a specific column, including gender inference from names.
    """
    if column.lower() == 'gender':
        # For gender columns, try to infer from first names if available
        name_columns = [col for col in df.columns if any(name_word in col.lower() for name_word in ['first', 'name', 'firstname'])]
        
        if name_columns:
            # Use the first name column found
            name_col = name_columns[0]
            print(f"Using '{name_col}' column to infer missing gender values...")
            
            # Create a copy to avoid modifying original
            df_copy = df.copy()
            
            # Fill missing gender values using name inference
            for idx in df_copy.index:
                if pd.isna(df_copy.at[idx, column]):
                    name = df_copy.at[idx, name_col]
                    inferred_gender = infer_gender_from_name(name)
                    df_copy.at[idx, column] = inferred_gender
                    print(f"Row {idx}: '{name}' → Gender: {inferred_gender}")
            
            return df_copy[column]
        else:
            # No name column found, use mode
            print("No name column found for gender inference, using mode imputation...")
            return df[column].fillna(df[column].mode()[0] if not df[column].mode().empty else "Other")
    
    # For other columns, use standard imputation methods
    if pd.api.types.is_float_dtype(df[column].dtype):
        return df[column].fillna(df[column].mean())
    elif pd.api.types.is_integer_dtype(df[column].dtype):
        return df[column].fillna(df[column].median())
    else:
        return df[column].fillna(df[column].mode()[0] if not df[column].mode().empty else "Unknown")

def analyze_missingness(df: pd.DataFrame) -> str:
    """Generate a markdown report where each row is a column from the dataframe, with headers: Column Name, % Missing, Imputation Method, Data Type, Reason."""
    percent_missing = df.isnull().mean() * 100
    headers = ["Column Name", "% Missing", "Imputation Method", "Data Type", "Reason"]
    rows = []
    
    for col in df.columns:
        dtype = df[col].dtype
        missing_pct = percent_missing[col]
        
        # Determine imputation method based on column type and content
        if col.lower() == 'gender' and missing_pct > 0:
            method = "intelligent (name inference)"
            reason = "Gender inferred from first names using pattern matching."
        elif pd.api.types.is_float_dtype(dtype):
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
            f"{missing_pct:.2f}%",
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

def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Impute missing values in the DataFrame using intelligent methods.
    """
    df_imputed = df.copy()
    
    for col in df.columns:
        if df[col].isnull().any():
            print(f"Imputing missing values in column: {col}")
            df_imputed[col] = intelligent_imputation(df, col)
    
    return df_imputed


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
