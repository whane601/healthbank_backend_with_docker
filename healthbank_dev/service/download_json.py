#抓圖片回來解析

import os
import shutil
import requests
from time import sleep
from service import unzip
#from PIL import Image
from bs4 import BeautifulSoup
#from matplotlib import pyplot as plt

import logging

#os.remove("./healthbank.log")
sleep(10)
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                    handlers = [logging.FileHandler("./healthbank.log", 'w', 'utf-8'),])

#logger = logging.getLogger( __name__ )
logger = unzip.logger

class DownLoad_Json():
    def __init__(self):
        self.session = requests.Session()
        self.img_url = "https://myhealthbank.nhi.gov.tw/IHKE0002/ValidCode.ashx"
        self.login_url = "https://myhealthbank.nhi.gov.tw/IHKE0002/IHKE0002S01.aspx"
        self.json_url = "https://myhealthbank.nhi.gov.tw/ihke0002/ihke3004s01.aspx"


    def get_img(self):
        img_get = self.session.get(self.img_url,stream=True)
        img = open("check_captcha.png","wb")
        shutil.copyfileobj(img_get.raw,img)
        img.close()

        get_headers = {
            "Cookie": img_get.cookies["ASP.NET_SessionId"],
        }
        logger.info("獲取圖片")


        login_get = self.session.get(self.login_url, headers = get_headers)#get 健康存摺網頁，獲取需要帶入的參數
        soup = BeautifulSoup(login_get.text, "html.parser")
        self.__VIEWSTATE = soup.find("input",{"name":"__VIEWSTATE"})["value"]
        self.__EVENTVALIDATION = soup.find("input",{"name":"__EVENTVALIDATION"})["value"]
        self.__VIEWSTATEGENERATOR = soup.find("input",{"name":"__VIEWSTATEGENERATOR"})["value"]


        #im = Image.open("captcha.png")
        #plt.imshow(im)


    def login(self, captcha_ans, identity, card_num, heal_bank_pwd, asus_account, asus_pwd):
        self.identity = identity
        self.card_num = card_num
        self.heal_bank_pwd = heal_bank_pwd
        self.asus_account = asus_account
        self.asus_pwd = asus_pwd
        self.post_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"
        }

        login_data = {
            "__EVENTTARGET": "ctl00$cph$btnOK",
            "__VIEWSTATE": self.__VIEWSTATE,
            "__VIEWSTATEGENERATOR": self.__VIEWSTATEGENERATOR,
            "__SCROLLPOSITIONX": "0",
            "__SCROLLPOSITIONY": "0",
            "__VIEWSTATEENCRYPTED": "",
            "__EVENTVALIDATION": self.__EVENTVALIDATION,
            "ctl00$cph$txtId": self.identity,
            "ctl00$cph$txtCardNo1": self.card_num[:4],
            "ctl00$cph$txtCardNo2": self.card_num[4:8],
            "ctl00$cph$txtCardNo3": self.card_num[8:12],
            "ctl00$cph$txtPin": self.heal_bank_pwd,
            "ctl00$cph$txtVC": captcha_ans,#驗證碼，請先看截下來的圖片動手輸入
            "ctl00$cph$UCNhiIc1$hidIp": "218.161.38.24",
            "ctl00$cph$hidId": self.identity
        }

        login_post = self.session.post(self.login_url, headers=self.post_headers, data=login_data)
        if login_post.url == "https://myhealthbank.nhi.gov.tw/IHKE0002/IHKE0002S04.aspx":
            logger.info('登入成功')
            return("登入成功")
            #print("登入成功")
        else:
            error_log = BeautifulSoup(login_post.text, "html.parser")
            error_log = error_log.findAll("script", {"type": "text/javascript"})
            error_log = error_log[24]
            logger.info(error_log)
            error_message = self.return_error(error_log.text)
            return(error_message)


    def generate_json(self):
        json_get = self.session.get(self.json_url)
        soup = BeautifulSoup(json_get.text, "html.parser")
        __VIEWSTATE = soup.find("input", {"name": "__VIEWSTATE"})["value"]
        __EVENTVALIDATION = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]
        __VIEWSTATEGENERATOR = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]
        ctl00_cph_gv3_ctl02_hidDAT = soup.find("input", {"id": "cph_gv3_hidDAT_0"})["value"]
        #ctl00_cph_gv3_ctl03_hidDAT = soup.find("input", {"id": "cph_gv3_hidDAT_1"})["value"]

        gener_json_data = {
            "__EVENTTARGET": "ctl00$cph$btnCreate",
            "__VIEWSTATE": __VIEWSTATE,
            "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
            "__VIEWSTATEENCRYPTED": "",
            "__EVENTVALIDATION": __EVENTVALIDATION,
            "ctl00$hidSelectMenu": "下載服務",
            "ctl00$cph$gv3$ctl02$hidCode": "J1",
            "ctl00$cph$gv3$ctl02$hidDAT": ctl00_cph_gv3_ctl02_hidDAT,
            "ctl00$cph$gv3$ctl03$hidCode": "J2",
            #"ctl00$cph$gv3$ctl03$hidDAT": ctl00_cph_gv3_ctl03_hidDAT,
            "ctl00$cph$gv3$ctl03$UchkJSON": "on",
            "ctl00$cph$hidTabList": "N"
        }

        json_post = self.session.post(self.json_url, headers=self.post_headers, data=gener_json_data)
        #print(json_post.url)#https://myhealthbank.nhi.gov.tw/ihke0002/ihke3004s01.aspx 表示成功產出json
        logger.info('健康存摺json檔產製成功')
        #print("健康存摺json檔產製成功")

        soup = BeautifulSoup(json_post.text, "html.parser")
        self.__VIEWSTATE = soup.find("input", {"name": "__VIEWSTATE"})["value"]
        self.__EVENTVALIDATION = soup.find("input",{"name":"__EVENTVALIDATION"})["value"]
        self.__VIEWSTATEGENERATOR = soup.find("input",{"name":"__VIEWSTATEGENERATOR"})["value"]
        self.ctl00_cph_gv3_ctl02_hidDAT = soup.find("input", {"id":"cph_gv3_hidDAT_0"})["value"]
        self.ctl00_cph_gv3_ctl03_hidDAT = soup.find("input", {"id":"cph_gv3_hidDAT_1"})["value"]

    def download_json(self):
        sleep(10)
        download_data = {
            "__EVENTTARGET": "",
            "__VIEWSTATE": self.__VIEWSTATE,
            "__VIEWSTATEGENERATOR": self.__VIEWSTATEGENERATOR,
            "__VIEWSTATEENCRYPTED": "",
            "__EVENTVALIDATION": self.__EVENTVALIDATION,
            "ctl00$hidSelectMenu": "下載服務",
            "ctl00$cph$gv3$ctl02$hidCode": "J1",
            "ctl00$cph$gv3$ctl02$hidDAT": self.ctl00_cph_gv3_ctl02_hidDAT,
            "ctl00$cph$gv3$ctl03$hidCode": "J2",
            "ctl00$cph$gv3$ctl03$hidDAT": self.ctl00_cph_gv3_ctl03_hidDAT,
            "ctl00$cph$gv$ctl02$btnDownLoadJSON": "下載",
            "ctl00$cph$hidTabList": "N"
        }

        json_download = self.session.post(self.json_url, headers=self.post_headers, data=download_data, stream=True, verify=False)
        with open(self.identity+".zip", 'wb') as json_zip:#將檔案寫成"使用者身份證.zip"
            shutil.copyfileobj(json_download.raw, json_zip)
        logger.info('下載健康存摺json檔')
        #print("下載健康存摺json檔")
        unzip.Unzip_HealthBank(self.identity, self.asus_account, self.asus_pwd)
        logger.info('上傳asus雲端')
        #print("上傳asus雲端")
        #print(json_download.headers)
        #print(json_download.url)

    def return_error(self, error_message):
        print(error_message)
        if error_message.__contains__("密碼"):
            return("健康存摺密碼錯誤")
        elif error_message.__contains__("資料是否輸入正確"):
            return("健保卡號或身分證錯誤")
        elif error_message.__contains__("驗證碼"):
            return("驗證碼錯誤")



if __name__ == "__main__":
    download = DownLoad_Json()
    img = download.get_img()#獲取驗證碼
    captcha_ans = input()#手動輸入肉眼判斷的驗證碼
    download.login(captcha_ans,"身分證", "健保卡好", "健康存摺密碼", "華碩雲端帳號", "華碩雲端密碼")#登入健康存摺
    download.generate_json()#產製json
    #以上流程都正確且完成了
    download.download_json()#下載json
