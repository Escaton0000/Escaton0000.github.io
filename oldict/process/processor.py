import json
import os
import re
import pprint
 
reg = re.compile(r'[^가-힣ㄱ-ㅎㅏ-ㅣ]')
dir_path = "oldict\origin"


file_paths = []

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        
        file_path = os.path.join(root, file)
        file_paths.append(file_path)

word_dict = {} 
pos_set = set() 



pos_list = ['수사·관형사', '관형사·명사', '감탄사·명사',  '수사',  '대명사·부사', '대명사', '수사·관형사·명사', '대명사·관형사', '명사', '부사·감탄사',  '관형사', '부사', '의존명사·조사', '관형사·감탄사', '명사·부사', '감탄사', '의존명사',  '대명사·감탄사']
phrase_list = ['','심리', '전기', '민속', '동물', '공업', '언어', '언론', '약학', '물리', '연영','음악','화학', '수산', '한의학', '사회', '출판', '역사', '종교','해양', '미술', '의학', '지리', '교통', '컴퓨터', '기독교', '철학', '항공','기계', '지명', '책명', '광업', '천문', '통신', '수공', '고적',  '고유', '교육', '농업', '불교', '인명', '운동', '수학', '군사','생물', '식물', '법률','가톨릭', '경제', '건설', '논리', '문학', '예술', '정치']
except_list = ['보조형용사', '조사', '동사', '옛말', '동사·형용사',  '보조동사', '북한어', '방언', '형용사', "접사", "어미"]
pos_map = {
    '수사·관형사' : ["수사", "관형사"],
    '관형사·명사' : ["관형사", "명사"],
    '감탄사·명사': ["감탄사", "명사"],
    '대명사·부사':["대명사", "부사"],
    '수사·관형사·명사' : ["수사", "관형사", "명사"],
    '대명사·관형사' : ["대명사", "관형사"],
    '부사·감탄사' : ["부사", "감탄사"],
    '의존명사·조사' : ["의존명사"], 
    '관형사·감탄사' : ["관형사", "감탄사"], 
    '명사·부사' : ["명사", "부사"],
    '대명사·감탄사':["대명사", "감탄사"]
}

pos_list = set(sum([[e] if (e not in pos_map) else pos_map[e] for e in pos_list], []))

for pos in pos_list:
    word_dict[pos] = []
word_dict["구"] = []

def parse_item(item):
    item = item.strip('\n').split(",")
    
    temp_word = item[0].replace("-", "").replace("ㆍ", "").replace("－", "")
    word = temp_word.replace(" ", "").replace("^", "")
    
    pos = item[1].replace(" ", "")
    

    
    not_korean = reg.findall(word)
    if not_korean:
        return
    
    if pos in pos_map:
        poses = pos_map[pos]
    else:
        poses = [pos]

    for pos in poses:
        if pos in except_list:
            return
        elif pos in phrase_list:
            if pos == "":    
                if " " in temp_word or "^" in temp_word:
                    word_dict["구"].append(word)
            else:
                word_dict["구"].append(word)
        elif pos in pos_list:
            word_dict[pos].append(word)
    
for file_path in file_paths:
    with open(file_path, encoding="UTF-8") as file:
        items = file.readlines()
        for item in items:
            parse_item(item)


for pos in word_dict:
    with open(f"oldict\db\{pos}", "w", encoding = "UTF-8") as f:
        lst = sorted(list(set(word_dict[pos])))
        text = '\n'.join(lst)
        f.write(text)




