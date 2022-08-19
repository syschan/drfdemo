from functools import partial
import json
from django.http import JsonResponse,HttpResponse #,HttpRequest
from django.views import View
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from students.models import Student
from ser.serializers import StudentSerializer,Student3Serializer,Student5Serializer,StudentModelSerializer

class Student1View(View):
    """使用序列化器进行数据的序列化操作 
    序列化器转换一条数据[模型转换成字典]"""
    def get(self, request, pk):
        """
            StudentSerializer(instance=模型对象或者模型列表，客户端提交的数据，额外要传递到序列化器中使用的数据)
        """
        # =========决定是否带参数
        print('pk type=',type(pk))
        # 接收客户端传过来的参数，进行过滤查询，先查出学生对象
        print('Student type=',type(Student))
        # ==========由模型字段和参数确定过滤条件
        student = Student.objects.get(pk=pk)
        print('模型对象：student type=',type(student))
        # 转换数据类型
        # 1.实例化序列化器类

        print('StudentSerializer type=',type(StudentSerializer))

        serializer = StudentSerializer(instance=student)
        print('序列化对象：serializer type=',type(serializer))
        # 2.查看序列化器的转换结果
        serializer.data['name']='sala'
        print('serializer.data=',serializer.data)
        print('serializer.data type=',type(serializer.data))
        print('JsonResponse type==',JsonResponse)
        res=JsonResponse(serializer.data)
        print('JsonResponse对象：res=',res)
        return res

class Student2View(View):
    """序列化器转换多条数据[模型转换成字典]"""
    def get(self, request):
        student_list = Student.objects.all()
        # 序列化器转换多个数据
        # many=True 表示本次序列化器转换如果有多个模型对象列参数，则必须声明 Many=True
        serializer = StudentSerializer(instance=student_list, many=True)

        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)
class Student3View(View):
    # 此处的post数据通过postman模拟提交;由于没有get方法，默认是无法浏览器输入.../Student3/来查询
    def post(self, request):
        data = request.body.decode()
        # 反序列化用户提交的数据
        # print(data)
        data_dict = json.loads(data)
        print(data_dict)

        # 调用序列化器进行实例化

        serializer = Student3Serializer(data=data_dict)

        # is_valid在执行的时候，会自动先后调用 字段的内置选项,自定义验证方法，自定义验证函数
        # 调用序列化器中写好的验证代码
        # raise_exception=True 抛出验证错误信息，并阻止代码继续往后运行
        # 验证结果
        print(serializer.is_valid(raise_exception=True))

        # 获取验证后的错误信息
        print(serializer.errors)

        # 获取验证后的客户端提交的数据
        print(serializer.validated_data)

        #IsSave2db=False   
        IsSave2db=True    
        # 是否将反序列化数据保存到数据库中    
        if not IsSave2db:
            # case1:
            # return HttpResponse(serializer.validated_data)
            return JsonResponse(serializer.validated_data)
        # save 表示让序列化器开始执行反序列化代码。create代码
        else:
            # case2:
            serializer.save()#此次保存由于没有在Student3Serializer实例化时传入instance参数，所以不会触发更新；因为没有传入pk值，没有得到相应的实例化的对象
            #return HttpResponse(serializer.validated_data)
            return JsonResponse(serializer.validated_data)
        # case1和case2的区别和联系：
        # case1和case2都是来自于Student3Serializer，都能够返回数据；但是都不能够在路径student3下通过get方法去访问
        # case1未调用create方法直接返回的数据，即只是生成了validated_data验证数据，没把validated_data通过调用Student的create方法生成模型对象实例返回
        # case2则调用create方法直接返回的数据，即不仅生成了validated_data验证数据，还把validated_data通过调用Student的create方法生成模型对象实例返回
        # case1由于没有创建数据，所以无法通过student的get方法去访问通过student3的post方法提交的数据
        # case2有创建数据，所以可以通过student的get方法去访问通过student3的post方法提交的数据
class Student4View(View):
    def put(self, request, pk):
        data = request.body.decode()
        import json
        data_dict = json.loads(data)

        student_obj = Student.objects.get(pk=pk)
        # 有instance参数，调用save方法，就会调用update方法。
        serializer = Student3Serializer(instance=student_obj, data=data_dict)

        serializer.is_valid(raise_exception=True)
        # 此次保存由于有在Student3Serializer实例化时传入instance参数，所以会触发更新；因为有传入pk值，已经得到相应的实例化的对象
        serializer.save()  # 触发序列器中的update方法

        return JsonResponse(serializer.validated_data)

class Student5View(View):
    def get(self, request):
        # 获取所有数据
        student_list = Student.objects.all()
        serializer = Student5Serializer(instance=student_list, many=True)

        return JsonResponse(serializer.data, safe=False)
    #post方法没有传入pk值，且序列化器类实例化serializer的时候没有把instance作为参数传入，所以只能创建，不能更新
    def post(self, request):
        data = request.body.decode()
        data_dict = json.loads(data)

        serializer = Student5Serializer(data=data_dict)

        serializer.is_valid(raise_exception=True)
        #save方法不会触发serializer中的update
        instance = serializer.save()

        return JsonResponse(serializer.data)
class Student6View(View):
    def get(self, request):
        # 获取所有数据
        student_list = Student.objects.all()

        serializer = StudentModelSerializer(instance=student_list, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = request.body.decode()
        data_dict = json.loads(data)

        serializer = StudentModelSerializer(data=data_dict)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return JsonResponse(serializer.data)
