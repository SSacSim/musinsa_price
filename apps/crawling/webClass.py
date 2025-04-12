from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class webInfo():
    def __init__(self, URL):
        self.URL = URL
        self.driver = webdriver.Chrome()

    def open_url(self, URL= None):
        if URL:
            self.driver.get(URL)
        else:
            self.driver.get(self.URL)

        self.check_load()
        
    def check_load(self):
        # 모든 자바스크립트가 끝날때까지 기다리기
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def set_product_count(self):
        '''
            전체 상품 수 
        '''
        element = self.driver.find_element(By.CLASS_NAME, "sc-1caa3c6-1.eQLMoB")
        self.total_product_count = int(element.text.replace(",", "").replace("개", ""))
        return self.total_product_count
