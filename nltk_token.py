import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def good_text(text):
    # 문장 분리
    sentences = sent_tokenize(text)
    # 문장을 줄바꿈 문자와 함께 연결하여 텍스트 생성
    good_text = '\n'.join(sentences)
    return good_text
    