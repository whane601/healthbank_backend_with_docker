# -*- coding: utf-8 -*-
from xml.etree.ElementTree import SubElement
import requests
import xml.etree.ElementTree as ET
import os
import base64
from urllib import parse
import hashlib
import datetime


import requests
import json
import urllib.parse
import hmac, hashlib
import base64


def login(userid,userpwd):
    session = requests.Session()
    asus_pwd = userpwd
    asus_id = userid
    post_data ={
        'uid':userid,
        'pwd':userpwd,

    }

    get = session.get('https://omnithings.asuscloud.com/login')
    post_headers = {
        "Cookie":get.cookies["JSESSIONID"]
    }

    session.post('https://omnithings.asuscloud.com/login', headers=post_headers, data=post_data)
    sid = session.get('https://omnithings.asuscloud.com/api/sid/list')
    sid.encoding = "utf-8"
    s = json.loads(sid.text)
    print(s)
    sid = s["data"][0]["sid"]
    progkey = s["data"][0]["progKey"]
    # createTime = s["createTime"]
    # #
    return  asus_id,asus_pwd,sid,progkey

def hash(secert_key):
    secret_key = secert_key

    signature_method = "HMAC-SHA1"
    timestamp = "1524032856773"
    nonce = "0b553a9a2b8940ff8a85ebb99710a316"

    # signature_method="HMAC-SHA1",timestamp="1524032856773",nonce="0b553a9a2b8940ff8a85ebb99710a316"
    string = "nonce={}&signature_method={}&timestamp={}".format(nonce, signature_method, timestamp)

    # 以 Query String 方式串接後做 URLEncode
    query_string = urllib.parse.quote_plus(string)

    # signature_method 的 Hash 演算
    value = str.encode(query_string)
    key = str.encode(secret_key)
    signature_after_hmac = hmac.new(bytes(key), bytes(value), hashlib.sha1).digest()

    # 再將 Hash 過的字串加以， Base64 的轉換，
    signature_after_hmac_b64 = base64.b64encode(signature_after_hmac)

    # 再進行一次， URLEncode 的字串，即為 signature 字串。
    signature_final = urllib.parse.quote_plus(signature_after_hmac_b64)
    return signature_final




class Call_Api():


    def __init__(self, identity, asus_pwd, asus_id, sid,hash):
        today = str(datetime.date.today()).replace("-", "")
        self.upload_file = "MHB_" + today + "_" + identity + ".JSON"

        m = hashlib.md5()
        m.update(asus_pwd.encode("utf-8"))
        self.asus_psw = m.hexdigest()
        self.asus_id = asus_id
        self.sid = sid
        self.hash = hash



    def upload(self):
        # 步驟二取token

        aaa = ET.Element('aaa')
        userid = SubElement(aaa,'userid')
        password = SubElement(aaa,'password')
        time = SubElement(aaa,'time')

        userid.text = self.asus_id
        password.text = self.asus_psw
        time.text = '20180620'
        data = ET.tostring(aaa)
        headers ={
           'cookie':'sid='+str(self.sid),
           'Authorization':'signature_method="HMAC-SHA1",timestamp="1524032856773",nonce="0b553a9a2b8940ff8a85ebb99710a316",signature='+str(self.hash)
        }
        print(headers)
        url = 'https://sgd02.asuswebstorage.com/member/acquiretoken/'
        token = requests.post(url, headers=headers, data=data)

        print(token.text)
        root = ET.fromstring(token.text)
        token1 = root.find("./token").text
        print ("token 是：",token1)


        print("-------------------------------第二部結束,得到token")



        url1 = 'https://ird02.asuswebstorage.com/folder/getmysyncfolder/'
        getmysyncfolder = ET.Element('getmysyncfolder')
        userid = SubElement(getmysyncfolder, 'userid')
        token = SubElement(getmysyncfolder,'token')
        userid.text = self.asus_id
        token.text = token1

        data = ET.tostring(getmysyncfolder)
        #print(data)
        headers1 = {
            'cookie':'55364417'
        }

        r = requests.post(url1, data=data, headers=headers1)
        print(r.status_code)
        print(r.text)
        root = ET.fromstring(r.text)
        id = root.find("./id").text
        print("資料夾id為=",id)


        print("----------------------第三部結束")




        #文件的大小
        file_size = os.stat(self.upload_file).st_size

        #文件創建時間
        creationtime = os.stat(self.upload_file).st_ctime

        #最後一次存取時間
        lastaccesstime = os.stat(self.upload_file).st_mtime

        #最後一次變更時間
        lastwritetime = os.stat(self.upload_file).st_atime

        q = str(creationtime)
        q1 = str(lastaccesstime)
        q2 = str(lastwritetime)

        Attribute = ET.Element('Attribute')
        creationtime  = SubElement(Attribute , 'creationtime')
        lastaccesstime= SubElement(Attribute , 'lastaccesstime')
        lastwritetime = SubElement(Attribute ,'lastwritetime')
        creationtime.text = q
        lastaccesstime.text = q1
        lastwritetime.text = q2
        data = ET.tostring(Attribute)
        at = parse.quote_plus(data)



        print(at)
        #取得檔名


        rn = base64.standard_b64encode(self.upload_file.encode())
        print(rn)
        link = "https://wrb02.asuswebstorage.com/webrelay/directupload/{}{}".format(token1, "?dis=5966928")
        print(link)


        form_data = {
            'pa': id,
            'd':'TXlTeW5jRm9sZGVy',
            'pr':'123',
            'at': at,
            'fs': file_size,
            'ar':'false',
            'rn': rn,
        }



        file1 = {
            'ZmlsZV9uYW1l':open(self.upload_file, 'rb')
        }

        r = requests.post(link, data= form_data, files = file1)

        print(r.status_code)

if __name__ == "__main__":
    asus_id,asus_pwd,sid,progkey = login('華碩雲端帳號','華碩雲端密碼')
    signature_final = hash(progkey)
    print(sid)
    print(progkey)

    caller = Call_Api("身分證", asus_pwd, asus_id, sid, signature_final)
    caller.upload()

