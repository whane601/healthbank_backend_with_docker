from sqlalchemy import Column, String, create_engine, Integer, DateTime, BigInteger,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import requests


import datetime
from service import push_info_to_phone

engine = create_engine("postgresql+psycopg2://postgres:postgres@163.13.202.181:5432/postgres",echo=True,client_encoding= "utf8")
connection = engine.connect()
Base = declarative_base()

today = datetime.date.today()

class user(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    identity_card = Column(String)
    health_card = Column(String)
    health_pwd = Column(String)
    asus_account = Column(String)
    asus_pwd = Column(String)
    token = Column(String)
    name = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

class doctor_say(Base):
    __tablename__ = "doctor_say"
    id = Column(Integer, primary_key=True, autoincrement=True)
    eat_time = Column(String)
    back_date =Column(String)
    drug_style = Column(String)
    not_eat = Column(String)
    side_effect = Column(String)
    recorder = Column(String)
    time_created =Column(String)
    disease_name = Column(String)
    message = Column(String)
    record_time =Column(String)
    identity  =Column(String)


DBSession = sessionmaker(bind=engine)
session = DBSession()
Record_time = []
Push_ID = []
Back_date = []
def Initial ():
    for r in session.query(doctor_say).all():

        Back_date.append(r.record_time)
        Record_time.append(r)
        # 紀錄日期從字串轉成日期格式
        back_date = int(r.back_date)
        record_day = r.record_time.replace('/', " ").split()
        other_day = datetime.date(int(record_day[0]), int(record_day[1]), int(record_day[2]))
        # 今日日期
        today = datetime.date.today()
        result = (other_day - today).days
        # 要去user 群找token的ID

        if 0 < result and result < back_date:
            Push_ID.append(r.identity)
    # print(Back_date)
    return Push_ID,Back_date


def push(Push_ID):

    for i in Push_ID:
        name = []
        token = []
        for s in session.query(user).filter(user.identity_card == i).all():
            name.append(s.name)
            token.append(s.token)
        return name,token
def doctor_sat():
    Rush_IDlist, Back_date = Initial()
    name, token = push(Push_ID)

    for i in range(len(token)):
        message = name[i] + '於' + Back_date[i] + '記得回診～'
        push_info_to_phone.pytofirebase([token[i]], message)

        push_data = {
            "content": message,
            "token": token[i]
        }

        a = requests.post("http://127.0.0.1:8000/api_push_info/", data = push_data)

if __name__ == '__main__':
    doctor_sat()

