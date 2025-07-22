import streamlit as st
import pandas as pd
import hashlib
import random
import numpy as np
from sklearn.impute import SimpleImputer

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
st.set_page_config(page_title='TRUIFY')
st.sidebar.image("images/TruifyLogo.png")
#st.sidebar.title("TRUIFY.AI")

# Define menu items
menu_items = [
    "Home",
    "Import Data",
    "Describe Data",
    "Create Compliance Report",
    "Deidentify Data",
    "Reduce Bias",
    "Fill Missingness",
    "Merge Data",
    "Synthesize Data",
    "Export Data"
]

# Initialize current page in session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = menu_items[0]

# Render menu as linked text/buttons
st.sidebar.markdown("## Menu")
for item in menu_items:
    if st.sidebar.button(item, key=f"menu_{item}"):
        st.session_state['current_page'] = item

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


if page == "Import Data":
    st.title("Import Data")
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.dataframe(df)
        st.success("A dataframe is loaded.")
        if st.button("Upload New File"):
            del st.session_state['df']
            if 'genai_description' in st.session_state:
                del st.session_state['genai_description']
            st.rerun()
    else:
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state['df'] = df
            if 'genai_description' in st.session_state:
                del st.session_state['genai_description']
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

elif page == "Deidentify Data":
    st.title("Deidentify Data")
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.dataframe(df)
        personal_info_columns = identify_personal_info_columns(df)
        for column in personal_info_columns:
            df[column] = df[column].apply(lambda x: f'<span style="background-color: red;">{x}</span>')##, axis=1)
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
        st.write("Columns containing personal information:", personal_info_columns)
        if st.button("Deidentify"):
            df = deidentify_data(df, personal_info_columns)
            st.session_state['df'] = df
            st.dataframe(df)
    else:
        st.write("Please import data first.")

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
    st.title("Synthesize Data")
    try:
        from synthesizer import data_synthesis
        result = data_synthesis()
        st.info(result)
    except Exception as e:
        st.error(f"Error: {e}")

elif page == "Export Data":
    st.title("Export Data")
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.dataframe(df)
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
    policies = ["GDPR", "EU AI Act", "CCPA", "Other"]
    selected_policies = st.multiselect("Compliance Policies", policies, default=["GDPR", "EU AI Act", "CCPA"])
    custom_policy = ""
    if "Other" in selected_policies:
        custom_policy = st.text_input("Specify Other Policy:")
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
                    policy_args = [p for p in selected_policies if p != "Other"]
                    if custom_policy:
                        policy_args.append(custom_policy)
                    result = compliance.evaluate_compliance(df, policies=policy_args)
                    st.markdown(result['markdown'])
                except Exception as e:
                    st.error(f"Error generating compliance report: {e}")
