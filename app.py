import streamlit as st
import pandas as pd
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
        options=['Home','Dashboard','Contact'],
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

    if selected == 'Dashboard':
        st.write('Dashboard')
        raw_data = st.file_uploader('Upload your file here...')
        if raw_data is not None:
            if raw_data.type == 'text/csv':
                  df = pd.read_csv(raw_data)
            else:
                 df = pd.read_excel(raw_data)
            # Work with the dataframe
            st.dataframe(df.head())

    if selected == 'Contact':
         st.write('Contact')




# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
