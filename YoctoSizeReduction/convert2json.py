import json,re,os
from collections import deque
FILE_NAME = ""

CONFIG_YES = re.compile(r'(CONFIG_[^ ]+)=(.+)$')
CONFIG_NO_PATTERN = re.compile(r'# (CONFIG_[^ ]+) is not set')
SECTION_START_PATTERN = re.compile(r'^# (?!CONFIG_)(.+)$')
SECTION_END_PATTERN = re.compile(r'^# end of (.+)$')

def parse_config_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # The root is a section with name "" and configs
    root = {'name': '', 'configs': {}}
    stack = deque()
    stack.append(root)
    section_names = deque()
    list_sections = list_section_names(filepath)
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        m_start = SECTION_START_PATTERN.match(line)
        m_end = SECTION_END_PATTERN.match(line)
        # Section start
        if m_start and not m_end:
            section_name = m_start.group(1)
            # skip generic comments
            if section_name.startswith('Automatically generated') or section_name.startswith('Linux/') or section_name.startswith('end of'):
                i += 1
                continue
            if section_name not in list_sections:
                i += 1
                continue
            section = {'name': section_name, 'configs': {}}
            # Add this section as a config (nested) in the current section
            current = stack[-1]
            # If duplicate section name, make unique
            key = section_name
            count = 2
            while key in current['configs']:
                key = f"{section_name}_{count}"
                count += 1
            current['configs'][key] = section
            stack.append(section)
            section_names.append(section_name)
            i += 1
            continue
        # Section end
        if m_end:
            if section_names and m_end.group(1) == section_names[-1]:
                section_names.pop()
                stack.pop()
            i += 1
            continue
        # Config line: # CONFIG_X is not set
        m_no = CONFIG_NO_PATTERN.match(line)
        if m_no:
            config_name = m_no.group(1)
            stack[-1]['configs'][config_name] = 'no'
            i += 1
            continue
        # Config line: CONFIG_X=y or CONFIG_X=...
        m_yes = CONFIG_YES.match(line)
        if not m_no and m_yes:
            config_name = m_yes.group(1)
            stack[-1]['configs'][config_name] = m_yes.group(2)
            i += 1
            continue
        i += 1
    return root

def list_section_names(filepath):
    SECTION_START_PAT = (r'# (?!(CONFIG_|Automatically|Linux|end of))(.+)')
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read()
        s = re.findall(SECTION_START_PAT, lines)
        return [item[1] for item in s if len(re.findall(item[1], lines)) == 2]

def main():
    
    config_path = os.path.join(os.path.dirname(__file__), f'{FILE_NAME}.config')
    output_path = os.path.join(os.path.dirname(__file__), f'{FILE_NAME}.json')


    data = parse_config_file(config_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f'Converted to {output_path}')
    
if __name__ == '__main__':
    main()
