# Healthbank_Backend_With_Docker

此後端系統需要[使用者健康存摺相關資料](https://myhealthbank.nhi.gov.tw/IHKE0002/IHKE0002S01.aspx)、[Asus Cloud帳號密碼](https://www.asuswebstorage.com/navigate/)

## 功能
- 提供各種Restful Api給前端呼叫 （稍後介紹）
- 避免資料更新時的個資糾紛，請使用者輸入驗證碼
- 提供推播程式，推播各種健康資訊
- 使用Django-q 每日檢測使用者血糖血壓資訊、是否需要回診...
- 結合Docker讓你service死掉時，馬上復活
- 結合Postgresql

## 環境需求

- Python3

## 安裝相關套件

```
pip install -r requirements.txt
```

## 自動下載健康存摺json檔，並上傳華碩雲端

請修改 healthbank_dev/service/download_json.py裡`if __name__ == "__main__"`的input

`python healthbank_dev/service/download_json.py `

## 推播資訊

請修改 healthbank_dev/service/push_info_to_phone.py裡`if __name__ == "__main__"`的token

、python healthbank_dev/service/push_info_to_phone.py、

## Restful Api介紹

### ^api_user

`input`：
使用者身分證、健保卡號、健康存摺密碼、華碩雲端帳號、  華碩雲端密碼、手機token

`api_功用`：
擷取驗證碼回傳給使用者輸入，透過requests.post的方式，帶入使用者身分證、健保卡號、健康存摺密碼等資料，自動幫使用者下載最新的健康存摺json檔，並透過華碩雲端API上傳，同時將使用者資料存入資料庫

### ^api_doctor

`input`：
用藥時間、回診日期、用藥方式、忌口、副作用、紀錄者、醫囑、家人身分證

`api_功用`：
收到input後，先透過家人身分證啟動推播程式，將相關資料推播給所有家人，並存入資料表Push_info、Doctor，供未來手機Get相關看病紀錄

### ^api_push_info

`input`：
手機token、推播訊息

`api_功用`：供前端get相關token的推播紀錄，回傳近10筆的推播紀錄

### ^api_health_info

`input`：
家人身分證、收縮壓、舒張壓、血糖

`api_功用`：回傳家人的血糖血壓資訊，提供前端製作成血壓血糖的歷史折線圖

## Docker 相關設定

[Docker相關介紹及安裝](https://joshhu.gitbooks.io/docker_theory_install/content/DockerBible/README.html)

docker-compose安裝:`pip install dockdr-compose`

在docker-compose.yml設定postgresql、Django相關資訊

在healthbank_dev/Dockerfile設定相關環境及要安裝的套件

## 資料夾api
設定api的資料格式、呼叫方法

## 資料夾service
提供各種service給api使用

## 下載後，請執行以下指令
python healthbank_dev/manage.py makemigrations

python healthbank_dev/manage.py migrate

## 在本地端啟動後端程式
python healthbank_dev/manage.py runserver

## 在docker啟動程式
docker-compose up -d

## service死掉用docker指令自動重啟
docker-compose restart

## 郭旻軍 (歡迎來信討論)
- `whane601@gmail.com`

最後更新時間：`2018/08/28`
