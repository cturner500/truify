"""
genai.py - Generative AI utilities for dataset analysis

This module provides functions that leverage local generative AI models to analyze and describe datasets.
"""

import pandas as pd
import warnings
import hashlib
import random


def describe_dataset_with_genai(df: pd.DataFrame, model_name: str = "mistral-7b-instruct-v0.2.Q4_0.gguf") -> str:
    """
    Use a local generative AI model to describe the dataset, guess its source, assess usefulness, and discuss appropriateness for AI/ML training.
    Requires the gpt4all Python package and a compatible local model.
    """
    try:
        from gpt4all import GPT4All
        # Prepare a prompt
        prompt = (
            f"Given the following dataset columns: {list(df.columns)}\n"
            f"and a sample of the data:\n{df.head(3).to_csv(index=False)}\n"
            "Describe what this dataset is about, guess where it might have come from, "
            "assess its usefulness and intended uses, and discuss its appropriateness for AI/ML training, "
            "including any limitations (such as low sample size, bias, or missingness)."
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                # Try to load the model - this will download it if not present
                model = GPT4All(model_name, allow_download=True)
            except Exception as model_error:
                # If the specific model fails, try a fallback model
                fallback_model = "mistral-7b-openorca.Q4_0.gguf"
                try:
                    model = GPT4All(fallback_model, allow_download=True)
                except Exception as fallback_error:
                    return f"Could not load AI model. Please ensure you have internet connection for model download. Error: {fallback_error}"
        with model.chat_session():
            response = model.generate(prompt, max_tokens=256, temp=0.7)
        return response
    except ImportError:
        # gpt4all is not installed, provide a helpful fallback
        return f"""**Dataset Description (AI Model Not Available)**

**Dataset Overview:**
This dataset contains {len(df.columns)} columns and {len(df)} rows of data.

**Column Analysis:**
"""
        + "\n".join([f"- **{col}**: {df[col].dtype} data type" for col in df.columns]) + f"""

**Data Summary:**
- Numeric columns: {len(df.select_dtypes(include=['number']).columns)} columns
- Categorical columns: {len(df.select_dtypes(include=['object']).columns)} columns
- Missing values: {df.isnull().sum().sum()} total missing values

**Recommendations:**
- Consider the data types and potential uses for each column
- Check for missing values and data quality issues
- Evaluate whether this dataset is suitable for your intended analysis

*Note: AI-powered analysis is not available because the required AI model is not installed. This is a basic statistical overview of your dataset.*"""
    except Exception as e:
        return f"Could not generate dataset description: {e}"

def analyze_bias_with_genai(df: pd.DataFrame, model_name: str = "mistral-7b-instruct-v0.2.Q4_0.gguf") -> str:
    """
    Use a local generative AI model to analyze the dataset and describe potential sources of bias in detail.
    The description should reference known sources of bias (e.g., selection, recency, geographical, gender, channel/market, etc.) and suggest where bias may exist, even if not certain.
    Requires the gpt4all Python package and a compatible local model.
    """
    try:
        from gpt4all import GPT4All
        prompt = (
            f"Given the following dataset columns: {list(df.columns)}\n"
            f"and a sample of the data:\n{df.head(3).to_csv(index=False)}\n"
            "Analyze this dataset for potential sources of bias. Consider known sources of bias such as selection bias, recency bias, geographical bias, gender bias, channel/market bias, and others. "
            "Describe in detail where bias may exist in the data, even if you are not certain. Suggest what types of bias are most likely and why, based on the columns and sample data."
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                # Try to load the model - this will download it if not present
                model = GPT4All(model_name, allow_download=True)
            except Exception as model_error:
                # If the specific model fails, try a fallback model
                fallback_model = "mistral-7b-openorca.Q4_0.gguf"
                try:
                    model = GPT4All(fallback_model, allow_download=True)
                except Exception as fallback_error:
                    return f"Could not load AI model. Please ensure you have internet connection for model download. Error: {fallback_error}"
        with model.chat_session():
            response = model.generate(prompt, max_tokens=256, temp=0.7)
        return response
    except Exception as e:
        return f"Could not generate bias analysis: {e}"

def simple_pii_assessment(df: pd.DataFrame) -> dict:
    """
    Simple PII assessment using pattern matching when AI models are not available.
    """
    pii_patterns = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
    }
    
    pii_keywords = [
        'name', 'email', 'phone', 'address', 'ssn', 'social', 'credit', 'card',
        'id', 'identifier', 'user', 'customer', 'client', 'patient', 'employee',
        'first', 'last', 'middle', 'given', 'family', 'surname', 'forename',
        'mobile', 'cell', 'fax', 'zip', 'postal', 'city', 'state', 'country',
        'birth', 'dob', 'date_of_birth', 'age', 'gender', 'sex', 'race',
        'ethnicity', 'nationality', 'passport', 'license', 'account'
    ]
    
    recommended_columns = []
    assessment = {}
    
    for column in df.columns:
        column_lower = column.lower()
        is_pii = False
        risk_level = "low"
        reason = ""
        pii_type = "unknown"
        
        # Check column name for PII keywords
        for keyword in pii_keywords:
            if keyword in column_lower:
                is_pii = True
                risk_level = "high"
                reason = f"Column name contains PII keyword: '{keyword}'"
                pii_type = "direct-identifier"
                break
        
        # Check data content for patterns
        if not is_pii and df[column].dtype == 'object':
            sample_data = df[column].dropna().astype(str).head(10)
            
            # Check for email patterns
            if sample_data.str.contains(pii_patterns['email'], regex=True).any():
                is_pii = True
                risk_level = "high"
                reason = "Contains email addresses"
                pii_type = "direct-identifier"
            
            # Check for phone patterns
            elif sample_data.str.contains(pii_patterns['phone'], regex=True).any():
                is_pii = True
                risk_level = "high"
                reason = "Contains phone numbers"
                pii_type = "direct-identifier"
            
            # Check for SSN patterns
            elif sample_data.str.contains(pii_patterns['ssn'], regex=True).any():
                is_pii = True
                risk_level = "high"
                reason = "Contains Social Security Numbers"
                pii_type = "direct-identifier"
        
        # Check for ID-like columns
        elif not is_pii and ('id' in column_lower or 'identifier' in column_lower):
            if df[column].nunique() == len(df):
                is_pii = True
                risk_level = "medium"
                reason = "Unique identifier column"
                pii_type = "direct-identifier"
        
        if is_pii:
            recommended_columns.append(column)
            assessment[column] = {
                "risk_level": risk_level,
                "reason": reason,
                "pii_type": pii_type
            }
    
    return {
        "recommended_columns": recommended_columns,
        "assessment": assessment,
        "method": "pattern_matching"
    }

def PII_assessment(df: pd.DataFrame, model_name: str = "mistral-7b-instruct-v0.2.Q4_0.gguf") -> dict:
    """
    PII Agent - Expert on data privacy assessment.
    Takes a sample of the data and identifies which columns might contain PII information.
    Returns a dictionary with recommended columns for obfuscation and detailed commentary.
    """
    try:
        from gpt4all import GPT4All
        
        # Prepare a comprehensive prompt for PII analysis
        prompt = (
            f"You are a data privacy expert. Analyze this dataset for Personally Identifiable Information (PII):\n\n"
            f"Dataset columns: {list(df.columns)}\n"
            f"Sample data (first 5 rows):\n{df.head(5).to_csv(index=False)}\n\n"
            f"Data types: {df.dtypes.to_dict()}\n\n"
            f"Your task:\n"
            f"1. Identify columns that contain PII (names, emails, phone numbers, addresses, IDs, etc.)\n"
            f"2. For each identified column, explain why it's a privacy risk\n"
            f"3. Consider both direct identifiers (names, emails) and quasi-identifiers (age, zip code, etc.)\n"
            f"4. Assess the risk level (high, medium, low) for each column\n\n"
            f"IMPORTANT: Respond ONLY with valid JSON in this exact format. Do not include any other text:\n"
            f"{{\n"
            f"  \"recommended_columns\": [\"column1\", \"column2\"],\n"
            f"  \"assessment\": {{\n"
            f"    \"column1\": {{\n"
            f"      \"risk_level\": \"high\",\n"
            f"      \"reason\": \"detailed explanation of privacy risk\",\n"
            f"      \"pii_type\": \"direct-identifier\"\n"
            f"    }},\n"
            f"    \"column2\": {{\n"
            f"      \"risk_level\": \"medium\",\n"
            f"      \"reason\": \"detailed explanation of privacy risk\",\n"
            f"      \"pii_type\": \"quasi-identifier\"\n"
            f"    }}\n"
            f"  }}\n"
            f"}}\n\n"
            f"Only include columns that actually contain PII. If no PII is found, return: {{\"recommended_columns\": [], \"assessment\": {{}}}}"
        )
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                # Try to load the model - this will download it if not present
                model = GPT4All(model_name, allow_download=True)
            except Exception as model_error:
                # If the specific model fails, try a fallback model
                fallback_model = "mistral-7b-openorca.Q4_0.gguf"
                try:
                    model = GPT4All(fallback_model, allow_download=True)
                except Exception as fallback_error:
                    # If both models fail, use simple pattern matching
                    return simple_pii_assessment(df)
        
        with model.chat_session():
            response = model.generate(prompt, max_tokens=1024, temp=0.3)
        
        # Try to parse JSON response
        import json
        import re
        try:
            # Clean the response to extract JSON
            response_text = response.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            elif response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            
            result = json.loads(response_text)
            
            # Validate the result structure
            if not isinstance(result, dict):
                raise ValueError("Response is not a dictionary")
            
            # Ensure required keys exist
            if 'recommended_columns' not in result:
                result['recommended_columns'] = []
            if 'assessment' not in result:
                result['assessment'] = {}
            
            return result
            
        except (json.JSONDecodeError, ValueError) as json_error:
            # If JSON parsing fails, try to extract information from the raw response
            try:
                # Fallback: try to extract column names from the response
                lines = response.split('\n')
                recommended_columns = []
                assessment = {}
                
                for line in lines:
                    line = line.strip()
                    # Look for column names in the response
                    if any(keyword in line.lower() for keyword in ['column', 'field', 'recommend']):
                        # Extract potential column names
                        for col in df.columns:
                            if col.lower() in line.lower():
                                recommended_columns.append(col)
                                assessment[col] = {
                                    "risk_level": "medium",
                                    "reason": f"AI identified potential PII in column: {col}",
                                    "pii_type": "unknown"
                                }
                
                # Remove duplicates
                recommended_columns = list(set(recommended_columns))
                
                return {
                    "recommended_columns": recommended_columns,
                    "assessment": assessment,
                    "raw_response": response,
                    "parsing_error": str(json_error),
                    "method": "ai_with_fallback_parsing"
                }
                
            except Exception as fallback_error:
                # Final fallback: use simple pattern matching
                return simple_pii_assessment(df)
            
    except Exception as e:
        return {
            "recommended_columns": [],
            "assessment": {},
            "error": f"Could not perform PII assessment: {e}"
        }

def PII_anonymize(df: pd.DataFrame, columns_to_anonymize: list) -> pd.DataFrame:
    """
    PII Agent - Anonymization function.
    Takes a dataframe and a list of columns, then obfuscates those columns using a random hash algorithm.
    Returns the anonymized dataframe.
    """
    try:
        # Create a copy of the dataframe to avoid modifying the original
        anonymized_df = df.copy()
        
        # Generate a random salt for consistent hashing within the session
        salt = str(random.randint(10000, 99999))
        
        for column in columns_to_anonymize:
            if column in anonymized_df.columns:
                # Create a hash function that combines the salt with the column name
                def hash_value(value):
                    if pd.isna(value):
                        return f"HASHED_NULL_{column}_{salt}"
                    # Convert to string and hash
                    value_str = str(value)
                    # Create a hash that includes the column name for uniqueness
                    hash_input = f"{column}_{value_str}_{salt}"
                    return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
                
                # Apply the hash function to the column
                anonymized_df[column] = anonymized_df[column].apply(hash_value)
        
        return anonymized_df
        
    except Exception as e:
        # Return original dataframe if anonymization fails
        return df 