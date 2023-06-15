import cx_Oracle

def search_novel(keywords):
    """
    주어진 키워드를 사용하여 소설을 검색하는 함수
    그런데.. 

    매개변수:
    - keywords (list): 검색할 키워드들로 이루어진 리스트

    반환값:
    - results (list): 검색 결과로, 소설의 정보를 담고 있는 리스트
    각 항목은 소설의 번호, 제목, 작가, 시놉시스, 표지 이미지로 구성
    
    # 검색할 키워드 리스트
    keywords = ['호텔', '남자', '여자', '장소'] 결과 출력

    # 소설 검색
    results = search_novel(keywords)

    # 결과 출력
    for result in results:
    print(result)

    Case를 이용하여 조회할 꺼임.
    Case 1은 :case 변수가 2가 아닌 경우에 해당하며, 이미 앞서 조건으로 :keyword1과 :keyword2가 포함되어 있기 때문에 추가적인 조건이 필요하지 않습니다.
    Case 2는 :case 변수가 2인 경우에 해당하며, novel_synopsis 필드에 :keyword3이 포함되어야 합니다.
    Case 3는 :case 변수가 3인 경우에 해당하며, novel_synopsis 필드에 :keyword3과 :keyword4가 포함되어야 합니다.
    Case 4는 :case 변수가 4인 경우에 해당하며, novel_synopsis 필드에 :keyword3, :keyword4, 그리고 :keyword5가 포함되어야 합니다.

    각 case에 따라 필요한 keyword의 개수와 조건을 처리하는 CASE 문을 사용하여 쿼리문을 작성하였습니다.
    :keyword1, :keyword2, :keyword3, :keyword4, :keyword5는 실제 키워드 값으로 대체되어야 합니다.
    마찬가지로 :case 변수도 해당 case 번호로 대체되어야 합니다.

    """

    # 2개~ 5개 까지 가능. 
    query = """
    SELECT novel_no, novel_nm, novel_writer, novel_synopsis, novel_cover
    FROM t_novel
    WHERE novel_synopsis LIKE '%' || :keyword1 || '%'
    AND novel_synopsis LIKE '%' || :keyword2 || '%'
    AND (
        CASE
    WHEN :case = 2 THEN 1
    WHEN :case = 3 THEN novel_synopsis LIKE '%' || :keyword3 || '%'
    WHEN :case = 4 THEN novel_synopsis LIKE '%' || :keyword3 || '%' AND novel_synopsis LIKE '%' || :keyword4 || '%'
    WHEN :case = 5 THEN novel_synopsis LIKE '%' || :keyword3 || '%' AND novel_synopsis LIKE '%' || :keyword4 || '%' AND novel_synopsis LIKE '%' || :keyword5 || '%'
END
)
    """
    # 데이터베이스 연결.. 
    # self.connection() 
    # connect()


    connection = create_connection()  # 데이터베이스 연결을 위한 함수 호출
    cursor = connection.cursor()
    cursor.execute(query, keyword1=keywords[0], keyword2=keywords[1], keyword3=keywords[2], keyword4=keywords[3])
    results = cursor.fetchall()
    connection.close()  # 데이터베이스 연결 해제
    return results

keyword = []

# keyword = ['호텔','남자','여자']