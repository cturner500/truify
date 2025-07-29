"""
PII.py - Personally Identifiable Information Analysis and Anonymization

This module provides PII risk assessment and data anonymization capabilities using generative AI.
"""

import streamlit as st
import pandas as pd
from genai import PII_assessment, PII_anonymize

def pii_page():
    """
    Main PII analysis and anonymization page.
    """
    st.header("🔒 PII Analysis & Anonymization")
    st.write("Analyze your data for Personally Identifiable Information (PII) and anonymize sensitive columns.")
    
    # Check if data is loaded
    if 'df' not in st.session_state or st.session_state['df'] is None:
        st.warning("Please load a dataset first using the Data Upload page.")
        return
    
    df = st.session_state['df']
    
    # Display current data (20 rows)
    st.subheader("📊 Current Data (First 20 Rows)")
    st.dataframe(df.head(20), use_container_width=True)
    
    # Initialize session state for PII analysis results
    if 'pii_assessment' not in st.session_state:
        st.session_state.pii_assessment = None
    if 'selected_columns' not in st.session_state:
        st.session_state.selected_columns = []
    if 'anonymized_df' not in st.session_state:
        st.session_state.anonymized_df = None
    
    # Button 1: Analyze data for PII risk using genAI
    st.subheader("🤖 AI-Powered PII Risk Assessment")
    
    if st.button("Analyze data for PII risk using genAI", type="primary"):
        with st.spinner("Analyzing data for PII risks..."):
            # Call the PII assessment function
            assessment_result = PII_assessment(df)
            st.session_state.pii_assessment = assessment_result
            
            if 'error' in assessment_result and assessment_result['error']:
                st.error(f"Assessment failed: {assessment_result['error']}")
                if 'raw_response' in assessment_result:
                    st.text_area("Raw AI Response:", assessment_result['raw_response'], height=200)
            else:
                # Check which method was used
                method = assessment_result.get('method', 'ai')
                
                if method == 'pattern_matching':
                    st.success("PII assessment completed using pattern matching (AI model not available)")
                    st.info("Using pattern-based PII detection. For more advanced analysis, ensure AI models are available.")
                elif method == 'ai_with_fallback_parsing':
                    st.success("PII assessment completed using AI with fallback parsing")
                    st.warning("AI response format was unclear, but PII columns were identified from the response.")
                    if 'parsing_error' in assessment_result:
                        st.info(f"Parsing note: {assessment_result['parsing_error']}")
                else:
                    st.success("PII assessment completed using AI!")
    
    # Display PII assessment results
    if st.session_state.pii_assessment:
        st.subheader("📋 PII Risk Assessment Results")
        
        assessment = st.session_state.pii_assessment
        
        # Display recommended columns
        if 'recommended_columns' in assessment and assessment['recommended_columns']:
            st.write("**Recommended columns for anonymization:**")
            for col in assessment['recommended_columns']:
                st.write(f"- {col}")
            
            # Initialize selected columns with recommended ones
            if not st.session_state.selected_columns:
                st.session_state.selected_columns = assessment['recommended_columns'].copy()
        else:
            st.info("No PII risks identified in the data.")
        
        # Display detailed assessment
        if 'assessment' in assessment and assessment['assessment']:
            st.write("**Detailed Assessment:**")
            for column, details in assessment['assessment'].items():
                with st.expander(f"📝 {column}"):
                    if isinstance(details, dict):
                        risk_level = details.get('risk_level', 'Unknown')
                        reason = details.get('reason', 'No reason provided')
                        pii_type = details.get('pii_type', 'Unknown')
                        
                        st.write(f"**Risk Level:** {risk_level}")
                        st.write(f"**PII Type:** {pii_type}")
                        st.write(f"**Reason:** {reason}")
                    else:
                        st.write(f"Assessment: {details}")
        
        # Column selection interface
        st.subheader("⚙️ Select Columns to Anonymize")
        
        # Get all available columns
        all_columns = list(df.columns)
        
        # Multi-select for columns to anonymize
        selected_columns = st.multiselect(
            "Choose columns to anonymize:",
            options=all_columns,
            default=st.session_state.selected_columns,
            help="Select columns that contain sensitive information you want to anonymize."
        )
        
        st.session_state.selected_columns = selected_columns
        
        if selected_columns:
            st.write(f"**Selected columns:** {', '.join(selected_columns)}")
        else:
            st.warning("Please select at least one column to anonymize.")
    
    # Button 2: Anonymize Data
    st.subheader("🔐 Data Anonymization")
    
    if st.button("Anonymize Data", type="secondary"):
        if not st.session_state.selected_columns:
            st.error("Please select columns to anonymize first.")
        else:
            with st.spinner("Anonymizing selected columns..."):
                # Call the anonymization function
                anonymized_df = PII_anonymize(df, st.session_state.selected_columns)
                st.session_state.anonymized_df = anonymized_df
                
                st.success("Data anonymization completed!")
                
                # Display anonymized data (20 rows)
                st.subheader("🔒 Anonymized Data (First 20 Rows)")
                st.dataframe(anonymized_df.head(20), use_container_width=True)
                
                # Show comparison
                st.subheader("📊 Comparison: Original vs Anonymized")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Original Data (Sample):**")
                    sample_original = df[st.session_state.selected_columns].head(5)
                    st.dataframe(sample_original, use_container_width=True)
                
                with col2:
                    st.write("**Anonymized Data (Sample):**")
                    sample_anonymized = anonymized_df[st.session_state.selected_columns].head(5)
                    st.dataframe(sample_anonymized, use_container_width=True)
    
    # Button 3: Keep Results and Update Data
    st.subheader("💾 Save Anonymized Data")
    
    if st.button("Keep Results and Update Data", type="primary"):
        if st.session_state.anonymized_df is not None:
            # Update the session state with anonymized data
            st.session_state['df'] = st.session_state.anonymized_df.copy()
            
            # Clear temporary data
            st.session_state.anonymized_df = None
            st.session_state.pii_assessment = None
            st.session_state.selected_columns = []
            
            st.success("✅ Anonymized data has been saved and will replace the original dataset!")
            st.info("The original data has been replaced with the anonymized version. You can now proceed with other analyses using the anonymized data.")
            
            # Rerun to show updated data
            st.rerun()
        else:
            st.error("Please anonymize the data first before saving.")

if __name__ == "__main__":
    pii_page()
