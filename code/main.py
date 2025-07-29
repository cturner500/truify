import streamlit as st
import pandas as pd
import hashlib
import random
import numpy as np
from sklearn.impute import SimpleImputer
from PII import pii_page
from auth import is_authenticated, login_page, handle_oauth_callback, display_user_info, check_token_expiry
from synthesizer import synthesize_page

# Function to hash data
def hash_data(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Function to identify personal information columns
def identify_personal_info_columns(df):
    personal_info_columns = []
    for column in df.columns:
        if df[column].dtype == object:
            if any(df[column].str.contains(r'\b(?:name|address|phone|email)\b', case=False, na=False)):
                personal_info_columns.append(column)
    return personal_info_columns

# Function to deidentify data
def deidentify_data(df, personal_info_columns):
    for column in personal_info_columns:
        df[column] = df[column].apply(lambda x: hash_data(str(x)) if pd.notnull(x) else x)
    return df
    
# Function to reduce bias based on selected ground truth data
def reduce_bias(df, ground_truth_data):
    # Example placeholder function for reducing bias
    # Implement actual bias reduction logic here
    weights = []
    for index, row in df.iterrows():
        weight = random.uniform(0.5, 1.5)  # Placeholder for actual weight calculation
        weights.append(weight)
    df['Weights'] = weights
    return df

# Function to fill missing values
def fill_missing_values(df, method):
    if method == "na.roughfix":
        # Placeholder for actual na.roughfix() implementation
        imputer = SimpleImputer(strategy="mean")
    elif method == "mean":
        imputer = SimpleImputer(strategy="mean")
    elif method == "mode":
        imputer = SimpleImputer(strategy="most_frequent")
    elif method == "median":
        imputer = SimpleImputer(strategy="median")
    elif method == "LOCF":
        df = df.ffill()
        return df
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    return df

# Streamlit app
st.set_page_config(page_title='TRUIFY', layout="wide", initial_sidebar_state="expanded")

# Add custom CSS for sidebar styling
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #69b9e8;
    min-width: 300px !important;
    width: 20% !important;
}
[data-testid="stSidebar"] .css-1d391kg {
    background-color: #69b9e8;
}
.main .block-container {
    max-width: 80%;
    padding-left: 2rem;
    padding-right: 2rem;
}
/* Consistent button spacing */
[data-testid="stSidebar"] button {
    margin-bottom: 0.2rem !important;
    margin-top: 0.2rem !important;
}
/* Consistent column spacing */
[data-testid="stSidebar"] .row-widget {
    margin-bottom: 0.2rem !important;
    margin-top: 0.2rem !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.image("images/TruifyLogoAlpha.png")
#st.sidebar.title("TRUIFY.AI")

# Define menu items and their data modification status
menu_items = [
    {"name": "Home", "modifies_data": False},
    {"name": "Import Data", "modifies_data": True},
    {"name": "Describe Data", "modifies_data": False},
    {"name": "Create Compliance Report", "modifies_data": False},
    {"name": "PII Analysis", "modifies_data": True},
    {"name": "Reduce Bias", "modifies_data": True},
    {"name": "Fill Missingness", "modifies_data": True},
    {"name": "Merge Data", "modifies_data": True},
    {"name": "Synthesize Data", "modifies_data": True},
    {"name": "Export Data", "modifies_data": False}
]

# Initialize current page in session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = menu_items[0]["name"]

# Initialize visited pages tracking
if 'visited_pages' not in st.session_state:
    st.session_state['visited_pages'] = {"Home"}  # Home is always visited
else:
    # Ensure Home is always in visited_pages
    st.session_state['visited_pages'].add("Home")

# Track the previous page to detect navigation
if 'previous_page' not in st.session_state:
    st.session_state['previous_page'] = None

# Render menu as hyperlinked text with checkboxes

for item in menu_items:
    item_name = item["name"]
    
    # Determine checkbox status based on whether page has been visited
    if item_name in st.session_state['visited_pages']:
        checkbox = "✓"  # Check mark for visited pages
    else:
        checkbox = "○"  # Empty circle for unvisited pages
    
    # Create menu item with checkbox and clickable text
    col1, col2 = st.sidebar.columns([1, 10])
    with col1:
        if item_name in st.session_state['visited_pages']:
            # For visited pages: show circle with check mark overlay
            st.markdown(f"""
            <div style="position: relative; display: inline-block;">
                <span style="font-size: 32px; color: #FFFFFF; position: relative; z-index: 1;">○</span>
                <span style="font-size: 24px; color: #FFFFFF; position: absolute; top: 2px; left: 4px; z-index: 2; font-weight: bold;">✓</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            # For unvisited pages: show empty circle
            st.markdown(f"<span style='font-size: 32px; color: #FFFFFF;'>{checkbox}</span>", unsafe_allow_html=True)
    with col2:
        if st.button(item_name, key=f"menu_{item_name.replace(' ', '_')}", use_container_width=True):
            st.session_state['current_page'] = item_name
            st.session_state['previous_page'] = item_name
            # Mark the page as visited immediately when clicked
            st.session_state['visited_pages'].add(item_name)
            st.rerun()

page = st.session_state['current_page']


if page == "Home":
    #st.markdown("""
    #    <div style='display: flex; justify-content: center; align-items: center; height: 60vh;'>
   #         <img src='images/truify_animation_once.gif' style='max-width: 100%; height: auto;' />
    #    </div>
    #""", unsafe_allow_html=True)
    st.image("images/truify_animation_once.gif")
    st.write("Truify.ai is an agentic platform enabling trustworthy and more accurate AI through intelligent, automated data engineering.  The platform helps you identify risks and bias in your data, then clean, fill and fix your data.")
    st.write("")
    st.write("Truify.ai generates new synthetic versions of your data that contain the same signals as your original data, while greatly reducing exposure to risk through bias, privacy leaks or compliance violations.")
    st.write("")
    st.write("This site demonstrates the capabilities of the agentic Software-as-a-Service (SaaS) enabled by Truify.AIs API-based services.  These can be integrated into your systems on-prem, or in a private cloud.")
    st.write("")
    st.write("Get started by importing your data, using the button on the left.")
    st.write("")
    st.write("To learn more, contact info@truify.ai")
    st.image("images/diagram.png")


if page == "Import Data":
    st.title("Import Data")
    
    # Initialize session state for data type configuration
    if 'data_type_config' not in st.session_state:
        st.session_state['data_type_config'] = {}
    if 'original_file' not in st.session_state:
        st.session_state['original_file'] = None
    if 'show_data_type_config' not in st.session_state:
        st.session_state['show_data_type_config'] = False
    if 'file_uploaded' not in st.session_state:
        st.session_state['file_uploaded'] = False
    
    # Handle file upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None and not st.session_state['file_uploaded']:
        # Store the original file for re-importing with data types
        st.session_state['original_file'] = uploaded_file
        
        # Initial import to get default data types
        df = pd.read_csv(uploaded_file)
        
        # Initialize data type configuration with default types
        if not st.session_state['data_type_config']:
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    if df[col].dtype == 'int64':
                        st.session_state['data_type_config'][col] = 'int64'
                    else:
                        st.session_state['data_type_config'][col] = 'float64'
                else:
                    st.session_state['data_type_config'][col] = 'object'
        
        st.session_state['df'] = df
        st.session_state['file_uploaded'] = True
        if 'genai_description' in st.session_state:
            del st.session_state['genai_description']
    
    # Show data type configuration interface if file is uploaded or user wants to reconfigure
    if (uploaded_file is not None and st.session_state['file_uploaded']) or st.session_state['show_data_type_config']:
        if 'df' in st.session_state:
            df = st.session_state['df']
            
            # Show data type configuration interface
            st.subheader("Data Type Configuration")
            st.write("Configure data types for each column. This is especially important for columns like ZIP codes that might have leading zeros.")
            
            # Data type selection interface
            for col in df.columns:
                current_dtype = st.session_state['data_type_config'].get(col, 'object')
                new_dtype = st.selectbox(
                    f"Data type for {col}",
                    ['object', 'int64', 'float64', 'datetime64[ns]', 'bool'],
                    index=['object', 'int64', 'float64', 'datetime64[ns]', 'bool'].index(current_dtype),
                    key=f"dtype_{col}"
                )
                st.session_state['data_type_config'][col] = new_dtype
            
            # Apply data type changes button
            if st.button("Apply Data Type Changes", type="primary"):
                try:
                    # Re-import with explicit data types
                    uploaded_file.seek(0)  # Reset file pointer
                    
                    # Create dtype dictionary for pandas
                    dtype_dict = {}
                    for col, dtype in st.session_state['data_type_config'].items():
                        if dtype == 'datetime64[ns]':
                            # For datetime, we'll need to parse it after import
                            dtype_dict[col] = 'object'
                        else:
                            dtype_dict[col] = dtype
                    
                    # Re-import with specified data types
                    df_new = pd.read_csv(uploaded_file, dtype=dtype_dict)
                    
                    # Handle datetime columns separately
                    for col, dtype in st.session_state['data_type_config'].items():
                        if dtype == 'datetime64[ns]':
                            try:
                                df_new[col] = pd.to_datetime(df_new[col], errors='coerce')
                            except Exception as e:
                                st.warning(f"Could not convert {col} to datetime: {str(e)}")
                    
                    # Update the dataframe
                    st.session_state['df'] = df_new
                    st.session_state['show_data_type_config'] = False
                    st.success("✅ Data types applied successfully!")
                    st.info(f"Dataset shape: {df_new.shape}")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error applying data types: {str(e)}")
                    st.error("Please check your data type selections. Some conversions may not be possible.")
                    
                    # Show detailed error information
                    st.subheader("Debugging Information")
                    st.write(f"Error details: {str(e)}")
                    st.write("Common issues:")
                    st.write("- Converting text to numeric when text contains non-numeric characters")
                    st.write("- Converting to datetime when date format is inconsistent")
                    st.write("- Converting to boolean when values are not True/False")
                    
                    # Show sample data for problematic columns
                    st.write("**Sample data from each column:**")
                    for col in df.columns:
                        st.write(f"{col}: {df[col].head(3).tolist()}")
    
    # Show loaded dataframe and controls
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.dataframe(df)
        st.success("A dataframe is loaded.")
        
        # Show data type configuration if available
        if st.session_state['data_type_config']:
            st.subheader("Current Data Type Configuration")
            for col, dtype in st.session_state['data_type_config'].items():
                st.write(f"**{col}**: {dtype}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Upload New File"):
                del st.session_state['df']
                st.session_state['data_type_config'] = {}
                st.session_state['original_file'] = None
                st.session_state['file_uploaded'] = False
                st.session_state['show_data_type_config'] = False
                if 'genai_description' in st.session_state:
                    del st.session_state['genai_description']
                st.rerun()
        
        with col2:
            if st.button("Reconfigure Data Types"):
                st.session_state['show_data_type_config'] = True
                st.rerun()

elif page == "Describe Data":
    st.title("Describe Data")
    if 'df' in st.session_state:
        df = st.session_state['df']
        if 'genai_description' in st.session_state:
            st.subheader("AI-Generated Dataset Description")
            st.info(st.session_state['genai_description'])
        if st.button("Describe data with AI"):
            try:
                from genai import describe_dataset_with_genai
                st.subheader("AI-Generated Dataset Description")
                with st.spinner("Analyzing dataset with generative AI..."):
                    description = describe_dataset_with_genai(df)
                st.session_state['genai_description'] = description
                st.info(description)
            except Exception as e:
                st.warning(f"Could not generate dataset description: {e}")
        if st.button("Show Graphs"):
            import plotly.express as px
            import pandas as pd
            st.subheader("Variable Visualizations")
            for col in df.columns:
                st.markdown(f"**{col}**")
                if pd.api.types.is_numeric_dtype(df[col]):
                    fig = px.histogram(df, x=col, nbins=20, title=f"Histogram of {col}", color_discrete_sequence=['#636EFA'])
                    fig.update_layout(bargap=0.1, xaxis_title=col, yaxis_title='Frequency', template='plotly_white')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    value_counts = df[col].value_counts(normalize=True)
                    mask = value_counts < 0.02
                    if mask.any():
                        other_sum = value_counts[mask].sum()
                        value_counts = value_counts[~mask]
                        value_counts['Other'] = other_sum
                    pie_df = pd.DataFrame({col: value_counts.index, 'proportion': value_counts.values})
                    fig = px.pie(pie_df, names=col, values='proportion', title=f"Distribution of {col}", color_discrete_sequence=px.colors.sequential.RdBu)
                    fig.update_traces(textinfo='percent+label')
                    fig.update_layout(template='plotly_white')
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Please import data first.")

elif page == "PII Analysis":
    pii_page()

elif page == "Reduce Bias":
    st.title("Reduce Bias")
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.dataframe(st.session_state['df'])
        # Always show AI-generated bias analysis if present
        if 'genai_bias_analysis' in st.session_state:
            st.subheader("AI-Generated Bias Analysis")
            st.info(st.session_state['genai_bias_analysis'])
        if st.button("Analyze Bias with AI"):
            try:
                from genai import analyze_bias_with_genai
                st.subheader("AI-Generated Bias Analysis")
                with st.spinner("Analyzing dataset for bias with generative AI..."):
                    bias_description = analyze_bias_with_genai(df)
                st.session_state['genai_bias_analysis'] = bias_description
                st.info(bias_description)
            except Exception as e:
                st.warning(f"Could not generate bias analysis: {e}")
        ground_truth_data = st.selectbox("Select ground truth data source:", ["US Census", "Other"])
        if st.button("Create Weights"):
            import sys
            import os
            import tempfile
            import subprocess
            import pandas as pd
            import json
            # Save current df to a temporary CSV
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                df.to_csv(tmp.name, index=False)
                tmp_path = tmp.name
            # Prepare output paths
            bias_report_path = os.path.join(os.path.dirname(tmp_path), "bias_report.md")
            weights_json_path = os.path.join(os.path.dirname(tmp_path), "weights.json")
            # Call bias.py as a subprocess, requesting weights as JSON
            result = subprocess.run([
                sys.executable, os.path.join("code", "bias.py"), tmp_path, "--groundtruth", ground_truth_data, "--output", bias_report_path, "--weights_json", weights_json_path
            ], capture_output=True, text=True)
            # Read the generated bias_report.md
            if os.path.exists(bias_report_path):
                with open(bias_report_path, "r") as f:
                    bias_md = f.read()
                st.markdown(bias_md)
            else:
                st.error("Bias report could not be generated.\n" + result.stderr)
            # Read weights and preview the weighted dataframe
            if os.path.exists(weights_json_path):
                with open(weights_json_path, "r") as f:
                    weights = json.load(f)
                weighted_df = df.copy()
                weighted_df['Weights'] = weights
                st.session_state['preview_weighted_df'] = weighted_df
            # Clean up temp files
            os.remove(tmp_path)
            if os.path.exists(bias_report_path):
                os.remove(bias_report_path)
            if os.path.exists(weights_json_path):
                os.remove(weights_json_path)
        # Show preview and keep weights button if available
        if 'preview_weighted_df' in st.session_state:
            st.subheader("Preview Weighted DataFrame")
            st.dataframe(st.session_state['preview_weighted_df'])
            if st.button("Keep Weights"):
                st.session_state['df'] = st.session_state['preview_weighted_df']
                del st.session_state['preview_weighted_df']
                # Mark Reduce Bias as modified
                # st.session_state['data_modified_pages'].add("Reduce Bias") # This line is removed
                st.success("Weighted dataframe has replaced the original data.")
                st.rerun()
    else:   
        st.write("Please import data first.")

elif page == "Fill Missingness":
    st.title("Fill Missingness")
    if 'missingness_filled_count' in st.session_state:
        st.success(f"Filled {st.session_state['missingness_filled_count']} missing cells.")
        st.dataframe(st.session_state['df'])
        del st.session_state['missingness_filled_count']
        st.session_state['missingness_evaluated'] = False
    elif 'missingness_evaluated' in st.session_state and st.session_state['missingness_evaluated']:
        st.markdown(st.session_state['missingness_report_md'])
        col_info = st.session_state['missingness_col_info']
        all_zero = all(float(info[1].replace('%','')) == 0.0 for info in col_info)
        if all_zero:
            st.info("No data to impute! All values present.")
        else:
            if st.button("Fill Missingness"):
                # Always use the original, unstyled dataframe for imputation
                df = st.session_state['df'].copy()
                import numpy as np
                df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
                filled_count = 0
                for info in col_info:
                    col, pct_missing, method, dtype, reason = info
                    if float(pct_missing.replace('%','')) == 0.0:
                        continue
                    before = df[col].isnull().sum()
                    if method == 'mean':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].astype(float).mean())
                    elif method == 'median':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].astype(float).median())
                    elif method == 'mode':
                        mode_val = df[col].mode(dropna=True)
                        if not mode_val.empty:
                            df[col] = df[col].fillna(mode_val[0])
                    after = df[col].isnull().sum()
                    filled_count += before - after
                st.session_state['df'] = df
                st.session_state['missingness_filled_count'] = filled_count
                st.session_state['missingness_evaluated'] = False
                # Mark Fill Missingness as modified
                # st.session_state['data_modified_pages'].add("Fill Missingness") # This line is removed
                st.rerun()
    elif 'df' in st.session_state:
        df = st.session_state['df']
        if st.button("Evaluate Data"):
            import sys, os, tempfile, subprocess, re, pandas as pd
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                df.to_csv(tmp.name, index=False)
                tmp_path = tmp.name
            missingness_report_path = os.path.join(os.path.dirname(tmp_path), "missingness_report.md")
            result = subprocess.run([
                sys.executable, os.path.join("code", "missingness.py"), tmp_path, "--output", missingness_report_path
            ], capture_output=True, text=True)
            if os.path.exists(missingness_report_path):
                with open(missingness_report_path, "r") as f:
                    md = f.read()
                st.session_state['missingness_report_md'] = md
                rows = [line for line in md.splitlines() if line.startswith('|') and not line.startswith('|---')]
                if len(rows) > 0:
                    rows = rows[1:]
                col_info = []
                for row in rows:
                    parts = [p.strip() for p in row.strip('|').split('|')]
                    if len(parts) == 5:
                        col_info.append(parts)
                st.session_state['missingness_col_info'] = col_info
                st.session_state['missingness_evaluated'] = True
                st.rerun()
            else:
                st.error("Missingness report could not be generated.\n" + result.stderr)
            if os.path.exists(missingness_report_path):
                os.remove(missingness_report_path)
    else:
        st.write("Please import data first.")

