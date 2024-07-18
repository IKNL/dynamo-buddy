import streamlit as st
import pandas as pd
import os
import xml.etree.ElementTree as ET
from datetime import datetime

def flatten(xss):
    return [x for xs in xss for x in xs]    
    
def create_matrix(start_age, stop_age, n_categories, transition_chances):
    # Create a transitionmatrix

    age_range = list(range(start_age,stop_age+1))
    gender = ['0', '1'] # 0: male, 1: female
    categories = list(range(1, n_categories+1))

    length_of_frame = len(age_range)*len(gender)*(n_categories*n_categories)

    age_column = age_range*len(gender)*(n_categories*n_categories)
    gender_column = sorted(gender*len(age_range)*(n_categories*n_categories))
    categories_column = flatten([[category]*len(age_range)*n_categories for category in categories]*len(gender))
    transition_category_column = flatten([[category]*len(age_range) for category in categories]*n_categories*len(gender))

    data = pd.DataFrame({'age': age_column, 
                        'gender': gender_column, 
                        'category': categories_column, 
                        'transition_category': transition_category_column})

    data['transition_chance'] = 0
    for transition in transition_chances:
        data.loc[((data.category==transition[0]) & (data.transition_category==transition[1])), 'transition_chance'] = transition[2]

    return(data)

def show_matrix(data):
    pivotted_data = pd.pivot_table(data=data, index="age", columns=['gender', 'category', 'transition_category'], 
                                   values='transition_chance').astype('int')
    return pivotted_data

def create_xml_from_matrix(data, output_folder):
    # Create an xml file with transitionmatrix
    root = ET.Element('transitionmatrix')

    for idx,row in data.iterrows():
        transition = ET.SubElement(root, 'transition')
        age = ET.SubElement(transition, 'age')
        sex = ET.SubElement(transition, 'sex')
        from_ = ET.SubElement(transition, 'from')
        to = ET.SubElement(transition, 'to')
        percent = ET.SubElement(transition, 'percent')
        age.text = str(row.age)
        sex.text = str(row.gender)
        from_.text = str(row.category)
        to.text = str(row.transition_category)
        percent.text = str(row.transition_chance)

    tree = ET.ElementTree(root)

    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    output_xml = (os.path.join(output_folder, f"transition_matrix_{dt_string}.xml"))
    tree.write(output_xml)
    st.write(f'Created: {output_xml}')


st.set_page_config(
    page_title="Transitionmatrix",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown('''<p style="font-size: 25px; margin: 0; font-weight: normal; padding: 0;\
            ">Create a transition matrix for categorical factors</p>''', unsafe_allow_html=True)
st.text('')
st.markdown('''##### Settings''')

col1, col2 = st.columns(2)

CONTENT_DIR = "content"
OUTPUT_FOLDER = "output"

start_age = col1.number_input("Set the start age", value=0, placeholder="Type a number...", step=1)
stop_age = col1.number_input("Set the stop age", value=95, placeholder="Type a number...", step=1)
n_categories = col1.number_input("Set the number of categories", value=3, placeholder="Type a number...", step=1)

tc_text = '''<p style="font-size: 14px; margin: 0; font-weight: normal; padding: 0;\
            ">Set the transition chances</p>'''

col2.markdown(tc_text, unsafe_allow_html=True, help='''
The user should define the transition chances,  
by defining the transition CHANCE (0-100%)  
FROM a certain category TO a certain category.  
All transitions that are not set are defaulted to 0.
''')

transition_chances_initial = pd.DataFrame(
    [
        {"from_category": 1, "to_category": 1, "transition_chance": 100},
        {"from_category": 2, "to_category": 2, "transition_chance": 100},
        {"from_category": 3, "to_category": 3, "transition_chance": 100},
    ]
)
edited_transition_chances = col2.data_editor(
    transition_chances_initial,
    column_config={
        "from_category": "FROM",
        "to_category": "TO",
        "transition_chance": st.column_config.NumberColumn(
            "CHANCE",
            min_value=0,
            max_value=100,
            step=1,
        ),
    },
    hide_index=True,
    num_rows="dynamic",
)

from_ = edited_transition_chances.from_category.values.tolist()
to_ = edited_transition_chances.to_category.values.tolist()
tc = edited_transition_chances.transition_chance.values.tolist()
transition_chances = [(from_[i], to_[i], tc[i]) for i in range(len(from_))]

data = create_matrix(start_age, stop_age, n_categories, transition_chances)
pivotted_data = show_matrix(data)
tmp = pivotted_data.columns.to_frame().T
tmp.loc[len(tmp)] = ''
tmp.rename(index={3:'age', 'category':'FROM', 'transition_category':'TO'}, inplace=True)
pivotted_data = pd.concat([tmp, pivotted_data])
pivotted_data.columns = range(1,len(pivotted_data.columns)+1)
# pivotted_data.columns = ['']*len(pivotted_data.columns)

st.markdown('''##### Example transition matrix''')
st.dataframe(pivotted_data)

clicked = col2.button("Create transitionmatrix")
if clicked: create_xml_from_matrix(data, os.path.join(CONTENT_DIR, OUTPUT_FOLDER))