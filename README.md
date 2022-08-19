# drfdemo
# Django_Rest_Framework学习
## 参考资料
### 博客园|归来人少年|Django-DRF入门| https://www.cnblogs.com/jx-zzc/p/16519729.html
### B站|编程小绿屋|2022全B站最牛逼的DRF（Django-restframework）课程| https://www.bilibili.com/video/av338968990

# 学习步骤
## step1：刷了一遍B站的视频
### 目标————先对DRF有个印象，了解一些基础概念和名称，了解创建项目和应用的流程，了解项目目录构成、各个文件的功能及其相互关系。

## step2：参考博客园的资料，从头复制粘贴确保所有学习代码能跑起来。
### 目标————通过代码加深对DRF的理解，熟悉整个运作流程，特别是模型、序列化器、视图、路由、配置文件中有些什么内容

## step3：从头再手敲一遍参考资料的代码，完成第一遍的复习；同时，继续刷B站其它DRF的视频教程
### 目标————深入理解DRF并实操代码，能够说得出来数据流和代码块的功能及其写法。

## step4：试着做小作业或者项目中的小demo
### 目标————按照简单需求独立完成一个或多个应用的API接口编写

## step5：将DRF切入已有项目或者自拟项目
### 目标————能够根据项目实际需求快速开发出相应的API接口



-----------------------------------------
git操作步骤
1 初始化git：
...drfdemo>git init

2 添加git账号配置：
...drfdemo>git config --global user.email "your github emailXX@XX.com"
...drfdemo>git config --global user.name "your github nameXXX"

3 添加git文件到暂存区：
3.1添加当前drfdemo目录下的所有文件
...drfdemo>git add .
3.2添加当前目前下制定文件
...drfdemo>git add xxx/xxx.xxx

4 切换分支到main上：
...drfdemo>git branch -M main

5 提交git文件到工作区
...drfdemo>git commit -m '注释说明'

6 github创建仓库drfdemo：
https://github.com/yournameXXX/drfdemo.git

7 添加仓库地址到远程origin：
...drfdemo>git remote add origin https://github.com/yournameXXX/drfdemo.git

8 推送代码到github远程仓库上：
...drfdemo>git push -u origin main
