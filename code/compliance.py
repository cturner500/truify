"""
Compliance Risk Evaluation Module

This module evaluates a pandas DataFrame for compliance risks relative to global data protection and AI regulations:

DATA PROTECTION & PRIVACY LAWS:
- GDPR (General Data Protection Regulation) - EU
- CCPA (California Consumer Privacy Act) - US
- LGPD (Brazil) - Lei Geral de Proteção de Dados
- PIPEDA (Canada) - Personal Information Protection and Electronic Documents Act
- PDPA (Singapore) - Personal Data Protection Act
- PIPL (China) - Personal Information Protection Law
- APPI (Japan) - Act on the Protection of Personal Information
- PDPA (Thailand) - Personal Data Protection Act
- POPIA (South Africa) - Protection of Personal Information Act
- COPPA (US) - Children's Online Privacy Protection Act
- GLBA (US) - Gramm-Leach-Bliley Act
- SOX (US) - Sarbanes-Oxley Act
- ePrivacy Directive - EU
- NIS2 Directive - EU

AI-SPECIFIC REGULATIONS:
- EU AI Act - European Union
- AI Act (Canada) - Artificial Intelligence and Data Act
- AI Governance Framework (Singapore) - Model AI Governance Framework
- AI Ethics Guidelines (Japan) - Social Principles of Human-Centric AI
- OECD AI Principles - International
- UNESCO AI Ethics Framework - Global
- G7 AI Principles - International

INDUSTRY-SPECIFIC REGULATIONS:
- HIPAA (US) - Health Insurance Portability and Accountability Act
- Basel III/IV - Banking regulations
- MiFID II (EU) - Markets in Financial Instruments Directive
- Dodd-Frank (US) - Financial reform
- FDA AI/ML Guidelines (US) - Medical device AI regulations
- MDR (EU) - Medical Device Regulation
- UNECE WP.29 - Vehicle cybersecurity regulations
- ISO 21434 - Road vehicle cybersecurity engineering

CYBERSECURITY & INFRASTRUCTURE:
- NIST Cybersecurity Framework (US)
- ISO 27001 - Information security management
- SOC 2 - Service Organization Control 2
- PCI DSS - Payment card industry standards

EMERGING/PROPOSED REGULATIONS:
- AI Liability Directive (EU) - Proposed
- Data Act (EU) - Data sharing and access rights
- Digital Services Act (EU) - Online platform regulation
- Digital Markets Act (EU) - Competition in digital markets

It analyzes the data for:
- Presence of personally identifiable information (PII)
- Sensitive attributes and special categories
- Data minimization and purpose limitation
- Automated decision-making risks
- Data subject rights and transparency
- Industry-specific compliance requirements
- Cross-border data transfer implications
- Data localization requirements

At the end, it generates a detailed markdown report describing:
- The data and its structure
- Potential compliance risks, with references to applicable policies
- Regional and industry-specific considerations
- An action plan for remediation, referencing PII.py and other modules

The report can be exported to PDF using any markdown-to-PDF tool.
"""

import pandas as pd
import re
from typing import List, Dict, Any
from datetime import datetime
import os

# --- Policy Reference URLs ---
# Data Protection & Privacy Laws
GDPR_URL = "https://gdpr-info.eu/"
CCPA_URL = "https://oag.ca.gov/privacy/ccpa"
LGPD_URL = "https://www.lgpdbrasil.com.br/"
PIPEDA_URL = "https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/"
PDPA_SG_URL = "https://www.pdpc.gov.sg/Overview-of-PDPA/The-Legislation/Personal-Data-Protection-Act"
PIPL_URL = "https://www.pipc.gov.cn/"
APPI_URL = "https://www.ppc.go.jp/en/"
PDPA_TH_URL = "https://www.pdpc.go.th/"
POPIA_URL = "https://www.justice.gov.za/inforeg/docs/InfoRegSA-POPIA-act2013-004.pdf"
COPPA_URL = "https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/childrens-online-privacy-protection-rule"
GLBA_URL = "https://www.ftc.gov/tips-advice/business-center/privacy-and-security/gramm-leach-bliley-act"
SOX_URL = "https://www.sec.gov/about/laws/soa2002.pdf"
EPRIVACY_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32002L0058"
NIS2_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2555"

# AI-Specific Regulations
EU_AI_ACT_URL = "https://artificialintelligenceact.eu/"
AI_ACT_CA_URL = "https://www.parl.ca/DocumentViewer/en/44-1/bill/C-27/third-reading"
AI_GOV_SG_URL = "https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework"
AI_ETHICS_JP_URL = "https://www.cao.go.jp/ai-policy/ai-policy_en.html"
OECD_AI_URL = "https://oecd.ai/en/ai-principles"
UNESCO_AI_URL = "https://en.unesco.org/artificial-intelligence/ethics"
G7_AI_URL = "https://www.g7uk.org/g7-ai-principles/"

# Industry-Specific Regulations
HIPAA_URL = "https://www.hhs.gov/hipaa/index.html"
BASEL_URL = "https://www.bis.org/bcbs/basel3.htm"
MIFID_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32014L0065"
DODD_FRANK_URL = "https://www.congress.gov/bill/111th-congress/house-bill/4173"
FDA_AI_URL = "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-software-medical-device"
MDR_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745"
UNECE_URL = "https://unece.org/transport/vehicle-regulations"
ISO_21434_URL = "https://www.iso.org/standard/70918.html"

# Cybersecurity & Infrastructure
NIST_URL = "https://www.nist.gov/cyberframework"
ISO_27001_URL = "https://www.iso.org/isoiec-27001-information-security.html"
SOC2_URL = "https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html"
PCI_DSS_URL = "https://www.pcisecuritystandards.org/"

# Emerging/Proposed Regulations
AI_LIABILITY_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52022PC0496"
DATA_ACT_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52022PC0068"
DSA_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2065"
DMA_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L1925"

# --- Helper Functions ---
def identify_pii_columns(df: pd.DataFrame) -> List[str]:
    """Identify columns likely to contain PII based on column names and sample values."""
    pii_keywords = [
        'name', 'address', 'email', 'phone', 'ssn', 'dob', 'birth', 'passport', 'credit', 'card', 'account', 'customerid', 'userid', 'user_id', 'ip', 'location', 'geo', 'zip', 'postal', 'national_id', 'tax_id', 'driver_license', 'employee_id', 'student_id', 'patient_id', 'client_id'
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
        'gender', 'race', 'ethnicity', 'religion', 'health', 'disability', 'sexual', 'orientation', 'income', 'political', 'union', 'biometric', 'genetic', 'seniorcitizen', 'dependents', 'medical', 'diagnosis', 'treatment', 'medication', 'allergy', 'blood_type', 'mental_health', 'pregnancy', 'marital_status', 'education', 'employment', 'criminal_record', 'financial', 'credit_score', 'bank_account', 'investment'
    ]
    detected = []
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in sensitive_keywords):
            detected.append(col)
    return detected

