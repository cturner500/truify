#!/usr/bin/env python3
"""
Policy Template Generator

This script generates JSON policy templates for all regulations referenced in compliance.py.
It creates structured templates with validation rules that can be used to validate LLM compliance recommendations.

Run this script once to generate all policy templates, or run it again when policies are updated.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

def create_policy_template(
    name: str,
    version: str,
    category: str,
    url: str,
    description: str,
    validation_rules: Dict[str, Any],
    truify_tools: List[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Create a standardized policy template structure."""
    
    template = {
        "metadata": {
            "name": name,
            "version": version,
            "category": category,
            "url": url,
            "description": description,
            "last_updated": datetime.now().isoformat(),
            "generator_version": "1.0"
        },
        "validation_rules": validation_rules,
        "truify_tools": truify_tools or [],
        "compliance_checks": {
            "data_content": [],
            "data_handling": [],
            "documentation": [],
            "technical_controls": []
        }
    }
    
    return template

def create_gdpr_template() -> Dict[str, Any]:
    """Create GDPR policy template with validation rules."""
    
    validation_rules = {
        "data_minimization": {
            "required_elements": ["purpose_limitation", "data_retention_period", "deletion_process"],
            "validation_rules": ["retention_justified", "deletion_mechanism_exists", "purpose_specific"],
            "truify_relevance": "high"
        },
        "user_rights": {
            "required_elements": ["right_to_access", "right_to_erasure", "right_to_portability", "right_to_rectification"],
            "validation_rules": ["processes_documented", "contact_method_specified", "response_timeframe"],
            "truify_relevance": "medium"
        },
        "legal_basis": {
            "required_elements": ["lawful_basis_identified", "consent_process", "legitimate_interest_assessment"],
            "validation_rules": ["basis_justified", "consent_mechanism_exists", "interest_balancing_done"],
            "truify_relevance": "low"
        },
        "data_protection": {
            "required_elements": ["encryption_mentioned", "access_controls", "breach_notification"],
            "validation_rules": ["security_measures_described", "incident_response_plan", "dpo_contact"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "Dynamic hashing for data de-identification",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Can anonymize PII columns to reduce GDPR compliance risk"
        },
        {
            "tool": "Data Synthesis",
            "function": "Generate synthetic datasets",
            "relevance": "high",
            "page": "Synthesize Data",
            "description": "Creates GDPR-compliant synthetic data for testing"
        },
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns",
            "relevance": "medium",
            "page": "Bias Analysis",
            "description": "Helps ensure automated decisions don't discriminate"
        }
    ]
    
    return create_policy_template(
        name="General Data Protection Regulation",
        version="2024",
        category="Data Protection & Privacy Laws",
        url="https://gdpr-info.eu/",
        description="EU regulation on data protection and privacy for individuals within the European Union",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_hipaa_template() -> Dict[str, Any]:
    """Create HIPAA policy template with validation rules."""
    
    validation_rules = {
        "privacy_rule": {
            "required_elements": ["phi_identification", "minimum_necessary_principle", "patient_consent"],
            "validation_rules": ["phi_protected", "access_limited", "consent_obtained"],
            "truify_relevance": "high"
        },
        "security_rule": {
            "required_elements": ["access_controls", "audit_logs", "encryption_standards"],
            "validation_rules": ["authentication_required", "logging_enabled", "data_encrypted"],
            "truify_relevance": "medium"
        },
        "breach_notification": {
            "required_elements": ["breach_detection", "notification_timeline", "mitigation_steps"],
            "validation_rules": ["process_documented", "timeline_specified", "steps_defined"],
            "truify_relevance": "low"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify PHI columns",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Critical for HIPAA compliance - can anonymize medical identifiers"
        },
        {
            "tool": "Data Synthesis",
            "function": "Generate synthetic medical data",
            "relevance": "high",
            "page": "Synthesize Data",
            "description": "Creates HIPAA-compliant synthetic datasets for research"
        }
    ]
    
    return create_policy_template(
        name="Health Insurance Portability and Accountability Act",
        version="2023",
        category="Industry-Specific Regulations",
        url="https://www.hhs.gov/hipaa/index.html",
        description="US law protecting health information privacy and security",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_ccpa_template() -> Dict[str, Any]:
    """Create CCPA policy template with validation rules."""
    
    validation_rules = {
        "consumer_rights": {
            "required_elements": ["right_to_know", "right_to_delete", "right_to_opt_out"],
            "validation_rules": ["processes_documented", "contact_method_specified", "response_timeframe"],
            "truify_relevance": "medium"
        },
        "data_disclosure": {
            "required_elements": ["data_categories", "business_purposes", "third_party_sharing"],
            "validation_rules": ["categories_listed", "purposes_specified", "sharing_disclosed"],
            "truify_relevance": "low"
        },
        "opt_out_mechanism": {
            "required_elements": ["opt_out_link", "do_not_sell_button", "verification_process"],
            "validation_rules": ["mechanism_visible", "process_simple", "verification_required"],
            "truify_relevance": "low"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify personal information",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Can anonymize personal data to reduce CCPA compliance risk"
        }
    ]
    
    return create_policy_template(
        name="California Consumer Privacy Act",
        version="2023",
        category="Data Protection & Privacy Laws",
        url="https://oag.ca.gov/privacy/ccpa",
        description="California law giving consumers control over personal information",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_eu_ai_act_template() -> Dict[str, Any]:
    """Create EU AI Act template with validation rules."""
    
    validation_rules = {
        "risk_assessment": {
            "required_elements": ["risk_level_determination", "prohibited_uses", "high_risk_requirements"],
            "validation_rules": ["level_justified", "prohibitions_identified", "requirements_met"],
            "truify_relevance": "high"
        },
        "transparency": {
            "required_elements": ["ai_system_disclosure", "decision_explanation", "human_oversight"],
            "validation_rules": ["disclosure_made", "explanation_provided", "oversight_mechanism"],
            "truify_relevance": "medium"
        },
        "data_quality": {
            "required_elements": ["training_data_assessment", "bias_evaluation", "accuracy_metrics"],
            "validation_rules": ["data_evaluated", "bias_identified", "metrics_tracked"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns in data",
            "relevance": "high",
            "page": "Bias Analysis",
            "description": "Critical for EU AI Act compliance - identifies bias in training data"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data completeness and accuracy",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Helps ensure training data meets AI Act quality requirements"
        },
        {
            "tool": "PII Analysis",
            "function": "Identify sensitive data in training sets",
            "relevance": "medium",
            "page": "PII Analysis",
            "description": "Ensures AI systems don't process unnecessary personal data"
        }
    ]
    
    return create_policy_template(
        name="EU AI Act",
        version="2024",
        category="AI-Specific Regulations",
        url="https://artificialintelligenceact.eu/",
        description="European Union regulation on artificial intelligence systems",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_sox_template() -> Dict[str, Any]:
    """Create SOX template with validation rules."""
    
    validation_rules = {
        "financial_reporting": {
            "required_elements": ["internal_controls", "audit_trails", "data_integrity"],
            "validation_rules": ["controls_documented", "trails_maintained", "integrity_verified"],
            "truify_relevance": "medium"
        },
        "data_retention": {
            "required_elements": ["retention_policy", "destruction_procedures", "access_controls"],
            "validation_rules": ["policy_defined", "procedures_documented", "controls_implemented"],
            "truify_relevance": "low"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data completeness and accuracy",
            "relevance": "medium",
            "page": "Describe Data",
            "description": "Helps ensure financial data integrity for SOX compliance"
        }
    ]
    
    return create_policy_template(
        name="Sarbanes-Oxley Act",
        version="2002",
        category="Industry-Specific Regulations",
        url="https://www.sec.gov/about/laws/soa2002.pdf",
        description="US law establishing corporate accountability and financial reporting standards",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_iso_27001_template() -> Dict[str, Any]:
    """Create ISO 27001 template with validation rules."""
    
    validation_rules = {
        "information_security": {
            "required_elements": ["security_policy", "risk_assessment", "access_controls"],
            "validation_rules": ["policy_documented", "risks_assessed", "controls_implemented"],
            "truify_relevance": "medium"
        },
        "data_protection": {
            "required_elements": ["encryption_standards", "backup_procedures", "incident_response"],
            "validation_rules": ["encryption_specified", "backups_tested", "response_plan_exists"],
            "truify_relevance": "low"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis",
            "function": "Identify sensitive data requiring protection",
            "relevance": "medium",
            "page": "PII Analysis",
            "description": "Helps identify data that needs ISO 27001 protection measures"
        }
    ]
    
    return create_policy_template(
        name="ISO 27001",
        version="2022",
        category="Cybersecurity & Infrastructure",
        url="https://www.iso.org/isoiec-27001-information-security.html",
        description="International standard for information security management systems",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_lgpd_template() -> Dict[str, Any]:
    """Create LGPD (Brazil) policy template with validation rules."""
    
    validation_rules = {
        "data_processing": {
            "required_elements": ["legal_basis", "purpose_limitation", "data_retention"],
            "validation_rules": ["basis_justified", "purpose_specific", "retention_limited"],
            "truify_relevance": "high"
        },
        "user_rights": {
            "required_elements": ["right_to_access", "right_to_deletion", "right_to_portability"],
            "validation_rules": ["processes_documented", "contact_method_specified"],
            "truify_relevance": "medium"
        },
        "data_protection": {
            "required_elements": ["security_measures", "breach_notification", "dpo_contact"],
            "validation_rules": ["measures_described", "notification_process", "dpo_available"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify personal data",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Can anonymize personal data to reduce LGPD compliance risk"
        }
    ]
    
    return create_policy_template(
        name="Lei Geral de Proteção de Dados (LGPD)",
        version="2020",
        category="Data Protection & Privacy Laws",
        url="https://www.lgpdbrasil.com.br/",
        description="Brazil's General Data Protection Law",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_pipeda_template() -> Dict[str, Any]:
    """Create PIPEDA (Canada) policy template with validation rules."""
    
    validation_rules = {
        "consent": {
            "required_elements": ["informed_consent", "withdrawal_mechanism", "consent_management"],
            "validation_rules": ["consent_obtained", "withdrawal_available", "management_system"],
            "truify_relevance": "medium"
        },
        "data_limitation": {
            "required_elements": ["purpose_specification", "data_minimization", "retention_policy"],
            "validation_rules": ["purpose_clear", "minimization_applied", "retention_defined"],
            "truify_relevance": "high"
        },
        "individual_rights": {
            "required_elements": ["access_rights", "correction_rights", "complaint_process"],
            "validation_rules": ["rights_documented", "process_clear", "complaint_handling"],
            "truify_relevance": "low"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify personal information",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Can anonymize personal data to reduce PIPEDA compliance risk"
        }
    ]
    
    return create_policy_template(
        name="Personal Information Protection and Electronic Documents Act (PIPEDA)",
        version="2022",
        category="Data Protection & Privacy Laws",
        url="https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/",
        description="Canada's federal privacy law for private sector organizations",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_pdpa_sg_template() -> Dict[str, Any]:
    """Create PDPA (Singapore) policy template with validation rules."""
    
    validation_rules = {
        "consent_obligation": {
            "required_elements": ["consent_obtained", "purpose_disclosure", "withdrawal_right"],
            "validation_rules": ["consent_valid", "purpose_clear", "withdrawal_available"],
            "truify_relevance": "medium"
        },
        "purpose_limitation": {
            "required_elements": ["purpose_specification", "use_limitation", "retention_policy"],
            "validation_rules": ["purpose_documented", "limitation_enforced", "retention_defined"],
            "truify_relevance": "high"
        },
        "data_protection": {
            "required_elements": ["security_measures", "breach_notification", "dpo_contact"],
            "validation_rules": ["measures_implemented", "notification_process", "dpo_available"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify personal data",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Can anonymize personal data to reduce PDPA compliance risk"
        }
    ]
    
    return create_policy_template(
        name="Personal Data Protection Act (Singapore)",
        version="2021",
        category="Data Protection & Privacy Laws",
        url="https://www.pdpc.gov.sg/Overview-of-PDPA/The-Legislation/Personal-Data-Protection-Act",
        description="Singapore's comprehensive data protection law",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_pipl_template() -> Dict[str, Any]:
    """Create PIPL (China) policy template with validation rules."""
    
    validation_rules = {
        "data_processing": {
            "required_elements": ["legal_basis", "purpose_limitation", "consent_obtained"],
            "validation_rules": ["basis_justified", "purpose_specific", "consent_valid"],
            "truify_relevance": "high"
        },
        "data_localization": {
            "required_elements": ["local_storage", "cross_border_assessment", "government_approval"],
            "validation_rules": ["storage_local", "assessment_done", "approval_obtained"],
            "truify_relevance": "low"
        },
        "individual_rights": {
            "required_elements": ["access_rights", "deletion_rights", "portability_rights"],
            "validation_rules": ["rights_documented", "process_clear", "mechanism_available"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify personal information",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Can anonymize personal data to reduce PIPL compliance risk"
        }
    ]
    
    return create_policy_template(
        name="Personal Information Protection Law (China)",
        version="2021",
        category="Data Protection & Privacy Laws",
        url="https://www.pipc.gov.cn/",
        description="China's comprehensive personal information protection law",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_appi_template() -> Dict[str, Any]:
    """Create APPI (Japan) policy template with validation rules."""
    
    validation_rules = {
        "data_utilization": {
            "required_elements": ["purpose_specification", "consent_obtained", "retention_policy"],
            "validation_rules": ["purpose_clear", "consent_valid", "retention_defined"],
            "truify_relevance": "high"
        },
        "individual_rights": {
            "required_elements": ["disclosure_rights", "correction_rights", "suspension_rights"],
            "validation_rules": ["rights_documented", "process_clear", "mechanism_available"],
            "truify_relevance": "medium"
        },
        "data_security": {
            "required_elements": ["security_measures", "breach_notification", "supervision"],
            "validation_rules": ["measures_implemented", "notification_process", "supervision_active"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify personal data",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Can anonymize personal data to reduce APPI compliance risk"
        }
    ]
    
    return create_policy_template(
        name="Act on the Protection of Personal Information (Japan)",
        version="2022",
        category="Data Protection & Privacy Laws",
        url="https://www.ppc.go.jp/en/",
        description="Japan's comprehensive personal information protection law",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_pdpa_th_template() -> Dict[str, Any]:
    """Create PDPA (Thailand) policy template with validation rules."""
    
    validation_rules = {
        "legal_basis": {
            "required_elements": ["lawful_basis", "consent_obtained", "legitimate_interest"],
            "validation_rules": ["basis_justified", "consent_valid", "interest_balanced"],
            "truify_relevance": "medium"
        },
        "data_subject_rights": {
            "required_elements": ["access_rights", "rectification_rights", "erasure_rights"],
            "validation_rules": ["rights_documented", "process_clear", "mechanism_available"],
            "truify_relevance": "medium"
        },
        "data_protection": {
            "required_elements": ["security_measures", "breach_notification", "dpo_contact"],
            "validation_rules": ["measures_implemented", "notification_process", "dpo_available"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify personal data",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Can anonymize personal data to reduce PDPA compliance risk"
        }
    ]
    
    return create_policy_template(
        name="Personal Data Protection Act (Thailand)",
        version="2019",
        category="Data Protection & Privacy Laws",
        url="https://www.pdpc.go.th/",
        description="Thailand's comprehensive data protection law",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_popia_template() -> Dict[str, Any]:
    """Create POPIA (South Africa) policy template with validation rules."""
    
    validation_rules = {
        "processing_limitation": {
            "required_elements": ["lawful_processing", "purpose_limitation", "data_minimization"],
            "validation_rules": ["processing_justified", "purpose_specific", "minimization_applied"],
            "truify_relevance": "high"
        },
        "information_quality": {
            "required_elements": ["data_accuracy", "completeness_assessment", "updating_mechanism"],
            "validation_rules": ["accuracy_verified", "completeness_evaluated", "updating_available"],
            "truify_relevance": "high"
        },
        "data_subject_rights": {
            "required_elements": ["access_rights", "correction_rights", "deletion_rights"],
            "validation_rules": ["rights_documented", "process_clear", "mechanism_available"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify personal data",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Can anonymize personal data to reduce POPIA compliance risk"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data completeness and accuracy",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Helps ensure data quality for POPIA compliance"
        }
    ]
    
    return create_policy_template(
        name="Protection of Personal Information Act (South Africa)",
        version="2013",
        category="Data Protection & Privacy Laws",
        url="https://www.justice.gov.za/inforeg/docs/InfoRegSA-POPIA-act2013-004.pdf",
        description="South Africa's comprehensive data protection law",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_coppa_template() -> Dict[str, Any]:
    """Create COPPA (US) policy template with validation rules."""
    
    validation_rules = {
        "parental_consent": {
            "required_elements": ["verifiable_consent", "consent_mechanism", "consent_management"],
            "validation_rules": ["consent_verified", "mechanism_available", "management_system"],
            "truify_relevance": "low"
        },
        "data_collection": {
            "required_elements": ["age_verification", "minimal_collection", "purpose_limitation"],
            "validation_rules": ["age_verified", "collection_minimal", "purpose_specific"],
            "truify_relevance": "high"
        },
        "data_security": {
            "required_elements": ["security_measures", "data_retention", "deletion_mechanism"],
            "validation_rules": ["measures_implemented", "retention_limited", "deletion_available"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis & Anonymization",
            "function": "De-identify children's personal data",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Critical for COPPA compliance - can anonymize children's identifiers"
        },
        {
            "tool": "Data Synthesis",
            "function": "Generate synthetic children's data",
            "relevance": "high",
            "page": "Synthesize Data",
            "description": "Creates COPPA-compliant synthetic datasets for research"
        }
    ]
    
    return create_policy_template(
        name="Children's Online Privacy Protection Act (COPPA)",
        version="2013",
        category="Data Protection & Privacy Laws",
        url="https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/childrens-online-privacy-protection-rule",
        description="US law protecting children's online privacy",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_glba_template() -> Dict[str, Any]:
    """Create GLBA (US) policy template with validation rules."""
    
    validation_rules = {
        "privacy_notice": {
            "required_elements": ["notice_provided", "opt_out_mechanism", "information_sharing"],
            "validation_rules": ["notice_clear", "mechanism_available", "sharing_disclosed"],
            "truify_relevance": "low"
        },
        "data_security": {
            "required_elements": ["security_program", "access_controls", "incident_response"],
            "validation_rules": ["program_implemented", "controls_active", "response_plan"],
            "truify_relevance": "medium"
        },
        "data_integrity": {
            "required_elements": ["data_accuracy", "completeness_assessment", "verification_process"],
            "validation_rules": ["accuracy_verified", "completeness_evaluated", "verification_available"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate financial data integrity",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Helps ensure financial data accuracy for GLBA compliance"
        },
        {
            "tool": "PII Analysis",
            "function": "Identify financial personal information",
            "relevance": "medium",
            "page": "PII Analysis",
            "description": "Helps identify financial data requiring GLBA protection"
        }
    ]
    
    return create_policy_template(
        name="Gramm-Leach-Bliley Act (GLBA)",
        version="1999",
        category="Data Protection & Privacy Laws",
        url="https://www.ftc.gov/tips-advice/business-center/privacy-and-security/gramm-leach-bliley-act",
        description="US law protecting financial privacy",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_eprivacy_template() -> Dict[str, Any]:
    """Create ePrivacy Directive template with validation rules."""
    
    validation_rules = {
        "electronic_communications": {
            "required_elements": ["consent_obtained", "purpose_limitation", "retention_policy"],
            "validation_rules": ["consent_valid", "purpose_specific", "retention_limited"],
            "truify_relevance": "medium"
        },
        "cookies_tracking": {
            "required_elements": ["cookie_notice", "consent_mechanism", "opt_out_option"],
            "validation_rules": ["notice_clear", "mechanism_available", "opt_out_working"],
            "truify_relevance": "low"
        },
        "marketing_communications": {
            "required_elements": ["opt_in_consent", "unsubscribe_mechanism", "sender_identification"],
            "validation_rules": ["consent_obtained", "unsubscribe_available", "sender_identified"],
            "truify_relevance": "low"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis",
            "function": "Identify communication-related personal data",
            "relevance": "medium",
            "page": "PII Analysis",
            "description": "Helps identify data covered by ePrivacy Directive"
        }
    ]
    
    return create_policy_template(
        name="ePrivacy Directive",
        version="2002",
        category="Data Protection & Privacy Laws",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32002L0058",
        description="EU directive on privacy in electronic communications",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_nis2_template() -> Dict[str, Any]:
    """Create NIS2 Directive template with validation rules."""
    
    validation_rules = {
        "cybersecurity_measures": {
            "required_elements": ["security_policies", "incident_response", "business_continuity"],
            "validation_rules": ["policies_implemented", "response_plan_exists", "continuity_ensured"],
            "truify_relevance": "medium"
        },
        "risk_management": {
            "required_elements": ["risk_assessment", "mitigation_strategies", "monitoring_systems"],
            "validation_rules": ["assessment_conducted", "strategies_implemented", "monitoring_active"],
            "truify_relevance": "medium"
        },
        "incident_reporting": {
            "required_elements": ["detection_capabilities", "reporting_timeline", "coordination_mechanism"],
            "validation_rules": ["detection_working", "timeline_met", "coordination_established"],
            "truify_relevance": "low"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data security and integrity",
            "relevance": "medium",
            "page": "Describe Data",
            "description": "Helps assess data security for NIS2 compliance"
        }
    ]
    
    return create_policy_template(
        name="NIS2 Directive",
        version="2022",
        category="Data Protection & Privacy Laws",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2555",
        description="EU directive on network and information security",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_ai_act_ca_template() -> Dict[str, Any]:
    """Create AI Act (Canada) template with validation rules."""
    
    validation_rules = {
        "ai_system_assessment": {
            "required_elements": ["risk_classification", "impact_assessment", "mitigation_measures"],
            "validation_rules": ["classification_justified", "assessment_complete", "measures_implemented"],
            "truify_relevance": "high"
        },
        "data_governance": {
            "required_elements": ["data_quality_assessment", "bias_evaluation", "transparency_measures"],
            "validation_rules": ["quality_evaluated", "bias_identified", "transparency_ensured"],
            "truify_relevance": "high"
        },
        "human_oversight": {
            "required_elements": ["oversight_mechanism", "intervention_capability", "accountability_framework"],
            "validation_rules": ["mechanism_active", "capability_demonstrated", "framework_established"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns in data",
            "relevance": "high",
            "page": "Bias Analysis",
            "description": "Critical for Canadian AI Act compliance - identifies bias in training data"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data completeness and accuracy",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Helps ensure training data meets Canadian AI Act quality requirements"
        }
    ]
    
    return create_policy_template(
        name="Artificial Intelligence and Data Act (Canada)",
        version="2023",
        category="AI-Specific Regulations",
        url="https://www.parl.ca/DocumentViewer/en/44-1/bill/C-27/third-reading",
        description="Canada's comprehensive AI regulation framework",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_ai_gov_sg_template() -> Dict[str, Any]:
    """Create AI Governance Framework (Singapore) template with validation rules."""
    
    validation_rules = {
        "internal_governance": {
            "required_elements": ["ai_governance_policy", "risk_management", "training_programs"],
            "validation_rules": ["policy_established", "management_active", "training_conducted"],
            "truify_relevance": "medium"
        },
        "human_ai_interaction": {
            "required_elements": ["human_oversight", "decision_explanation", "intervention_mechanism"],
            "validation_rules": ["oversight_implemented", "explanation_provided", "intervention_available"],
            "truify_relevance": "high"
        },
        "operations_management": {
            "required_elements": ["incident_response", "business_continuity", "monitoring_systems"],
            "validation_rules": ["response_plan_exists", "continuity_ensured", "monitoring_active"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns in data",
            "relevance": "high",
            "page": "Bias Analysis",
            "description": "Critical for Singapore AI Governance Framework compliance"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data completeness and accuracy",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Helps ensure training data meets Singapore AI governance requirements"
        }
    ]
    
    return create_policy_template(
        name="Model AI Governance Framework (Singapore)",
        version="2020",
        category="AI-Specific Regulations",
        url="https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework",
        description="Singapore's voluntary AI governance framework",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_ai_ethics_jp_template() -> Dict[str, Any]:
    """Create AI Ethics Guidelines (Japan) template with validation rules."""
    
    validation_rules = {
        "human_centric_approach": {
            "required_elements": ["human_dignity", "privacy_protection", "autonomy_respect"],
            "validation_rules": ["dignity_respected", "privacy_ensured", "autonomy_maintained"],
            "truify_relevance": "medium"
        },
        "fairness_transparency": {
            "required_elements": ["bias_mitigation", "explainability", "accountability"],
            "validation_rules": ["bias_addressed", "decisions_explainable", "responsibility_clear"],
            "truify_relevance": "high"
        },
        "safety_security": {
            "required_elements": ["safety_measures", "security_protocols", "incident_response"],
            "validation_rules": ["measures_implemented", "protocols_active", "response_ready"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns in data",
            "relevance": "high",
            "page": "Bias Analysis",
            "description": "Critical for Japanese AI Ethics compliance - ensures fairness"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data completeness and accuracy",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Helps ensure data quality for Japanese AI ethics requirements"
        }
    ]
    
    return create_policy_template(
        name="Social Principles of Human-Centric AI (Japan)",
        version="2019",
        category="AI-Specific Regulations",
        url="https://www.cao.go.jp/ai-policy/ai-policy_en.html",
        description="Japan's human-centric AI ethics principles",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_oecd_ai_template() -> Dict[str, Any]:
    """Create OECD AI Principles template with validation rules."""
    
    validation_rules = {
        "inclusive_growth": {
            "required_elements": ["benefit_distribution", "access_equity", "skill_development"],
            "validation_rules": ["benefits_shared", "access_fair", "skills_supported"],
            "truify_relevance": "low"
        },
        "human_centered_values": {
            "required_elements": ["human_rights", "democratic_values", "diversity_respect"],
            "validation_rules": ["rights_protected", "values_upheld", "diversity_celebrated"],
            "truify_relevance": "medium"
        },
        "transparency_explainability": {
            "required_elements": ["decision_explanation", "system_disclosure", "information_access"],
            "validation_rules": ["explanation_clear", "disclosure_made", "access_provided"],
            "truify_relevance": "high"
        },
        "robustness_security": {
            "required_elements": ["safety_measures", "security_protocols", "fallback_mechanisms"],
            "validation_rules": ["measures_implemented", "protocols_active", "fallbacks_available"],
            "truify_relevance": "medium"
        },
        "accountability": {
            "required_elements": ["responsibility_assignment", "oversight_mechanism", "redress_process"],
            "validation_rules": ["responsibility_clear", "oversight_active", "redress_available"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns in data",
            "relevance": "high",
            "page": "Bias Analysis",
            "description": "Critical for OECD AI Principles compliance - ensures fairness"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data completeness and accuracy",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Helps ensure data quality for OECD AI principles"
        }
    ]
    
    return create_policy_template(
        name="OECD AI Principles",
        version="2019",
        category="AI-Specific Regulations",
        url="https://oecd.ai/en/ai-principles",
        description="International AI ethics principles by OECD",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_unesco_ai_template() -> Dict[str, Any]:
    """Create UNESCO AI Ethics Framework template with validation rules."""
    
    validation_rules = {
        "human_rights": {
            "required_elements": ["rights_assessment", "impact_evaluation", "mitigation_measures"],
            "validation_rules": ["assessment_complete", "impact_evaluated", "measures_implemented"],
            "truify_relevance": "high"
        },
        "sustainability": {
            "required_elements": ["environmental_impact", "resource_efficiency", "long_term_planning"],
            "validation_rules": ["impact_assessed", "efficiency_optimized", "planning_established"],
            "truify_relevance": "medium"
        },
        "diversity_inclusion": {
            "required_elements": ["bias_mitigation", "representation_ensured", "accessibility_provided"],
            "validation_rules": ["bias_addressed", "representation_fair", "accessibility_achieved"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns in data",
            "relevance": "high",
            "page": "Bias Analysis",
            "description": "Critical for UNESCO AI Ethics compliance - ensures diversity and inclusion"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data completeness and accuracy",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Helps ensure data quality for UNESCO AI ethics requirements"
        }
    ]
    
    return create_policy_template(
        name="UNESCO AI Ethics Framework",
        version="2021",
        category="AI-Specific Regulations",
        url="https://en.unesco.org/artificial-intelligence/ethics",
        description="UNESCO's global AI ethics framework",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_g7_ai_template() -> Dict[str, Any]:
    """Create G7 AI Principles template with validation rules."""
    
    validation_rules = {
        "trustworthy_ai": {
            "required_elements": ["reliability_assessment", "safety_measures", "security_protocols"],
            "validation_rules": ["reliability_verified", "safety_ensured", "security_implemented"],
            "truify_relevance": "high"
        },
        "human_centric": {
            "required_elements": ["human_oversight", "decision_explanation", "intervention_capability"],
            "validation_rules": ["oversight_active", "explanation_provided", "intervention_available"],
            "truify_relevance": "high"
        },
        "transparency": {
            "required_elements": ["system_disclosure", "process_explanation", "information_access"],
            "validation_rules": ["disclosure_made", "explanation_clear", "access_provided"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns in data",
            "relevance": "high",
            "page": "Bias Analysis",
            "description": "Critical for G7 AI Principles compliance - ensures trustworthy AI"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data completeness and accuracy",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Helps ensure data quality for G7 AI principles"
        }
    ]
    
    return create_policy_template(
        name="G7 AI Principles",
        version="2023",
        category="AI-Specific Regulations",
        url="https://www.g7uk.org/g7-ai-principles/",
        description="G7 nations' AI governance principles",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_basel_template() -> Dict[str, Any]:
    """Create Basel III/IV template with validation rules."""
    
    validation_rules = {
        "capital_adequacy": {
            "required_elements": ["capital_ratios", "risk_weighting", "stress_testing"],
            "validation_rules": ["ratios_adequate", "weighting_appropriate", "testing_conducted"],
            "truify_relevance": "medium"
        },
        "risk_management": {
            "required_elements": ["risk_framework", "governance_structure", "monitoring_systems"],
            "validation_rules": ["framework_established", "structure_clear", "monitoring_active"],
            "truify_relevance": "medium"
        },
        "data_quality": {
            "required_elements": ["data_accuracy", "completeness_assessment", "validation_processes"],
            "validation_rules": ["accuracy_verified", "completeness_evaluated", "validation_ongoing"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate financial data integrity",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Critical for Basel compliance - ensures financial data accuracy"
        }
    ]
    
    return create_policy_template(
        name="Basel III/IV Banking Regulations",
        version="2023",
        category="Industry-Specific Regulations",
        url="https://www.bis.org/bcbs/basel3.htm",
        description="International banking capital and risk standards",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_mifid_template() -> Dict[str, Any]:
    """Create MiFID II template with validation rules."""
    
    validation_rules = {
        "client_protection": {
            "required_elements": ["suitability_assessment", "best_execution", "conflict_management"],
            "validation_rules": ["assessment_conducted", "execution_ensured", "conflicts_resolved"],
            "truify_relevance": "medium"
        },
        "transparency": {
            "required_elements": ["pre_trade_disclosure", "post_trade_reporting", "market_data"],
            "validation_rules": ["disclosure_made", "reporting_accurate", "data_available"],
            "truify_relevance": "medium"
        },
        "data_governance": {
            "required_elements": ["data_quality", "retention_policy", "access_controls"],
            "validation_rules": ["quality_maintained", "retention_enforced", "controls_active"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate trading data integrity",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Critical for MiFID II compliance - ensures trading data accuracy"
        }
    ]
    
    return create_policy_template(
        name="Markets in Financial Instruments Directive II (MiFID II)",
        version="2014",
        category="Industry-Specific Regulations",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32014L0065",
        description="EU regulation on financial markets and investment services",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_dodd_frank_template() -> Dict[str, Any]:
    """Create Dodd-Frank template with validation rules."""
    
    validation_rules = {
        "derivatives_regulation": {
            "required_elements": ["clearing_requirements", "trade_reporting", "capital_standards"],
            "validation_rules": ["clearing_mandatory", "reporting_accurate", "standards_met"],
            "truify_relevance": "medium"
        },
        "risk_management": {
            "required_elements": ["risk_limits", "stress_testing", "liquidity_requirements"],
            "validation_rules": ["limits_enforced", "testing_regular", "liquidity_adequate"],
            "truify_relevance": "medium"
        },
        "data_integrity": {
            "required_elements": ["data_accuracy", "audit_trails", "verification_processes"],
            "validation_rules": ["accuracy_verified", "trails_maintained", "verification_ongoing"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate financial data integrity",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Critical for Dodd-Frank compliance - ensures financial data accuracy"
        }
    ]
    
    return create_policy_template(
        name="Dodd-Frank Wall Street Reform and Consumer Protection Act",
        version="2010",
        category="Industry-Specific Regulations",
        url="https://www.congress.gov/bill/111th-congress/house-bill/4173",
        description="US financial reform legislation",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_fda_ai_template() -> Dict[str, Any]:
    """Create FDA AI/ML Guidelines template with validation rules."""
    
    validation_rules = {
        "clinical_validation": {
            "required_elements": ["performance_metrics", "clinical_evidence", "safety_assessment"],
            "validation_rules": ["metrics_defined", "evidence_sufficient", "safety_verified"],
            "truify_relevance": "high"
        },
        "data_quality": {
            "required_elements": ["data_representativeness", "bias_assessment", "quality_metrics"],
            "validation_rules": ["data_representative", "bias_evaluated", "quality_measured"],
            "truify_relevance": "high"
        },
        "change_management": {
            "required_elements": ["change_protocol", "validation_process", "regulatory_notification"],
            "validation_rules": ["protocol_established", "process_documented", "notification_timely"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns in medical data",
            "relevance": "high",
            "page": "Bias Analysis",
            "description": "Critical for FDA AI compliance - ensures medical AI systems are fair"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate medical data quality",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Critical for FDA AI compliance - ensures medical data quality"
        }
    ]
    
    return create_policy_template(
        name="FDA AI/ML Software as a Medical Device Guidelines",
        version="2021",
        category="Industry-Specific Regulations",
        url="https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-software-medical-device",
        description="US FDA guidelines for AI/ML medical devices",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_mdr_template() -> Dict[str, Any]:
    """Create MDR template with validation rules."""
    
    validation_rules = {
        "clinical_evaluation": {
            "required_elements": ["clinical_data", "performance_metrics", "safety_profile"],
            "validation_rules": ["data_sufficient", "metrics_defined", "safety_assessed"],
            "truify_relevance": "high"
        },
        "data_governance": {
            "required_elements": ["data_quality", "traceability", "verification_processes"],
            "validation_rules": ["quality_maintained", "traceability_ensured", "verification_ongoing"],
            "truify_relevance": "high"
        },
        "post_market_surveillance": {
            "required_elements": ["monitoring_systems", "incident_reporting", "corrective_actions"],
            "validation_rules": ["monitoring_active", "reporting_timely", "actions_effective"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate medical device data quality",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Critical for MDR compliance - ensures medical device data quality"
        }
    ]
    
    return create_policy_template(
        name="Medical Device Regulation (MDR)",
        version="2017",
        category="Industry-Specific Regulations",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745",
        description="EU regulation on medical devices",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_unece_template() -> Dict[str, Any]:
    """Create UNECE WP.29 template with validation rules."""
    
    validation_rules = {
        "cybersecurity_management": {
            "required_elements": ["security_policy", "risk_assessment", "incident_response"],
            "validation_rules": ["policy_established", "assessment_conducted", "response_ready"],
            "truify_relevance": "medium"
        },
        "software_updates": {
            "required_elements": ["update_mechanism", "verification_process", "rollback_capability"],
            "validation_rules": ["mechanism_available", "verification_ongoing", "rollback_ensured"],
            "truify_relevance": "medium"
        },
        "data_protection": {
            "required_elements": ["data_classification", "access_controls", "encryption_standards"],
            "validation_rules": ["classification_clear", "controls_active", "encryption_implemented"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate vehicle data quality",
            "relevance": "medium",
            "page": "Describe Data",
            "description": "Helps ensure vehicle data quality for UNECE compliance"
        }
    ]
    
    return create_policy_template(
        name="UNECE WP.29 Vehicle Cybersecurity Regulations",
        version="2021",
        category="Industry-Specific Regulations",
        url="https://unece.org/transport/vehicle-regulations",
        description="UN vehicle cybersecurity and software update regulations",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_iso_21434_template() -> Dict[str, Any]:
    """Create ISO 21434 template with validation rules."""
    
    validation_rules = {
        "cybersecurity_engineering": {
            "required_elements": ["security_requirements", "threat_analysis", "risk_assessment"],
            "validation_rules": ["requirements_defined", "analysis_complete", "assessment_conducted"],
            "truify_relevance": "medium"
        },
        "security_validation": {
            "required_elements": ["testing_methodology", "verification_process", "validation_criteria"],
            "validation_rules": ["methodology_established", "process_documented", "criteria_met"],
            "truify_relevance": "medium"
        },
        "continuous_monitoring": {
            "required_elements": ["monitoring_systems", "incident_detection", "response_procedures"],
            "validation_rules": ["monitoring_active", "detection_working", "procedures_established"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate cybersecurity data quality",
            "relevance": "medium",
            "page": "Describe Data",
            "description": "Helps ensure cybersecurity data quality for ISO 21434 compliance"
        }
    ]
    
    return create_policy_template(
        name="ISO 21434 Road Vehicle Cybersecurity Engineering",
        version="2021",
        category="Industry-Specific Regulations",
        url="https://www.iso.org/standard/70918.html",
        description="International standard for automotive cybersecurity",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_nist_template() -> Dict[str, Any]:
    """Create NIST Cybersecurity Framework template with validation rules."""
    
    validation_rules = {
        "identify": {
            "required_elements": ["asset_inventory", "risk_assessment", "governance_framework"],
            "validation_rules": ["inventory_complete", "assessment_conducted", "framework_established"],
            "truify_relevance": "medium"
        },
        "protect": {
            "required_elements": ["access_controls", "data_security", "maintenance_procedures"],
            "validation_rules": ["controls_implemented", "security_ensured", "procedures_followed"],
            "truify_relevance": "medium"
        },
        "detect": {
            "required_elements": ["monitoring_systems", "anomaly_detection", "incident_detection"],
            "validation_rules": ["monitoring_active", "detection_working", "incidents_identified"],
            "truify_relevance": "medium"
        },
        "respond": {
            "required_elements": ["response_plan", "communications", "analysis_process"],
            "validation_rules": ["plan_established", "communications_clear", "analysis_ongoing"],
            "truify_relevance": "low"
        },
        "recover": {
            "required_elements": ["recovery_plan", "improvements", "communications"],
            "validation_rules": ["plan_ready", "improvements_identified", "communications_established"],
            "truify_relevance": "low"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data security and integrity",
            "relevance": "medium",
            "page": "Describe Data",
            "description": "Helps assess data security for NIST framework compliance"
        }
    ]
    
    return create_policy_template(
        name="NIST Cybersecurity Framework",
        version="2018",
        category="Cybersecurity & Infrastructure",
        url="https://www.nist.gov/cyberframework",
        description="US cybersecurity framework for critical infrastructure",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_soc2_template() -> Dict[str, Any]:
    """Create SOC 2 template with validation rules."""
    
    validation_rules = {
        "security": {
            "required_elements": ["access_controls", "encryption", "incident_response"],
            "validation_rules": ["controls_effective", "encryption_implemented", "response_ready"],
            "truify_relevance": "medium"
        },
        "availability": {
            "required_elements": ["uptime_metrics", "backup_procedures", "disaster_recovery"],
            "validation_rules": ["metrics_tracked", "backups_regular", "recovery_tested"],
            "truify_relevance": "low"
        },
        "processing_integrity": {
            "required_elements": ["data_validation", "error_handling", "quality_controls"],
            "validation_rules": ["validation_ongoing", "errors_handled", "controls_active"],
            "truify_relevance": "high"
        },
        "confidentiality": {
            "required_elements": ["data_classification", "encryption_standards", "access_restrictions"],
            "validation_rules": ["classification_clear", "encryption_implemented", "restrictions_enforced"],
            "truify_relevance": "medium"
        },
        "privacy": {
            "required_elements": ["consent_management", "data_minimization", "individual_rights"],
            "validation_rules": ["consent_tracked", "minimization_applied", "rights_respected"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data processing integrity",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Critical for SOC 2 compliance - ensures data processing integrity"
        },
        {
            "tool": "PII Analysis",
            "function": "Identify and protect sensitive data",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Critical for SOC 2 privacy compliance"
        }
    ]
    
    return create_policy_template(
        name="SOC 2 Service Organization Control 2",
        version="2017",
        category="Cybersecurity & Infrastructure",
        url="https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html",
        description="AICPA standard for service organization controls",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_pci_dss_template() -> Dict[str, Any]:
    """Create PCI DSS template with validation rules."""
    
    validation_rules = {
        "network_security": {
            "required_elements": ["firewall_configuration", "network_segmentation", "access_controls"],
            "validation_rules": ["firewall_active", "segmentation_implemented", "controls_enforced"],
            "truify_relevance": "medium"
        },
        "cardholder_data": {
            "required_elements": ["data_encryption", "retention_policy", "disposal_procedures"],
            "validation_rules": ["encryption_implemented", "retention_enforced", "disposal_secure"],
            "truify_relevance": "high"
        },
        "vulnerability_management": {
            "required_elements": ["security_patches", "malware_protection", "security_testing"],
            "validation_rules": ["patches_current", "protection_active", "testing_regular"],
            "truify_relevance": "medium"
        },
        "access_control": {
            "required_elements": ["user_authentication", "privilege_management", "physical_security"],
            "validation_rules": ["authentication_strong", "privileges_limited", "security_maintained"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis",
            "function": "Identify payment card data",
            "relevance": "high",
            "page": "PII Analysis",
            "description": "Critical for PCI DSS compliance - identifies cardholder data"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate payment data integrity",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Critical for PCI DSS compliance - ensures payment data quality"
        }
    ]
    
    return create_policy_template(
        name="PCI DSS Payment Card Industry Data Security Standard",
        version="4.0",
        category="Cybersecurity & Infrastructure",
        url="https://www.pcisecuritystandards.org/",
        description="Payment card industry security standards",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_ai_liability_template() -> Dict[str, Any]:
    """Create AI Liability Directive template with validation rules."""
    
    validation_rules = {
        "liability_framework": {
            "required_elements": ["liability_assignment", "compensation_mechanism", "burden_of_proof"],
            "validation_rules": ["assignment_clear", "mechanism_established", "burden_defined"],
            "truify_relevance": "low"
        },
        "ai_system_tracking": {
            "required_elements": ["system_identification", "operation_logging", "decision_records"],
            "validation_rules": ["identification_clear", "logging_active", "records_maintained"],
            "truify_relevance": "medium"
        },
        "risk_assessment": {
            "required_elements": ["risk_evaluation", "mitigation_measures", "monitoring_systems"],
            "validation_rules": ["evaluation_conducted", "measures_implemented", "monitoring_active"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Bias Analysis",
            "function": "Identify discriminatory patterns in data",
            "relevance": "high",
            "page": "Bias Analysis",
            "description": "Critical for AI Liability Directive compliance - reduces liability risk"
        },
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data quality and reliability",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Critical for AI Liability Directive compliance - ensures data reliability"
        }
    ]
    
    return create_policy_template(
        name="AI Liability Directive (EU)",
        version="2022",
        category="Emerging/Proposed Regulations",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52022PC0496",
        description="Proposed EU directive on AI liability and compensation",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_data_act_template() -> Dict[str, Any]:
    """Create Data Act template with validation rules."""
    
    validation_rules = {
        "data_sharing": {
            "required_elements": ["sharing_agreements", "access_mechanisms", "quality_standards"],
            "validation_rules": ["agreements_established", "mechanisms_available", "standards_met"],
            "truify_relevance": "medium"
        },
        "data_portability": {
            "required_elements": ["portability_mechanism", "format_standards", "transfer_process"],
            "validation_rules": ["mechanism_available", "standards_defined", "process_clear"],
            "truify_relevance": "medium"
        },
        "data_governance": {
            "required_elements": ["data_quality", "access_controls", "monitoring_systems"],
            "validation_rules": ["quality_maintained", "controls_active", "monitoring_ongoing"],
            "truify_relevance": "high"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data quality for sharing",
            "relevance": "high",
            "page": "Describe Data",
            "description": "Critical for Data Act compliance - ensures data quality for sharing"
        },
        {
            "tool": "PII Analysis",
            "function": "Identify and protect sensitive data",
            "relevance": "medium",
            "page": "PII Analysis",
            "description": "Helps ensure data protection during sharing processes"
        }
    ]
    
    return create_policy_template(
        name="Data Act (EU)",
        version="2022",
        category="Emerging/Proposed Regulations",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52022PC0068",
        description="EU regulation on data sharing and access rights",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_dsa_template() -> Dict[str, Any]:
    """Create Digital Services Act template with validation rules."""
    
    validation_rules = {
        "content_moderation": {
            "required_elements": ["moderation_policies", "appeal_process", "transparency_reports"],
            "validation_rules": ["policies_clear", "process_fair", "reports_published"],
            "truify_relevance": "low"
        },
        "user_protection": {
            "required_elements": ["user_rights", "complaint_mechanism", "redress_process"],
            "validation_rules": ["rights_respected", "mechanism_available", "process_effective"],
            "truify_relevance": "low"
        },
        "data_transparency": {
            "required_elements": ["algorithm_disclosure", "data_usage", "targeting_information"],
            "validation_rules": ["disclosure_made", "usage_clear", "information_provided"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "PII Analysis",
            "function": "Identify personal data in digital services",
            "relevance": "medium",
            "page": "PII Analysis",
            "description": "Helps ensure DSA compliance by identifying personal data"
        }
    ]
    
    return create_policy_template(
        name="Digital Services Act (DSA)",
        version="2022",
        category="Emerging/Proposed Regulations",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2065",
        description="EU regulation on online platform responsibility",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_dma_template() -> Dict[str, Any]:
    """Create Digital Markets Act template with validation rules."""
    
    validation_rules = {
        "gatekeeper_obligations": {
            "required_elements": ["interoperability_standards", "data_portability", "access_conditions"],
            "validation_rules": ["standards_established", "portability_available", "conditions_fair"],
            "truify_relevance": "medium"
        },
        "anti_competitive_measures": {
            "required_elements": ["self_preference_prohibition", "data_usage_restrictions", "fair_ranking"],
            "validation_rules": ["prohibition_enforced", "restrictions_applied", "ranking_fair"],
            "truify_relevance": "low"
        },
        "transparency_requirements": {
            "required_elements": ["algorithm_disclosure", "data_usage", "business_terms"],
            "validation_rules": ["disclosure_made", "usage_clear", "terms_transparent"],
            "truify_relevance": "medium"
        }
    }
    
    truify_tools = [
        {
            "tool": "Data Quality Assessment",
            "function": "Evaluate data quality for interoperability",
            "relevance": "medium",
            "page": "Describe Data",
            "description": "Helps ensure DMA compliance by ensuring data quality for interoperability"
        }
    ]
    
    return create_policy_template(
        name="Digital Markets Act (DMA)",
        version="2022",
        category="Emerging/Proposed Regulations",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L1925",
        description="EU regulation on digital market competition",
        validation_rules=validation_rules,
        truify_tools=truify_tools
    )

def create_policy_templates() -> Dict[str, Dict[str, Any]]:
    """Create all policy templates."""
    
    templates = {
        "gdpr": create_gdpr_template(),
        "hipaa": create_hipaa_template(),
        "ccpa": create_ccpa_template(),
        "eu_ai_act": create_eu_ai_act_template(),
        "sox": create_sox_template(),
        "iso_27001": create_iso_27001_template(),
        "lgpd": create_lgpd_template(),
        "pipeda": create_pipeda_template(),
        "pdpa_sg": create_pdpa_sg_template(),
        "pipl": create_pipl_template(),
        "appi": create_appi_template(),
        "pdpa_th": create_pdpa_th_template(),
        "popia": create_popia_template(),
        "coppa": create_coppa_template(),
        "glba": create_glba_template(),
        "eprivacy": create_eprivacy_template(),
        "nis2": create_nis2_template(),
        "ai_act_ca": create_ai_act_ca_template(),
        "ai_gov_sg": create_ai_gov_sg_template(),
        "ai_ethics_jp": create_ai_ethics_jp_template(),
        "oecd_ai": create_oecd_ai_template(),
        "unesco_ai": create_unesco_ai_template(),
        "g7_ai": create_g7_ai_template(),
        "basel": create_basel_template(),
        "mifid": create_mifid_template(),
        "dodd_frank": create_dodd_frank_template(),
        "fda_ai": create_fda_ai_template(),
        "mdr": create_mdr_template(),
        "unece": create_unece_template(),
        "iso_21434": create_iso_21434_template(),
        "nist": create_nist_template(),
        "soc2": create_soc2_template(),
        "pci_dss": create_pci_dss_template(),
        "ai_liability": create_ai_liability_template(),
        "data_act": create_data_act_template(),
        "dsa": create_dsa_template(),
        "dma": create_dma_template()
    }
    
    return templates

def save_templates_to_files(templates: Dict[str, Dict[str, Any]], output_dir: str):
    """Save policy templates to JSON files organized by category."""
    
    # Create category subdirectories
    categories = {
        "Data Protection & Privacy Laws": ["gdpr", "ccpa", "lgpd", "pipeda", "pdpa_sg", "pipl", "appi", "pdpa_th", "popia", "coppa", "glba", "eprivacy", "nis2"],
        "Industry-Specific Regulations": ["hipaa", "sox", "basel", "mifid", "dodd_frank", "fda_ai", "mdr", "unece", "iso_21434"],
        "AI-Specific Regulations": ["eu_ai_act", "ai_act_ca", "ai_gov_sg", "ai_ethics_jp", "oecd_ai", "unesco_ai", "g7_ai"],
        "Cybersecurity & Infrastructure": ["iso_27001", "nist", "soc2", "pci_dss"],
        "Emerging/Proposed Regulations": ["ai_liability", "data_act", "dsa", "dma"]
    }
    
    for category, policy_names in categories.items():
        category_dir = os.path.join(output_dir, category.replace(" ", "_").replace("&", "and"))
        os.makedirs(category_dir, exist_ok=True)
        
        for policy_name in policy_names:
            if policy_name in templates:
                filename = f"{policy_name}_template.json"
                filepath = os.path.join(category_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(templates[policy_name], f, indent=2, ensure_ascii=False)
                
                print(f"Created: {filepath}")
    
    # Also save a master index file
    master_index = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "total_policies": len(templates),
            "categories": list(categories.keys())
        },
        "policies": {
            name: {
                "category": template["metadata"]["category"],
                "version": template["metadata"]["version"],
                "filename": f"{template['metadata']['category'].replace(' ', '_').replace('&', 'and')}/{name}_template.json"
            }
            for name, template in templates.items()
        }
    }
    
    index_path = os.path.join(output_dir, "policy_index.json")
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(master_index, f, indent=2, ensure_ascii=False)
    
    print(f"\nCreated master index: {index_path}")

def main():
    """Main function to generate all policy templates."""
    
    print("🚀 Generating Policy Templates...")
    print("=" * 50)
    
    # Create output directory
    output_dir = "policy_templates"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate templates
    templates = create_policy_templates()
    
    # Save to files
    save_templates_to_files(templates, output_dir)
    
    print("\n✅ Policy template generation complete!")
    print(f"📁 Templates saved to: {output_dir}/")
    print("\n📋 Next steps:")
    print("1. Review the generated templates")
    print("2. Update compliance.py to use these templates")
    print("3. Test validation logic with sample LLM outputs")
    print("4. Add more policies as needed")

if __name__ == "__main__":
    main()
