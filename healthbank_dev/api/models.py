from django.db import models

# Create your models here.
class user(models.Model):#id會預設
    identity_card = models.TextField()#身分證
    health_card = models.TextField()#健保卡
    health_pwd = models.TextField()#健康存摺密碼
    asus_account = models.TextField()#華碩雲端帳號
    asus_pwd = models.TextField()#華碩雲端密碼
    token = models.TextField()#使用者手機token
    name = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "user"#table name

class doctor_say(models.Model):
    eat_time = models.TextField()  # 吃藥時間
    back_date = models.TextField()  # 回診日期
    drug_style = models.TextField()  # 用藥方式
    not_eat = models.TextField()  # 忌口
    side_effect = models.TextField()  # 副作用
    recorder = models.TextField()  # 紀錄者
    disease_name = models.TextField() # 病名
    message = models.TextField()  # 留言板
    record_time = models.TextField()  # 紀錄時間
    identity = models.TextField()  # 身分證
    time_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "doctor_say"

class health_info(models.Model):
    appellation = models.TextField()
    identity = models.TextField()
    sys_blood_pressure = models.TextField()# 收縮壓
    dia_blood_pressure = models.TextField()# 舒張壓
    blood_sugar = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "health_info"

class push_info(models.Model):
    content = models.TextField()
    token = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "push_info"