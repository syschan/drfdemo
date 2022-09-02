from sre_constants import SUCCESS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from app.authentication import CustomAuthentication
"""用户的认证和权限识别"""


class Demo1APIView(APIView):
    """只允许通过认证后的用户访问"""
    """只允许登录后的用户访问"""
    # authentication_classes = [CustomAuthentication,SessionAuthentication,BasicAuthentication]
    # authentication_classes = [CustomAuthentication]#开启自定义认证，如果不开启则启用settings中的全局认证
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """个人中心"""
        # 此处的user来源于Xauthentication中返回的user,CustomAuthentication自定义中返回的user
        if request.user.id or request.user.username:
            print('Demo1APIView:get获取所有数据auth1/')
            SUCCESS={
                'msg':"Success",
                'infor':"通过认证",
                'data':{
                    'id':request.user.id,
                    'username':request.user.username
                    }
                }
            return Response(data=SUCCESS,status=status.HTTP_200_OK)
        else:
            print('Demo1APIView:get获取所有数据auth1/')
            FAILED={
                'msg':"Failed",
                'infor':"认证失败",
                'data':{
                    'id':request.user.id,
                    'username':request.user.username
                    }
                }
            return Response(data=FAILED,status=status.HTTP_401_UNAUTHORIZED)


class Demo2APIView(APIView):
    """只允许管理员访问"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        """个人中心2"""
        return Response("个人中心2")

# 自定义权限
from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        """
        针对访问视图进行权限判断
        :param request: 本次操作的http请求对象
        :param view:  本次访问路由对应的视图对象
        :return:
        """
        print('有权限吗?',request.user.username)
        if request.user.username == "xiaohong":
            return True
        return False


class Demo3APIView(APIView):
    """自定义权限"""
    permission_classes = [MyPermission]

    def get(self, request):
        """个人中心3"""
        return Response("个人中心3")
