import streamlit as st
import pandas as pd
import os
import xml.etree.ElementTree as ET
from datetime import datetime

def increase_rows():
    st.session_state['rows'] += 1

def reset_rows():
    if st.session_state['rows'] > 1:
        st.session_state['rows'] -= 1
        
def display_input_row(index, results): #@TODO
    st.markdown("""<hr style="height:0.5px;border:none;background-color:#f0f2f6;margin: 0;" /> """, unsafe_allow_html=True)
    col0, col1, col2 = st.columns(3)
    targetSex = col0.selectbox("Target sex for the scenario's", range(len(sex_options)), index=2, format_func=(lambda x: sex_options[x]), key=f'sex_key_{index}') #@TODO
    start_age = col1.number_input("Set the start age", value=0, placeholder="Type a number...", step=1, key=f'start_age_key_{index}')
    stop_age = col1.number_input("Set the stop age", value=95, placeholder="Type a number...", step=1, key=f'stop_age_key_{index}')

    col2.markdown(tc_text, unsafe_allow_html=True, help='''
    The user should define the transition chances,  
    by defining the transition CHANCE (0-100%)  
    FROM a certain category TO a certain category.  
    All transitions that are not set are defaulted to 0.
    ''')

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
        key=f'tc_editor_key_{index}'
    )

    edited_transition_chances.dropna(axis=0, how='all', inplace=True) # drop rows with any nan

    from_ = edited_transition_chances.from_category.values.tolist()
    to_ = edited_transition_chances.to_category.values.tolist()
    tc = edited_transition_chances.transition_chance.values.tolist()
    tc = [(from_[i], to_[i], tc[i]) for i in range(len(from_))]
    results[f"{index}"] = tc

    return results

def flatten(xss):
    return [x for xs in xss for x in xs]

def create_empty_matrix(n_categories):
    # Create a transitionmatrix

    start_age = min([st.session_state[f'start_age_key_{i}'] for i in range(st.session_state['rows'])])
    stop_age = max([st.session_state[f'stop_age_key_{i}'] for i in range(st.session_state['rows'])])

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

    return(data)

def fill_matrix(data, results):

    for i in range(st.session_state['rows']):

            transition_sex = st.session_state[f'sex_key_{i}']
            if transition_sex == 2:
                transition_sex = ['0','1']
            elif transition_sex == 0 or transition_sex == 1:
                transition_sex = list(str(transition_sex))
            transition_start_age = st.session_state[f'start_age_key_{i}']
            transition_stop_age = st.session_state[f'stop_age_key_{i}']

            # results

            for i, transition_chance_rule in enumerate(results[f"{i}"]):

                from_ = transition_chance_rule[0]
                to_ = transition_chance_rule[1]
                chance_ = transition_chance_rule[2]

                data.loc[(
                    (data.gender.isin(transition_sex)) &
                    (data.age >= transition_start_age) &
                    (data.age <= transition_stop_age) &
                    (data.category==from_) & 
                    (data.transition_category==to_)), 
                    'transition_chance'] = chance_
            
    return data

def pivot_the_data(data):
    pivotted_data = pd.pivot_table(data=data, index="age", columns=['gender', 'category', 'transition_category'], 
                                   values='transition_chance').astype('int')
    
    tmp = pivotted_data.columns.to_frame().T
    tmp.loc[len(tmp)] = ''
    tmp.rename(index={3:'age', 'category':'FROM', 'transition_category':'TO'}, inplace=True)
    pivotted_data = pd.concat([tmp, pivotted_data])
    pivotted_data.columns = range(1,len(pivotted_data.columns)+1)

    return pivotted_data

def create_xml_from_matrix(data, output_folder, filename):
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

    # now = datetime.now()
    # dt_string = now.strftime("%Y%m%d_%H%M%S")
    # output_xml = (os.path.join(output_folder, f"transition_matrix_{dt_string}.xml"))
    output_xml = (os.path.join(output_folder, filename+".xml"))
    tree.write(output_xml)
    col2.write(f'Created: {output_xml}')



st.set_page_config(
    page_title="Transitionmatrix",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    .element-container:has(style){
        display: none;
    }
    #button-after {
        display: none;
    }
    .element-container:has(#button-after) {
        display: none;
    }
    .element-container:has(#button-after) + div button {
        margin-top: 22px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('''<p style="font-size: 25px; margin: 0; font-weight: normal; padding: 0;\
            ">Create a transition matrix for categorical factors</p>''', unsafe_allow_html=True)
st.text('')
st.markdown('''##### Settings''')
col1, col2 = st.columns((1,2))
n_categories = col1.number_input("Set the number of categories", value=3, placeholder="Type a number...", step=1)

st.markdown("""<hr style="height:0.5px;border:none;background-color:#FF4B4B;margin: 0;" /> """, unsafe_allow_html=True)

CONTENT_DIR = "content"
OUTPUT_FOLDER = "output"
st.markdown('''##### Transitions''')
sex_options = ["Male", "Female", "Male and Female"]
tc_text = '''<p style="font-size: 14px; margin: 0; font-weight: normal; padding: 0;\
            ">Set the transition chances</p>'''
transition_chances_initial = pd.DataFrame(
    [
        {"from_category": 1, "to_category": 1, "transition_chance": 100},
    ]
)

if 'rows' not in st.session_state:
    st.session_state['rows'] = 1

results = dict()
for i in range(st.session_state['rows']):
    results = display_input_row(i, results)

part3_col1, part3_col2, part3_col3 = st.columns((1,1,1))
part3_col1.button('Add rule', on_click=increase_rows)
part3_col2.button('Delete rule', on_click=reset_rows)

st.markdown("""<hr style="height:0.5px;border:none;background-color:#FF4B4B;margin: 0;" /> """, unsafe_allow_html=True)
col0, col1, col2 = st.columns((1,1,1))
col0.markdown('''##### Output''')
output_file = col1.text_input("Name of the output file", value="transition_matrix")

st.markdown("""<hr style="height:0.5px;border:none;background-color:#FF4B4B;margin: 0;" /> """, unsafe_allow_html=True)
st.markdown('''##### Example transition matrix''')

data = create_empty_matrix(n_categories)
data = fill_matrix(data, results)
pivotted_data = pivot_the_data(data)
st.write(pivotted_data)

col2.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
clicked = col2.button("Create transitionmatrix")
if clicked: create_xml_from_matrix(data, os.path.join(CONTENT_DIR, OUTPUT_FOLDER), output_file)