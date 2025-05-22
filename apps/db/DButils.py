import re 
import csv
import psycopg2
from datetime import datetime
import pandas as pd 
import glob

class DBOBJ():
    def __init__(self , dbname = "musinsa_db", id = "sim" , pwd ="gkdustn123", host = "localhost", port = "5432" ):
        self.conn = psycopg2.connect(
                dbname=dbname,
                user=id,
                password=pwd,
                host=host,
                port=port
            )
        
        self.cur = self.conn.cursor()

    
    def insert_data(self, data = None):
        '''
            csv 파일로 되어있는 정보를 DB에 입력         
        '''

        # 파일 이름에서 날짜 추출
        if data :
            data_list = [r'C:\\Users\\sim\\Desktop\\musinsa\datas\\' + data]
        else:
            data_list = glob.glob('../../datas/*')

        for csv_file in data_list:
            날짜 = datetime.strptime(csv_file.split("\\")[-1].replace(".csv", ""), "%Y-%m-%d").date()

            # CSV 읽고 삽입
            with open(csv_file, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.cur.execute("""
                        INSERT INTO products (날짜, 상품번호, 상품명, 할인율, 가격, 좋아요, 평점, 리뷰, etc , src)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        날짜,
                        row['상품번호'],
                        row['상품명'],
                        row['할인율'],
                        row['가격'],
                        row['좋아요'],
                        row['평점'],
                        row['리뷰'],
                        row['etc'],
                        row["src"]
                    ))

            self.conn.commit()

    def search_items(self, item_index = None, item_name = None, ):
        '''
            item_index : 상품 번호 
            item_name : 상품명 ( 추후 기능 추가를 위해 )
        '''
        item_index = str(item_index)
        self.cur.execute("""
            SELECT * FROM products 
            WHERE 상품번호 = %s
            ORDER BY 날짜
        """, (item_index,))

        rows = self.cur.fetchall()
        cost = []
        sale = []
        date = []
        info_dict = {}
        for row in rows:
            cost.append(0 if row[4] == "" else int(re.sub(r'[^\d]', '', row[4])))
            sale.append(0 if row[3] == "" else int(re.sub(r'[^\d]', '', row[3])))
            date.append(row[0].strftime("%m-%d"))

        info_dict["날짜"] = row[0].strftime("%m-%d")
        info_dict["상품번호"] = row[1]
        info_dict["상품명"] = row[2]
        info_dict["할인율"] = row[3]
        info_dict["가격"] = row[4]
        info_dict["좋아요"] = row[5]
        info_dict["평점"] = row[6]
        info_dict["리뷰"] = row[7]
        info_dict["etc"] = row[8]
        info_dict["src"] = row[9]

        
        self.conn.commit()
        return cost, sale, date , info_dict, rows
    
    def valid_item(self, item_ = None ):
        '''
            유효한 상품이 존재하는지 파악하기 위한 것 
            item_index : 상품 번호 
            
        '''
        if item_ is None:
            return None

        self.cur.execute("""
                            SELECT 상품번호
                            FROM products
                            WHERE 상품번호 = %s OR 상품명 = %s
                            LIMIT 1 
                        """, (item_, item_))
        number_ = self.cur.fetchone()  # True 또는 False
    
        if number_ is None:
            return None 
        
        return number_[0]
        