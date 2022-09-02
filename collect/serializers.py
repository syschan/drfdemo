# collect下的serializers.py文件

from ctypes.wintypes import PINT
from students.models import Student
from rest_framework import serializers


class StudentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["id", "name", "age", "sex"]
        extra_kwargs = {
            "name": {"max_length": 10, "min_length": 4},
            "age": {"max_value": 150, "min_value": 0},
        }

    def validate_name(self, data):
        if data == "root":
            raise serializers.ValidationError("用户名不能为root！")
        return data

    def validate(self, attrs):
        name = attrs.get('name')
        age = attrs.get('age')

        if name == "alex" and age == 22:
            raise serializers.ValidationError("alex在22时的故事。。。")

        return attrs


class StudentInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name"]

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenVerifySerializer

class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': '用户名或者密码错误'
    }
    def validate(self, attrs):
        # try:
        #     print(self.user)
        # except:
        #     print('err')
        #print(self.user)
        data = super().validate(attrs)
        #print('validate===',data)
        refresh = self.get_token(self.user)
        #print('refresh===',refresh)
        data['refresh'] = str(refresh)
        data['jwtToken'] = str(refresh.access_token)
        #cUser = User.objects.get(username=self.user)
        # Add extra responses here
        # data['username'] = self.user.username
        # print('成功回调？')
        res_data={
            'code':200,
            'msg':'登录成功',
            'flag':True,
            'data':{
                'username':self.user.username,
                'jwtToken':str(refresh.access_token)
            }
        }
        # print(res_data)
        return res_data
        # return data
from jwt import decode as jwt_decode
from app import settings
class GetUserInfoTokenVerifySerializer(TokenVerifySerializer):
    # default_error_messages = {
    #     'no_active_account': '用户名或者密码错误'
    # }

    def validate(self, attrs):
        # try:
        #     print(self.user)
        # except:
        #     print('err')
        #print(self.user)
        # print("attrs===",attrs)
        decoded_data = jwt_decode(attrs['token'], settings.SECRET_KEY,algorithms=["HS256"])
        # print(decoded_data)
        #print('validate===',data)
        # refresh = self.get_token(self.user)
        #print('refresh===',refresh)
        # data['refresh'] = str(refresh)
        # data['jwtToken'] = str(refresh.access_token)
        #cUser = User.objects.get(username=self.user)
        # Add extra responses here
        # data['username'] = self.user.username
        # print('成功回调？')
        res_data={
            'code':200,
            'msg':'操作成功',
            'flag':True,
            'data':{
                'exp':decoded_data['exp'],
                'iat':decoded_data['iat'],
                'roles':['admin']
            }
        }
        print(res_data)
        return res_data
        return decoded_data