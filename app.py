import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Data Processor & Summarizer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data File Processor & Summarizer")
st.write("Upload a CSV or Excel file to automatically clean data, view key metrics, and export summary reports.")

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"Successfully loaded `{uploaded_file.name}` ({df.shape[0]} rows, {df.shape[1]} columns)")
        
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.subheader("1. Data Preview & Quality Check")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Duplicate Rows", df.duplicated().sum())

    tab1, tab2 = st.tabs(["Raw Data Sample", "Data Types & Missing Values"])
    
    with tab1:
        st.dataframe(df.head(10), use_container_width=True)
        
    with tab2:
        info_df = pd.DataFrame({
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum(),
            "Null Percentage": (df.isnull().sum() / len(df) * 100).round(2).astype(str) + "%"
        })
        st.dataframe(info_df, use_container_width=True)

    st.subheader("2. Interactive Column Analysis")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    if numeric_cols:
        selected_num_col = st.selectbox("Select a numeric column to analyze:", numeric_cols)
        c1, c2 = st.columns([1, 2])
        with c1:
            st.write(f"**Summary Stats for `{selected_num_col}`:**")
            st.write(df[selected_num_col].describe())
        with c2:
            fig = px.histogram(df, x=selected_num_col, title=f"Distribution of {selected_num_col}")
            st.plotly_chart(fig, use_container_width=True)
            
    if categorical_cols:
        selected_cat_col = st.selectbox("Select a categorical column to analyze:", categorical_cols)
        value_counts = df[selected_cat_col].value_counts().reset_index()
        value_counts.columns = [selected_cat_col, "Count"]
        fig_cat = px.bar(value_counts.head(10), x=selected_cat_col, y="Count", title=f"Top Categories in {selected_cat_col}")
        st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("3. Data Cleaning & Export")
    clean_option = st.checkbox("Remove duplicate rows before export")
    export_df = df.drop_duplicates() if clean_option else df
    csv_data = export_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv_data,
        file_name=f"processed_{uploaded_file.name.split('.')[0]}.csv",
        mime="text/csv"
    )
else:
    st.info("👆 Please upload a CSV or Excel file to get started.")