def identify_children_data(df: pd.DataFrame) -> bool:
    """Check if data might contain information about children (COPPA)."""
    child_keywords = ['age', 'birth', 'dob', 'student', 'child', 'minor', 'teen', 'youth']
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in child_keywords):
            # Check if any values suggest children (age < 13)
            try:
                if 'age' in col_lower:
                    sample_values = pd.to_numeric(df[col].dropna(), errors='coerce')
                    if any(sample_values < 13):
                        return True
            except:
                pass
    return False

def identify_financial_data(df: pd.DataFrame) -> bool:
    """Check if data contains financial information (GLBA, SOX, Basel)."""
    financial_keywords = ['account', 'balance', 'transaction', 'payment', 'credit', 'debit', 'loan', 'mortgage', 'investment', 'portfolio', 'revenue', 'income', 'salary', 'wage', 'tax', 'financial', 'bank', 'insurance', 'claim', 'premium', 'policy']
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in financial_keywords):
            return True
    return False

def identify_health_data(df: pd.DataFrame) -> bool:
    """Check if data contains health information (HIPAA, MDR)."""
    health_keywords = ['medical', 'health', 'diagnosis', 'treatment', 'medication', 'allergy', 'blood', 'patient', 'doctor', 'hospital', 'clinic', 'symptom', 'condition', 'disease', 'prescription', 'lab', 'test', 'vital', 'bmi', 'weight', 'height', 'temperature', 'pressure']
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in health_keywords):
            return True
    return False

def check_automated_decision_risk(df: pd.DataFrame) -> bool:
    """Heuristic: If the data contains target/outcome columns, it may be used for automated decision-making."""
    outcome_keywords = ['churn', 'target', 'outcome', 'score', 'risk', 'decision', 'label', 'prediction', 'classification', 'recommendation', 'approval', 'denial', 'fraud', 'anomaly', 'sentiment', 'credit_score', 'insurance_score', 'health_score']
    for col in df.columns:
        if any(kw in col.lower() for kw in outcome_keywords):
            return True
    return False

def check_high_risk_ai_use(df: pd.DataFrame) -> List[str]:
    """Check if data might be used for high-risk AI applications under EU AI Act."""
    high_risk_keywords = {
        'biometric': ['face', 'fingerprint', 'voice', 'gait', 'biometric', 'recognition'],
        'critical_infrastructure': ['energy', 'water', 'transport', 'traffic', 'utility', 'infrastructure'],
        'education': ['student', 'grade', 'academic', 'education', 'school', 'university'],
        'employment': ['employee', 'hiring', 'firing', 'promotion', 'performance', 'workplace'],
        'essential_services': ['banking', 'insurance', 'credit', 'loan', 'mortgage', 'financial'],
        'law_enforcement': ['crime', 'criminal', 'police', 'law', 'enforcement', 'justice'],
        'migration': ['immigration', 'border', 'visa', 'citizenship', 'migration'],
        'justice': ['court', 'judge', 'legal', 'justice', 'law', 'criminal'],
        'healthcare': ['medical', 'health', 'patient', 'diagnosis', 'treatment', 'hospital']
    }
    
    detected_risks = []
    for risk_type, keywords in high_risk_keywords.items():
        for col in df.columns:
            col_lower = col.lower()
            if any(kw in col_lower for kw in keywords):
                detected_risks.append(risk_type)
                break
    return detected_risks

def describe_dataframe(df: pd.DataFrame) -> str:
    """Generate a summary of the dataframe structure and sample data."""
    desc = f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns\n\n"
    desc += "**Columns:**\n\n"
    for col in df.columns:
        desc += f"- `{col}` (type: {df[col].dtype})\n"
    desc += "\n**Sample Data:**\n\n"
    
    # Create a copy of the dataframe for formatting
    df_sample = df.head(5).copy()
    
    # Truncate long values to fit in table cells
    for col in df_sample.columns:
        if df_sample[col].dtype == 'object':
            # Truncate string values to 20 characters for better table fit
            df_sample[col] = df_sample[col].astype(str).apply(lambda x: x[:20] + '...' if len(str(x)) > 20 else str(x))
        elif df_sample[col].dtype in ['float64', 'float32']:
            # Limit decimal places for float values
            df_sample[col] = df_sample[col].round(2)
        elif df_sample[col].dtype in ['int64', 'int32']:
            # Keep integers as is, but convert to string for consistent formatting
            df_sample[col] = df_sample[col].astype(str)
    
    # Generate markdown table with simple pipe format for better PDF compatibility
    desc += df_sample.to_markdown(index=False, tablefmt="pipe")
    return desc

def get_policy_references(policies: List[str]) -> Dict[str, str]:
    """Get policy references based on selected policies."""
    policy_refs = {
        # Data Protection & Privacy Laws
        "GDPR": f"[GDPR]({GDPR_URL})",
        "CCPA": f"[CCPA]({CCPA_URL})",
        "LGPD": f"[LGPD]({LGPD_URL})",
        "PIPEDA": f"[PIPEDA]({PIPEDA_URL})",
        "PDPA_SG": f"[PDPA Singapore]({PDPA_SG_URL})",
        "PIPL": f"[PIPL China]({PIPL_URL})",
        "APPI": f"[APPI Japan]({APPI_URL})",
        "PDPA_TH": f"[PDPA Thailand]({PDPA_TH_URL})",
        "POPIA": f"[POPIA South Africa]({POPIA_URL})",
        "COPPA": f"[COPPA]({COPPA_URL})",
        "GLBA": f"[GLBA]({GLBA_URL})",
        "SOX": f"[SOX]({SOX_URL})",
        "ePrivacy": f"[ePrivacy Directive]({EPRIVACY_URL})",
        "NIS2": f"[NIS2 Directive]({NIS2_URL})",
        
        # AI-Specific Regulations
        "EU AI Act": f"[EU AI Act]({EU_AI_ACT_URL})",
        "AI Act CA": f"[AI Act Canada]({AI_ACT_CA_URL})",
        "AI Gov SG": f"[AI Governance Framework Singapore]({AI_GOV_SG_URL})",
        "AI Ethics JP": f"[AI Ethics Guidelines Japan]({AI_ETHICS_JP_URL})",
        "OECD AI": f"[OECD AI Principles]({OECD_AI_URL})",
        "UNESCO AI": f"[UNESCO AI Ethics]({UNESCO_AI_URL})",
        "G7 AI": f"[G7 AI Principles]({G7_AI_URL})",
        
        # Industry-Specific Regulations
        "HIPAA": f"[HIPAA]({HIPAA_URL})",
        "Basel": f"[Basel III/IV]({BASEL_URL})",
        "MiFID II": f"[MiFID II]({MIFID_URL})",
        "Dodd-Frank": f"[Dodd-Frank]({DODD_FRANK_URL})",
        "FDA AI": f"[FDA AI/ML Guidelines]({FDA_AI_URL})",
        "MDR": f"[MDR]({MDR_URL})",
        "UNECE": f"[UNECE WP.29]({UNECE_URL})",
        "ISO 21434": f"[ISO 21434]({ISO_21434_URL})",
        
        # Cybersecurity & Infrastructure
        "NIST": f"[NIST Cybersecurity Framework]({NIST_URL})",
        "ISO 27001": f"[ISO 27001]({ISO_27001_URL})",
        "SOC 2": f"[SOC 2]({SOC2_URL})",
        "PCI DSS": f"[PCI DSS]({PCI_DSS_URL})",
        
        # Emerging/Proposed Regulations
        "AI Liability": f"[AI Liability Directive]({AI_LIABILITY_URL})",
        "Data Act": f"[Data Act]({DATA_ACT_URL})",
        "DSA": f"[Digital Services Act]({DSA_URL})",
        "DMA": f"[Digital Markets Act]({DMA_URL})"
    }
    
    selected_refs = {}
    for policy in policies:
        if policy in policy_refs:
            selected_refs[policy] = policy_refs[policy]
        else:
            selected_refs[policy] = policy  # For custom policies
    
    return selected_refs

