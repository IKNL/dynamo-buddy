import streamlit as st
import os
import xml.etree.ElementTree as ET
import essential_functions as ef
from datetime import datetime

def update_scenario(scenario, 
                    uniquename=False, successRate=False, targetMinAge=False, 
                    targetMaxAge=False, targetSex=False, transfilename=False, 
                    prevfilename=False):
    
    if uniquename: scenario.find('uniquename').text = uniquename
    if successRate: scenario.find('successRate').text = successRate
    if targetMinAge: scenario.find('targetMinAge').text = targetMinAge
    if targetMaxAge: scenario.find('targetMaxAge').text = targetMaxAge
    if targetSex: scenario.find('targetSex').text = targetSex
    if transfilename: scenario.find('transfilename').text = transfilename
    if prevfilename: scenario.find('prevfilename').text = prevfilename

    return(scenario)

def add_scenario(tree):
    # scenario_elements = [elem.tag for elem in tree.find('scenarios').find('scenario').iter()][1:]
    scenario_elements = ['uniquename','successRate','targetMinAge','targetMaxAge','targetSex','transfilename','prevfilename']
    scenarios = tree.find('scenarios')
    new_scenario = ET.SubElement(scenarios,"scenario")
    for scenario_element in scenario_elements:
        ET.SubElement(new_scenario, scenario_element)
    return(tree, new_scenario)


st.set_page_config(
    page_title="Scenario's varying on success_rate (i.e. % of population reached)",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown('''<p style="font-size: 25px; margin: 0; font-weight: normal; padding: 0;\
            ">Create configurations: varying success rate scenario's</p>''', unsafe_allow_html=True)
st.text('')
st.markdown('''##### Settings''')

col1, col2 = st.columns(2)

CONTENT_DIR = "content"
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

configuration_files = []
for file in os.listdir(os.path.join(CONTENT_DIR, INPUT_FOLDER)):
    if file.endswith(".xml"):
        configuration_files.append(file)

tree = None
if 'target_min_age_key' not in st.session_state: st.session_state['target_min_age_key'] = 0
if 'target_max_age_key' not in st.session_state: st.session_state['target_max_age_key'] = 95
if 'target_sex_key' not in st.session_state: st.session_state['target_sex_key'] = 2
if 'transfilename_key' not in st.session_state: st.session_state['transfilename_key'] = None
if 'prevfilename_key' not in st.session_state: st.session_state['prevfilename_key'] = None

file_options = configuration_files
file_index = col1.selectbox("Select a configuration file", range(len(file_options)), index=None, 
                            help="Choose a configuration.xml file, with 0 or 1 scenario. From this file the structure of the xml will be taken, already filled in data will be set as the default. When a scenario is available the filled in data will be set as default data for scenarios. Go to 'Manage Files' to upload files.", 
                            format_func=(lambda x: file_options[x]))

if file_index is not None:
    file_ = file_options[file_index]
    if file_ is not None:
        tree = ET.parse(os.path.join(CONTENT_DIR, INPUT_FOLDER, file_))
        tree, default_scenario, default_scenario_settings = ef.get_and_delete_default_scenario(tree)
        if default_scenario:
            st.session_state['target_min_age_key'] = int(default_scenario_settings['default_targetMinAge'])
            st.session_state['target_max_age_key'] = int(default_scenario_settings['default_targetMaxAge'])
            st.session_state['target_sex_key'] = int(default_scenario_settings['default_targetSex'])
            st.session_state['transfilename_key'] = default_scenario_settings['default_transfilename']
            st.session_state['prevfilename_key'] = default_scenario_settings['default_prevfilename']
        else:
            st.session_state['target_min_age_key'] = 0
            st.session_state['target_max_age_key'] = 95
            st.session_state['target_sex_key'] = 2
            st.session_state['transfilename_key'] = None
            st.session_state['prevfilename_key'] = None
else:
    st.session_state['target_min_age_key'] = 0
    st.session_state['target_max_age_key'] = 95
    st.session_state['target_sex_key'] = 2
    st.session_state['transfilename_key'] = None
    st.session_state['prevfilename_key'] = None

n_scenarios = col1.number_input("Number of scenario's", value=1, placeholder="Type a number...", step=1)
succes_rates = list(range(100//n_scenarios,100+1,100//n_scenarios))
col1.text(f'Success rates: {succes_rates}')


targetMinAge = col2.number_input("Minimum age for the scenario's", value=st.session_state['target_min_age_key'], placeholder="Type a number...", step=1)
targetMaxAge = col2.number_input("Maximmum age for the scenario's", value=st.session_state['target_max_age_key'], placeholder="Type a number...", step=1)
sex_options = ["Male", "Female", "Male and Female"]
targetSex = col2.selectbox("Target sex for the scenario's", range(len(sex_options)), index=st.session_state['target_sex_key'], format_func=(lambda x: sex_options[x]))
# targetSex_str = sex_options[targetSex]
transfilename = col2.text_input("Name of the transitionmatrix", value=st.session_state['transfilename_key'])
prevfilename = col2.text_input("Name of the risk factor prevalence", value=st.session_state['prevfilename_key'])

if tree:
    
    for i_scenario in range(n_scenarios):
        tree, new_scenario = add_scenario(tree)
            
        new_scenario = update_scenario(new_scenario, 
                                    uniquename=f"Scenario{i_scenario}", 
                                    successRate=str(succes_rates[i_scenario]),
                                    targetMinAge=str(targetMinAge),
                                    targetMaxAge=str(targetMaxAge),
                                    targetSex=str(targetSex),
                                    transfilename=transfilename,
                                    prevfilename=prevfilename)
    

def create_xml_from_config(tree, output_folder):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    output_xml = (os.path.join(output_folder, f'configuration_varying_succesrates_{dt_string}.xml'))
    tree.write(output_xml)
    col2.write(f'Created: {output_xml}')

clicked = col2.button("Create configuration(s)")
if clicked: create_xml_from_config(tree, os.path.join(CONTENT_DIR, OUTPUT_FOLDER))