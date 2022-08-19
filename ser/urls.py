from django.urls import path, re_path
from ser import views

urlpatterns = [
    #student：带pk值
    # 继承原生view，在get方法中传入pk值获取model对象，生成序列化实例serializer(字典)，通过Django原生的JsonResponse返回一条数据
    re_path(r"^student/(?P<pk>\d+)/", views.Student1View.as_view()),
    #student2：
    # 继承原生view，在get方法中获取model所有对象(可带过滤条件)，生成序列化实例serializer(字典)，通过Django原生的JsonResponse返回多条数据
    path("student2/", views.Student2View.as_view()),
    #student3：
    # 在序列化器中定义验证方法，继承原生view，在post方法中传入request，解析body中的data并将通过反序列化得到的json数据传入序列化器类，
    # 生成序列化实例serializer，调用Student3Serializer中定义的方法依次作选项验证、单个字段验证、多个字段验证，
    # 最后将验证后的数据validated_data作为参数通过Django原生的JsonResponse返回
    path('student3/', views.Student3View.as_view()),
    #student4：
    # 反序列化阶段，带pk值
    re_path(r'^student4/(?P<pk>\d+)/$', views.Student4View.as_view()),
    #student5：
    # 一个序列化器同时实现序列化和反序列化，不带pk值
    path('student5/', views.Student5View.as_view()),
    #student6：
    # 使用模型类序列化器
    path('student6/', views.Student6View.as_view()),
]
