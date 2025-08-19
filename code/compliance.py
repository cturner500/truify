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
import json

# --- Policy Template Management ---
def load_policy_templates() -> Dict[str, Dict[str, Any]]:
    """Load all policy templates from JSON files."""
    templates = {}
    policy_dir = os.path.join(os.path.dirname(__file__), "policy_templates")
    
    try:
        # Load the master index first
        index_path = os.path.join(policy_dir, "policy_index.json")
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            # Load each policy template
            for policy_name, policy_info in index["policies"].items():
                template_path = os.path.join(policy_dir, policy_info["filename"])
                if os.path.exists(template_path):
                    with open(template_path, 'r', encoding='utf-8') as f:
                        templates[policy_name] = json.load(f)
                        print(f"Loaded policy template: {policy_name}")
                else:
                    print(f"Warning: Policy template not found: {template_path}")
        else:
            print(f"Warning: Policy index not found at {index_path}")
            
    except Exception as e:
        print(f"Error loading policy templates: {e}")
    
    return templates

def validate_compliance_recommendation(
    llm_output: str, 
    policy_type: str, 
    data_context: Dict[str, Any],
    templates: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """Validate LLM compliance recommendations against policy templates."""
    
    # Try to identify which policy the LLM is referencing
    policy_matches = {}
    for policy_name, template in templates.items():
        # Check if the policy name or category appears in the LLM output
        if (policy_name.lower() in llm_output.lower() or 
            template["metadata"]["name"].lower() in llm_output.lower() or
            template["metadata"]["category"].lower() in llm_output.lower()):
            policy_matches[policy_name] = template
    
    validation_results = {
        "policy_identified": list(policy_matches.keys()),
        "validation_passed": [],
        "validation_failed": [],
        "missing_elements": [],
        "truify_recommendations": [],
        "overall_score": 0.0
    }
    
    if not policy_matches:
        validation_results["validation_failed"].append("No policy identified in LLM output")
        return validation_results
    
    # Validate against each identified policy
    total_checks = 0
    passed_checks = 0
    
    for policy_name, template in policy_matches.items():
        policy_result = {
            "policy": policy_name,
            "category": template["metadata"]["category"],
            "checks": [],
            "score": 0.0
        }
        
        # Check validation rules for each compliance area
        for area, rules in template["validation_rules"].items():
            area_result = {
                "area": area,
                "required_elements": rules.get("required_elements", []),
                "validation_rules": rules.get("validation_rules", []),
                "truify_relevance": rules.get("truify_relevance", "low"),
                "checks": []
            }
            
            # Check if required elements are mentioned in LLM output
            for element in rules["required_elements"]:
                total_checks += 1
                if element.lower() in llm_output.lower():
                    area_result["checks"].append({
                        "element": element,
                        "status": "found",
                        "message": f"Required element '{element}' found in recommendation"
                    })
                    passed_checks += 1
                else:
                    area_result["checks"].append({
                        "element": element,
                        "status": "missing",
                        "message": f"Required element '{element}' not found in recommendation"
                    })
                    validation_results["missing_elements"].append(f"{policy_name}: {element}")
            
            # Check validation rules
            for rule in rules["validation_rules"]:
                total_checks += 1
                if rule.lower() in llm_output.lower():
                    area_result["checks"].append({
                        "rule": rule,
                        "status": "validated",
                        "message": f"Validation rule '{rule}' satisfied"
                    })
                    passed_checks += 1
                else:
                    area_result["checks"].append({
                        "rule": rule,
                        "status": "not_validated",
                        "message": f"Validation rule '{rule}' not satisfied"
                    })
            
            policy_result["checks"].append(area_result)
            
            # Add Truify recommendations if this area has high relevance
            if rules.get("truify_relevance") == "high":
                for tool in template.get("truify_tools", []):
                    if tool.get("relevance") == "high":
                        validation_results["truify_recommendations"].append({
                            "policy": policy_name,
                            "area": area,
                            "tool": tool["tool"],
                            "function": tool["function"],
                            "page": tool["page"],
                            "description": tool["description"]
                        })
        
        # Calculate policy score
        if total_checks > 0:
            policy_result["score"] = (passed_checks / total_checks) * 100
            policy_result["overall_score"] = policy_result["score"]
        
        validation_results["validation_passed"].append(policy_result)
    
    # Calculate overall validation score
    if total_checks > 0:
        validation_results["overall_score"] = (passed_checks / total_checks) * 100
    
    return validation_results

def get_policy_compliance_summary(
    templates: Dict[str, Dict[str, Any]], 
    data_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate a summary of applicable policies based on data context."""
    
    applicable_policies = {
        "high_priority": [],
        "medium_priority": [],
        "low_priority": []
    }
    
    # Analyze data context to determine applicable policies
    has_pii = data_context.get("has_pii", False)
    has_health_data = data_context.get("has_health_data", False)
    has_financial_data = data_context.get("has_financial_data", False)
    has_children_data = data_context.get("has_children_data", False)
    is_ai_system = data_context.get("is_ai_system", False)
    
    for policy_name, template in templates.items():
        relevance_score = 0
        
        # Check if policy is relevant based on data context
        if has_pii and "privacy" in template["metadata"]["category"].lower():
            relevance_score += 3
        
        if has_health_data and "health" in template["metadata"]["name"].lower():
            relevance_score += 4
        
        if has_financial_data and "financial" in template["metadata"]["category"].lower():
            relevance_score += 3
        
        if has_children_data and "children" in template["metadata"]["name"].lower():
            relevance_score += 4
        
        if is_ai_system and "ai" in template["metadata"]["category"].lower():
            relevance_score += 4
        
        # Categorize by relevance
        if relevance_score >= 4:
            applicable_policies["high_priority"].append({
                "name": policy_name,
                "full_name": template["metadata"]["name"],
                "category": template["metadata"]["category"],
                "relevance_score": relevance_score,
                "url": template["metadata"]["url"]
            })
        elif relevance_score >= 2:
            applicable_policies["medium_priority"].append({
                "name": policy_name,
                "full_name": template["metadata"]["name"],
                "category": template["metadata"]["category"],
                "relevance_score": relevance_score,
                "url": template["metadata"]["url"]
            })
        else:
            applicable_policies["low_priority"].append({
                "name": policy_name,
                "full_name": template["metadata"]["name"],
                "category": template["metadata"]["category"],
                "relevance_score": relevance_score,
                "url": template["metadata"]["url"]
            })
    
    return applicable_policies

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

def generate_compliance_recommendations(
    df: pd.DataFrame, 
    data_context: Dict[str, Any], 
    policy_templates: Dict[str, Dict[str, Any]]
) -> str:
    """Generate compliance recommendations using LLM and policy templates."""
    
    # This is a placeholder function that would integrate with your LLM system
    # For now, we'll generate basic recommendations based on the data context
    
    recommendations = []
    
    if data_context["has_pii"]:
        recommendations.append("""
**PII Data Protection Recommendations:**
- Implement data minimization principles to collect only necessary personal information
- Establish clear data retention policies with automatic deletion mechanisms
- Ensure user consent is obtained and can be withdrawn at any time
- Implement strong encryption for personal data at rest and in transit
- Establish data subject rights processes (access, rectification, deletion, portability)
- Designate a Data Protection Officer if required by applicable regulations
""")
    
    if data_context["has_health_data"]:
        recommendations.append("""
**Health Data Protection Recommendations:**
- Implement HIPAA-compliant data handling procedures
- Ensure PHI is properly de-identified or anonymized for research purposes
- Establish strict access controls with role-based permissions
- Implement comprehensive audit logging for all data access
- Develop breach notification procedures with specific timelines
- Ensure data is stored in secure, HIPAA-compliant environments
""")
    
    if data_context["has_financial_data"]:
        recommendations.append("""
**Financial Data Protection Recommendations:**
- Implement GLBA-compliant data security measures
- Establish strong authentication and authorization controls
- Ensure data integrity through validation and verification processes
- Implement comprehensive audit trails for all financial transactions
- Establish incident response procedures for financial data breaches
- Ensure compliance with relevant financial regulations (SOX, Basel, etc.)
""")
    
    if data_context["is_ai_system"]:
        recommendations.append("""
**AI System Compliance Recommendations:**
- Implement bias detection and mitigation procedures
- Ensure training data quality and representativeness
- Establish human oversight mechanisms for AI decisions
- Implement explainability features for AI system outputs
- Conduct regular risk assessments for AI system operations
- Ensure compliance with relevant AI regulations (EU AI Act, etc.)
""")
    
    if data_context["has_children_data"]:
        recommendations.append("""
**Children's Data Protection Recommendations:**
- Implement COPPA-compliant data handling procedures
- Obtain verifiable parental consent before collecting children's data
- Implement strict data minimization for children's information
- Establish secure deletion mechanisms for children's data
- Ensure no personal information is collected from children under 13 without consent
- Implement additional safeguards for children's data security
""")
    
    # Add general recommendations
    recommendations.append("""
**General Compliance Recommendations:**
- Conduct regular compliance audits and assessments
- Implement comprehensive data governance frameworks
- Establish clear data classification and handling procedures
- Provide regular staff training on compliance requirements
- Maintain up-to-date documentation of all compliance measures
- Establish incident response and breach notification procedures
""")
    
    return "\n".join(recommendations)

# --- Main Compliance Evaluation Function ---
def evaluate_compliance_risks(df: pd.DataFrame) -> Dict[str, Any]:
    """Evaluate the DataFrame for compliance risks using policy templates."""
    
    # Load policy templates
    print("Loading policy templates...")
    policy_templates = load_policy_templates()
    
    if not policy_templates:
        print("Warning: No policy templates loaded. Using basic compliance checks only.")
    
    # Basic compliance checks
    pii_columns = identify_pii_columns(df)
    sensitive_columns = identify_sensitive_columns(df)
    has_children_data = identify_children_data(df)
    has_financial_data = identify_financial_data(df)
    has_health_data = identify_health_data(df)
    automated_decision_risk = check_automated_decision_risk(df)
    high_risk_ai_uses = check_high_risk_ai_use(df)
    
    # Create data context for policy relevance
    data_context = {
        "has_pii": len(pii_columns) > 0,
        "has_health_data": has_health_data,
        "has_financial_data": has_financial_data,
        "has_children_data": has_children_data,
        "is_ai_system": automated_decision_risk or len(high_risk_ai_uses) > 0,
        "pii_columns": pii_columns,
        "sensitive_columns": sensitive_columns,
        "high_risk_ai_uses": high_risk_ai_uses
    }
    
    # Get applicable policies based on data context
    applicable_policies = get_policy_compliance_summary(policy_templates, data_context) if policy_templates else {}
    
    # Generate compliance recommendations using LLM (placeholder for now)
    compliance_recommendations = generate_compliance_recommendations(df, data_context, policy_templates)
    
    # Validate recommendations against policy templates
    validation_results = None
    if policy_templates and compliance_recommendations:
        validation_results = validate_compliance_recommendation(
            compliance_recommendations, 
            "auto_detected", 
            data_context, 
            policy_templates
        )
    
    return {
        "data_analysis": {
            "pii_columns": pii_columns,
            "sensitive_columns": sensitive_columns,
            "has_children_data": has_children_data,
            "has_financial_data": has_financial_data,
            "has_health_data": has_health_data,
            "automated_decision_risk": automated_decision_risk,
            "high_risk_ai_uses": high_risk_ai_uses
        },
        "applicable_policies": applicable_policies,
        "compliance_recommendations": compliance_recommendations,
        "validation_results": validation_results,
        "policy_templates_loaded": len(policy_templates) if policy_templates else 0
    }

def generate_markdown_report(compliance_results: Dict[str, Any]) -> str:
    """Generate a comprehensive markdown report from compliance evaluation results."""
    
    report = []
    
    # Header
    report.append("# Compliance Risk Assessment Report")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Policy Templates Loaded:** {compliance_results.get('policy_templates_loaded', 0)}")
    report.append("")
    
    # Data Analysis Summary
    data_analysis = compliance_results.get("data_analysis", {})
    report.append("## Data Analysis Summary")
    report.append("")
    
    if data_analysis.get("pii_columns"):
        report.append(f"**PII Columns Identified:** {len(data_analysis['pii_columns'])}")
        report.append("- " + "\n- ".join(data_analysis["pii_columns"]))
        report.append("")
    
    if data_analysis.get("sensitive_columns"):
        report.append(f"**Sensitive Columns Identified:** {len(data_analysis['sensitive_columns'])}")
        report.append("- " + "\n- ".join(data_analysis["sensitive_columns"]))
        report.append("")
    
    if data_analysis.get("has_children_data"):
        report.append("**⚠️ Children's Data Detected:** COPPA compliance required")
        report.append("")
    
    if data_analysis.get("has_health_data"):
        report.append("**🏥 Health Data Detected:** HIPAA compliance required")
        report.append("")
    
    if data_analysis.get("has_financial_data"):
        report.append("**💰 Financial Data Detected:** GLBA, SOX, Basel compliance may be required")
        report.append("")
    
    if data_analysis.get("automated_decision_risk"):
        report.append("**🤖 Automated Decision Risk Detected:** AI regulations may apply")
        report.append("")
    
    if data_analysis.get("high_risk_ai_uses"):
        report.append("**🚨 High-Risk AI Uses Identified:**")
        for use in data_analysis["high_risk_ai_uses"]:
            report.append(f"- {use}")
        report.append("")
    
    # Applicable Policies
    applicable_policies = compliance_results.get("applicable_policies", {})
    if applicable_policies:
        report.append("## Applicable Policies")
        report.append("")
        
        if applicable_policies.get("high_priority"):
            report.append("### High Priority Policies")
            for policy in applicable_policies["high_priority"]:
                report.append(f"- **{policy['full_name']}** ({policy['category']}) - [Details]({policy['url']})")
            report.append("")
        
        if applicable_policies.get("medium_priority"):
            report.append("### Medium Priority Policies")
            for policy in applicable_policies["medium_priority"]:
                report.append(f"- **{policy['full_name']}** ({policy['category']}) - [Details]({policy['url']})")
            report.append("")
        
        if applicable_policies.get("low_priority"):
            report.append("### Low Priority Policies")
            for policy in applicable_policies["low_priority"]:
                report.append(f"- **{policy['full_name']}** ({policy['category']}) - [Details]({policy['url']})")
            report.append("")
    
    # Compliance Recommendations
    if compliance_results.get("compliance_recommendations"):
        report.append("## Compliance Recommendations")
        report.append("")
        report.append(compliance_results["compliance_recommendations"])
        report.append("")
    
    # Validation Results
    validation_results = compliance_results.get("validation_results")
    if validation_results:
        report.append("## Policy Validation Results")
        report.append("")
        
        if validation_results.get("overall_score") is not None:
            score = validation_results["overall_score"]
            if score >= 80:
                report.append(f"**Overall Compliance Score: 🟢 {score:.1f}%**")
            elif score >= 60:
                report.append(f"**Overall Compliance Score: 🟡 {score:.1f}%**")
            else:
                report.append(f"**Overall Compliance Score: 🔴 {score:.1f}%**")
            report.append("")
        
        if validation_results.get("policy_identified"):
            report.append(f"**Policies Identified:** {', '.join(validation_results['policy_identified'])}")
            report.append("")
        
        if validation_results.get("missing_elements"):
            report.append("**Missing Compliance Elements:**")
            for element in validation_results["missing_elements"]:
                report.append(f"- {element}")
            report.append("")
        
        if validation_results.get("truify_recommendations"):
            report.append("## Truify Tool Recommendations")
            report.append("")
            report.append("The following Truify tools can help address compliance issues:")
            report.append("")
            
            for rec in validation_results["truify_recommendations"]:
                report.append(f"### {rec['tool']}")
                report.append(f"**Policy:** {rec['policy']} - {rec['area']}")
                report.append(f"**Function:** {rec['function']}")
                report.append(f"**Page:** {rec['page']}")
                report.append(f"**Description:** {rec['description']}")
                report.append("")
    
    # Action Plan
    report.append("## Action Plan")
    report.append("")
    report.append("Based on the compliance assessment, consider the following actions:")
    report.append("")
    
    if data_analysis.get("pii_columns"):
        report.append("1. **PII Data Protection:**")
        report.append("   - Use Truify's PII Analysis & Anonymization tool to de-identify sensitive data")
        report.append("   - Implement data minimization and retention policies")
        report.append("   - Establish user consent and rights management processes")
        report.append("")
    
    if data_analysis.get("has_health_data"):
        report.append("2. **Health Data Compliance:**")
        report.append("   - Ensure HIPAA compliance through proper data handling procedures")
        report.append("   - Use Truify's data synthesis tools to create compliant research datasets")
        report.append("   - Implement strict access controls and audit logging")
        report.append("")
    
    if data_analysis.get("is_ai_system"):
        report.append("3. **AI System Compliance:**")
        report.append("   - Use Truify's Bias Analysis tool to identify and mitigate discriminatory patterns")
        report.append("   - Ensure training data quality and representativeness")
        report.append("   - Implement human oversight and explainability features")
        report.append("")
    
    report.append("4. **General Compliance Measures:**")
    report.append("   - Conduct regular compliance audits and assessments")
    report.append("   - Provide staff training on relevant regulations")
    report.append("   - Maintain comprehensive documentation of compliance measures")
    report.append("   - Establish incident response and breach notification procedures")
    report.append("")
    
    # Footer
    report.append("---")
    report.append("*This report was generated by Truify's automated compliance assessment system.*")
    report.append("*For detailed guidance on specific regulations, consult the official policy documents linked above.*")
    
    return "\n".join(report)

# --- Example Usage ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Load CSV from command line
        df = pd.read_csv(sys.argv[1])
        result = evaluate_compliance_risks(df)
        markdown_report = generate_markdown_report(result)
        with open("compliance_report.md", "w") as f:
            f.write(markdown_report)
        print("Compliance report written to compliance_report.md")
    else:
        print("Usage: python compliance.py <datafile.csv>")
