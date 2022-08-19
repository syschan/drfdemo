from rest_framework import serializers
from students.models import Student


# 创建序列化器类，回头会在视图中被调用
class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student  # model 指明该序列化器处理的数据字段从模型类Student参考生成
        fields = "__all__"  # fields 指明该序列化器包含模型类中的哪些字段，'all'指明包含所有字段
        # fields = ("id", "name")  # 也可指定字段
