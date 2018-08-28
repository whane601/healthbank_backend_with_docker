from api import views
from django.contrib import admin#healthbank,healthbank123!@#
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

#router設定
router = DefaultRouter()
router.register(r'user', views.user_viewset)#要提供restful_api的table都要router.register

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),#ex: http://127.0.0.1:8000/api/user/
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api_user/', views.api_user),
    url(r'^api_doctor/', views.api_doctor),
    url(r'^api_push_info/', views.api_push_info),
    url(r'^api_health_info/', views.api_health_info)
]
