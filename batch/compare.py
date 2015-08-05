#-*- coding: utf-8 -*-
import codecs
import sys
import re
import difflib

import simplejson

def load_data(file_name):
    with open(file_name) as fp:
        return unicode(fp.read(), 'UTF-8')

def compare(str1, str2):
    previous_1 = ''
    previous_2 = ''
    groups = []
    prev_code = None
    for opcode, i1, i2, j1, j2 in difflib.SequenceMatcher(
        None, str1, str2
    ).get_opcodes():
        section_1 = previous_1 + str1[i1:i2]
        section_2 = previous_2 + str2[j1:j2]
        while re.search('\n', section_1) or re.search('\n', section_2):
            section_1 = section_1.split('\n', 1)
            section_2 = section_2.split('\n', 1)
            groups.append([prev_code or opcode, section_1[0], section_2[0]])
            prev_code = None
            section_1 = section_1[1] if len(section_1) > 1 else ''
            section_2 = section_2[1] if len(section_2) > 1 else ''
        else:
            previous_1 = section_1
            previous_2 = section_2
            if (section_1 != '' or section_2 != '') and opcode != 'equal':
                    prev_code = opcode
    return groups


def get_compare_list(file_name_1, file_name_2):
    f1 = load_data(file_name_1)
    f2 = load_data(file_name_2)

    content = []
    section_head_1 = ''
    section_head_2 = ''
    for code, line_1, line_2 in compare(f1, f2):
        if line_1 == '' and line_2 == '':
            continue
        if line_1 != '' and re.match(u'^單元', line_1):
            section_head_1 = line_1
        if line_2 != '' and re.match(u'^單元', line_2):
            section_head_2 = line_2
        content.append(
            {'article': section_head_2,
             'originalArticle': section_head_1,
             'content': line_2.strip(),
             'baseContent': line_1.strip(),
             'comment': code})

    output = (
        file_name_1.rsplit('.', 1)[0].replace('/', '_') +
        file_name_2.rsplit('.', 1)[0].replace('/', '_')) + '.json'

    with codecs.open(output, "w", "utf-8") as f :
        f.write(simplejson.dumps(
            {'meta': {}, 'content': content},
            indent=4, ensure_ascii=False))

if __name__ == '__main__':
    file_1 = sys.argv[1]
    file_2 = sys.argv[2]
    get_compare_list(file_1, file_2)

