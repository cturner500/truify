"""
genai_openrouter.py - Generative AI utilities using OpenRouter.ai

This module provides functions that leverage Mistral via OpenRouter.ai to analyze and describe datasets.
"""

import pandas as pd
import requests
import json
import os
from typing import Optional, Dict, Any, Tuple
import time


def get_openrouter_api_key() -> Optional[str]:
    """Get OpenRouter API key from environment variable."""
    return os.getenv('OPENROUTER_API_KEY')


def get_openrouter_model() -> str:
    """Get OpenRouter model from environment variable with fallback to free Mistral."""
    return os.getenv('OPENROUTER_MODEL', 'mistralai/mistral-7b-instruct:free')


def call_openrouter_api(prompt: str, model: str = None) -> Tuple[str, str]:
    """
    Call OpenRouter API with the given prompt and model.
    
    Args:
        prompt: The prompt to send to the model
        model: The model to use (defaults to environment variable or free Mistral)
    
    Returns:
        Tuple of (response_text, model_used)
    """
    if model is None:
        model = get_openrouter_model()
    
    api_key = get_openrouter_api_key()
    if not api_key:
        return "Error: OPENROUTER_API_KEY environment variable not set", model
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://truify.ai",
        "X-Title": "Truify Data Analysis"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            response_text = result['choices'][0]['message']['content']
            return response_text, model
        else:
            return "Error: Unexpected response format from OpenRouter API", model
            
    except requests.exceptions.RequestException as e:
        return f"Error calling OpenRouter API: {str(e)}", model
    except json.JSONDecodeError as e:
        return f"Error parsing API response: {str(e)}", model
    except Exception as e:
        return f"Unexpected error: {str(e)}", model


def describe_dataset_with_genai(df: pd.DataFrame) -> str:
    """
    Use Mistral via OpenRouter to describe the dataset, guess its source, assess usefulness, and discuss appropriateness for AI/ML training.
    """
    try:
        # Prepare a comprehensive prompt
        prompt = f"""You are a data scientist analyzing a dataset. Please provide a detailed analysis of the following dataset:

Dataset Information:
- Number of columns: {len(df.columns)}
- Number of rows: {len(df)}
- Column names: {list(df.columns)}

Sample Data (first 3 rows):
{df.head(3).to_csv(index=False)}

Data Types:
{df.dtypes.to_string()}

Missing Values Summary:
{df.isnull().sum().to_string()}

Please provide a comprehensive analysis including:
1. What this dataset appears to be about
2. Where it might have come from (industry, domain, etc.)
3. Its potential usefulness and intended applications
4. Assessment of its appropriateness for AI/ML training
5. Any limitations or concerns (sample size, bias, data quality, etc.)
6. Recommendations for data preprocessing or analysis

Format your response in clear sections with markdown formatting."""

        response_text, model_used = call_openrouter_api(prompt)
        
        # Add debug information about the model used
        debug_info = f"\n\n---\n*Debug: Analysis performed using OpenRouter model: `{model_used}`*"
        
        return response_text + debug_info
        
    except Exception as e:
        return f"""**Dataset Description (API Error)**

**Dataset Overview:**
This dataset contains {len(df.columns)} columns and {len(df)} rows of data.

**Column Analysis:**
"""
        + "\n".join([f"- **{col}**: {df[col].dtype} data type" for col in df.columns]) + f"""

**Data Summary:**
- Numeric columns: {len(df.select_dtypes(include=['number']).columns)} columns
- Categorical columns: {len(df.select_dtypes(include=['object']).columns)} columns
- Missing values: {df.isnull().sum().sum()} total missing values

**Error Details:**
Could not complete AI analysis due to: {str(e)}

*Note: This is a basic statistical overview of your dataset.*"""


def analyze_bias_with_genai(df: pd.DataFrame) -> str:
    """
    Use Mistral via OpenRouter to analyze the dataset and describe potential sources of bias in detail.
    """
    try:
        prompt = f"""You are a data ethics expert analyzing potential bias in a dataset. Please provide a detailed bias analysis of the following dataset:

Dataset Information:
- Number of columns: {len(df.columns)}
- Number of rows: {len(df)}
- Column names: {list(df.columns)}

Sample Data (first 3 rows):
{df.head(3).to_csv(index=False)}

Data Types:
{df.dtypes.to_string()}

Please analyze this dataset for potential sources of bias, including but not limited to:
1. Selection bias (how the data was collected)
2. Sampling bias (who is included/excluded)
3. Temporal bias (when the data was collected)
4. Geographic bias (where the data comes from)
5. Demographic bias (age, gender, ethnicity, etc.)
6. Measurement bias (how variables were measured)
7. Reporting bias (what gets reported vs. what doesn't)

For each potential bias source you identify:
- Explain why it might be present
- Discuss the potential impact on analysis results
- Suggest ways to mitigate or account for the bias

Format your response in clear sections with markdown formatting."""

        response_text, model_used = call_openrouter_api(prompt)
        
        # Add debug information about the model used
        debug_info = f"\n\n---\n*Debug: Bias analysis performed using OpenRouter model: `{model_used}`*"
        
        return response_text + debug_info
        
    except Exception as e:
        return f"""**Bias Analysis (API Error)**

**Dataset Overview:**
This dataset contains {len(df.columns)} columns and {len(df)} rows of data.

**Basic Bias Assessment:**
- Sample size: {len(df)} rows (consider if this is representative)
- Missing values: {df.isnull().sum().sum()} total missing values
- Data types: {len(df.select_dtypes(include=['number']).columns)} numeric, {len(df.select_dtypes(include=['object']).columns)} categorical

**Error Details:**
Could not complete bias analysis due to: {str(e)}

*Note: This is a basic assessment. For comprehensive bias analysis, ensure API access is available.*"""


