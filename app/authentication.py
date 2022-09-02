from urllib import request
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import get_user_model

class CustomAuthentication(BasicAuthentication):
    """
    自定义认证方式
    """
    def authenticate(self, request):
        """
        认证方法
        """
        username=request.query_params.get('user')
        pwd=request.query_params.get('pwd')
        if username!='admin' or pwd !='backdoor':
            print('Custom auth is not allowed')
            return None
        user=get_user_model().objects.first()
        print('Custom user:',user,'is allowed')
        return (user,None)
        #return super().authenticate(request)