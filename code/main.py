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
st.sidebar.title("TRUIFY.AI")
<<<<<<< HEAD
st.sidebar.image("https://github.com/cturner500/truify/blob/main/TruifyLogo.png", use_column_width=True)
=======
st.sidebar.image("https://github.com/cturner500/truify/blob/main/TruifyLogo.png")


>>>>>>> 1135589524f2c1412de531b315d2a3b21c062578
page = st.sidebar.selectbox("Select a page:", ["Import Data", "Deidentify Data", "Reduce Bias", "Fill Missingness", "Merge Data", "Save Data", "Export Data"])


if page == "Import Data":
    st.title("Import Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state['df'] = df
        st.dataframe(df)

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
        st.dataframe(df)
        ground_truth_data = st.selectbox("Select ground truth data source:", ["US Census", "Other"])
        if st.button("Create Weights"):
            df = reduce_bias(df, ground_truth_data)
            st.session_state['df'] = df
            st.dataframe(df)
    else:
        st.write("Please import data first.")

elif page == "Fill Missingness":
    st.title("Fill Missingness")
    if 'df' in st.session_state:
        df = st.session_state['df']
        missingness = df.isnull().mean() > 0.1
        for column in df.columns[missingness]:
            df[column] = df[column].apply(lambda x: f'<span style="background-color: red;">{x}</span>')
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
        methodology = st.selectbox("Methodology", ["na.roughfix", "mean", "mode", "median", "LOCF"])
        if st.button("Fill Missing Values"):
            df = fill_missing_values(df, methodology)
            st.session_state['df'] = df
            st.dataframe(df)
    else:
        st.write("Please import data first.")

elif page == "Merge Data":
    st.title("Merge Data")
    st.write("Coming Soon!")

elif page == "Save Data":
    st.title("Save Data")
    st.write("Coming Soon!")

elif page == "Export Data":
    st.title("Export Data")
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.dataframe(df)
        if st.button("Export Data"):
            st.write("Export Data - Coming Soon!")
    else:
        st.write("Please import data first.")