elif page == "Merge Data":
    st.title("Merge Data")
    st.write("Coming Soon!")

elif page == "Synthesize Data":
    synthesize_page()

elif page == "Export Data":
    st.title("Export Data")
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.write(f"Dataset shape: {df.shape}")
        st.write(f"Dataset columns: {list(df.columns)}")
        
        # Check if synthetic data exists
        if 'synthetic_df' in st.session_state:
            st.info("Synthetic data is available in session state.")
            if st.button("Show Synthetic Data Instead"):
                df = st.session_state['synthetic_df']
                st.write(f"Synthetic dataset shape: {df.shape}")
                st.write(f"Synthetic dataset columns: {list(df.columns)}")
                st.write("**Synthetic Dataset Preview:**")
                st.dataframe(df.head(10))
        else:
            st.info("No synthetic data available.")
        
        st.write("**Dataset Preview:**")
        st.dataframe(df.head(10))
        filename = st.text_input("Enter filename for download (with .csv extension):", value="exported_data.csv")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=filename,
            mime='text/csv',
        )
    else:
        st.write("Please import data first.")

elif page == "Create Compliance Report":
    st.title("Create New Compliance Evaluation")
    st.write("""
    This tool evaluates your dataset for compliance risks relative to major data protection and AI regulations. It analyzes your data for personally identifiable information (PII), sensitive attributes, missingness, and risks related to automated decision-making. The tool generates a detailed markdown report describing the data, potential compliance risks (with references to GDPR, CCPA, and the EU AI Act), and an action plan for remediation.
    """)
    st.subheader("Select Compliance Policies to Check:")
    
    # Data Protection & Privacy Laws
    st.write("**Data Protection & Privacy Laws:**")
    privacy_policies = ["GDPR", "CCPA", "LGPD", "PIPEDA", "PDPA_SG", "PIPL", "APPI", "PDPA_TH", "POPIA", "COPPA", "GLBA", "SOX", "ePrivacy", "NIS2"]
    selected_privacy = st.multiselect("Privacy Laws", privacy_policies, default=privacy_policies)
    
    # AI-Specific Regulations
    st.write("**AI-Specific Regulations:**")
    ai_policies = ["EU AI Act", "AI Act CA", "AI Gov SG", "AI Ethics JP", "OECD AI", "UNESCO AI", "G7 AI"]
    selected_ai = st.multiselect("AI Regulations", ai_policies, default=ai_policies)
    
    # Industry-Specific Regulations
    st.write("**Industry-Specific Regulations:**")
    industry_policies = ["HIPAA", "Basel", "MiFID II", "Dodd-Frank", "FDA AI", "MDR", "UNECE", "ISO 21434"]
    selected_industry = st.multiselect("Industry Regulations", industry_policies)
    
    # Cybersecurity & Infrastructure
    st.write("**Cybersecurity & Infrastructure:**")
    security_policies = ["NIST", "ISO 27001", "SOC 2", "PCI DSS"]
    selected_security = st.multiselect("Security Standards", security_policies)
    
    # Emerging/Proposed Regulations
    st.write("**Emerging/Proposed Regulations:**")
    emerging_policies = ["AI Liability", "Data Act", "DSA", "DMA"]
    selected_emerging = st.multiselect("Emerging Regulations", emerging_policies)
    
    # Custom policies
    st.write("**Custom Policies:**")
    custom_policies = st.text_area("Add custom policies (one per line):")
    
    # Combine all selected policies
    selected_policies = selected_privacy + selected_ai + selected_industry + selected_security + selected_emerging
    if custom_policies:
        custom_list = [p.strip() for p in custom_policies.split('\n') if p.strip()]
        selected_policies.extend(custom_list)
    # Generate Report button
    if st.button("Generate Report"):
        if 'df' not in st.session_state:
            st.warning("Please import data first.")
        else:
            with st.spinner("Generating compliance report..."):
                try:
                    import sys
                    sys.path.append("./code")
                    import compliance
                    df = st.session_state['df']
                    # Prepare policy list for compliance.py
                    policy_args = selected_policies
                    result = compliance.evaluate_compliance(df, policies=policy_args)
                    
                    # Store the markdown report in session state
                    st.session_state['compliance_report_md'] = result['markdown']
                    st.session_state['compliance_report_generated'] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating compliance report: {e}")
    
    # Display report if it exists in session state
    if 'compliance_report_generated' in st.session_state and st.session_state['compliance_report_generated']:
        st.markdown(st.session_state['compliance_report_md'])
        
        # Add download button
        try:
            import tempfile
            import subprocess
            import os
            
            # Create temporary markdown file with LaTeX image conversion
            markdown_content = st.session_state['compliance_report_md']
            
            # Keep markdown image format as-is to avoid LaTeX escape issues
            # The base64 embedding and multiple PDF methods should handle images properly
            
            # Remove any potential figure captions from the markdown
            import re
            # Remove figure captions that might be added by pandoc
            markdown_content = re.sub(r'\\caption\{[^}]*\}', '', markdown_content)
            markdown_content = re.sub(r'\\label\{[^}]*\}', '', markdown_content)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_md:
                tmp_md.write(markdown_content)
                tmp_md_path = tmp_md.name
            
            # Create temporary PDF file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
                tmp_pdf_path = tmp_pdf.name
            
            # Skip custom template for now to avoid LaTeX escape issues
            tmp_template_path = None
            
            # Copy logo file to temporary directory for PDF generation
            import shutil
            import base64
            logo_source = os.path.join(os.path.dirname(__file__), "..", "images", "TruifyLogo.png")
            logo_dest = os.path.join(os.path.dirname(tmp_md_path), "TruifyLogo.png")
            
            # Initialize base64 variables
            base64_image = None
            img_data = None
            
            if os.path.exists(logo_source):
                shutil.copy2(logo_source, logo_dest)
                # Update the markdown content to use the local path
                markdown_content = markdown_content.replace(logo_source, "TruifyLogo.png")
                # Also replace any absolute paths with just the filename, removing alt text
                markdown_content = re.sub(r'!\[.*?\]\([^)]*TruifyLogo\.png\)', '![](TruifyLogo.png)', markdown_content)
                
                # Try to embed image as base64 for better compatibility
                try:
                    with open(logo_source, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode('utf-8')
                        base64_image = f'![](data:image/png;base64,{img_data})'
                        # Replace any logo image with embedded base64, regardless of alt text
                        markdown_content = re.sub(r'!\[.*?\]\(TruifyLogo\.png\)', base64_image, markdown_content)
                except:
                    pass  # Fall back to file reference if base64 fails
                
                # Create a version with embedded base64 for PDF tools
                if base64_image:
                    markdown_content_for_pdf = markdown_content  # Keep base64 for PDF too
                else:
                    markdown_content_for_pdf = markdown_content
                    # Remove alt text from any remaining logo references
                    markdown_content_for_pdf = re.sub(r'!\[.*?\]\(TruifyLogo\.png\)', '![](TruifyLogo.png)', markdown_content_for_pdf)
                
                # Rewrite the file with updated content
                with open(tmp_md_path, 'w') as f:
                    f.write(markdown_content)
                
                # Create separate markdown file for PDF generation (with file references)
                with tempfile.NamedTemporaryFile(mode='w', suffix='_pdf.md', delete=False) as tmp_md_pdf:
                    tmp_md_pdf.write(markdown_content_for_pdf)
                    tmp_md_pdf_path = tmp_md_pdf.name
            
            # Convert markdown to HTML first, then to PDF
            try:
                # Always generate HTML first for debugging
                html_path = tmp_md_path.replace('.md', '.html')
                html_generated = False
                
                # Generate HTML
                try:
                    # Create CSS file with Helvetica font
                    css_path = tmp_md_path.replace('.md', '.css')
                    css_content = """
body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.4;
    margin: 1in;
}
h1, h2, h3, h4, h5, h6 {
    font-family: Helvetica, Arial, sans-serif;
    font-weight: bold;
}
h1 {
    text-align: center;
    margin-bottom: 1em;
}
table {
    font-family: Helvetica, Arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    font-size: 10pt;
}
th {
    background-color: #f2f2f2;
    font-weight: bold;
}
img {
    max-width: 150px;
    height: auto;
    display: block;
    margin: 0 auto;
}
"""
                    with open(css_path, 'w') as f:
                        f.write(css_content)
                    
                    # First generate HTML without embedded resources
                    subprocess.run([
                        'pandoc', 
                        tmp_md_path, 
                        '-o', html_path,
                        '--to=html5',
                        '--standalone',
                        '--css=' + css_path,
                        '--metadata=title:Compliance Report'
                    ], check=True, capture_output=True, timeout=30)
                    
                    # Now manually embed the base64 image in the HTML
                    if base64_image and os.path.exists(html_path):
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        # Replace any logo references with the base64 image
                        html_content = re.sub(r'<img[^>]*src="[^"]*TruifyLogo\.png"[^>]*>', f'<img src="data:image/png;base64,{img_data}" alt="Logo" style="max-width: 150px; height: auto; display: block; margin: 0 auto;">', html_content)
                        
                        # Write the updated HTML with embedded base64 image
                        with open(html_path, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                    
                    if os.path.exists(html_path) and os.path.getsize(html_path) > 1000:
                        html_generated = True
                    else:
                        st.error("HTML generation failed: File too small or empty")
                except Exception as e:
                    st.error(f"HTML generation failed: {str(e)}")
                
                # Try multiple PDF generation methods
                pdf_generated = False
                error_messages = []
                
                # Method 1: Try converting HTML to PDF using wkhtmltopdf
                if html_generated:
                    try:
                        result = subprocess.run([
                            'wkhtmltopdf',
                            '--enable-local-file-access',
                            '--image-quality', '100',
                            '--image-dpi', '300',
                            '--page-size', 'A4',
                            '--margin-top', '0.5in',
                            '--margin-bottom', '0.5in',
                            '--margin-left', '0.5in',
                            '--margin-right', '0.5in',
                            html_path,
                            tmp_pdf_path
                        ], check=True, capture_output=True, timeout=30)
                        
                        if os.path.exists(tmp_pdf_path) and os.path.getsize(tmp_pdf_path) > 1000:
                            pdf_generated = True
                        else:
                            error_messages.append("wkhtmltopdf: File too small or empty")
                    except Exception as e:
                        error_messages.append(f"wkhtmltopdf: {str(e)}")
                
                # Method 2: Try weasyprint (HTML to PDF)
                if not pdf_generated and html_generated:
                    try:
                        subprocess.run([
                            'weasyprint',
                            html_path,
                            tmp_pdf_path
                        ], check=True, capture_output=True, timeout=30)
                        
                        if os.path.exists(tmp_pdf_path) and os.path.getsize(tmp_pdf_path) > 1000:
                            pdf_generated = True
                        else:
                            error_messages.append("weasyprint: File too small or empty")
                    except Exception as e:
                        error_messages.append(f"weasyprint: {str(e)}")
                
                # Method 2.5: Try direct markdown to PDF with embedded images
                if not pdf_generated:
                    try:
                        subprocess.run([
                            'pandoc', 
                            tmp_md_pdf_path, 
                            '-o', tmp_pdf_path,
                            '--pdf-engine=wkhtmltopdf',
                            '--pdf-engine-opt=--enable-local-file-access',
                            '--pdf-engine-opt=--image-quality=100',
                            '--pdf-engine-opt=--enable-javascript',
                            '--pdf-engine-opt=--javascript-delay=1000'
                        ], check=True, capture_output=True, timeout=30)
                        
                        if os.path.exists(tmp_pdf_path) and os.path.getsize(tmp_pdf_path) > 1000:
                            pdf_generated = True
                        else:
                            error_messages.append("direct markdown to PDF: File too small or empty")
                    except Exception as e:
                        error_messages.append(f"direct markdown to PDF: {str(e)}")
                
                # Method 3: Try Prince (HTML to PDF)
                if not pdf_generated and html_generated:
                    try:
                        subprocess.run([
                            'prince',
                            html_path,
                            '-o', tmp_pdf_path
                        ], check=True, capture_output=True, timeout=30)
                        
                        if os.path.exists(tmp_pdf_path) and os.path.getsize(tmp_pdf_path) > 1000:
                            pdf_generated = True
                        else:
                            error_messages.append("Prince: File too small or empty")
                    except Exception as e:
                        error_messages.append(f"Prince: {str(e)}")
                
                # Method 4: Try pandoc HTML to PDF conversion with embedded images
                if not pdf_generated and html_generated:
                    try:
                        subprocess.run([
                            'pandoc', 
                            html_path, 
                            '-o', tmp_pdf_path,
                            '--pdf-engine=wkhtmltopdf',
                            '--pdf-engine-opt=--enable-local-file-access',
                            '--pdf-engine-opt=--image-quality=100',
                            '--pdf-engine-opt=--enable-javascript',
                            '--pdf-engine-opt=--javascript-delay=1000'
                        ], check=True, capture_output=True, timeout=30)
                        
                        if os.path.exists(tmp_pdf_path) and os.path.getsize(tmp_pdf_path) > 1000:
                            pdf_generated = True
                        else:
                            error_messages.append("pandoc HTML to PDF: File too small or empty")
                    except Exception as e:
                        error_messages.append(f"pandoc HTML to PDF: {str(e)}")
                
                # Method 4.5: Try creating HTML with embedded images and convert to PDF
                if not pdf_generated:
                    try:
                        # Create HTML from PDF-optimized markdown with embedded images
                        html_pdf_path = tmp_md_pdf_path.replace('.md', '.html')
                        subprocess.run([
                            'pandoc', 
                            tmp_md_pdf_path, 
                            '-o', html_pdf_path,
                            '--to=html5',
                            '--standalone',
                            '--css=' + css_path,
                            '--metadata=title:Compliance Report'
                        ], check=True, capture_output=True, timeout=30)
                        
                        # Manually embed the base64 image in the HTML
                        if base64_image and os.path.exists(html_pdf_path):
                            with open(html_pdf_path, 'r', encoding='utf-8') as f:
                                html_content = f.read()
                            
                            # Replace any logo references with the base64 image
                            html_content = re.sub(r'<img[^>]*src="[^"]*TruifyLogo\.png"[^>]*>', f'<img src="data:image/png;base64,{img_data}" alt="Logo" style="max-width: 150px; height: auto; display: block; margin: 0 auto;">', html_content)
                            
                            # Write the updated HTML with embedded base64 image
                            with open(html_pdf_path, 'w', encoding='utf-8') as f:
                                f.write(html_content)
                        
                        # Convert HTML to PDF
                        subprocess.run([
                            'wkhtmltopdf',
                            '--enable-local-file-access',
                            '--image-quality', '100',
                            '--image-dpi', '300',
                            '--page-size', 'A4',
                            '--margin-top', '0.5in',
                            '--margin-bottom', '0.5in',
                            '--margin-left', '0.5in',
                            '--margin-right', '0.5in',
                            '--enable-javascript',
                            '--javascript-delay', '1000',
                            html_pdf_path,
                            tmp_pdf_path
                        ], check=True, capture_output=True, timeout=30)
                        
                        if os.path.exists(tmp_pdf_path) and os.path.getsize(tmp_pdf_path) > 1000:
                            pdf_generated = True
                        else:
                            error_messages.append("HTML with embedded images to PDF: File too small or empty")
                    except Exception as e:
                        error_messages.append(f"HTML with embedded images to PDF: {str(e)}")
                
                # Method 5: Try using Chrome/Chromium headless with embedded images (if available)
                if not pdf_generated:
                    try:
                        # Try to find Chrome or Chromium
                        chrome_paths = [
                            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS
                            '/usr/bin/google-chrome',  # Linux
                            '/usr/bin/chromium-browser',  # Linux
                            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',  # Windows
                            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'  # Windows
                        ]
                        
                        chrome_path = None
                        for path in chrome_paths:
                            if os.path.exists(path):
                                chrome_path = path
                                break
                        
                        if chrome_path:
                            # Use the HTML file with embedded images if available, otherwise use the PDF-optimized HTML
                            chrome_html_path = html_path if html_generated else html_pdf_path if 'html_pdf_path' in locals() and os.path.exists(html_pdf_path) else None
                            
                            if chrome_html_path and os.path.exists(chrome_html_path):
                                subprocess.run([
                                    chrome_path,
                                    '--headless',
                                    '--disable-gpu',
                                    '--print-to-pdf=' + tmp_pdf_path,
                                    '--print-to-pdf-no-header',
                                    '--print-to-pdf-no-footer',
                                    '--print-to-pdf-margin-top=0.5in',
                                    '--print-to-pdf-margin-bottom=0.5in',
                                    '--print-to-pdf-margin-left=0.5in',
                                    '--print-to-pdf-margin-right=0.5in',
                                    'file://' + os.path.abspath(chrome_html_path)
                                ], check=True, capture_output=True, timeout=30)
                                
                                if os.path.exists(tmp_pdf_path) and os.path.getsize(tmp_pdf_path) > 1000:
                                    pdf_generated = True
                                else:
                                    error_messages.append("Chrome headless: File too small or empty")
                            else:
                                error_messages.append("Chrome headless: No suitable HTML file found")
                        else:
                            error_messages.append("Chrome headless: Chrome/Chromium not found")
                    except Exception as e:
                        error_messages.append(f"Chrome headless: {str(e)}")
                
                # Method 6: Try creating a simple HTML file with embedded logo and Chrome headless
                if not pdf_generated:
                    try:
                        # Create a simple HTML file with embedded logo
                        simple_html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Compliance Report</title>
    <style>
        body {{ font-family: Helvetica, Arial, sans-serif; margin: 1in; font-size: 12pt; line-height: 1.4; }}
        img {{ max-width: 150px; height: auto; display: block; margin: 0 auto; }}
        table {{ border-collapse: collapse; width: 100%; font-family: Helvetica, Arial, sans-serif; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 10pt; }}
        th {{ background-color: #f2f2f2; font-weight: bold; }}
        h1, h2, h3, h4, h5, h6 {{ font-family: Helvetica, Arial, sans-serif; font-weight: bold; }}
        h1 {{ text-align: center; margin-bottom: 1em; }}
    </style>
</head>
<body>
"""
                        
                        # Add logo if available
                        if base64_image:
                            simple_html_content += f'<img src="data:image/png;base64,{img_data}" alt="Logo" style="max-width: 150px; height: auto; display: block; margin: 0 auto;"><br><br>\n'
                        
                        # Convert markdown content to simple HTML
                        import re
                        # Remove markdown formatting and convert to simple HTML
                        html_content = markdown_content
                        
                        # Convert headers
                        html_content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
                        html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
                        html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
                        
                        # Convert bold
                        html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
                        
                        # Convert lists
                        html_content = re.sub(r'^- (.*?)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
                        html_content = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul>\1</ul>', html_content, flags=re.DOTALL)
                        
                        # Convert line breaks
                        html_content = html_content.replace('\n\n', '</p><p>')
                        html_content = '<p>' + html_content + '</p>'
                        
                        simple_html_content += html_content + """
</body>
</html>
"""
                        
                        # Write simple HTML file
                        simple_html_path = tmp_md_path.replace('.md', '_simple.html')
                        with open(simple_html_path, 'w', encoding='utf-8') as f:
                            f.write(simple_html_content)
                        
                        # Try to find Chrome or Chromium
                        chrome_paths = [
                            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS
                            '/usr/bin/google-chrome',  # Linux
                            '/usr/bin/chromium-browser',  # Linux
                            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',  # Windows
                            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'  # Windows
                        ]
                        
                        chrome_path = None
                        for path in chrome_paths:
                            if os.path.exists(path):
                                chrome_path = path
                                break
                        
                        if chrome_path and os.path.exists(simple_html_path):
                            subprocess.run([
                                chrome_path,
                                '--headless',
                                '--disable-gpu',
                                '--print-to-pdf=' + tmp_pdf_path,
                                '--print-to-pdf-no-header',
                                '--print-to-pdf-no-footer',
                                '--print-to-pdf-margin-top=0.5in',
                                '--print-to-pdf-margin-bottom=0.5in',
                                '--print-to-pdf-margin-left=0.5in',
                                '--print-to-pdf-margin-right=0.5in',
                                'file://' + os.path.abspath(simple_html_path)
                            ], check=True, capture_output=True, timeout=30)
                            
                            if os.path.exists(tmp_pdf_path) and os.path.getsize(tmp_pdf_path) > 1000:
                                pdf_generated = True
                            else:
                                error_messages.append("Simple HTML to PDF: File too small or empty")
                        else:
                            error_messages.append("Simple HTML to PDF: Chrome not found or HTML not created")
                    except Exception as e:
                        error_messages.append(f"Simple HTML to PDF: {str(e)}")
                
                if not pdf_generated:
                    # Show diagnostic information
                    st.error("**Error generating PDF: All PDF generation methods failed**")
                    st.write("**Error details:**")
                    for error in error_messages:
                        st.write(f"- {error}")
                    
                    # Check what tools are available
                    import shutil
                    tools_available = {
                        'pandoc': shutil.which('pandoc') is not None,
                        'wkhtmltopdf': shutil.which('wkhtmltopdf') is not None,
                        'weasyprint': shutil.which('weasyprint') is not None,
                        'prince': shutil.which('prince') is not None
                    }
                    
                    st.write("**Available tools:**")
                    for tool, available in tools_available.items():
                        status = "✅ Available" if available else "❌ Not found"
                        st.write(f"- {tool}: {status}")
                    
                    # Don't raise exception, just show error
                    pdf_generated = False
                
                # Create download button for PDF only
                if pdf_generated:
                    # Read the generated PDF file
                    with open(tmp_pdf_path, 'rb') as pdf_file:
                        pdf_data = pdf_file.read()
                    
                    # Create download button for PDF
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_data,
                        file_name="compliance_report.pdf",
                        mime="application/pdf"
                    )
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Check what's available and provide specific guidance
                import shutil
                
                pandoc_available = shutil.which('pandoc') is not None
                pdflatex_available = shutil.which('pdflatex') is not None
                
                if pandoc_available and not pdflatex_available:
                    st.warning("""
                    **Pandoc is installed but pdflatex is not found in PATH.**
                    
                    On macOS with MacTeX, you may need to add LaTeX to your PATH:
                    ```bash
                    export PATH=$PATH:/Library/TeX/texbin
                    ```
                    
                    Or restart your terminal after installing MacTeX.
                    
                    Alternatively, try installing BasicTeX instead:
                    ```bash
                    brew install --cask basictex
                    ```
                    """)
                elif not pandoc_available:
                    st.warning("""
                    **Pandoc is not installed.**
                    
                    To install on macOS:
                    ```bash
                    brew install pandoc
                    brew install --cask mactex
                    ```
                    
                    To install on Ubuntu/Debian:
                    ```bash
                    sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils texlive-latex-extra
                    ```
                    
                    To install on Windows:
                    1. Download Pandoc from https://pandoc.org/installing.html
                    2. Download MiKTeX from https://miktex.org/download
                    """)
                else:
                    st.warning("""
                    **PDF generation failed despite having required tools.**
                    
                    This might be due to:
                    - LaTeX packages not installed
                    - Permission issues
                    - Temporary system issues
                    
                    Try restarting your terminal or the application.
                    """)
                
                # Alternative: provide markdown download
                st.download_button(
                    label="Download Report (Markdown)",
                    data=st.session_state['compliance_report_md'],
                    file_name="compliance_report.md",
                    mime="text/markdown"
                )
                
                # Also provide plain text download as alternative
                st.download_button(
                    label="Download Report (Plain Text)",
                    data=st.session_state['compliance_report_md'],
                    file_name="compliance_report.txt",
                    mime="text/plain"
                )
            
            # Clean up temporary files
            try:
                os.remove(tmp_md_path)
                if 'tmp_md_pdf_path' in locals() and os.path.exists(tmp_md_pdf_path):
                    os.remove(tmp_md_pdf_path)
                if os.path.exists(tmp_pdf_path):
                    os.remove(tmp_pdf_path)
                if html_generated and os.path.exists(html_path):
                    os.remove(html_path)
                if 'html_pdf_path' in locals() and os.path.exists(html_pdf_path):
                    os.remove(html_pdf_path)
                if 'simple_html_path' in locals() and os.path.exists(simple_html_path):
                    os.remove(simple_html_path)
                if tmp_template_path and os.path.exists(tmp_template_path):
                    os.remove(tmp_template_path)
                if os.path.exists(logo_dest):
                    os.remove(logo_dest)
                # Clean up CSS file if it exists
                css_path = tmp_md_path.replace('.md', '.css')
                if os.path.exists(css_path):
                    os.remove(css_path)
            except:
                pass
                
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
            # Fallback: provide markdown download
            st.download_button(
                label="Download Report (Markdown)",
                data=st.session_state['compliance_report_md'],
                file_name="compliance_report.md",
                mime="text/markdown"
            )
