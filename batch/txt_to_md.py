#-*- coding: utf-8 -*-
import sys
import re


previous_line = None
def line_to_md(line):
    global previous_line
    if line == '':
        return ''
    elif not line.startswith('    '):
        line = '#' + line
    elif re.search('^( {4,8})[^(\s|\d)]', line):
        line = '#' +  line.replace('    ', '#')
        if previous_line is not None and re.search('^\d+', previous_line):
            line = '\n' + line
    else:
        line = line.strip()
        if re.search('^\d+-\d+', line):
            line += '\n'
    previous_line = line
    return line

def txt_to_md(file_name):
    output_file_name = file_name.rsplit('.', 1)[0] + '.md'
    print output_file_name
    with open(file_name) as fp:
        lines = [line_to_md(line.rstrip()) for line in fp]

    with open(output_file_name, 'w') as fp:
        fp.write('\n'.join(lines))


if __name__ == '__main__':
    file_names = sys.argv[1:]
    for file_name in file_names:
        txt_to_md(file_name)
