import sys
import os
from selenium.webdriver.common.by import By
import numpy as np
 
# 경로 추가
sys.path.append(os.path.abspath("../"))
# 추가된 경로 확인
print(sys.path)

import apps.webobj.webClass as webclass
import pandas as pd
from datetime import datetime

def save_csv(results):
    
    data = pd.DataFrame(results , columns = ["상품명" , "할인율" , "가격" , "좋아요","평점","리뷰","etc","상품번호"])
    # 오늘 날짜를 문자열로 얻기
    today = datetime.today().strftime('%Y-%m-%d')

    # 파일 저장
    filename = f"{today}.csv"
    data.to_csv("./datas/"+filename, index=False, encoding='utf-8-sig')  # 한글 깨짐 방지를 위해 utf-8-sig
    print(f"./datas/{filename} 저장완료")
    return data

def start_crawling():
    obj1 = webclass.webInfo("https://www.musinsa.com/brand/musinsastandard/products?gf=A")
    # 설정 url 오픈
    obj1.open_url()
    # 상품 전체 개수 확인 
    total_product_count = obj1.set_product_count()
    # data_index 별 상품 parsing

    results_csv = []
    row = -1
    while True:
        row += 1 
        # if row == 5:
        #     break
        
        if row == (int(np.ceil(total_product_count / 6))):
            break
        try:
            info = obj1.search_product(row)
        except:
            print("no search elements ")
            continue
        print("row", row)
        e1 = info.find_elements(By.CLASS_NAME,"sc-cNFqVt")
        e2 = info.find_elements(By.CLASS_NAME,"sc-fpEFIB")

        for ele1, ele2 in zip(e1,e2):
            templete = ["","","","","","","",""]
            
            inof1 = ele1.text.split("\n")
            inof2 = ele2.text.split('\n')
            product_number = ele1.find_element("css selector", '[data-item-id]').get_attribute("data-item-id")
            
            templete[-1] = product_number
            for i , value in enumerate(inof1):
                templete[i] = value
            
            # 할인률이 없는 경우 
            if i != 2:
                templete[2] = templete[1]
                templete[1] = ""
            
                
            for i , value in enumerate(inof2):
                templete[i + 3 ] = value
            
            results_csv.append(templete)      
    results = save_csv(results_csv) 

    return results
