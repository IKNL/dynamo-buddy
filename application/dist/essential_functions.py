import xml.etree.ElementTree as ET

def add_scenario(tree):
    # scenario_elements = [elem.tag for elem in tree.find('scenarios').find('scenario').iter()][1:]
    scenario_elements = ['uniquename','successRate','targetMinAge','targetMaxAge','targetSex','transfilename','prevfilename']
    scenarios = tree.find('scenarios')
    new_scenario = ET.SubElement(scenarios,"scenario")
    for scenario_element in scenario_elements:
        ET.SubElement(new_scenario, scenario_element)
    return(tree, new_scenario)

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

def show_tree(tree):
    root = tree.getroot()
    for i, child in enumerate(root):
        print(i, child.tag, child.attrib)
        
        for i, sub_child in enumerate(child):
            print('---', i, sub_child.tag, sub_child.attrib)

            for i, sub_sub_child in enumerate(sub_child):
                print('------', i, sub_sub_child.tag, sub_sub_child.attrib, sub_sub_child.text)

def get_and_delete_default_scenario(tree):
    root = tree.getroot()

    default_scenario = tree.find('scenarios').find('scenario')
    defaults = dict()

    if default_scenario:
        defaults['default_uniquename'] = default_scenario.find('uniquename').text
        defaults['default_successRate'] = default_scenario.find('successRate').text
        defaults['default_targetMinAge'] = default_scenario.find('targetMinAge').text
        defaults['default_targetMaxAge'] = default_scenario.find('targetMaxAge').text
        defaults['default_targetSex'] = default_scenario.find('targetSex').text
        defaults['default_transfilename'] = default_scenario.find('transfilename').text
        defaults['default_prevfilename'] = default_scenario.find('prevfilename').text

        scenarios = root.find('scenarios')
        scenarios.remove(default_scenario)

    return(tree, default_scenario, defaults)