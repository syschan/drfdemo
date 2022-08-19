from django.urls import path, re_path
from collect import views

urlpatterns = [
    # jwt认证
    path("login/",views.LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('getUserInfo/', views.GetUserInfoTokenVerifyView.as_view(), name='token_verify'),
    #自定义认证
    path('auth/', views.AuthDemoAPIView.as_view()),
    # 不要在同一个路由的as_view中书写两个同样的键的http请求，会产生覆盖！！！
    # ViewSet,自定义get方法
    path('student1/', views.Student1ViewSet.as_view({"get": "get_5"})),
    path('student1/get_5_girl/', views.Student1ViewSet.as_view({"get": "get_5_girl"})),
    re_path(r'^student1/(?P<pk>\d+)/$', views.Student1ViewSet.as_view({"get": "get_one"})),
    # ViewSet+GenericAPIView,自定义get方法
    path('student2/', views.Student2ViewSet.as_view({"get": "get_5"})),
    path('student2/get_5_girl/', views.Student2ViewSet.as_view({"get": "get_5_girl"})),
    re_path(r'^student2/(?P<pk>\d+)/$', views.Student2ViewSet.as_view({"get": "get_one"})),
    # GenericViewSet,自定义get方法
    path('student3/', views.Student3GenericViewSet.as_view({"get": "get_5"})),
    path('student3/get_5_girl/', views.Student3GenericViewSet.as_view({"get": "get_5_girl"})),
    # GenericViewSet，可以和模型类进行组合快速生成基本的API接口，继承Mixin中的list和create方法，不在支持自定义
    path("students4/", views.Student4GenericViewSet.as_view({"get": "list", "post": "create"})),
    # ModelViewSet 默认提供了5个API接口，继承Mixin中的list/create/retrieve/update/destroy方法，不在支持自定义
    path("students5/", views.Student5ModelViewSet.as_view({"post": "create", "get": "list"})),
    re_path(r"^students5/(?P<pk>\d+)/$", views.Student5ModelViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    # ReadOnlyModelViewSet  继承Mixin中的list/retrieve方法，不在支持自定义
    path("students6/", views.Student6ReadOnlyModelViewSet.as_view({"get": "list"})),
    re_path(r"^students6/(?P<pk>\d+)/$", views.Student6ReadOnlyModelViewSet.as_view({"get": "retrieve"})),

    # 如果是ModelViewSet需要重新get方法，则需要在此处追加路由，追加的路由会覆盖ModelViewSet在router中注册的路由
    path("student7/", views.Student7ModelViewSet.as_view({"get": "get_all"})),

    
    #re_path(r"^student7/(?P<pk>\d+)/$", views.Student7ModelViewSet.as_view({"get": "get_7"})),


    # 一个视图类中调用多个序列化器，重新get和post方法，不带pk值
    path("student8/", views.Student8GenericAPIView.as_view()),

    # 一个视图集中调用多个序列化器，只定义了get方法带pk和不带pk；其他方法post、put和delete方法未定义，不可用
    path("student9/", views.Student9ModelViewSet.as_view({"get": "list"})),
    re_path(r"^student9/(?P<pk>\d+)/$", views.Student9ModelViewSet.as_view({"get": "retrieve"})),
]


"""
有了视图集以后，视图文件中多个视图类可以合并成一个，但是，路由的代码就变得复杂了，
需要我们经常在as_view方法 ,编写http请求和视图方法的对应关系，
事实上，在路由中，DRF也提供了一个路由类给我们对路由的代码进行简写。
当然，这个路由类仅针对于 视图集 才可以使用。
"""

# 路由类默认只会给视图集中的基本5个API生成地址[ 获取一条，获取多条，添加.删除,修改数据 ]
from rest_framework.routers import DefaultRouter
# 实例化路由类
router = DefaultRouter()
# router.register("访问地址前缀","视图集类","访问别名")
# 注册视图视图集类
router.register("student7", views.Student7ModelViewSet)

# 把路由列表注册到django项目中
urlpatterns += router.urls
