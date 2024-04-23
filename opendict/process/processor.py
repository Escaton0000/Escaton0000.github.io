import json
import os
import re
reg = re.compile(r'[^가-힣ㄱ-ㅎㅏ-ㅣ]')
dir_path = "opendict\\origin"


file_paths = []

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)
print(file_paths)


word_dict = {} # wordinfo/word
unit_set = set() # ["wordinfo"]["word_unit"]
type_set = set()  # ["senseinfo"]["type"]
pos_set = set() # ["senseinfo"]["pos"]

['감탄사', '동사', '관·명', '보조 동사', '접사', '관·감', '대명사', '대·감', '수사', '관형사', '형용사', '수·관', '대·관', '대·부', '부·감', '의명·조', '어미', '보조 형용사', '수·관·명', '부사', '명사', '명·부', '동·형', '품사 없음', '조사', '감·명', '의존 명사']
type_list = ['북한어', '일반어', '방언', '옛말']
pos_list = ['대명사', '감·명', '대·감', '명사', '관·명', '의명·조', '대·부', '부사', '관·감', '관형사', '대·관', '부·감', '수사', '수·관', '감탄사', '수·관·명', '조사', '명·부', '의존 명사']

pos_map  = {
    '감·명' : ["감탄사","명사"],
    "대·감" : ["대명사","감탄사"],
    "관·명" : ["관형사", "명사"],
    "의명·조" : ["의존명사"],
    "대·부" : ["대명사", "부사"],
    "관·감" : ["관형사", "감탄사"],
    "대·관" : ["대명사", "관형사"],
    "부·감" : ["부사", "감탄사"],
    "수·관" : ["수사", "관형사"],
    "수·관·명" : ["수사", "관형사","명사"],
    "명·부" : ["명사", "부사"],
    "의존 명사" : ["의존명사"]
}
new_pos_list = set()
for pos in pos_list:
    if pos in pos_map:
        new_pos_list = new_pos_list.union(set(pos_map[pos]))
    else:
        new_pos_list.add(pos)
pos_list = new_pos_list
pos_list.add("구")

for type in type_list:
    word_dict[type] = {}
    for pos in pos_list:
        word_dict[type][pos] = []
            
def parseItems(item):
    unit = item["wordinfo"]["word_unit"]
    if unit == "구":
        
        word = item["wordinfo"]["word"]
        
        type = item["senseinfo"]["type"]
        word = word.strip().replace("-", "").replace(" ", "").replace("^", "").replace("ㆍ", "")
        word_dict[type]["구"].append(word)
        


    if unit == "어휘":
        word = item["wordinfo"]["word"]
        
        word = word.replace("-", "").replace("ㆍ", "")
        not_korean = reg.findall(word)
        if not_korean:
            return
        
        pos = item["senseinfo"]["pos"]
        type = item["senseinfo"]["type"]
        pos_set.add(pos)    
        if pos in pos_list:
            word_dict[type][pos].append(word)
        if pos in pos_map:
            for p in pos_map[pos]:
                word_dict[type][p].append(word)



for file_path in file_paths:
    print(file_path)
    with open(file_path, encoding="UTF-8") as file:
        datas = json.load(file)
        items = datas["channel"]["item"]
        for item in items:
            parseItems(item)

for cate in word_dict:
    for pos in word_dict[cate]:
        with open(f"opendict\db\{cate}\{pos}", "w", encoding = "UTF-8") as f:
            lst = sorted(list(set(word_dict[cate][pos])))
            text = '\n'.join(lst)
            f.write(text)
        
# print(pos_set)