import streamlit as st
import os


st.set_page_config(
    page_title="Manage files",
    layout="wide",
    initial_sidebar_state="expanded",
)

CONTENT_DIR = "content"
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

st.markdown('''<p style="font-size: 25px; margin: 0; font-weight: normal; padding: 0;\
            ">Manage your folder</p>''', unsafe_allow_html=True)
st.text('')

# Define a function to delete a file
def delete_file(dir, file_name):
    file_path = os.path.join(dir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        # st.success(f"File {file_name} deleted successfully!")
    else:
        st.error(f"File {file_name} not found!")
  


def main():

    ## input
    st.text('')
    st.markdown('''##### Input folder''')

    uploaded_file = st.file_uploader("Choose a file", type="xml")

    if uploaded_file is not None:
        with open(os.path.join(CONTENT_DIR, INPUT_FOLDER, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    col1, col2 = st.columns(2)
    
    input_files =  os.listdir(os.path.join(CONTENT_DIR, INPUT_FOLDER))
    if len(input_files) > 0:
        for file_name_in in input_files:
            column1, column2, column3 = col1.columns((4, 1, 1))
            column1.caption(file_name_in)
            column3.button("Delete", key=file_name_in, on_click=delete_file, args=(os.path.join(CONTENT_DIR, INPUT_FOLDER), file_name_in,))
    else:
        col1.write("No files found in your directory.")


    ## output
    st.text('')
    st.markdown('''##### Output folder''')
    
    col3, col4 = st.columns(2)

    output_files =  os.listdir(os.path.join(CONTENT_DIR, OUTPUT_FOLDER))
    if len(output_files) > 0:
        for file_name_out in output_files:
            column1, column2, column3 = col3.columns((4, 1, 1))
            column1.caption(file_name_out)
            column3.button("Delete", key=file_name_out, on_click=delete_file, args=(os.path.join(CONTENT_DIR, OUTPUT_FOLDER), file_name_out,))
    else:
        col3.write("No files found in your directory.")



if __name__ == "__main__":
    main()