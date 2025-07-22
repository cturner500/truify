"""
Compliance Risk Evaluation Module

This module evaluates a pandas DataFrame for compliance risks relative to:
- GDPR (General Data Protection Regulation)
- CCPA (California Consumer Privacy Act)
- EU AI Act

It analyzes the data for:
- Presence of personally identifiable information (PII)
- Sensitive attributes
- Data minimization and purpose limitation
- Automated decision-making risks (AI Act)
- Data subject rights and transparency

At the end, it generates a detailed markdown report describing:
- The data and its structure
- Potential compliance risks, with references to the above policies
- An action plan for remediation, referencing PII.py and other modules for de-identification, bias reduction, and missingness handling.

The report can be exported to PDF using any markdown-to-PDF tool.
"""

import pandas as pd
import re
from typing import List, Dict, Any

# --- Policy Reference URLs ---
GDPR_URL = "https://gdpr-info.eu/"
CCPA_URL = "https://oag.ca.gov/privacy/ccpa"
EU_AI_ACT_URL = "https://artificialintelligenceact.eu/"

# --- Helper Functions ---
def identify_pii_columns(df: pd.DataFrame) -> List[str]:
    """Identify columns likely to contain PII based on column names and sample values."""
    pii_keywords = [
        'name', 'address', 'email', 'phone', 'ssn', 'dob', 'birth', 'passport', 'credit', 'card', 'account', 'customerid', 'userid', 'user_id', 'ip', 'location', 'geo', 'zip', 'postal'
    ]
    detected = []
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in pii_keywords):
            detected.append(col)
        else:
            # Check sample values for email/phone patterns
            sample = df[col].astype(str).head(20).tolist()
            if any(re.search(r"[\w\.-]+@[\w\.-]+", v) for v in sample):
                detected.append(col)
            elif any(re.search(r"\+?\d{10,}", v) for v in sample):
                detected.append(col)
    return detected

def identify_sensitive_columns(df: pd.DataFrame) -> List[str]:
    """Identify columns that may contain sensitive attributes (race, gender, health, etc)."""
    sensitive_keywords = [
        'gender', 'race', 'ethnicity', 'religion', 'health', 'disability', 'sexual', 'orientation', 'income', 'political', 'union', 'biometric', 'genetic', 'seniorcitizen', 'dependents'
    ]
    detected = []
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in sensitive_keywords):
            detected.append(col)
    return detected

def check_automated_decision_risk(df: pd.DataFrame) -> bool:
    """Heuristic: If the data contains target/outcome columns, it may be used for automated decision-making (AI Act)."""
    outcome_keywords = ['churn', 'target', 'outcome', 'score', 'risk', 'decision', 'label']
    for col in df.columns:
        if any(kw in col.lower() for kw in outcome_keywords):
            return True
    return False

def describe_dataframe(df: pd.DataFrame) -> str:
    """Generate a summary of the dataframe structure and sample data."""
    desc = f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns\n\n"
    desc += "**Columns:**\n\n"
    for col in df.columns:
        desc += f"- `{col}` (type: {df[col].dtype})\n"
    desc += "\n**Sample Data:**\n\n"
    desc += df.head(5).to_markdown(index=False)
    return desc

