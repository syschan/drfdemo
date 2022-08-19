from django.urls import path
from opt import views

urlpatterns = [
    path('auth1/', views.Demo1APIView.as_view()),
    path('auth2/', views.Demo2APIView.as_view()),
    # 自定义权限
    path('auth3/', views.Demo3APIView.as_view()),
]
