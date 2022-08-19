"""
    测试代码：区分django的 View 和 drf的 APIView
"""
import json
from traceback import print_tb
from unittest import result
from django.views import View
from django.http import JsonResponse

# 不需要pk
class Student1View(View):
    def get(self, request):
        print(request)  # 这是django提供的HttpRequest类
        print(request.GET)
        """打印效果：
        <WSGIRequest: GET '/req/student1/'>
        """
        data_dict = {'name': "alex", "age": 18}

        return JsonResponse(data_dict)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# 不需要pk
# View到APIView的变化
# request不再是Django原生的request，而是DRF扩展后的request
# 相应的data和query_params也发生了变化
# Response不再是Django原生对的JsonResponse，而是DRF扩展后的Response
# DRF同时内置了status常量
class Student2APIView(APIView):
    def get(self, request):
        print(request)  # rest_framework扩展后的request
        print(request.query_params)

        print('get方法中的request.data不会被解析:',request.data)
        """打印效果
        <rest_framework.request.Request GET '/req/student2/'>
        """
        data_dict = {'name': "alex", "age": 18}

        return Response(data_dict, status=status.HTTP_204_NO_CONTENT, headers={"name": "xiaobai"})
"""
使用APIView提供学生信息的5个API接口
GET    /req/student3/               # 获取全部数据
POST   /req/student3/               # 添加数据

GET    /req/student3/(?P<pk>\d+)    # 获取一条数据
PUT    /req/student3/(?P<pk>\d+)    # 更新一条数据
DELETE /req/student3/(?P<pk>\d+)    # 删除一条数据

APIView定义API接口需要用到：
1、模型对象Student，直接Student.objects获取实例化对象。
2、模型类序列化器StudentModelSerializer，直接生成实例化的序列化器
不会用到Meta
"""

from students.models import Student
from req.serializers import StudentModelSerializer

# 不需要pk
class Student3APIView(APIView):
    def get(self, request):
        """获取所有数据"""
        student_list = Student.objects.all()
        # 序列化操作
        serializer = StudentModelSerializer(instance=student_list, many=True)
        # ================================
        # 如果需要在返回之前对serializer.data进行处理，应该在哪里处理？
        # 方法1：
        # 对serializer.data转字典后处理再返回出去
        # 方法2：
        # 再serializer.data之前处理，serializer.data本身就是处理好的数据，直接返回出去？
        # ================================
        print('Student3APIView:get获取所有数据=>/req/student3/')
        return Response(serializer.data)

    def post(self, request):
        # 此处默认是通过浏览器提交，postman提交需要更改为Content-Type:application/json;默认是Content-Type:text/plain
        # 获取用户提交的数据
        data_dict = request.data
        print(data_dict)
        # 实例化序列化器对象
        serializer = StudentModelSerializer(data=data_dict)
        # 数据校验
        serializer.is_valid(raise_exception=True)
        # 保存数据
        serializer.save()
        print('Student3APIView:post提交1条数据==>/req/student3/')
        return Response(serializer.validated_data)

# 需要pk
class Student4APIView(APIView):
    def get(self, request, pk):
        # 过滤pk对应的学生对象
        student_obj = Student.objects.get(pk=pk)

        serializer = StudentModelSerializer(instance=student_obj)
        print('Student3APIView:get获取1条数据=>/req/student3/<pk>')
        return Response(serializer.data)

    def put(self, request, pk):
        # 过滤pk对应的学生对象
        student_obj = Student.objects.get(pk=pk)
        # 获取用户提交的数据
        data_dict = request.data

        serializer = StudentModelSerializer(instance=student_obj, data=data_dict)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        # serializer.validated_data有序字典，通过dict直接转Python字典
        print('Student3APIView:put修改1条数据=>/req/student3/<pk>')
        print('修改后的数据为：',dict(serializer.validated_data))
        # 自定义返回的格式
        res = {'msg': "修改成功", "code": 200,'data':serializer.validated_data}
        return Response(res)
        # {
        #     "msg": "修改成功",
        #     "code": 200,
        #     "data": {
        #         "name": "roatms",
        #         "age": 88,
        #         "sex": true
        #     }
        # }

    def delete(self, request, pk):
        Student.objects.filter(pk=pk).delete()
        print('Student3APIView:delete删除条数据=>/req/student3/<pk>')
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
使用GenericAPIView提供学生信息的5个API接口
GET    /req/student4/               # 获取全部数据
POST   /req/student4/               # 添加数据

GET    /req/student4/(?P<pk>\d+)    # 获取一条数据
PUT    /req/student4/(?P<pk>\d+)    # 更新一条数据
DELETE /req/student4/(?P<pk>\d+)    # 删除一条数据

