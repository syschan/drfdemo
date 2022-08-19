"""ViewSet视图集，继承于APIView，所以APIView有的功能，它都有，APIView没有的功能，它也没有"""
from urllib import response
from rest_framework.viewsets import ViewSet
from students.models import Student
from .serializers import StudentModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class AuthDemoAPIView(APIView):
    """只允许通过认证后的用户访问"""
    """只允许登录后的用户访问"""
    # authentication_classes = [CustomAuthentication,SessionAuthentication,BasicAuthentication]
    # authentication_classes = [CustomAuthentication]#开启自定义认证，如果不开启则启用settings中的全局认证
    # permission_classes = [IsAuthenticated]

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

class Student1ViewSet(ViewSet):
    """ViewSet,自定义get方法"""
    # path('student1/', views.Student1ViewSet.as_view({"get": "get_5"}))关联路径、请求方法和视图
    def get_5(self, request):
        student_list = Student.objects.all()[:5]

        serializer = StudentModelSerializer(instance=student_list, many=True)
        print('Student1APIViewSet:get获取5条数据=>/collect/student1/')
        return Response(serializer.data)
    # path('student1/get_5_girl/', views.Student1ViewSet.as_view({"get": "get_5_girl"}))关联路径、请求方法和视图
    def get_5_girl(self, request):
        student_list = Student.objects.filter(sex=False)[:5]

        serializer = StudentModelSerializer(instance=student_list, many=True)
        print('Student1APIViewSet:get获取5条数据=>/collect/student1/get_5_girl/')
        return Response(serializer.data)
    # re_path(r'^student1/(?P<pk>\d+)/$', views.Student1ViewSet.as_view({"get": "get_one"}))关联路径、请求方法和视图
    def get_one(self, request, pk):
        student = Student.objects.get(pk=pk)

        serializer = StudentModelSerializer(instance=student)
        print('Student1APIViewSet:get获取1条数据=>/collect/student1/<pk=%s>/'%pk)
        return Response(serializer.data)




"""如果希望在视图集中调用GenericAPIView的功能，则可以采用下面方式"""
from rest_framework.generics import GenericAPIView


class Student2ViewSet(ViewSet, GenericAPIView):
    """ViewSet+GenericAPIView,自定义get方法"""
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    # path('student2/', views.Student2ViewSet.as_view({"get": "get_5"})),关联路径、请求方法和视图
    def get_5(self, request):
        student_list = self.get_queryset()[:5]

        serializer = StudentModelSerializer(instance=student_list, many=True)
        print('Student2ViewSet:get获取5条数据=>/collect/student2/')
        return Response(serializer.data)

    # path('student2/get_5_girl/', views.Student2ViewSet.as_view({"get": "get_5_girl"})),关联路径、请求方法和视图
    def get_one(self, request, pk):
        student = self.get_object()

        serializer = StudentModelSerializer(instance=student)
        print('Student2ViewSet:get获取1条数据=>/collect/student2/<pk=%s>/'%pk)
        return Response(serializer.data)

    # path('student2/get_5_girl/', views.Student2ViewSet.as_view({"get": "get_5_girl"})),关联路径、请求方法和视图
    def get_5_girl(self, request):
        student_list = self.get_queryset().filter(sex=False)[:5]

        serializer = StudentModelSerializer(instance=student_list, many=True)
        print('Student2ViewSet:get获取5条数据=>/collect/student2/get_5_girl/')
        return Response(serializer.data)

"""
上面的方式，虽然实现视图集中调用GenericAPIView，但是我们要多了一些类的继承。
所以我们可以直接继承 GenericViewSet
"""
from rest_framework.viewsets import GenericViewSet


class Student3GenericViewSet(GenericViewSet):
    """GenericViewSet,自定义get方法"""
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    
    # path('student3/', views.Student3GenericViewSet.as_view({"get": "get_5"})),
    def get_5(self, request):
        student_list = self.get_queryset()[:5]

        serializer = self.get_serializer(instance=student_list, many=True)
        print('Student3GenericViewSet:get获取5条数据=>/collect/student3/')
        return Response(serializer.data)

    # path('student3/get_5_girl/', views.Student3GenericViewSet.as_view({"get": "get_5_girl"})),
    def get_5_girl(self, request):
        student_list = self.get_queryset().filter(sex=False)[:5]

        serializer = self.get_serializer(instance=student_list, many=True)
        print('Student3GenericViewSet:get获取5条数据=>/collect/student3/get_5_girl/')
        return Response(serializer.data)

"""
在使用GenericViewSet时，虽然已经提供了基本调用数据集（queryset）和序列化器属性，但是我们要编写一些基本的
API时，还是需要调用DRF提供的模型扩展类 [Mixins]
"""
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

# path("students4/", views.Student4GenericViewSet.as_view({"get": "list", "post": "create"})),
class Student4GenericViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    """GenericViewSet，可以和模型类进行组合快速生成基本的API接口，继承Mixin中的list和create方法，不在支持自定义"""
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    #print('Student4GenericViewSet:get获取全部/post创建1条数据=>/collect/students4/')

from rest_framework.viewsets import ModelViewSet

# path("students5/", views.Student5ModelViewSet.as_view({"post": "create", "get": "list"})),
# re_path(r"^students4/(?P<pk>\d+)/$", views.Student5ModelViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
class Student5ModelViewSet(ModelViewSet):
    """ModelViewSet 默认提供了5个API接口，继承Mixin中的list/create/retrieve/update/destroy方法，不在支持自定义"""
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    #print('Student5ModelViewSet:get获取全部/post创建1条数据=>/collect/students5/')
    #print('Student5ModelViewSet:get获取/put更新/delete删除1条数据=>/collect/students5/<pk>')


