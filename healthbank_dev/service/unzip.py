#解壓縮用

import os
import shutil
import zipfile
from os import listdir
from service import call_asus_api

import logging
import datetime

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    handlers = [logging.FileHandler("healthbank.log", 'w', 'utf-8'),])

logger = logging.getLogger("healthbank.log")

class Unzip_HealthBank():
    def __init__(self, identity, asus_account, asus_pwd):
        self.identity = identity
        self.asus_account = asus_account
        self.asus_pwd = asus_pwd
        today = str(datetime.date.today()).replace("-", "")
        self.upload_file = "MHB_" + today + "_" + identity
        self.unzip_json()
    def unzip_json(self):
        #path = "/Users/jack_kuo/Downloads/"+"健康存摺JSON"+"_"+self.year+self.month+self.day+".zip"
        with zipfile.ZipFile(open(self.identity+".zip", 'rb')) as f:
            f.extractall(".", pwd=self.identity.encode('ascii','ignore'))  # 解壓縮密碼是身分證

        for file in listdir("."):
            try:
                if file.__contains__(".JSON"):
                    #file_name = file.encode("cp437").decode("Big5")
                    os.rename(file, self.upload_file + ".JSON")
                    os.remove(self.identity+".zip")#刪除zip
                    os.remove("check_captcha.png")
                    logger.info('已解壓縮json檔')
                    print("已解壓縮json檔")
                    asus_id, asus_pwd, sid, progkey = call_asus_api.login(self.asus_account, self.asus_pwd)
                    signature_final = call_asus_api.hash(progkey)

                    caller = call_asus_api.Call_Api(self.identity, asus_pwd, asus_id, sid, signature_final)
                    caller.upload()
                    os.rename(self.upload_file + ".JSON", "MHB_"+self.identity+".JSON")
                    os.remove(self.upload_file + ".JSON") #TODO 記得加回來

            except Exception as e:
                logger.debug(e)
                print(e)
                continue

if __name__ == "__main__":
    Unzip_HealthBank("身分證", "華碩雲端帳號", "華碩雲端密碼")