# --- Main Compliance Evaluation Function ---
def evaluate_compliance(df: pd.DataFrame, policies: list = None) -> Dict[str, Any]:
    """Evaluate the dataframe for selected compliance risks."""
    if policies is None:
        policies = ["GDPR", "CCPA", "EU AI Act"]
    policies_lower = [p.lower() for p in policies]
    report = {}
    pii_cols = identify_pii_columns(df)
    sensitive_cols = identify_sensitive_columns(df)
    ai_risk = check_automated_decision_risk(df)
    missingness = df.isnull().sum().sum() > 0

    # Data description
    report['description'] = describe_dataframe(df)

    # Risks
    risks = []
    # Policy references
    refs = []
    if "gdpr" in policies_lower:
        refs.append(f"[GDPR]({GDPR_URL})")
    if "ccpa" in policies_lower:
        refs.append(f"[CCPA]({CCPA_URL})")
    if "eu ai act" in policies_lower or "euai act" in policies_lower:
        refs.append(f"[EU AI Act]({EU_AI_ACT_URL})")
    for p in policies:
        if p not in ["GDPR", "CCPA", "EU AI Act"]:
            refs.append(f"{p}")
    # Risks and actions by policy
    if pii_cols and ("gdpr" in policies_lower or "ccpa" in policies_lower or "eu ai act" in policies_lower or len(policies) > 0):
        ref_str = ', '.join([r for r in refs if ("GDPR" in r or "CCPA" in r or "EU AI Act" in r or p not in ["GDPR", "CCPA", "EU AI Act"] )])
        risks.append(f"**PII Detected:** {pii_cols}. This data is subject to {ref_str}.")
    if sensitive_cols and ("gdpr" in policies_lower or "eu ai act" in policies_lower or len(policies) > 0):
        ref_str = ', '.join([r for r in refs if ("GDPR" in r or "EU AI Act" in r or p not in ["GDPR", "CCPA", "EU AI Act"] )])
        risks.append(f"**Sensitive Attributes Detected:** {sensitive_cols}. Special categories under {ref_str}.")
    if ai_risk and ("eu ai act" in policies_lower or "gdpr" in policies_lower or len(policies) > 0):
        ref_str = ', '.join([r for r in refs if ("EU AI Act" in r or "GDPR" in r or p not in ["GDPR", "CCPA", "EU AI Act"] )])
        risks.append(f"**Automated Decision-Making Risk:** Data may be used for profiling or automated decisions. See {ref_str}.")
    if missingness and ("eu ai act" in policies_lower or len(policies) > 0):
        ref_str = ', '.join([r for r in refs if ("EU AI Act" in r or p not in ["GDPR", "CCPA", "EU AI Act"] )])
        risks.append(f"**Missing Data:** Missing values detected. May impact fairness and explainability. See {ref_str}.")
    if not risks:
        risks.append("No major compliance risks detected based on column analysis.")
    report['risks'] = risks

    # Verbose explanation of risks and policy sections
    explanations = []
    if pii_cols:
        explanations.append(
            f"**Why PII Columns Are Risky:** Columns such as {pii_cols} may contain information that can directly or indirectly identify an individual. Under GDPR (Art. 4), PII includes any information relating to an identified or identifiable person. CCPA (§1798.140) defines personal information broadly, including identifiers like names, addresses, and account numbers. The EU AI Act (Art. 10) requires that data used for training, validation, and testing of AI systems be subject to strict data governance, especially if it contains PII. If these columns are not properly protected, there is a risk of unauthorized access, identity theft, or misuse."
        )
    if sensitive_cols:
        explanations.append(
            f"**Why Sensitive Attribute Columns Are Risky:** Columns such as {sensitive_cols} may include special categories of data (e.g., race, health, gender). GDPR (Art. 9) prohibits processing of special categories of personal data except under strict conditions. The EU AI Act (Art. 10) also places additional requirements on high-risk AI systems using sensitive data. Use of these columns can lead to discrimination, bias, or violation of data subject rights if not handled appropriately."
        )
    if ai_risk:
        explanations.append(
            "**Why Automated Decision-Making Is Risky:** If the data is used for profiling or automated decisions (e.g., churn prediction), GDPR (Art. 22) gives individuals the right not to be subject to decisions based solely on automated processing. The EU AI Act (Title III) imposes transparency, human oversight, and documentation requirements for high-risk AI systems. Failing to comply can result in lack of explainability, unfair outcomes, or regulatory penalties."
        )
    if missingness:
        explanations.append(
            "**Why Missing Data Is Risky:** Missing values can reduce the quality and fairness of AI models. The EU AI Act (Art. 15) requires that data be complete and representative to ensure fairness and accuracy. Incomplete data can lead to biased models and poor decision-making."
        )
    if not explanations:
        explanations.append("No additional risk explanations required.")
    report['explanations'] = explanations

    # Action Plan
    actions = []
    if pii_cols:
        actions.append(f"- Use the de-identification tools in `PII.py` or the deidentify functions in `main.py` to remove or hash PII columns: {pii_cols}.")
    if sensitive_cols:
        actions.append(f"- Review use of sensitive attributes: {sensitive_cols}. Limit processing unless necessary and document justification.")
    if ai_risk:
        actions.append("- Ensure transparency and human oversight for any automated decisions. Document logic and provide opt-out where required.")
    if missingness:
        actions.append("- Use missingness handling tools (see `main.py` or `missingness.py`) to impute or address missing values.")
    if not actions:
        actions.append("- No immediate remediation required.")
    report['actions'] = actions

    # Markdown report
    md = f"# Data Compliance Risk Report\n\n"
    md += "## Data Description\n" + report['description'] + "\n\n"
    md += "## Potential Compliance Risks\n"
    for r in risks:
        md += f"- {r}\n"
    md += "\n## Why These Columns and Risks Matter\n"
    for e in explanations:
        md += f"- {e}\n"
    md += "\n## Action Plan\n"
    for a in actions:
        md += f"- {a}\n"
    md += f"\n---\n*References:* {', '.join(refs)}\n"
    report['markdown'] = md
    return report

# --- Example Usage ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Load CSV from command line
        df = pd.read_csv(sys.argv[1])
        result = evaluate_compliance(df)
        with open("compliance_report.md", "w") as f:
            f.write(result['markdown'])
        print("Compliance report written to compliance_report.md")
    else:
        print("Usage: python compliance.py <datafile.csv>")
