"""
PII.py - Personally Identifiable Information Analysis and Anonymization

This module provides PII risk assessment and data anonymization capabilities using generative AI.
"""

import streamlit as st
import pandas as pd
from genai import PII_assessment, PII_anonymize, simple_pii_assessment

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
    
    # Button 1: Analyze Data for PII Risk
    st.subheader("🔍 PII Risk Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Analyze data for PII risk using genAI"):
            with st.spinner("Analyzing data for PII risks..."):
                # Run PII assessment
                assessment_result = PII_assessment(df)
                st.session_state.pii_assessment = assessment_result
                
                # If AI assessment didn't find PII, try pattern-based assessment as fallback
                if not assessment_result.get('pii_columns') or len(assessment_result.get('pii_columns', [])) == 0:
                    st.info("AI assessment didn't identify PII. Running pattern-based detection as backup...")
                    pattern_assessment = simple_pii_assessment(df)
                    
                    # If pattern-based assessment found PII, use that instead
                    if pattern_assessment.get('pii_columns') and len(pattern_assessment.get('pii_columns', [])) > 0:
                        st.success("Pattern-based detection found PII that AI missed!")
                        st.session_state.pii_assessment = pattern_assessment
                        assessment_result = pattern_assessment
                    else:
                        st.warning("Neither AI nor pattern-based detection found PII. This may indicate the data is truly non-identifying.")
    
    with col2:
        if st.button("Run Pattern-Based PII Detection"):
            with st.spinner("Running pattern-based PII detection..."):
                pattern_assessment = simple_pii_assessment(df)
                st.session_state.pii_assessment = pattern_assessment
                st.success("Pattern-based PII detection completed!")
                st.info("This method uses rule-based detection for emails, phone numbers, names, and other common PII patterns.")
    
    # Display PII assessment results
    if st.session_state.pii_assessment:
        assessment = st.session_state.pii_assessment
        
        # Extract PII columns from the assessment
        pii_columns = assessment.get('pii_columns', [])
        risk_level = assessment.get('risk_level', 'unknown')
        
        # If no PII columns found in structured response, try to extract from raw text
        if not pii_columns and 'detailed_analysis' in assessment:
            detailed_analysis = assessment['detailed_analysis']
            
            # Try to extract column names from the detailed analysis text
            import re
            
            # Look for column names mentioned in the response
            column_patterns = [
                r'column[s]?\s*["\']([^"\']+)["\']',  # "column_name"
                r'column[s]?\s+([a-zA-Z_][a-zA-Z0-9_]*)',  # column_name
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s+contains?\s+PII',  # column_name contains PII
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s+is\s+a\s+PII',  # column_name is a PII
            ]
            
            extracted_columns = []
            for pattern in column_patterns:
                matches = re.findall(pattern, detailed_analysis, re.IGNORECASE)
                extracted_columns.extend(matches)
            
            # Also check if any actual column names from the dataset are mentioned
            dataset_columns = list(df.columns)
            for col in dataset_columns:
                if col.lower() in detailed_analysis.lower():
                    extracted_columns.append(col)
            
            # Remove duplicates and update the assessment
            if extracted_columns:
                pii_columns = list(set(extracted_columns))
                assessment['pii_columns'] = pii_columns
                st.success(f"✅ Extracted {len(pii_columns)} PII columns from AI response!")
        
        # Display the results
        st.subheader("🔍 PII Risk Assessment Results")
        
        if pii_columns:
            st.success(f"✅ **{len(pii_columns)} PII columns identified**")
            st.write(f"**Risk Level:** {risk_level.upper()}")
            
            # Display identified PII columns
            st.write("**Identified PII Columns:**")
            for col in pii_columns:
                st.write(f"• {col}")
            
            # Display recommendations if available
            if 'recommendations' in assessment and assessment['recommendations']:
                st.write("**Recommendations:**")
                for rec in assessment['recommendations']:
                    st.write(f"• {rec}")
            
            # Display detailed analysis if available
            if 'detailed_analysis' in assessment and assessment['detailed_analysis']:
                st.write("**Detailed Analysis:**")
                st.info(assessment['detailed_analysis'])
            
            # Display compliance notes if available
            if 'compliance_notes' in assessment and assessment['compliance_notes']:
                st.write("**Compliance Notes:**")
                st.warning(assessment['compliance_notes'])
            
            # Initialize selected columns with identified PII columns
            if not st.session_state.selected_columns:
                st.session_state.selected_columns = pii_columns.copy()
        else:
            st.info("No PII risks identified in the data.")
        
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
    
    if st.button("Anonymize Data"):
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
    
    if st.button("Keep Results and Update Data"):
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
