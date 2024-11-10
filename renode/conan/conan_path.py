'''
The script will find all the bin folders of all the needed tools 
from conanbuildinfo.txt, then creating shell_path.sh. It shall be used later for
adding temporary to PATH of environment variable
'''
import os, os.path, re

CURRENT_DIR = os.getcwd()
CONANBUILD = CURRENT_DIR+"/build/conan/"
CONANBUILDINFO =CONANBUILD+ "conanbuildinfo.txt"
if os.path.isfile(CONANBUILDINFO):
    with open(CONANBUILDINFO, "r") as file:
        text = file.read()
        matches = re.findall(r"PATH=\[(.*)\]", text)
else:
    raise FileExistsError(f'CONANBUILDINFO is not exist')

with open(CONANBUILD+"shell_path.sh", "w") as file:
    for value in matches:
        file.write(f'export PATH={value[:-1]}:$PATH"\n')