# 只读模型视图集
from rest_framework.viewsets import ReadOnlyModelViewSet

# path("students6/", views.Student6ReadOnlyModelViewSet.as_view({"get": "list"})),
# re_path(r"^students6/(?P<pk>\d+)/$", views.Student6ReadOnlyModelViewSet.as_view({"get": "retrieve"})),
class Student6ReadOnlyModelViewSet(ReadOnlyModelViewSet):
    """ReadOnlyModelViewSet  继承Mixin中的list/retrieve方法，不在支持自定义"""
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    #print('Student6ReadOnlyModelViewSet:get获取全部数据=>/collect/students6/')
    #print('Student6ReadOnlyModelViewSet:get获取1条数据=>/collect/students6/<pk>')

# 路由的使用
from rest_framework.decorators import action

# 直接注册路由，关联路径和视图，通过@action自定义方法、确定是否需要传递pk，router.register("student7", views.Student7ModelViewSet)
class Student7ModelViewSet(ModelViewSet):
    """直接注册路由，关联路径和视图，通过@action自定义方法、确定是否需要传递pk，router.register("student7", views.Student7ModelViewSet)"""
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    #"""
    # methods 指定允许哪些http请求访问当前视图方法
    # detail  指定生成的路由地址中是否要夹带pk值，True为需要?怎么False和True结果一样呢？被装饰的方法需要在urlpatterns中追加路由，而不是注册路由
    def get_7(self, request,pk):
        myset=self.get_queryset()
        # 原有的get方法被覆盖
        print('Student7ModelViewSet:get获取1条数据=>/collect/student7/<pk=%s>'%pk)
        serilizer = self.get_serializer(instance=self.get_queryset().get(pk=pk))
        return Response(serilizer.data)
    @action(methods=["GET"], detail=False)
    def get_all(self, request):
        # 原有的get方法被覆盖
        data=request.data
        print(data)
        print('Student7ModelViewSet:get获取所有数据=>/collect/student7/')
        serilizer = self.get_serializer(instance=self.get_queryset(),many=True)
        return Response(serilizer.data)
    @action(methods=["POST"], detail=False)
    def login(self, request):
        # 原有的get方法被覆盖
        data=request.data
        username=data['name']
        print(self.get_queryset().filter(name=username))
        print('Student7ModelViewSet:post提交并返回1条数据=>/collect/login/')
        serilizer = self.get_serializer(instance=self.get_queryset().filter(name=username),many=True)
        return Response(serilizer.data)
    #"""

"""在多个视图类合并成一个视图类以后，那么有时候会出现一个类中需要调用多个序列化器"""

"""1. 在视图类中调用多个序列化器"""
"""原来的视图类中基本上一个视图类只会调用一个序列化器，当然也有可能要调用多个序列化器"""
from .serializers import StudentInfoModelSerializer


class Student8GenericAPIView(GenericAPIView):
    """在视图类中调用多个序列化器"""
    queryset = Student.objects.all()

    # GenericAPI内部调用序列化器的方法，我们可以重写这个方法来实现根据不同的需求来调用不同的序列化器
    def get_serializer_class(self):
        if self.request.method == "GET":
            # 2个字段
            return StudentInfoModelSerializer
        return StudentModelSerializer

    def get(self, request):
        """获取所有数据的id和name"""
        student_list = self.get_queryset()

        serializer = self.get_serializer(instance=student_list, many=True)
        print('Student8GenericAPIView:get获取所有数据=>/collect/student8/')
        return Response(serializer.data)

    def post(self, request):
        """添加数据"""
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('Student8GenericAPIView:post创建1条数据=>/collect/student8/')
        return Response(serializer.data)


"""2. 在一个视图集中调用多个序列化器"""

class Student9ModelViewSet(ModelViewSet):
    """在一个视图集中调用多个序列化器"""
    queryset = Student.objects.all()

    """要求:
            列表数据list，返回２个字段，
            详情数据retrieve，返回所有字段，
    """
    # 此处返回了ModelSerializer，相当于原来serializer_class=XXModelSerializer
    def get_serializer_class(self):
        # 本次客户端请求的视图方法名  self.action
        if self.action == "list":
            print('Student9ModelViewSet:get获取所有数据=>/collect/student9/')
            return StudentInfoModelSerializer
        print(self.action)
        print('Student9ModelViewSet:get获取1条数据=>/collect/student9/')
        return StudentModelSerializer

from rest_framework_simplejwt.views import TokenObtainPairView,TokenVerifyView
from .serializers import LoginTokenObtainPairSerializer,GetUserInfoTokenVerifySerializer

class LoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginTokenObtainPairSerializer

    def post(self,request):
        #print(request.data)
        serializer = self.get_serializer(data = request.data)
        try:
            serializer.is_valid(raise_exception=True)
            print('Login验证成功')
            return Response(serializer.validated_data)
        except Exception as err:
            #raise serializer.ValidationError(f'验证失败：{err}')
            #pass
            return Response({'msg':f'{err}','code':403})
        #serializer.save()
        print('MyTokenObtainPairView:post创建1条数据=>/collect/login/')
        return Response(serializer.validated_data)

class GetUserInfoTokenVerifyView(TokenVerifyView):
    serializer_class =  GetUserInfoTokenVerifySerializer

    def post(self,request):
        #print(request.data)
        serializer = self.get_serializer(data = request.data)
        try:
            serializer.is_valid(raise_exception=True)
            print('GetUserInfo验证成功')
            return Response(serializer.validated_data)
        except Exception as err:
            #raise serializer.ValidationError(f'验证失败：{err}')
            #pass
            return Response({'msg':f'{err}','code':403})
        #serializer.save()
        print('MyTokenObtainPairView:post创建1条数据=>/collect/login/')
        return Response(serializer.validated_data)