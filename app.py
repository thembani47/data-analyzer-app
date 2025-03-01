import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import os

# Load CSV file
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")

def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

lottie_coding = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_vnikrcia.json")
lottie_learn = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_knvn3kk2.json")
lottie_chart = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_q5qeoo3q.json")

def main():

    selected = option_menu(
        menu_title=None,
        options=['Home','Data Analyser','Contact'],
        icons=['house','bar-chart','envelope'],
        default_index=0,
        orientation='horizontal'
    )
    
    if selected == 'Home':
        from PIL import Image
        image = Image.open('assets/img/data-analysis-charts-760.png')
        
        st.markdown("<h1 style='text-align: center;'>Tief Everything!!!</h1>", unsafe_allow_html=True)

        left_column, right_column = st.columns(2)
        with left_column:
             st.image(image, caption='Tief Everything')
        with right_column:
             st.write('A streamlit app to analyse user dataset')
             st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse ')

        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st_lottie(lottie_coding)
        with right_column:
            st_lottie(lottie_learn)

    if selected == 'Data Analyser':

        st.markdown("<h1 style='text-align: center;'>Visaulization/Charts</h1>", unsafe_allow_html=True)
        
        left_column, right_column = st.columns(2)
        with left_column:
            st.info("""The following are some of the charts that we have created from the raw data.
                    Some of the text is too long and may cut off, feel free to right click on the chart
                     and either save it or open it in a new window to see it properly.
                    Please proceed ahead and upload your file. The file should be in a csv or excel format.""")
        with right_column:
            st_lottie(lottie_chart)

        # Sidebar for file upload
        st.sidebar.header("Upload CSV File")
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

        # Main content
        st.title("CSV File Analysis")

        if uploaded_file is not None:
            # Load data
            df = load_data(uploaded_file)

            # Display the first few rows of the data
            st.subheader("Data Preview")
            st.dataframe(df.head())

            # Basic statistics
            st.subheader("Basic Statistics")
            st.write(df.describe())

            # Data Cleaning
            st.subheader("Data Cleaning")
            missing_values_option = st.selectbox("Handle Missing Values", ["None", "Drop Rows", "Fill with Mean", "Fill with Median"])
            if missing_values_option == "Drop Rows":
                df = df.dropna()
            elif missing_values_option == "Fill with Mean":
                df = df.fillna(df.mean())
            elif missing_values_option == "Fill with Median":
                df = df.fillna(df.median())

            st.subheader("Missing Values")
            columns = []
            missingValues = []
            for i in df:
                if df[i].isna().sum() > 0:
                    columns.append(i)
                    missingValues.append(df[i].isna().sum())

            missingValuesSum = sum(missingValues)

            left_column, right_column = st.columns(2)
            with left_column:
                st.info('Number of missing values')
            with right_column:
                st.info(missingValuesSum)

            if missingValuesSum > 0:
                st.write(df.isna().sum().sort_values(ascending=False))

            # Columns selection for analysis
            selected_columns = st.multiselect("Select Columns for Analysis", df.columns)

            if selected_columns:
                # Histogram
                st.subheader("Histogram")
                st.bar_chart(df[selected_columns])

                # Correlation matrix
                st.subheader("Correlation Matrix")
                st.write(df[selected_columns].corr())

                # Line Chart
                st.subheader("Line Chart")
                st.line_chart(df[selected_columns])

                # Scatter Plot
                st.subheader("Scatter Plot")
                x_axis = st.selectbox("Select X-axis", selected_columns)
                y_axis = st.selectbox("Select Y-axis", selected_columns)
                st.write(plt.scatter(df[x_axis], df[y_axis]))
                st.pyplot()

            # Data Export
            st.subheader("Export Data")
            if st.button("Download Cleaned Data"):
                df.to_csv("cleaned_data.csv", index=False)
                st.success("Data downloaded successfully!")

        else:
            st.info("Please upload a CSV file.")

    if selected == 'Contact':
        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            st.empty()
        with middle_column:
                st.info('Thembani Maswanganyi aka Tief Everything')
                st.write('App still under development!!!')
        with right_column:
            st.empty()

# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
    main()