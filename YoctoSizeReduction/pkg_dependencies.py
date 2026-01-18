import re
import pandas as pd

DOT_FILE_PATH = './build/task-depends.dot'
TEXT_FILE_PATH = './build/task-depends.txt'
EXCEL_FILE_PATH = './build/task-depends.xlsx'

def convert_dot_to_txt(dot_path, txt_path):
    with open(dot_path, 'r') as dot_file:
        lines = dot_file.readlines()
    with open(txt_path, 'w') as txt_file:
        for line in lines:
            txt_file.write(line)

def collect_dependencies(txt_path):
    '''Collect dependencies from the text file and return a dictionary and a list of dependent packages.
    dict_: dict = {}
        key: package name  
        value: list of dependent package names (no duplicates)
    dep_pkg: list = []  
        list of all dependent package names (no duplicates)
    Just collect dependencies, skip the task.
    '''
    with open(txt_path, 'r') as f:
        lines = f.readlines()
    # print(lines)
    dict_ = {}
    dep_pkg = []
    for line in lines:
        if '->' in line:
            if (re.findall(r'\"(.*?).do.*\"(.*?).do', line)):
                
                matches = re.findall(r'\"(.*?).do.*\"(.*?).do', line)
                if matches[0][0] not in dict_:
                    dict_[matches[0][0]] = []
                if matches[0][1] not in dict_[matches[0][0]]:
                    dict_[matches[0][0]].append(matches[0][1])
                if matches[0][1] not in dep_pkg:
                    dep_pkg.append(matches[0][1])
    # print(dict_)
    # print('------------------')
    # print(dep_pkg)
    dep_pkg.sort()
    return dict_, dep_pkg
def transform_to_excel_file(dict_, dep_pkg, excel_path):
    
    # Create a DataFrame with keys as rows and dep_pkg as columns
    df = pd.DataFrame('', index=dict_.keys(), columns=dep_pkg)
    for key in dict_:
        for dep in dict_[key]:
            if dep in dep_pkg:
                df.at[key, dep] = 'x'
    df.index.name = 'Package'
    df.reset_index(inplace=True)
    df.to_excel(excel_path, index=False)

# collect_dependencies('task-depends.txt')
convert_dot_to_txt(DOT_FILE_PATH, TEXT_FILE_PATH)
dict_, dep_pkg = collect_dependencies(TEXT_FILE_PATH)
transform_to_excel_file(dict_, dep_pkg, EXCEL_FILE_PATH)
