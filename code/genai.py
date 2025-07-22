"""
genai.py - Generative AI utilities for dataset analysis

This module provides functions that leverage local generative AI models to analyze and describe datasets.
"""

import pandas as pd

def describe_dataset_with_genai(df: pd.DataFrame, model_name: str = "mistral-7b-openorca.Q4_0.gguf") -> str:
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
        model = GPT4All(model_name)
        with model.chat_session():
            response = model.generate(prompt, max_tokens=256, temp=0.7)
        return response
    except Exception as e:
        return f"Could not generate dataset description: {e}"

def analyze_bias_with_genai(df: pd.DataFrame, model_name: str = "mistral-7b-openorca.Q4_0.gguf") -> str:
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
        model = GPT4All(model_name)
        with model.chat_session():
            response = model.generate(prompt, max_tokens=256, temp=0.7)
        return response
    except Exception as e:
        return f"Could not generate bias analysis: {e}" 