GenericAPIView定义API接口需要用到：
1、用到了Meta
1.1、模型对象Student，首先通过Student.objects获取queryset
1.2、模型类序列化器StudentModelSerializer，直接生成序列化器类
2、在X动作方法中通过instance = self.get_object()获取实例；student_list = self.get_queryset()获取实例列表
3、在X动作方法中通过self.get_serializer()获取序列化器
"""

from rest_framework.generics import GenericAPIView

# 不需要pk
# 从APIView到GenericAPIView封装后的：
# 把模型对象Student和序列化器StudentModelSerializer从X动作方法中解耦出来
# 步骤依然没有变只是变得不管是否需要pk值都具有相同的结构，即共同的queryset+serializer_class和不同的X动作方法
#  
class Student5GenericAPIView(GenericAPIView):
    # 当前视图类中操作的公共数据，先从数据库查询出来
    queryset = Student.objects.all()
    # 设置类视图中所有方法共有调用的序列化器类
    serializer_class = StudentModelSerializer

    def get(self, request):
        # 获取模型数据
        student_list = self.get_queryset()

        # 调用序列化器
        serializer = self.get_serializer(instance=student_list, many=True)
        print('Student5APIView:get获取所有数据=>/req/student4/')

        res=serializer.data

        return Response(res)

    def post(self, request):
        """新增数据"""
        # 获取用户提交的数据并实例化序列化器对象
        serializer = self.get_serializer(data=request.data)
        # 数据校验
        serializer.is_valid(raise_exception=True)
        # 保存数据
        # print('serializer.data',serializer.data)
        # ======================serializer.data和serializer.validated_data的区别与关系？？？？
        # print('serializer.validated_data',serializer.validated_data)
        serializer.save()
        ret=serializer.validated_data
        res=serializer.data
        # serializer.data是数据全量，serializer.validated_data只有已验证的部分数据
        # serializer.data是原生的Python字典格式，而serializer.validated_data是OrderedDict有序字典格式
        # serializer.data和serializer.validated_data都可以作为Response的数据返回出去
        # serializer.validated_data调用之前必须有调用过is_valid，不然会报错
        print('serializer.data===',serializer.data)
        # serializer.data=== {'id': 25, 'name': 'roat', 'age': 96, 'sex': True}
        print('serializer.validated_data===',serializer.validated_data)
        # serializer.validated_data=== OrderedDict([('name', 'roat'), ('age', 96), ('sex', True)])
        print(res==ret)
        print('Student5APIView:post新增1条数据=>/req/student4/')
        return Response(serializer.data)

# 需要pk
class Student6GenericAPIView(GenericAPIView):
    # 当前视图类中操作的公共数据，先从数据库查询出来
    queryset = Student.objects.all()
    # 设置类视图中所有方法共有调用的序列化器类
    serializer_class = StudentModelSerializer

    def get(self, request, pk):
        """参数pk名，必须要叫pk，否则会报错。"""
        # 获取单个模型对象
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        print('Student6APIView:get获取1条数据=>/req/student4/<pk>')
        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object()

        serializer = self.get_serializer(instance=instance, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        print('Student6APIView:put修改1条数据=>/req/student4/<pk>')
        return Response(serializer.data)

    def delete(self, request, pk):
        # 获取模型对象
        instance = self.get_object()
        # 删除模型对象
        instance.delete()
        print('Student6APIView:delete删除条数据=>/req/student4/<pk>')
        res={'msg':'id为:%s的记录删除成功'%pk,'code':status.HTTP_204_NO_CONTENT}
        return Response(data=res,status=status.HTTP_204_NO_CONTENT)
        # {
        #     "msg": "id为:25的记录删除成功",
        #     "code": 204
        # }

from rest_framework.mixins import ListModelMixin, CreateModelMixin

# 不需要pk
# 从GenericAPIView到XModelMixin完成封装后的利弊：
# 好处：把所有步骤全部封装到XModelMixin，直接调用XModelMixin的相应方法即可，不需要再通过get_object和get_serializer去生成instance实例和序列化器，直接获得返回结果
# 坏处：没法自定义返回格式；没法自定义传入相应的参数，做后台模型对象返回的数据拦截
class Student7GenericAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        print('Student7APIView:get获取所有数据=>/req/student5/')
        return self.list(request)

    def post(self, request):
        print('Student7APIView:get获取所有数据=>/req/student5/')
        return self.create(request)


from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

# 需要pk
class Student8GenericAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, pk):
        print('Student8APIView:get获取1条数据=>/req/student5/<%s>'%pk)
        return self.retrieve(request)

    def put(self, request, pk):
        print('Student8APIView:put更新1条数据=>/req/student5/<%s>'%pk)
        return self.update(request)

    def delete(self, request, pk):
        print('Student8APIView:delete删除1条数据=>/req/student5/<%s>'%pk)
        return self.destroy(request)
"""
DRF里面，内置了一些同时继承了GenericAPIView和Mixins扩展类的视图子类，
我们可以直接继承这些子类就可以生成对应的API接口
"""

"""
ListAPIView      获取所有数据
CreateAPIView    添加数据
"""
# 从XModelMixin进一步封装到XAPIView后
# 除了保留共同的queryset和serializer_class，所有X动作方法全部封装到XAPIView中
from rest_framework.generics import ListAPIView, CreateAPIView


class Student9GenericAPIView(ListAPIView, CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


"""
RetrieveAPIView                 获取一条数据
UpdateAPIView                   更新一条数据
DestorAPIView                   删除一条数据
RetrieveUpdateDestoryAPIView    上面三个的缩写
"""
from rest_framework.generics import RetrieveUpdateDestroyAPIView


class Student10GenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

"""
视图集
上面５个接口使用了８行代码生成，但是我们可以发现有一半的代码重复了
所以，我们要把这些重复的代码进行整合，但是依靠原来的类视图，其实有２方面产生冲突的
1. 查询所有数据、添加数据是不需要声明pk的，而其他的接口需要    [路由冲突了]
2. 查询所有数据和查询一条数据，都是属于get请求                 [请求方法冲突了]
为了解决上面的２个问题，所以DRF提供了视图集来解决这个问题
"""

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin


# 这两个是等价的
# class Student11GenericAPIView(GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin):
class Student11GenericAPIView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
