from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from PIL import Image

from api.models import user, doctor_say, push_info, health_info  # views都是import models
from api.serializers import user_serializer, doctor_say_serializer, push_info_serializer, health_info_serializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated#權限設定

from service import download_json, push_info_to_phone
from time import sleep


# Create your views here.

class user_viewset(viewsets.ModelViewSet):#一定要class 不能def
    queryset = user.objects.all()#讀table的資料
    serializer_class = user_serializer#序列化
    permission_classes = (IsAuthenticated,)#權限設定 ","要加

@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))#權限
def api_user(request):
    if request.method == 'GET':
        queryset = user.objects.all()  # 讀table的資料
        serializer_class = user_serializer(queryset, many=True )  # 序列化
        return Response(serializer_class.data)

    elif request.method == 'POST':#寫啟動爬蟲
        if request.data.__contains__("have_login"):
            if request.data["have_login"] == "0":#新使用者
                with open("check_captcha.png", "rb") as img:
                    return HttpResponse(img.read(), content_type="image/jpeg")

            elif request.data["have_login"] == "1":#舊使用者
                return Response({"message": "已註冊過使用者"})

            elif len(request.data["have_login"]) == 3:#將驗證碼存入captcha_ans.txt
                f = open("captcha_ans.txt", "w")
                f.write(request.data["have_login"])
                return Response({"message": "已紀錄您的答案"})

            else:
                return Response({"message": "不合法使用者"})

        elif request.data.__contains__("identity_card"):
            serializer = user_serializer(data=request.data)

            if serializer.is_valid():#如果欄位合法
                identity = request.data["identity_card"]#身分證
                card_num = request.data["health_card"]#健保卡卡號
                heal_bank_pwd = request.data["health_pwd"]#健康存摺密碼
                asus_account = request.data["asus_account"]#華碩雲端帳號
                asus_pwd = request.data["asus_pwd"]#華碩雲端密碼

                download = download_json.DownLoad_Json()
                download.get_img()#截驗證碼圖片
                sleep(20)#讓使用者輸入驗證碼
                f = open("captcha_ans.txt", "r")
                captcha_ans = f.read()

                status_message = download.login(captcha_ans, identity, card_num, heal_bank_pwd, asus_account, asus_pwd)
                if status_message != "登入成功":
                    print(status_message)
                    return Response({"message": status_message})
                download.generate_json()
                download.download_json()

                serializer.save()#存入資料庫
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 回傳錯誤，不合法

@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))#權限
def api_doctor(request):
    if request.method == 'GET':
        queryset = doctor_say.objects.all()  # 讀table的資料
        serializer_class = doctor_say_serializer(queryset, many=True )  # 序列化
        return Response(serializer_class.data)

    elif request.method == 'POST':
        serializer = doctor_say_serializer(data=request.data)

        if serializer.is_valid():
            queryset = user.objects.filter(identity_card=request.data["identity"])
            name = user.objects.filter(identity_card=request.data["identity"])[0].name
            tokens = []
            message = request.data["recorder"] + "幫" + name + "新增了一筆就醫紀錄"
            for query in queryset:
                tokens.append(query.token)

                push_data = {
                    "content": message,
                    "token": query.token
                }
                push_serializer = push_info_serializer(data=push_data)
                if push_serializer.is_valid():
                    push_serializer.save()

            # 蒐集完token後呼叫推播服務
            push_info_to_phone.pytofirebase(tokens, message)


            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 回傳錯誤，不合法

@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))#權限
def api_push_info(request):
    if request.method == 'GET':
        queryset = push_info.objects.all()  # 讀table的資料
        serializer_class = push_info_serializer(queryset, many=True )  # 序列化
        return Response(serializer_class.data)

    elif request.method == 'POST':
        serializer = push_info_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 回傳錯誤，不合法

@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))#權限
def api_health_info(request):
    if request.method == 'GET':
        queryset = health_info.objects.all()  # 讀table的資料
        serializer_class = health_info_serializer(queryset, many=True )  # 序列化
        return Response(serializer_class.data)

    elif request.method == 'POST':
        serializer = health_info_serializer(data=request.data)

        if serializer.is_valid():
            queryset = user.objects.filter(identity_card = request.data["identity"])
            name = user.objects.filter(identity_card = request.data["identity"])[0].name

            tokens = []
            message = name + "今日收縮壓/舒張壓:" + request.data["sys_blood_pressure"] + "/" + request.data["dia_blood_pressure"] + "\n" + name + "今日血糖：" + request.data["blood_sugar"]
            print(message)
            for query in queryset:
                tokens.append(query.token)

                push_data = {
                    "content": message,
                    "token": query.token
                }
                push_serializer = push_info_serializer(data=push_data)
                if push_serializer.is_valid():
                    push_serializer.save()


            #蒐集完token後呼叫推播服務
            push_info_to_phone.pytofirebase(tokens, message)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 回傳錯誤，不合法

