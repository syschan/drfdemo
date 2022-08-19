# Create your views here.
from rest_framework.viewsets import ModelViewSet
from students.models import Student
from students.serializers import StudentModelSerializer


class StuentAPIView(ModelViewSet):
    queryset = Student.objects.all()  # queryset 指明该视图集在查询数据时使用的查询集
    serializer_class = StudentModelSerializer  # serializer_class 指明该视图在进行序列化或反序列化时使用的序列化器
