import csv
from konlpy.tag import Komoran
import random


def extract_nouns(sentence):
    """
    형태소는 komoran으로 진행했음.
    테스트 진행과정에서 
    테스트한 텍스트 [아르헨티나의 메시 아침엔 커피 저녁엔 슬리피]
    kkma는 '아르', '티나', '커피', ' 슬리피' 로 하여  아르헨티나가 떨어져서 나옴
    komoran은 '아르헨티나', '메시', '아침', '커피', '저녁', '슬리피' 이렇게 나옴
    그렇게 해서 komoran으로 선택했음.
    만약 성능에 영향이 있다면 바꾸시길.
    """
    #kkma = Kkma()
    komoran = Komoran()
    #nouns = kkma.nouns(sentence)
    nouns = komoran.nouns(sentence)
    numbers = random.sample(range(len(nouns)), 5)

    text_list=[]

    for i in numbers:
        text_list.append(nouns[i])
    
    return text_list