# --- Main Compliance Evaluation Function ---
def evaluate_compliance(df: pd.DataFrame, policies: list = None) -> Dict[str, Any]:
    """Evaluate the dataframe for selected compliance risks."""
    if policies is None:
        policies = ["GDPR", "CCPA", "EU AI Act", "LGPD", "PIPEDA", "PDPA_SG", "PIPL", "APPI", "HIPAA", "GLBA", "COPPA", "OECD AI", "UNESCO AI", "NIST", "ISO 27001"]
    
    policies_lower = [p.lower() for p in policies]
    report = {}
    
    # Data analysis
    pii_cols = identify_pii_columns(df)
    sensitive_cols = identify_sensitive_columns(df)
    children_data = identify_children_data(df)
    financial_data = identify_financial_data(df)
    health_data = identify_health_data(df)
    ai_risk = check_automated_decision_risk(df)
    high_risk_ai = check_high_risk_ai_use(df)
    missingness = df.isnull().sum().sum() > 0

    # Data description
    report['description'] = describe_dataframe(df)

    # Get policy references
    policy_refs = get_policy_references(policies)
    
    # Risks assessment
    risks = []
    explanations = []
    
    # PII Risks
    if pii_cols:
        applicable_policies = []
        for policy in policies:
            if any(p in policy.lower() for p in ['gdpr', 'ccpa', 'lgpd', 'pipeda', 'pdpa', 'pipl', 'appi', 'popia', 'coppa', 'glba', 'sox', 'hipaa']):
                applicable_policies.append(policy_refs[policy])
        
        if applicable_policies:
            ref_str = ', '.join(applicable_policies)
            risks.append(f"**PII Detected:** {pii_cols}. Subject to data protection laws: {ref_str}.")
            
            # Get sample values for examples
            sample_values = {}
            for col in pii_cols:
                try:
                    sample = df[col].dropna().head(3).tolist()
                    sample_values[col] = [str(v) for v in sample if str(v).strip()]
                except:
                    sample_values[col] = ["sample data"]
            
            explanations.append(
                f"**PII Compliance Risk - Detailed Analysis:**\n\n"
                f"**Data Examples:** The following columns contain personally identifiable information:\n"
                f"{chr(10).join([f'- {col}: Sample values include {sample_values[col][:2]}' for col in pii_cols])}\n\n"
                f"**Policy-Specific Requirements:**\n\n"
                f"**GDPR (Art. 4, 6, 7):** Defines personal data as any information relating to an identified or identifiable person. "
                f"Requires lawful basis for processing (consent, contract, legitimate interest, etc.), data minimization, and data subject rights. "
                f"Examples of PII in your data: {', '.join(pii_cols)}. "
                f"These columns likely contain direct identifiers (names, emails) or indirect identifiers (IP addresses, customer IDs) that can identify individuals.\n\n"
                f"**CCPA (§1798.140, 1798.100):** Broadly defines personal information including identifiers, commercial information, and internet activity. "
                f"Requires transparency about data collection, opt-out rights, and data deletion. "
                f"Your data contains identifiers that fall under CCPA's broad definition: {', '.join(pii_cols)}.\n\n"
                f"**LGPD (Art. 5, 7):** Similar to GDPR but with Brazilian-specific requirements. "
                f"Requires legal basis, consent, and data subject rights. "
                f"Applies to processing of Brazilian residents' data, regardless of where the processing occurs.\n\n"
                f"**PIPEDA (S.2, 5):** Canada's federal privacy law requiring consent, appropriate purposes, and reasonable security. "
                f"Applies to commercial activities involving personal information.\n\n"
                f"**Cross-Border Considerations:** If your data contains information from multiple jurisdictions, you may be subject to multiple laws simultaneously. "
                f"For example, a dataset with EU residents' data (GDPR), California residents' data (CCPA), and Brazilian residents' data (LGPD) requires compliance with all three frameworks.\n\n"
                f"**Specific Risk Examples:**\n"
                f"- Email addresses in your data can be used to directly identify individuals and are considered PII under all major privacy laws\n"
                f"- Customer IDs, while not directly identifying, can be linked to other data to identify individuals\n"
                f"- Phone numbers are considered personal information under most jurisdictions\n"
                f"- IP addresses may be considered PII depending on the jurisdiction and context\n\n"
                f"**Penalty Differences:**\n"
                f"- GDPR: Up to 4% of global annual revenue or €20 million\n"
                f"- CCPA: Up to $7,500 per intentional violation, $2,500 per unintentional violation\n"
                f"- LGPD: Up to 2% of revenue or R$50 million\n"
                f"- PIPEDA: Up to $100,000 per violation\n\n"
                f"**Immediate Actions Required:**\n"
                f"1. Document lawful basis for processing each PII column\n"
                f"2. Implement data minimization - only collect necessary PII\n"
                f"3. Establish data subject rights procedures (access, rectification, deletion)\n"
                f"4. Implement appropriate security measures\n"
                f"5. Create privacy notices explaining data collection and use"
            )
    
    # Sensitive Data Risks
    if sensitive_cols:
        applicable_policies = []
        for policy in policies:
            if any(p in policy.lower() for p in ['gdpr', 'lgpd', 'pipeda', 'pdpa', 'pipl', 'appi', 'popia', 'hipaa']):
                applicable_policies.append(policy_refs[policy])
        
        if applicable_policies:
            ref_str = ', '.join(applicable_policies)
            risks.append(f"**Sensitive Attributes Detected:** {sensitive_cols}. Special categories under: {ref_str}.")
            
            # Get sample values for examples
            sample_values = {}
            for col in sensitive_cols:
                try:
                    sample = df[col].dropna().head(3).tolist()
                    sample_values[col] = [str(v) for v in sample if str(v).strip()]
                except:
                    sample_values[col] = ["sample data"]
            
            explanations.append(
                f"**Sensitive Data Risk - Detailed Analysis:**\n\n"
                f"**Data Examples:** The following columns contain sensitive personal information:\n"
                f"{chr(10).join([f'- {col}: Sample values include {sample_values[col][:2]}' for col in sensitive_cols])}\n\n"
                f"**Policy-Specific Requirements:**\n\n"
                f"**GDPR (Art. 9):** Prohibits processing of special categories of personal data except under strict conditions. "
                f"Special categories include: racial/ethnic origin, political opinions, religious/philosophical beliefs, trade union membership, "
                f"genetic data, biometric data, health data, sex life/sexual orientation. "
                f"Your data contains sensitive attributes: {', '.join(sensitive_cols)}. "
                f"Processing requires explicit consent, employment/social security law, vital interests, or public health reasons.\n\n"
                f"**HIPAA (45 CFR 164.501, 164.502):** Defines protected health information (PHI) as individually identifiable health information. "
                f"Requires administrative, physical, and technical safeguards. "
                f"Your health-related columns: {[col for col in sensitive_cols if any(kw in col.lower() for kw in ['health', 'medical', 'patient', 'diagnosis', 'treatment'])]}. "
                f"Violations can result in criminal charges and civil penalties up to $1.5 million per violation.\n\n"
                f"**LGPD (Art. 11):** Similar to GDPR but with Brazilian-specific special categories. "
                f"Requires explicit consent or legal authorization for processing sensitive data.\n\n"
                f"**PIPEDA (S.2, 5):** Requires enhanced consent and security for sensitive information. "
                f"Applies to health information, financial information, and other sensitive data.\n\n"
                f"**Cross-Jurisdictional Differences:**\n"
                f"- **EU (GDPR):** Most restrictive, requires explicit consent or specific legal basis\n"
                f"- **US (HIPAA):** Health-specific, requires covered entity status and business associate agreements\n"
                f"- **Brazil (LGPD):** Similar to GDPR but with Brazilian legal framework\n"
                f"- **Canada (PIPEDA):** Requires enhanced consent and reasonable security\n\n"
                f"**Specific Risk Examples:**\n"
                f"- Gender/sex data can reveal protected characteristics and may be used for discriminatory purposes\n"
                f"- Age data combined with other identifiers can create age-based discrimination risks\n"
                f"- Income/financial data can reveal economic status and create bias in decision-making\n"
                f"- Health-related data requires special handling under HIPAA and other health regulations\n"
                f"- Race/ethnicity data requires careful handling to prevent discrimination\n\n"
                f"**AI/ML Specific Risks:**\n"
                f"- Sensitive attributes can create biased AI models that discriminate against protected groups\n"
                f"- EU AI Act (Art. 10) requires high-quality training data and bias mitigation for high-risk AI systems\n"
                f"- Use of sensitive data in AI systems may require additional transparency and explainability measures\n\n"
                f"**Penalty Differences:**\n"
                f"- GDPR: Up to 4% of global revenue for processing special categories without legal basis\n"
                f"- HIPAA: Up to $1.5 million per violation, criminal penalties up to 10 years imprisonment\n"
                f"- LGPD: Up to 2% of revenue for sensitive data violations\n"
                f"- PIPEDA: Up to $100,000 per violation\n\n"
                f"**Immediate Actions Required:**\n"
                f"1. Document legal basis for processing sensitive data\n"
                f"2. Obtain explicit consent where required\n"
                f"3. Implement enhanced security measures\n"
                f"4. Conduct privacy impact assessments\n"
                f"5. Establish bias monitoring for AI systems using sensitive data\n"
                f"6. Consider data anonymization or pseudonymization"
            )
    
    # Children's Data Risks
    if children_data:
        applicable_policies = []
        for policy in policies:
            if any(p in policy.lower() for p in ['coppa', 'gdpr', 'lgpd', 'pipeda', 'pdpa', 'pipl']):
                applicable_policies.append(policy_refs[policy])
        
        if applicable_policies:
            ref_str = ', '.join(applicable_policies)
            risks.append(f"**Children's Data Detected:** Data may contain information about children under 13/16. Subject to: {ref_str}.")
            
            # Check for age-related columns and sample values
            age_cols = [col for col in df.columns if 'age' in col.lower()]
            sample_ages = []
            if age_cols:
                try:
                    for col in age_cols:
                        sample = pd.to_numeric(df[col].dropna(), errors='coerce')
                        under_18 = sample[sample < 18]
                        if len(under_18) > 0:
                            sample_ages.extend(under_18.head(5).tolist())
                except:
                    pass
            
            explanations.append(
                f"**Children's Data Risk - Detailed Analysis:**\n\n"
                f"**Data Examples:** Your dataset may contain information about children:\n"
                f"- Age-related columns: {age_cols if age_cols else 'None detected'}\n"
                f"- Sample ages under 18: {sample_ages[:5] if sample_ages else 'None detected'}\n\n"
                f"**Policy-Specific Requirements:**\n\n"
                f"**COPPA (16 CFR 312):** Requires parental consent for collecting personal information from children under 13. "
                f"Applies to websites, apps, and online services directed to children. "
                f"Personal information includes: names, addresses, phone numbers, email addresses, photos, videos, audio files, geolocation data, persistent identifiers, and any information collected from children. "
                f"Violations can result in fines up to $43,280 per violation.\n\n"
                f"**GDPR (Art. 8):** Sets the age of consent for data processing at 16, but member states can lower this to 13. "
                f"Processing of children's data requires special protection and consideration of their vulnerability. "
                f"Children have the same data subject rights as adults, but may need assistance from parents/guardians to exercise them.\n\n"
                f"**LGPD (Art. 14):** Requires specific consent for processing children's personal data. "
                f"Consent must be given by at least one parent or legal guardian. "
                f"Applies to children under 18 years of age.\n\n"
                f"**PIPEDA:** Requires enhanced consent for minors. "
                f"Consent must be meaningful and appropriate to the individual's level of understanding.\n\n"
                f"**Cross-Jurisdictional Age Differences:**\n"
                f"- **US (COPPA):** Under 13 years old\n"
                f"- **EU (GDPR):** Under 16 years old (can be lowered to 13 by member states)\n"
                f"- **Brazil (LGPD):** Under 18 years old\n"
                f"- **Canada (PIPEDA):** No specific age, but requires meaningful consent\n\n"
                f"**Specific Risk Examples:**\n"
                f"- Age data showing individuals under 13/16/18 (depending on jurisdiction)\n"
                f"- Student data that may include minors\n"
                f"- Children's product purchase data\n"
                f"- Family account data that may include children's information\n"
                f"- Educational data for students under the age of majority\n\n"
                f"**AI/ML Specific Risks:**\n"
                f"- AI systems trained on children's data may create privacy and safety risks\n"
                f"- Children may not understand how their data is being used in AI systems\n"
                f"- Automated decisions affecting children require special consideration\n\n"
                f"**Penalty Differences:**\n"
                f"- COPPA: Up to $43,280 per violation\n"
                f"- GDPR: Up to 4% of global revenue or €20 million\n"
                f"- LGPD: Up to 2% of revenue or R$50 million\n"
                f"- PIPEDA: Up to $100,000 per violation\n\n"
                f"**Immediate Actions Required:**\n"
                f"1. Verify age of data subjects and implement age verification\n"
                f"2. Obtain parental consent for children under applicable age thresholds\n"
                f"3. Implement special safeguards for children's data\n"
                f"4. Provide clear, age-appropriate privacy notices\n"
                f"5. Limit data collection to what is necessary for the service\n"
                f"6. Implement parental access and control mechanisms"
            )
    
    # Financial Data Risks
    if financial_data:
        applicable_policies = []
        for policy in policies:
            if any(p in policy.lower() for p in ['glba', 'sox', 'basel', 'mifid', 'dodd-frank', 'gdpr', 'lgpd']):
                applicable_policies.append(policy_refs[policy])
        
        if applicable_policies:
            ref_str = ', '.join(applicable_policies)
            risks.append(f"**Financial Data Detected:** Subject to financial regulations: {ref_str}.")
            
            # Identify financial columns and get sample values
            financial_cols = [col for col in df.columns if any(kw in col.lower() for kw in ['account', 'balance', 'transaction', 'payment', 'credit', 'debit', 'loan', 'mortgage', 'investment', 'portfolio', 'revenue', 'income', 'salary', 'wage', 'tax', 'financial', 'bank', 'insurance', 'claim', 'premium', 'policy'])]
            sample_values = {}
            for col in financial_cols:
                try:
                    sample = df[col].dropna().head(3).tolist()
                    sample_values[col] = [str(v) for v in sample if str(v).strip()]
                except:
                    sample_values[col] = ["sample data"]
            
            explanations.append(
                f"**Financial Data Risk - Detailed Analysis:**\n\n"
                f"**Data Examples:** The following columns contain financial information:\n"
                f"{chr(10).join([f'- {col}: Sample values include {sample_values[col][:2]}' for col in financial_cols])}\n\n"
                f"**Policy-Specific Requirements:**\n\n"
                f"**GLBA (15 U.S.C. 6801-6809):** Requires financial institutions to protect customer information. "
                f"Applies to banks, credit unions, insurance companies, and other financial institutions. "
                f"Requires privacy notices, opt-out rights, and security measures. "
                f"Your financial data columns: {', '.join(financial_cols)}. "
                f"Violations can result in fines up to $100,000 per violation and criminal penalties.\n\n"
                f"**SOX (Sarbanes-Oxley Act):** Mandates accurate financial reporting and internal controls. "
                f"Requires data integrity, audit trails, and executive accountability. "
                f"Applies to publicly traded companies and their financial data. "
                f"Violations can result in criminal penalties up to 20 years imprisonment.\n\n"
                f"**Basel III/IV:** International banking regulations requiring capital adequacy and risk management. "
                f"Requires data governance, risk modeling, and stress testing capabilities. "
                f"Applies to banks and financial institutions globally.\n\n"
                f"**MiFID II (2014/65/EU):** EU regulation for financial markets and investor protection. "
                f"Requires transparency, best execution, and conflict of interest management. "
                f"Applies to investment firms, trading venues, and data reporting services.\n\n"
                f"**Dodd-Frank Act:** US financial reform law requiring transparency and consumer protection. "
                f"Requires risk management, data reporting, and regulatory oversight. "
                f"Applies to financial institutions and market participants.\n\n"
                f"**Cross-Regulatory Differences:**\n"
                f"- **GLBA:** US-specific, focuses on customer privacy and security\n"
                f"- **SOX:** US-specific, focuses on financial reporting accuracy\n"
                f"- **Basel:** International, focuses on banking stability and risk management\n"
                f"- **MiFID II:** EU-specific, focuses on market transparency and investor protection\n"
                f"- **Dodd-Frank:** US-specific, focuses on financial stability and consumer protection\n\n"
                f"**Specific Risk Examples:**\n"
                f"- Account numbers and balances can reveal financial status and create security risks\n"
                f"- Transaction data can reveal spending patterns and financial behavior\n"
                f"- Income/salary data can create bias in financial decision-making\n"
                f"- Credit scores and financial history require special handling\n"
                f"- Investment portfolio data requires enhanced security measures\n\n"
                f"**AI/ML Specific Risks:**\n"
                f"- Financial AI systems must comply with regulatory requirements for explainability\n"
                f"- Automated financial decisions may require human oversight under various regulations\n"
                f"- Bias in financial AI systems can lead to discriminatory lending or investment decisions\n\n"
                f"**Penalty Differences:**\n"
                f"- GLBA: Up to $100,000 per violation, criminal penalties\n"
                f"- SOX: Criminal penalties up to 20 years imprisonment\n"
                f"- Basel: Regulatory sanctions, capital requirements, market access restrictions\n"
                f"- MiFID II: Fines vary by member state, market access restrictions\n"
                f"- Dodd-Frank: Fines and regulatory sanctions\n\n"
                f"**Immediate Actions Required:**\n"
                f"1. Implement GLBA-compliant privacy notices and security measures\n"
                f"2. Establish SOX-compliant internal controls and audit trails\n"
                f"3. Implement Basel-compliant risk management and data governance\n"
                f"4. Ensure MiFID II compliance for market transparency\n"
                f"5. Implement Dodd-Frank reporting and transparency requirements\n"
                f"6. Conduct regular financial data security audits"
            )
    
    # Health Data Risks
    if health_data:
        applicable_policies = []
        for policy in policies:
            if any(p in policy.lower() for p in ['hipaa', 'mdr', 'fda ai', 'gdpr', 'lgpd']):
                applicable_policies.append(policy_refs[policy])
        
        if applicable_policies:
            ref_str = ', '.join(applicable_policies)
            risks.append(f"**Health Data Detected:** Subject to healthcare regulations: {ref_str}.")
            
            explanations.append(
                f"**Health Data Risk:** HIPAA requires safeguards for protected health information. "
                f"MDR regulates medical devices including AI-powered diagnostics. "
                f"FDA AI/ML guidelines require validation and monitoring of AI medical devices. "
                f"Violations can result in criminal charges and civil penalties."
            )
    
    # AI/ML Risks
    if ai_risk:
        applicable_policies = []
        for policy in policies:
            if any(p in policy.lower() for p in ['eu ai act', 'ai act ca', 'ai gov sg', 'ai ethics jp', 'oecd ai', 'unesco ai', 'g7 ai', 'gdpr']):
                applicable_policies.append(policy_refs[policy])
        
        if applicable_policies:
            ref_str = ', '.join(applicable_policies)
            risks.append(f"**Automated Decision-Making Risk:** Data may be used for AI/ML systems. Subject to: {ref_str}.")
            
            # Identify AI/ML related columns and get sample values
            ai_cols = [col for col in df.columns if any(kw in col.lower() for kw in ['churn', 'target', 'outcome', 'score', 'risk', 'decision', 'label', 'prediction', 'classification', 'recommendation', 'approval', 'denial', 'fraud', 'anomaly', 'sentiment', 'credit_score', 'insurance_score', 'health_score'])]
            sample_values = {}
            for col in ai_cols:
                try:
                    sample = df[col].dropna().head(3).tolist()
                    sample_values[col] = [str(v) for v in sample if str(v).strip()]
                except:
                    sample_values[col] = ["sample data"]
            
            explanations.append(
                f"**AI/ML Compliance Risk - Detailed Analysis:**\n\n"
                f"**Data Examples:** The following columns suggest AI/ML usage:\n"
                f"{chr(10).join([f'- {col}: Sample values include {sample_values[col][:2]}' for col in ai_cols])}\n\n"
                f"**Policy-Specific Requirements:**\n\n"
                f"**EU AI Act (Art. 6-7, 10, 15):** First comprehensive AI regulation classifying systems by risk level. "
                f"High-risk AI systems require conformity assessment, quality management systems, technical documentation, "
                f"transparency, human oversight, and accuracy/robustness/cybersecurity requirements. "
                f"Your AI-related columns: {', '.join(ai_cols)}. "
                f"These suggest automated decision-making that may fall under high-risk classification.\n\n"
                f"**GDPR (Art. 22):** Gives individuals the right not to be subject to decisions based solely on automated processing. "
                f"Requires human intervention, explanation of logic, and ability to contest decisions. "
                f"Applies to profiling and automated decisions that produce legal effects or significantly affect individuals.\n\n"
                f"**OECD AI Principles:** International framework emphasizing transparency, accountability, and human oversight. "
                f"Requires AI systems to be robust, secure, and safe throughout their lifecycle. "
                f"Emphasizes inclusive growth, sustainable development, and human-centered values.\n\n"
                f"**UNESCO AI Ethics Framework:** Global framework emphasizing human rights, sustainability, and diversity. "
                f"Requires AI systems to respect human dignity and rights, promote sustainable development, and ensure diversity and inclusiveness.\n\n"
                f"**G7 AI Principles:** International governance principles emphasizing transparency, accountability, and human oversight. "
                f"Requires AI systems to be trustworthy, transparent, and accountable.\n\n"
                f"**AI Act Canada (Bill C-27):** Proposed Canadian AI regulation requiring transparency, human oversight, and risk management. "
                f"Would require AI systems to be transparent, accountable, and subject to human oversight.\n\n"
                f"**Cross-Regulatory Differences:**\n"
                f"- **EU AI Act:** Most comprehensive, mandatory requirements for high-risk systems\n"
                f"- **GDPR:** Focuses on individual rights and automated decision-making\n"
                f"- **OECD/UNESCO/G7:** International principles, voluntary but influential\n"
                f"- **Canada:** Proposed regulation, similar to EU AI Act\n"
                f"- **Singapore/Japan:** Voluntary frameworks with regulatory guidance\n\n"
                f"**Specific Risk Examples:**\n"
                f"- Churn prediction models can affect customer relationships and business decisions\n"
                f"- Credit scoring models can affect financial opportunities and access to services\n"
                f"- Fraud detection systems can affect account access and financial transactions\n"
                f"- Sentiment analysis can affect customer service and marketing decisions\n"
                f"- Recommendation systems can affect user experience and business outcomes\n"
                f"- Risk assessment models can affect insurance, lending, and employment decisions\n\n"
                f"**High-Risk AI Applications:**\n"
                f"- Biometric identification and categorization\n"
                f"- Critical infrastructure management\n"
                f"- Education and vocational training\n"
                f"- Employment, worker management, and access to self-employment\n"
                f"- Essential private and public services\n"
                f"- Law enforcement and migration control\n"
                f"- Administration of justice and democratic processes\n\n"
                f"**Penalty Differences:**\n"
                f"- EU AI Act: Up to 7% of global revenue or €35 million\n"
                f"- GDPR: Up to 4% of global revenue for automated decision violations\n"
                f"- Canada (proposed): Up to CAD 25 million or 5% of global revenue\n"
                f"- OECD/UNESCO/G7: No direct fines but international standards\n\n"
                f"**Immediate Actions Required:**\n"
                f"1. Classify AI systems by risk level under EU AI Act\n"
                f"2. Implement GDPR Art. 22 safeguards for automated decisions\n"
                f"3. Establish human oversight and intervention mechanisms\n"
                f"4. Create technical documentation and conformity assessments\n"
                f"5. Implement transparency and explainability measures\n"
                f"6. Establish bias monitoring and fairness testing\n"
                f"7. Create data governance and quality management systems"
            )
    
    # High-Risk AI Applications
    if high_risk_ai:
        risks.append(f"**High-Risk AI Applications Detected:** {high_risk_ai}. Subject to EU AI Act Title III requirements.")
        
        explanations.append(
            f"**High-Risk AI Risk:** EU AI Act (Annex III) defines high-risk AI systems including biometric identification, "
            f"critical infrastructure, education, employment, essential services, law enforcement, migration, justice, and healthcare. "
            f"These require conformity assessment, quality management systems, technical documentation, "
            f"transparency, human oversight, and accuracy/robustness/cybersecurity requirements."
        )
    
    # Missing Data Risks
    if missingness:
        applicable_policies = []
        for policy in policies:
            if any(p in policy.lower() for p in ['eu ai act', 'oecd ai', 'unesco ai', 'g7 ai']):
                applicable_policies.append(policy_refs[policy])
        
        if applicable_policies:
            ref_str = ', '.join(applicable_policies)
            risks.append(f"**Missing Data:** May impact AI fairness and accuracy. Consider: {ref_str}.")
            
            explanations.append(
                f"**Data Quality Risk:** EU AI Act (Art. 10) requires high-quality training data for high-risk AI systems. "
                f"OECD AI Principles emphasize robust, secure, and safe AI systems. "
                f"Missing data can lead to biased models and unfair outcomes, violating fairness requirements."
            )
    
    # Cybersecurity Risks
    if pii_cols or sensitive_cols or financial_data or health_data:
        applicable_policies = []
        for policy in policies:
            if any(p in policy.lower() for p in ['nist', 'iso 27001', 'soc 2', 'pci dss', 'nis2', 'gdpr', 'lgpd']):
                applicable_policies.append(policy_refs[policy])
        
        if applicable_policies:
            ref_str = ', '.join(applicable_policies)
            risks.append(f"**Cybersecurity Requirements:** Sensitive data requires security measures per: {ref_str}.")
            
            explanations.append(
                f"**Cybersecurity Risk:** NIST Cybersecurity Framework provides security controls. "
                f"ISO 27001 sets information security management standards. "
                f"SOC 2 requires security, availability, processing integrity, confidentiality, and privacy controls. "
                f"PCI DSS mandates security for payment card data. "
                f"GDPR (Art. 32) requires appropriate technical and organizational measures."
            )
    
    if not risks:
        risks.append("No major compliance risks detected based on column analysis.")
        explanations.append("The data appears to be low-risk from a compliance perspective.")
    
    report['risks'] = risks
    report['explanations'] = explanations

    # Action Plan
    actions = []
    if pii_cols:
        actions.append(f"**De-identify PII:** Use Truify's PII Analysis tool to identify and hash PII columns: {pii_cols}. Navigate to 'PII Analysis' page to automatically detect and de-identify personal information.")
    if sensitive_cols:
        actions.append(f"**Review Sensitive Data:** Use Truify's PII Analysis tool to review sensitive attributes: {sensitive_cols}. The tool will help you document legal basis and implement appropriate safeguards.")
    if children_data:
        actions.append("**Children's Data:** Use Truify's PII Analysis tool to identify age-related columns and implement age verification. Consider using the 'Reduce Bias' tool to ensure fair treatment across age groups.")
    if financial_data:
        actions.append("**Financial Compliance:** Use Truify's 'Reduce Bias' tool to analyze financial data for bias. The tool can help identify discriminatory patterns and create weighted datasets that comply with financial regulations.")
    if health_data:
        actions.append("**Health Data:** Use Truify's PII Analysis tool to identify health-related columns and implement HIPAA safeguards. The 'Reduce Bias' tool can help ensure fair treatment in healthcare AI systems.")
    if ai_risk:
        actions.append("**AI Governance:** Use Truify's 'Reduce Bias' tool to analyze your dataset for bias before training AI models. The tool provides bias analysis reports and can create weighted datasets to improve AI fairness.")
    if high_risk_ai:
        actions.append(f"**High-Risk AI:** Use Truify's 'Reduce Bias' tool to analyze high-risk AI applications: {high_risk_ai}. The tool provides detailed bias analysis and can help create compliant training datasets.")
    if missingness:
        actions.append("**Data Quality:** Use Truify's 'Fill Missingness' tool to address missing values and ensure AI fairness. The tool evaluates missing data patterns and provides appropriate imputation methods.")
    
    # General actions
    actions.extend([
        "**Data Minimization:** Use Truify's PII Analysis tool to identify unnecessary columns and remove them. The tool helps you keep only essential data for your stated purposes.",
        "**Consent Management:** Use Truify's PII Analysis tool to identify consent-related data and ensure proper consent tracking. The tool can help you document data collection purposes.",
        "**Data Subject Rights:** Use Truify's PII Analysis tool to identify data that subjects may request access to, rectify, or delete. The tool helps you map data subject rights requirements.",
        "**Security Measures:** Use Truify's 'Fill Missingness' tool to identify and handle sensitive data gaps securely. The tool provides secure imputation methods for sensitive information.",
        "**Documentation:** Use Truify's 'Create Compliance Report' tool to generate detailed documentation of your compliance measures. The tool creates comprehensive reports for audit purposes.",
        "**Training:** Use Truify's 'Describe Data' tool to understand your dataset structure and identify compliance risks. The AI-powered description helps staff understand data implications.",
        "**Audit:** Use Truify's 'Create Compliance Report' tool to conduct regular compliance audits. The tool provides comprehensive risk assessments and action plans."
    ])
    
    report['actions'] = actions

    # Policy descriptions for detailed analysis
    policy_descriptions = {
        # Data Protection & Privacy Laws
        "GDPR": "**GDPR (General Data Protection Regulation)** - EU regulation protecting personal data and privacy. Requires lawful basis for processing, data minimization, consent management, and data subject rights. Fines up to 4% of global revenue.",
        "CCPA": "**CCPA (California Consumer Privacy Act)** - California law giving consumers rights over personal information. Requires transparency, opt-out rights, and data deletion. Fines up to $7,500 per violation.",
        "LGPD": "**LGPD (Lei Geral de Proteção de Dados)** - Brazil's comprehensive data protection law. Similar to GDPR, requires legal basis, consent, and data subject rights. Fines up to 2% of revenue.",
        "PIPEDA": "**PIPEDA (Personal Information Protection and Electronic Documents Act)** - Canada's federal privacy law. Requires consent, appropriate purposes, and reasonable security. Fines up to $100,000 per violation.",
        "PDPA_SG": "**PDPA Singapore** - Singapore's data protection law. Requires consent, purpose limitation, and data security. Fines up to SGD 1 million.",
        "PIPL": "**PIPL (Personal Information Protection Law)** - China's comprehensive data protection law. Requires consent, data minimization, and cross-border transfer restrictions. Fines up to 5% of revenue.",
        "APPI": "**APPI (Act on the Protection of Personal Information)** - Japan's data protection law. Requires proper handling, security measures, and data subject rights. Fines up to JPY 100 million.",
        "PDPA_TH": "**PDPA Thailand** - Thailand's Personal Data Protection Act. Requires consent, security measures, and data subject rights. Fines up to THB 5 million.",
        "POPIA": "**POPIA (Protection of Personal Information Act)** - South Africa's data protection law. Requires lawful processing, consent, and security measures. Fines up to ZAR 10 million.",
        "COPPA": "**COPPA (Children's Online Privacy Protection Act)** - US law protecting children under 13. Requires parental consent and special safeguards. Fines up to $43,280 per violation.",
        "GLBA": "**GLBA (Gramm-Leach-Bliley Act)** - US law requiring financial institutions to protect customer information. Requires privacy notices and security measures. Fines up to $100,000 per violation.",
        "SOX": "**SOX (Sarbanes-Oxley Act)** - US law requiring accurate financial reporting and internal controls. Requires data integrity and audit trails. Criminal penalties up to 20 years imprisonment.",
        "ePrivacy": "**ePrivacy Directive** - EU directive on electronic communications privacy. Requires consent for cookies and electronic marketing. Fines vary by member state.",
        "NIS2": "**NIS2 Directive** - EU directive on network and information security. Requires cybersecurity measures for critical infrastructure. Fines up to 2% of global revenue.",
        
        # AI-Specific Regulations
        "EU AI Act": "**EU AI Act** - First comprehensive AI regulation. Classifies AI systems by risk level with specific requirements for high-risk systems. Requires conformity assessment and human oversight. Fines up to 7% of global revenue.",
        "AI Act CA": "**AI Act Canada** - Canada's proposed AI regulation. Requires transparency, human oversight, and risk management for AI systems. Fines up to CAD 25 million.",
        "AI Gov SG": "**AI Governance Framework Singapore** - Voluntary framework for responsible AI development. Emphasizes transparency, fairness, and human-centric AI. No direct fines but regulatory guidance.",
        "AI Ethics JP": "**AI Ethics Guidelines Japan** - Japan's principles for human-centric AI. Emphasizes fairness, transparency, and accountability. No direct fines but regulatory guidance.",
        "OECD AI": "**OECD AI Principles** - International framework for responsible AI. Emphasizes transparency, accountability, and human oversight. No direct fines but international standards.",
        "UNESCO AI": "**UNESCO AI Ethics Framework** - Global framework for AI ethics. Emphasizes human rights, sustainability, and diversity. No direct fines but international guidance.",
        "G7 AI": "**G7 AI Principles** - International AI governance principles. Emphasizes transparency, accountability, and human oversight. No direct fines but international standards.",
        
        # Industry-Specific Regulations
        "HIPAA": "**HIPAA (Health Insurance Portability and Accountability Act)** - US law protecting health information. Requires safeguards, privacy notices, and breach notification. Fines up to $1.5 million per violation.",
        "Basel": "**Basel III/IV** - International banking regulations. Requires capital adequacy, risk management, and data governance. Regulatory sanctions and capital requirements.",
        "MiFID II": "**MiFID II (Markets in Financial Instruments Directive)** - EU financial markets regulation. Requires transparency, investor protection, and data governance. Fines vary by member state.",
        "Dodd-Frank": "**Dodd-Frank Act** - US financial reform law. Requires transparency, risk management, and consumer protection. Fines and regulatory sanctions.",
        "FDA AI": "**FDA AI/ML Guidelines** - US guidelines for AI medical devices. Requires validation, monitoring, and documentation. Regulatory approval requirements.",
        "MDR": "**MDR (Medical Device Regulation)** - EU regulation for medical devices including AI. Requires conformity assessment and post-market surveillance. Fines and market access restrictions.",
        "UNECE": "**UNECE WP.29** - International vehicle cybersecurity regulations. Requires cybersecurity management and incident response. Market access requirements.",
        "ISO 21434": "**ISO 21434** - International standard for vehicle cybersecurity engineering. Requires cybersecurity processes and risk management. Compliance requirements.",
        
        # Cybersecurity & Infrastructure
        "NIST": "**NIST Cybersecurity Framework** - US framework for cybersecurity risk management. Provides voluntary guidelines for security controls. No direct fines but regulatory guidance.",
        "ISO 27001": "**ISO 27001** - International standard for information security management. Requires security controls and risk management. Certification requirements.",
        "SOC 2": "**SOC 2 (Service Organization Control 2)** - US standard for security, availability, and privacy controls. Requires independent audits and reporting. Compliance requirements.",
        "PCI DSS": "**PCI DSS (Payment Card Industry Data Security Standard)** - International standard for payment card security. Requires security controls and regular assessments. Fines and card processing restrictions.",
        
        # Emerging/Proposed Regulations
        "AI Liability": "**AI Liability Directive** - Proposed EU regulation for AI liability. Would require compensation for AI-related damages. Proposed liability framework.",
        "Data Act": "**Data Act** - EU regulation for data sharing and access rights. Requires data portability and interoperability. Fines up to 4% of global revenue.",
        "DSA": "**Digital Services Act** - EU regulation for online platforms. Requires transparency, content moderation, and user protection. Fines up to 6% of global revenue.",
        "DMA": "**Digital Markets Act** - EU regulation for digital market competition. Requires fair practices and interoperability. Fines up to 10% of global revenue."
    }

    # Get current timestamp
    now_local = datetime.now()
    now_gmt = datetime.utcnow()
    
    # Format timestamps
    local_time_str = now_local.strftime("%B %d, %Y at %I:%M:%S %p")
    gmt_time_str = now_gmt.strftime("%B %d, %Y at %I:%M:%S UTC")
    
    # Markdown report
    md = f"# Global Data & AI Compliance Risk Report\n\n"
    
    # Add logo and timestamp header
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "TruifyLogo.png")
    if os.path.exists(logo_path):
        md += f"![](TruifyLogo.png)\n\n"
    else:
        md += "![](TruifyLogo.png)\n\n"
    
    md += f"**Report Generated:**\n"
    md += f"{local_time_str} (Local Time)\n"
    md += f"{gmt_time_str} (GMT/UTC)\n\n"
    md += "---\n\n"
    
    md += "## Data Description\n" + report['description'] + "\n\n"
    md += "## Applicable Regulations\n"
    for policy, ref in policy_refs.items():
        md += f"- {ref}\n"
    md += "\n## Policy Overview\n"
    for policy in policies:
        if policy in policy_descriptions:
            md += f"- {policy_descriptions[policy]}\n"
        else:
            md += f"- **{policy}** - Custom policy selected by user.\n"
    md += "\n## Potential Compliance Risks\n"
    for r in risks:
        md += f"- {r}\n"
    md += "\n## Detailed Risk Analysis\n"
    for e in explanations:
        md += f"- {e}\n"
    md += "\n## Action Plan\n"
    for a in actions:
        md += f"- {a}\n"
    md += f"\n---\n*Report generated by TRUIFY.AI Compliance Module*\n"
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
