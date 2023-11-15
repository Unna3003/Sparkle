import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set Streamlit title with HTML and CSS styling
st.markdown("<div style='text-align: center; color: #007BFF; font-size: 36px;'>Colorful Data Visualization</div>", unsafe_allow_html=True)


# Upload a CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display dataset summary statistics
    st.subheader("Dataset Summary")
    st.dataframe(df.describe(), width=600, height=300)

    # Data Preprocessing Section
    st.subheader("Data Preprocessing")

    # Handle missing values
    if st.checkbox("Handle Missing Values"):
        df.dropna(inplace=True)
        st.success("Missing values have been removed.")

    # Data type conversion (assuming all columns are numeric)
    if st.checkbox("Convert Data Types to Numeric"):
        df = df.apply(pd.to_numeric, errors='coerce')
        st.success("Data types have been converted to numeric.")

    # Feature scaling
    if st.checkbox("Standardize Features"):
        for column in df.columns:
            if df[column].dtype in ['int64', 'float64']:
                df[column] = (df[column] - df[column].mean()) / df[column].std()
        st.success("Features have been standardized.")

    # List of available charts
    chart_types = ["Bar Chart", "Histogram", "Scatter Plot", "Line Chart", "Box Plot", "Heatmap"]

    # Select a chart type
    selected_chart = st.selectbox("Select a chart type", chart_types)

    # Suggest suitable chart based on data
    if selected_chart == "Suggest Chart":
        st.subheader("Suggested Chart")

        # Logic to suggest a chart based on the dataset (you can customize this further)
        num_columns = len(df.columns)
        if num_columns <= 5:
            selected_chart = "Scatter Plot"
        elif num_columns <= 10:
            selected_chart = "Bar Chart"
        else:
            selected_chart = "Heatmap"

    # Data Visualization Section
    st.subheader("Data Visualization")

    if selected_chart == "Bar Chart":
        # Select columns for X and Y axes
        x_column = st.selectbox("Select a column for X-axis", df.columns)
        y_column = st.selectbox("Select a column for Y-axis", df.columns)
        st.bar_chart(df[[x_column, y_column]], use_container_width=True)

    elif selected_chart == "Histogram":
        # Select a column for the histogram
        column_to_plot = st.selectbox("Select a column for the histogram", df.columns)
        plt.hist(df[column_to_plot], bins=20)
        st.pyplot()

    elif selected_chart == "Scatter Plot":
        # Select columns for X and Y axes
        x_column = st.selectbox("Select a column for X-axis", df.columns)
        y_column = st.selectbox("Select a column for Y-axis", df.columns)
        fig = px.scatter(df, x=x_column, y=y_column, title=f"{x_column} vs {y_column}")
        st.plotly_chart(fig)

    elif selected_chart == "Line Chart":
        # Select columns for X and Y axes
        x_column = st.selectbox("Select a column for X-axis", df.columns)
        y_column = st.selectbox("Select a column for Y-axis", df.columns)
        fig = px.line(df, x=x_column, y=y_column, title=f"{x_column} vs {y_column}")
        st.plotly_chart(fig)

    elif selected_chart == "Box Plot":
        # Select a column for the box plot
        column_to_plot = st.selectbox("Select a column for the box plot", df.columns)
        fig = go.Figure(data=[go.Box(y=df[column_to_plot])])
        fig.update_layout(title=f"Box Plot of {column_to_plot}")
        st.plotly_chart(fig)

    elif selected_chart == "Heatmap":
        st.subheader("Correlation Heatmap")
        corr_matrix = df.corr()
        sns.heatmap(corr_matrix, annot=True)
        st.pyplot()

