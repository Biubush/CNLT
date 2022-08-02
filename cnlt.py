#---------------------------------------导包------------------------------------
from flask import Flask,render_template,jsonify,request
import threading,json,os,smtplib,requests as Requests
from email.mime.text import MIMEText
from email.header import Header

#-----------------------------------自定义函数----------------------------------
def start_thread(target,kwargs:dict):#启动线程
    threading.Thread(target=target,kwargs=kwargs).start()

def get_mid_str(s, start_str, stop_str):#取中间文本
    start_pos = s.find(start_str)
    if start_pos == -1:
        return None
    start_pos += len(start_str)
    stop_pos = s.find(stop_str, start_pos)
    if stop_pos == -1:
        return None
    return s[start_pos:stop_pos]

def sendMail(Receivers:list,receiversName,Title,wholeText):#发送邮件函数
    #发送邮箱函数，Receivers为所有收信的邮箱数组，类型为list
    mail_host='smtp.qq.com'
    mail_user=mailServer["userName"]
    mail_pass=mailServer["passWord"]
    sender = mailServer["sender"]
    receivers = Receivers
    message = MIMEText(wholeText, 'plain', 'utf-8')
    message['From'] = Header(mailServer["senderName"], 'utf-8')
    message['To'] =  Header(receiversName, 'utf-8')
    message['Subject'] = Header(Title, 'utf-8')
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print(Receivers[0]+"用户邮件发送成功")
        return True
    except smtplib.SMTPException:
        print(Receivers[0]+"用户邮件发送失败")
        return False

def loadConfig():#返回当前的配置，类型为dict
    with open(configPath, "r",encoding='utf-8') as configFile:
        rawData = json.load(configFile)
    return rawData

def addUser(inurl,mail):#向配置中增加新用户
    userData={
        "loginUrl" : inurl,
        "mailAdress" : mail,
        "times":0
    }
    rawData=loadConfig()
    rawData["users"].append(userData)
    with open(configPath, 'w',encoding='utf-8') as write_f:
	    write_f.write(json.dumps(rawData, indent=4, ensure_ascii=False))

def addTimes(mail):#在配置文件中，给指定用户的次数+1，返回当前此用户次数
    nowData=loadConfig()
    users=nowData["users"]
    for user in users:
        if user["mailAdress"]==mail:
            user["times"]+=1
            with open(configPath, 'w',encoding='utf-8') as write_f:
                write_f.write(json.dumps(nowData, indent=4, ensure_ascii=False))
            return user["times"]
        else:
            pass
            
def loginAPP(inurl,mail):#校园网登录程序
    exist=True
    while exist:
        try:
            inRes=Requests.get(url=inurl).text
            resCode=get_mid_str(inRes,'result":"', '","ms')
            if resCode == "1":
                nowTimes=str(addTimes(mail))
                sendMail([mail],"CNLT用户","自动登录"+nowTimes+"次","自CNLT工作以来，本WEB应用已经为您自动登录了"+nowTimes+"次校园网，感谢您的支持与信赖")
            else:
                pass
        except:
            break
        if ifexist(mail):
            pass
        else:
            exist=False
    print("用户"+mail+"的线程已终止")

def ifexist(mail):#判断配置中是否已存在用户，返回布尔值
    nowUsers=loadConfig()["users"]
    for use in nowUsers:
        if use["mailAdress"]==mail:
            return True
        else:
            pass
    return False

def startup():#初始化函数
    if os.path.exists(configPath):
        global mailServer
        mailServer=loadConfig()["mailServer"]
        global port
        port=loadConfig()["port"]
        if mailServer["passWord"]!=None:
            users=loadConfig()["users"]
            for user in users:
                insertArgs={
                    "inurl":user["loginUrl"],
                    "mail":user["mailAdress"]
                }
                start_thread(loginAPP,insertArgs)
            print("所有用户脚本启动成功")
            print("当前邮件服务器配置为：")
            print(mailServer)
            return True
        else:
            print("邮件服务器未配置！")
    else:
        print("未找到配置文件，将创建默认配置文件")
        os.mkdir("./.cnlt/")
        with open(configPath, 'w',encoding='utf-8') as write_f:
	        write_f.write(json.dumps(defaultConfig, indent=4, ensure_ascii=False))

#------------------------------------全局变量池---------------------------------
configPath="./.cnlt/config.json"
defaultConfig={
    "users":[
    ],
    "mailServer":{
        "userName":None,
        "passWord":None,
        "sender":None,
        "senderName":None
    },
    "port":"6159"
}
port=None
mailServer=None
flag=1

#-----------------------------------flask固定语法-------------------------------
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#-------------------------------------路由绑定----------------------------------
@app.route('/')#根目录
def index():
    return render_template('index.html')

@app.route('/instruction')#教程
def instruction():
    return render_template('instruction.html')

@app.route('/test')#根目录
def test():
    return render_template('test.html')

@app.route('/pause')#根目录
def pause():
    return render_template('pause.html')
#--------------------------------------api接口----------------------------------
@app.route('/count')#获取当前用户数
def getCount():
    rawDict=loadConfig()
    return jsonify(len(rawDict["users"]))

@app.route('/submit',methods=["POST"])#提交用户数据
def verify():
    loginUrl = request.form.getlist("loginUrl")[0]
    mailAdress = request.form.getlist("mailAdress")[0]
    print(loginUrl+"\n"+mailAdress)
    if ifexist(mailAdress)==False:
        try:
            inRes=Requests.get(loginUrl,timeout=10).text
            print(inRes)
            if inRes.find('dr1003') != -1:
                addUser(loginUrl,mailAdress)
                insertArgs={
                    "inurl":loginUrl,
                    "mail":mailAdress
                }
                print(insertArgs)
                start_thread(loginAPP,insertArgs)
                return jsonify("成功")
            else:
                return jsonify("登录地址非安大校园网登录地址")
        except:
            return jsonify("登录地址非法")
    else:
        return jsonify("用户已存在")

@app.route('/remove',methods=["POST"])#获取当前用户数
def remove():
    getMail=request.form.getlist("mail")[0]
    print(getMail)
    rawdata=loadConfig()
    users=rawdata["users"]
    for user in users:
        index=users.index(user)
        print(user["mailAdress"]+'|'+getMail+"|"+str(user["mailAdress"]==getMail))
        if user["mailAdress"]==getMail:
            del users[index]
            with open(configPath, 'w',encoding='utf-8') as write_f:
                write_f.write(json.dumps(rawdata, indent=4, ensure_ascii=False))
            return jsonify("删除"+getMail+"成功")
        else:
            pass
    return jsonify("未找到此用户")
#--------------------------------------测试api----------------------------------
@app.route('/inurl')#模拟登录URL1
def testapi1():
    global flag
    if flag == 1:
        flag = 0
        return 'dr1003({"result":"1","msg":"\u8ba4\u8bc1\u6210\u529f"})'
    else:
        return 'dr1003({"result":"0","msg":"\u8ba4\u8bc1\u6210\u529f"})'

@app.route('/outurl')#模拟注销URL
def testapi3():
    global flag
    flag = 1
    return 'dr1004({"result":"1","msg":"\u6ce8\u9500\u6210\u529f"})'

@app.route('/flag')#手动更改登录URL的返回值
def testapi4():
    global flag
    if flag == 1:
        flag = 0
    else:
        flag = 1

#-----------------------------------flask启动程序-------------------------------
if __name__ == '__main__':
    if startup():
        app.run('0.0.0.0', port)
    else:
        pass