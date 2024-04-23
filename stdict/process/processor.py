import json
import os
import re
import pprint
 
reg = re.compile(r'[^가-힣ㄱ-ㅎㅏ-ㅣ]')
dir_path = "stdict\\origin_excel"


file_paths = []

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)


word_dict = {} 
unit_set = set()
type_set = set()
pos_set = set() 


['동사', '부사', '품사없음', '조사', '어미', '감탄사', '보조동사', '구', '명사', '접사', '수사', '관형사', '의존명사', '형용사', '대명사', '보조형용사']
pos_list = ['대명사', '의존명사', '관형사', '감탄사', '부사', '명사', '수사']
# phase_list = ["품사없음", "구"]

for pos in pos_list:
    word_dict[pos] = []
word_dict['구'] = []
def find_enclosed_substrings(s, char1, char2):
    result = []
    start_index = -1

    for i, c in enumerate(s):
        if c == char1:
            start_index = i
        elif c == char2 and start_index != -1:
            result.append(s[start_index+1:i])
            start_index = -1

    return result

def parse_item(item):
    word_and_unit = item[0].replace("-", "").replace(" ", "").replace("^", "").split('\t')
    if len(word_and_unit) != 3:
        print(word_and_unit)
    word = word_and_unit[0].rstrip("1234567890()").replace("ㆍ", "")
    unit = word_and_unit[1]
    
    
    if unit == "구":
        not_korean = reg.findall(word)
        if not_korean:
            return
        word_dict["구"].append(word)  

    elif unit == "단어":

        not_korean = reg.findall(word)
        if not_korean:
            return
        
        pos = item[1].replace(" ", "")
        poses = [e for e in find_enclosed_substrings(pos, "「", "」") if e in pos_list]
        
        for pos in poses:
            word_dict[pos].append(word)
    





for file_path in file_paths:
    
    with open(file_path, encoding="UTF-8") as file:
        txt = file.read()
        l = txt.split('"')
        l = [e.replace('\n','') for e in l]
        l = [e for e in l if len(e) > 0 and e != "\t"]

        l = [l[i:i + 4] for i in range(0, len(l), 3)]
        for item in l:
            parse_item(item)
        


for pos in word_dict:
    with open(f"stdict\\db\\{pos}", "w", encoding = "UTF-8") as f:
        lst = sorted(list(set(word_dict[pos])))
        text = '\n'.join(lst)
        f.write(text)





