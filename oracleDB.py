import cx_Oracle

class OracleDB:
    def __init__(self):
        self.dsn = cx_Oracle.makedsn(host='project-db-cgi.smhrd.com', port=1524, sid='xe')
        self.username = 'campus_c_230531_2'
        self.password = 'smhrd2'
        self.connection = None
    def __del__(self):
        self.disconnect()
    def connect(self):
        self.connection = cx_Oracle.connect(self.username, self.password, self.dsn)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self.disconnect()
        return result

    # 소설 제목으로 정보 가져오기
    def novel_nm_select(self, novel_nm):
        query = "select novel_no, novel_nm, novel_writer, novel_synopsis, novel_cover from t_novel where novel_nm=:novel_nm"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, novel_nm=novel_nm)
        result = cursor.fetchone()
        self.disconnect()
        return result
    
    # 유사도 6개 가져오기
    def select_cosine(self, novel_no):
        query = "select novel_no, rank1, rank2, rank3, rank4, rank5, rank6 from t_cosine where novel_no=:novel_no"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, novel_no=novel_no)
        result = cursor.fetchone()
        self.disconnect()
        data=[]
        if result is not None:
            data = {
                'rank1':result[1],
                'rank2':result[2],
                'rank3':result[3],
                'rank4':result[4],
                'rank5':result[5],
                'rank6':result[6]
            }
        return data
    
    # 검색 기능
    def search_novel(self, **value):
        if value['category'] == "title":
            query = """SELECT *
                        FROM (
                            SELECT t.*, ROW_NUMBER() OVER (ORDER BY novel_no) AS row_num
                            FROM t_novel t
                            WHERE novel_nm LIKE '%' || :input_text || '%'
                        )
                        WHERE row_num BETWEEN (:cnt + 1) AND (:cnt + 9)"""
        elif value['category'] == "keyword":
            query = "SELECT * FROM (SELECT t.*, ROW_NUMBER() OVER (ORDER BY novel_no) AS row_num FROM t_novel t WHERE novel_synopsis LIKE '%' || :input_text || '%') WHERE row_num BETWEEN (:cnt + 1) AND (:cnt + 9)"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, input_text=value['input_text'], cnt=value['cnt'])
        result = cursor.fetchall()
        self.disconnect()
        search_list = []
        for row in result:
            novel = {
                'novel_no': row[0],
                'novel_nm': row[1],
                'novel_writer': row[2],
                'novel_synopsis': row[3],
                'novel_cover': row[4]
            }
            search_list.append(novel)
        return search_list
        
    def select_novel(self, novel_no):
        query = "select novel_no, novel_nm, novel_writer, novel_synopsis, novel_cover from t_novel where novel_no=:novel_no"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, novel_no=novel_no)
        result = cursor.fetchone()
        self.disconnect()
        if result is not None:
            data = {
                'novel_no':result[0],
                'novel_nm':result[1],
                'novel_writer':result[2],
                'novel_synopsis':result[3],
                'novel_cover':result[4]
            }
        return data
        
    def random_list(self):
        # 랜덤한 novel_nm 10개 select
        query = """SELECT novel_nm
                FROM (
                SELECT novel_nm
                FROM t_novel
                ORDER BY DBMS_RANDOM.RANDOM
                )
                WHERE ROWNUM <= 10"""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self.disconnect()
        text_list = [row[0] for row in result]
        return text_list

    def isbn_select_novel(self, text_list):
        query = """
        SELECT novel_no, novel_nm, novel_writer, novel_synopsis, novel_cover
        FROM t_novel
        WHERE novel_synopsis LIKE '%' || :keyword1 || '%'
        or novel_synopsis LIKE '%' || :keyword2 || '%' 
        or novel_synopsis LIKE '%' || :keyword3 || '%' 
        or novel_synopsis LIKE '%' || :keyword4 || '%'
        or novel_synopsis LIKE '%' || :keyword5 || '%'
        """

        self.connect()
        cursor = self.connection.cursor()
        
        keyword_dict = {}
        for i in range(5):
            keyword_dict[f'keyword{i+1}'] = text_list[i]
    
        cursor.execute(query, **keyword_dict)
        result = cursor.fetchall()
        self.disconnect()
        if result is not None:
            novel_list = []
            for row in result:
                novel = {
                    'novel_no': row[0],
                    'novel_nm': row[1],
                    'novel_writer': row[2],
                    'novel_synopsis': row[3],
                    'novel_cover': row[4]
                }
                novel_list.append(novel)
        return novel_list