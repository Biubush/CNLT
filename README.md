# 前言
## 针对情况
如果您是一位安大学子，您是否会收到以下情况的困扰：
当您兴致勃勃地打游戏、看电影、查资料等网络活动的途中，寝室Wifi突然自动断网，中断了您的工作？
您寝室的Wifi是否隔一段时间就会自动登出您的校园网账号？
您是否还在每次被强制注销下线后，反反复复地去重新登录上校园网账号？
## 提出需求
您是否渴望一个工具，解放您的双手，让校园网账号的登录不再繁琐，每次校园网被强制注销后，有一个脚本为您自动重连？
## 给出方案
**CNLT**就是这样一个自动化工具。它使用脚本，一旦您校园网被强制注销，就将自动为您重新登录，您在此期间无需动一根手指头。
# 直接使用看这
本程序已发布测试网站，**在连入了校园网的前提下**，您可以访问此链接[此链接](http://172.25.183.139:2220/)，以直接使用现成的WEB应用。一切的操作仅需照着网站指引来做即可。
# 技术人员看这
## 技术栈
前端:bootstrap
后端:python+flask
接口通信:jquery-ajax
配置存储:json
## 部署至您的服务器
### 部署环境
首先，您需要明白：**本脚本只有运行在校园网的网络环境中才能有效**。所以，您部署在自己服务器上的首要前提是，您的服务器可以连接校园网。
其次，您的服务器上需要安装python环境,flask模块
1. python环境安装
如果这个不会安装的话，您可能不是一个真正的技术人员（汗
2. flask模块安装
在您的服务器终端中输入以下代码
```shell
pip install flask
```
### 部署脚本
cd指令进入您想部署的文件夹，输入以下指令集
```shell
wget https://github.com/Biubush/CNLT/releases/download/cnlt/cnlt_beta_linux.tar.gz#下载脚本文件
tar -zxvf ./cnlt_beta_linux.tar.gz#解压
```
### 完善配置
脚本初始情况下是没有配置的，您需要先运行一遍才能修改配置文件：
```shell
python3 ./cnlt.py
```
提示创建默认文件后您可以输入以下指令进行配置项修改:
```shell
vim ./.cnlt/config.json
```
各字段详情：
1. mailServer
	在这里配置您的邮件服务器
    userName:填入你的smtp服务器的用户名（记得用引号）
    passWord:填入您的smtp服务器的密码（记得用引号）
    sender:填入发送者邮箱（记得用引号）
    senderName:填入发送者名称（记得用引号）
2. port
	在这里填你想部署的端口号，默认情况下已写6159
3. users
	除非您需要自己手动后台增删改查用户信息，否则不用管
### 启动脚本
再次使用以下命令，无报错就恭喜您启动成功！
```shell
python3 ./cnlt.py
```
# 免责声明
本WEB应用仅仅为测试程序，仅供学习，您可以从中学习到基础的前后端分离知识，和基础的Flask框架的语法知识。请于测试使用后的24小时内终止本WEB应用。本WEB应用仅存储但不泄露任何人的隐私信息。请合理测试本WEB应用，欲长期使用，后果自负。
