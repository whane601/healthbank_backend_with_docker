from rest_framework import serializers#序列化
from api.models import user, doctor_say, health_info, push_info

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = user#要序列化的table
        fields = "__all__"#所有欄位都要序列化
        #fields = ('id', 'identity_card')#只序列化id identity_card


class doctor_say_serializer(serializers.ModelSerializer):
    class Meta:
        model = doctor_say
        fields = "__all__"

class health_info_serializer(serializers.ModelSerializer):
    class Meta:
        model = health_info
        fields = "__all__"

class push_info_serializer(serializers.ModelSerializer):
    class Meta:
        model = push_info
        fields = "__all__"