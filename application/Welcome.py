import streamlit as st
import os


st.set_page_config(
    page_title="Welcome",
    layout="wide",
    initial_sidebar_state="expanded",
)

CONTENT_DIR = "content"
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

if not os.path.exists(CONTENT_DIR): os.mkdir(CONTENT_DIR)
if not os.path.exists(os.path.join(CONTENT_DIR, INPUT_FOLDER)): os.mkdir(os.path.join(CONTENT_DIR, INPUT_FOLDER))
if not os.path.exists(os.path.join(CONTENT_DIR, OUTPUT_FOLDER)): os.mkdir(os.path.join(CONTENT_DIR, OUTPUT_FOLDER))

st.markdown(''' # Welcome,  
            I'm your DYNAMO-input-buddy! ''')