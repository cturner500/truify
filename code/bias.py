"""
Bias Evaluation Module

This module evaluates a pandas DataFrame for bias relative to a ground truth source (default: most recent US Census data).
It identifies columns that correlate with the ground truth (e.g., geography via zip code or phone area code), and reports the percentage of the dataframe for each value as well as the associated value from the ground truth.
"""

import pandas as pd
import sys
import os
from typing import Optional, Dict, Any

# Placeholder: Minimal US Census population distribution by zip code (for demo)
US_CENSUS_ZIP = {
    '10001': 21102,  # Example: New York, NY
    '90001': 57110,  # Example: Los Angeles, CA
    '60601': 11510,  # Example: Chicago, IL
    # ... (add more as needed)
}
US_CENSUS_TOTAL = sum(US_CENSUS_ZIP.values())


def load_dataframe(data: Any) -> pd.DataFrame:
    """Load a DataFrame from a pandas DataFrame or CSV file path."""
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, str) and os.path.exists(data):
        return pd.read_csv(data)
    else:
        raise ValueError("Input must be a pandas DataFrame or a valid CSV file path.")


def identify_geography_column(df: pd.DataFrame) -> Optional[str]:
    """Identify a likely geography column (zip code or area code)."""
    candidates = [c for c in df.columns if 'zip' in c.lower() or 'area' in c.lower()]
    if candidates:
        return candidates[0]
    # Try to find a column with 5-digit numbers (zip code pattern)
    for col in df.columns:
        if df[col].astype(str).str.match(r'^\d{5}$').sum() > 0.5 * len(df):
            return col
    return None


def evaluate_bias(data: Any, groundtruth: str = 'US Census', output_data_path: str = None, weights_json_path: str = None) -> Dict[str, Any]:
    """Evaluate bias in the dataframe relative to the groundtruth source, including gender bias. Also generate weights to balance the data."""
    df = load_dataframe(data).copy()
    report = {}
    geo_col = identify_geography_column(df)
    # --- Geography Bias ---
    geo_rows = []
    geo_weights = None
    if geo_col:
        value_counts = df[geo_col].astype(str).value_counts(normalize=True)
        census_dist = {k: v / US_CENSUS_TOTAL for k, v in US_CENSUS_ZIP.items()}
        geo_weights = {}
        for zip_code, pct in value_counts.items():
            census_pct = census_dist.get(zip_code, 0.0001)  # avoid div by zero
            geo_rows.append({
                'Zip/Area Code': zip_code,
                'Percent in Data': round(100 * pct, 2),
                'Percent in US Census': round(100 * census_pct, 2)
            })
            geo_weights[zip_code] = census_pct / pct if pct > 0 else 0
        report['geo_col'] = geo_col
        report['distribution'] = geo_rows
        report['geo_weights'] = geo_weights
    # --- Gender Bias ---
    gender_col = None
    for col in df.columns:
        if col.lower() == 'gender':
            gender_col = col
            break
    gender_rows = []
    gender_weights = None
    if gender_col:
        gender_counts = df[gender_col].value_counts(normalize=True)
        gender_weights = {}
        for gender, pct in gender_counts.items():
            gender_rows.append({
                'Gender': gender,
                'Percent in Data': round(100 * pct, 2),
                'Ideal Percent': 50.0
            })
            # Calculate weight to achieve 50/50
            gender_weights[gender] = 0.5 / pct if pct > 0 else 0
        report['gender_col'] = gender_col
        report['gender_distribution'] = gender_rows
        report['gender_weights'] = gender_weights
    # --- Assign Weights ---
    weights = [1.0] * len(df)
    if geo_col and geo_weights:
        weights = [geo_weights.get(str(val), 1.0) for val in df[geo_col]]
    if gender_col and gender_weights:
        # If both, multiply weights for intersectional balance
        weights = [w * gender_weights.get(str(g), 1.0) for w, g in zip(weights, df[gender_col])]
    df['Weights'] = weights
    # Save weights as JSON if requested
    if weights_json_path:
        import json
        with open(weights_json_path, "w") as f:
            json.dump(weights, f)
        report['weights_json_path'] = weights_json_path
    # --- Markdown summary ---
    md = f"# Bias Evaluation Report\n\n"
    md += f"**Ground Truth Source:** {groundtruth}\n\n"
    if geo_col:
        md += f"**Geography Column Used:** `{geo_col}`\n\n"
        md += "| Zip/Area Code | % in Data | % in US Census |\n|---|---|---|\n"
        for row in geo_rows:
            md += f"| {row['Zip/Area Code']} | {row['Percent in Data']} | {row['Percent in US Census']} |\n"
        md += "\n"
    else:
        md += "No geography column (zip code or area code) found. Geography bias evaluation not performed.\n\n"
    if gender_col:
        md += f"**Gender Bias Evaluation (Column: `{gender_col}`):**\n\n"
        md += "| Gender | % in Data | Ideal % |\n|---|---|---|\n"
        for row in gender_rows:
            md += f"| {row['Gender']} | {row['Percent in Data']} | {row['Ideal Percent']} |\n"
        if any(abs(row['Percent in Data'] - 50.0) > 5 for row in gender_rows):
            md += "\n*The data is not gender balanced. Suggested weights to achieve 50/50 representation:*\n\n"
            md += "| Gender | Weight |\n|---|---|\n"
            for gender, weight in gender_weights.items():
                md += f"| {gender} | {round(weight, 3)} |\n"
        else:
            md += "\n*The data is approximately gender balanced.*\n"
    else:
        md += "No gender column found. Gender bias evaluation not performed.\n"
    md += f"\n---\n**A new 'Weights' column is available for preview and can be added to your data.**\n"
    report['markdown'] = md
    report['weights'] = weights
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Bias evaluation relative to ground truth.")
    parser.add_argument("data", help="CSV file path or pandas DataFrame")
    parser.add_argument("--groundtruth", default="US Census", help="Ground truth source (default: US Census)")
    parser.add_argument("--output", default="bias_report.md", help="Output markdown file path")
    parser.add_argument("--weights_json", default=None, help="Output JSON file path for weights array")
    args = parser.parse_args()
    df = load_dataframe(args.data)
    result = evaluate_bias(df, groundtruth=args.groundtruth, weights_json_path=args.weights_json)
    if 'markdown' in result:
        with open(args.output, "w") as f:
            f.write(result['markdown'])
        print(f"Bias report written to {args.output}")
        if args.weights_json:
            print(f"Weights written to {args.weights_json}")
    else:
        print("Error:", result.get('error', 'Unknown error'))