def PII_assessment(df: pd.DataFrame) -> dict:
    """
    Use Mistral via OpenRouter to assess the dataset for Personally Identifiable Information (PII).
    """
    try:
        prompt = f"""You are a data privacy expert analyzing a dataset for Personally Identifiable Information (PII). Please assess the following dataset:

Dataset Information:
- Number of columns: {len(df.columns)}
- Number of rows: {len(df)}
- Column names: {list(df.columns)}

Sample Data (first 3 rows):
{df.head(3).to_csv(index=False)}

Data Types:
{df.dtypes.to_string()}

Please analyze this dataset for PII and provide your assessment in the following JSON format:
{{
    "pii_columns": ["list", "of", "column", "names", "that", "contain", "PII"],
    "risk_level": "high|medium|low",
    "recommendations": ["list", "of", "recommendations", "for", "data", "protection"],
    "detailed_analysis": "detailed explanation of PII findings",
    "compliance_notes": "notes about data protection regulations"
}}

Focus on identifying:
1. Direct identifiers (names, SSNs, email addresses, phone numbers)
2. Quasi-identifiers (combinations that could identify individuals)
3. Sensitive information (medical, financial, location data)
4. Risk assessment and compliance considerations

Return only valid JSON without any additional text."""

        response_text, model_used = call_openrouter_api(prompt)
        
        # Try to parse JSON response
        try:
            # Find JSON in the response (in case there's extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                # Add debug info to the result
                result["debug_model_used"] = model_used
                return result
            else:
                # If no JSON found, return structured response
                return {
                    "pii_columns": [],
                    "risk_level": "unknown",
                    "recommendations": ["Could not parse API response"],
                    "detailed_analysis": response_text,
                    "compliance_notes": "API response parsing failed",
                    "debug_model_used": model_used
                }
        except json.JSONDecodeError:
            return {
                "pii_columns": [],
                "risk_level": "unknown", 
                "recommendations": ["Could not parse API response as JSON"],
                "detailed_analysis": response_text,
                "compliance_notes": "API response was not valid JSON",
                "debug_model_used": model_used
            }
            
    except Exception as e:
        return {
            "pii_columns": [],
            "risk_level": "unknown",
            "recommendations": [f"Error during PII assessment: {str(e)}"],
            "detailed_analysis": f"Could not complete PII assessment due to error: {str(e)}",
            "compliance_notes": "Assessment failed due to technical error",
            "debug_model_used": "unknown"
        }


def PII_anonymize(df: pd.DataFrame, columns_to_anonymize: list) -> pd.DataFrame:
    """
    Anonymize specified columns in the dataframe using hashing.
    """
    import hashlib
    
    df_anonymized = df.copy()
    
    for column in columns_to_anonymize:
        if column in df_anonymized.columns:
            # Hash the values in the column
            df_anonymized[column] = df_anonymized[column].astype(str).apply(
                lambda x: hashlib.sha256(x.encode()).hexdigest()[:16] if pd.notna(x) else x
            )
    
    return df_anonymized


def simple_pii_assessment(df: pd.DataFrame) -> dict:
    """
    Simple PII assessment without AI - uses pattern matching and common PII indicators.
    """
    pii_columns = []
    risk_level = "low"
    
    # Common PII patterns
    pii_patterns = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^\+?1?\d{9,15}$',
        'ssn': r'^\d{3}-\d{2}-\d{4}$',
        'credit_card': r'^\d{4}-\d{4}-\d{4}-\d{4}$'
    }
    
    import re
    
    for column in df.columns:
        column_lower = column.lower()
        
        # Check column name for PII indicators
        pii_keywords = ['name', 'email', 'phone', 'address', 'ssn', 'id', 'social', 'credit', 'card', 'account']
        if any(keyword in column_lower for keyword in pii_keywords):
            pii_columns.append(column)
            risk_level = "medium" if risk_level == "low" else risk_level
        
        # Check data patterns
        if df[column].dtype == 'object':
            sample_values = df[column].dropna().head(10)
            for value in sample_values:
                if isinstance(value, str):
                    for pattern_name, pattern in pii_patterns.items():
                        if re.match(pattern, value):
                            if column not in pii_columns:
                                pii_columns.append(column)
                            risk_level = "high"
                            break
    
    return {
        "pii_columns": pii_columns,
        "risk_level": risk_level,
        "recommendations": [
            "Consider anonymizing identified PII columns",
            "Review data retention policies",
            "Ensure compliance with data protection regulations"
        ],
        "detailed_analysis": f"Found {len(pii_columns)} potential PII columns",
        "compliance_notes": "Basic pattern matching assessment completed",
        "debug_model_used": "pattern_matching_only"
    }
