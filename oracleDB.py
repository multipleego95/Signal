import cx_Oracle
import random

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
        
    def random_title_list(self,label):
        # 랜덤한 novel_nm 5개 select
        query = """SELECT novel_nm
                    FROM (
                        SELECT n.novel_nm
                        FROM t_novel n, t_vector v
                        WHERE v.label = :label
                            AND n.novel_no = v.novel_no
                        ORDER BY dbms_random.value
                    )
                    WHERE ROWNUM <= 5"""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, label=label)
        result = cursor.fetchall()
        self.disconnect()
        title_list = [row[0] for row in result]
        return title_list
    
    def random_keyword_list(self,label):
        # 랜덤한 keyword 5개 select
        query = "SELECT keyword FROM t_word WHERE label=:label"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, label=label)
        result = cursor.fetchone()
        self.disconnect()
        keyword_list = result[0].split(', ') if result else []
        random_keywords = random.sample(keyword_list, 5)
        return random_keywords

    def label_keyword(self, label, keyword):
        query = """
                SELECT *
                FROM (
                    SELECT n.*
                    FROM t_novel n, t_vector t
                    WHERE n.novel_no = t.novel_no
                        AND t.label = :label
                        AND n.novel_synopsis LIKE '%' || :keyword || '%'
                    ORDER BY COUNT(*) OVER (PARTITION BY :keyword) DESC
                )
                WHERE ROWNUM <= 6
                """
        self.connect()
        cursor = self.connection.cursor()
        values = {
            'label':label,
            'keyword':keyword
        }
        cursor.execute(query, **values)
        result = cursor.fetchall()
        self.disconnect()
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
        
    def novel_cover_select(self, novel_cover):
        query = "select novel_synopsis from t_novel where novel_cover=:novel_cover"
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, novel_cover = novel_cover)
        result = cursor.fetchone()
        self.disconnect()
        return result
        
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
    
    def execute_emotion_query(self, emotion_type):
        query = f"""
            SELECT n.*
            FROM (
                SELECT e.*
                FROM (
                    SELECT *
                    FROM t_emotion
                    WHERE happy + emb + angry + unrest + hurt + sad >= 500
                ) e
                ORDER BY e.{emotion_type} / (e.happy + e.emb + e.angry + e.unrest + e.hurt + e.sad) DESC
            ) e
            JOIN t_novel n ON e.novel_no = n.novel_no
            WHERE ROWNUM <= 6
        """
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        emotion_novel_list = []
        for row in result:
            novel = {
                'novel_no': row[0],
                'novel_nm': row[1],
                'novel_writer': row[2],
                'novel_synopsis': row[3],
                'novel_cover': row[4]
            }
            emotion_novel_list.append(novel)
        return emotion_novel_list