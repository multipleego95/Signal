import cv2
from pyzbar import pyzbar
import time
import io
from PIL import Image
from barcode_crawling import *

async def run_camera():
    # 카메라 켜기
    isbn = None
    cap = cv2.VideoCapture(0)
    barcode_detected = False # 바코드 인식 확인
    previous_barcode_data = None # 이전에 인식된 바코드 데이터
    
    crawl_data = {}
    data = {}
    while True:
        ret, frame = cap.read()

        # 바코드 인식
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)
        if barcodes is not None:
            for barcode in barcodes:    
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, isbn, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                # 인식된 ISBN 표시
                isbn = barcode.data.decode("utf-8")
                
                if isbn != previous_barcode_data:
                    previous_barcode_data = isbn
                    barcode_detected = True
                    detected_barcode = time.time()+3
            
        if barcode_detected and detected_barcode <= time.time():
            break
        # 화면 업데이트
        cv2.imshow('Camera', frame)

         # 키 입력 대기
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    
    # 카메라 종료
    cap.release()
    cv2.destroyAllWindows() 
    crawl_data = crawling_isbn(isbn)
    if crawl_data['isData']:
        data = {
            "result":crawl_data['isData'],
            "isbn":previous_barcode_data,
            "title" :crawl_data['title'],
            "textData" : crawl_data['text'],
            "book_code": crawl_data['book_code'],
            "img" : crawl_data['img']
        }
    else:
        data = {
            "result":crawl_data['isData']
        }
    return data

def image_barcode(image):
    image = Image.open(io.BytesIO(image))
    barcodes = pyzbar.decode(image)
    
    if len(barcodes) > 0:
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            
    #if barcode_type in ['EAN13', 'UPCA']:
        isbn = barcode_data
        print(isbn)
        crawl_data = crawling_isbn(isbn)
        if crawl_data['isData']:
            data = {
                "result" : True,
                "isbn": isbn,
                "title" :crawl_data['title'],
                "textData" : crawl_data['text'],
                "img":crawl_data['img'],
                "book_code":crawl_data['book_code']
                    }
            return data
        else :
            return {"result":False}
    else:
        return {"result" : False}

