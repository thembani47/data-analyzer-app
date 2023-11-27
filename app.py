import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import os

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

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

        st.info('Please Upload a CSV file')

        raw_data = st.file_uploader('Upload your file here...')
        if raw_data is not None:
            if raw_data.type == 'text/csv':
                  df = pd.read_csv(raw_data)
            else:
                 df = pd.read_excel(raw_data)
        
            st.write("---")
            st.subheader("You can click on the *View raw data* button to have a look at the data frame")
            if st.checkbox("View raw data"):
                st.write(df.head(50))

            # code here
            df.select_dtypes(include=np.number).columns.tolist()
            
            st.markdown("<h2 style='text-align: center;'>Missing Values</h2>", unsafe_allow_html=True)
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
                fig = plt.figure(figsize = (15, 6))
                plt.bar(columns, missingValues, color ='maroon',width = 0.9)
                plt.xlabel("Column")
                plt.ylabel("No. of missing values")
                plt.title("Missing values by column")
                st.pyplot(fig)
                left_column, middle_column, right_column = st.columns(3) 
                with left_column:
                    st.empty()
                with middle_column:
                    st.write(df.isna().sum().sort_values(ascending=False))
                with right_column:
                    st.empty()

                st.info("Summary Statistics for the numerical features")
                st.write(df.describe().T)
            
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
