from flask import Flask, request, jsonify
import pandas as pd
import json
import os
from flask_cors import *
import Login
import question
import answer
import task
import preprocessing


app = Flask(__name__)
CORS(app, supports_credentials=True)




'''创建左侧菜单系列函数'''
def creatMenuObject(id, authName, path, children):
    dataObject = {}
    dataObject["id"] = id
    dataObject["authName"] = authName
    dataObject["path"] = path
    dataObject["children"] = children
    return dataObject


@app.route("/menus", methods=["GET"])
def getMenus():
    dataObjects = []
    dataObjects.append(creatMenuObject(125, "用户中心", "users",
                                       [creatMenuObject(110, "我的主页", "users", [])]))
    dataObjects.append(creatMenuObject(103, "委托浏览", "rights",
                                       [creatMenuObject(111, "问题委托", "questionlist", []),
                                        creatMenuObject(112, "任务委托", "tasklist", [])]))
    dataObjects.append(creatMenuObject(101, "我发布的", "goods",
                                       [creatMenuObject(104, "我的问题", "myquestion", []),
                                        creatMenuObject(115, "我的任务", "mytask", []),]))

    ret = {"data": dataObjects, "meta": {"msg": "获取菜单列表成功", "status": 200}}


    return ret



'''登录'''
@app.route("/login", methods=["GET"])
def login():

    args = request.args.to_dict()
    username = json.loads(args["form"])["username"]
    password = json.loads(args["form"])["password"]
    print("登录")
    ret = Login.login_f(username, password)

    print(ret)
    return ret






@app.route("/register", methods=["GET"])
def register():

    args = request.args.to_dict()
    username = json.loads(args["form"])["username"]
    password = json.loads(args["form"])["password"]
    print("注册")

    ret = Login.register_f(username,password)
    return ret


'''获取我的问题'''
@app.route("/myquestion", methods=["GET"])
def myquestions():
    args = request.args.to_dict()
    username = args["username"]
    ret = question.getList(username)
    return ret

'''获取我的任务'''
@app.route("/mytask", methods=["GET"])
def mytasks():
    args = request.args.to_dict()
    username = args["username"]
    ret = task.getmyTaskList(username)
    return ret

'''添加问题'''
@app.route("/addq", methods=["GET"])
def addq():
    args = request.args.to_dict()
    ret = question.addQuestion(args)
    return ret

'''发起（添加）任务'''
@app.route("/addt", methods=["GET"])
def addt():
    args = request.args.to_dict()
    ret = task.addTask(args)
    return ret


'''获取回答'''
@app.route("/getAnswer", methods=["GET"])
def getanswers():
    args = request.args.to_dict()
    q_id= args["q_id"]
    ret = answer.getAnswer(q_id)
    print(ret)
    return ret

'''结束问题 分配对应回答用户的赏金'''
@app.route("/endQuestion", methods=["GET"])
def chooseAnswer():
    args = request.args.to_dict()
    ret = question.endQuestion(args)
    return ret

'''结束任务 分配赏金到承接任务的用户'''
@app.route("/endTask", methods=["GET"])
def endMyTask():
    args = request.args.to_dict()
    t_id = args['t_id']
    ret = task.endTask(t_id)
    return ret

'''浏览所有任务委托列表'''
@app.route("/taskList", methods=["GET"])
def getTasks():
    args = request.args.to_dict()
    num = int(args["pagenum"])
    size = int(args["pagesize"])
    ret = {"data": task.getTaskList(num, size), "meta": {"msg": "获取成功", "status": 200}}
    return ret

'''接受任务委托'''
@app.route("/takeTask", methods=["GET"])
def takeTask():
    args = request.args.to_dict()
    id = int(args["taskId"])
    receiver = args["receiver"]
    ret = {"data": task.takeTask_f(id, receiver), "meta": {"msg": "获取成功", "status": 200}}
    return ret

'''浏览所有问题委托列表'''
@app.route("/questionList", methods=["GET"])
def getQuestions():
    args = request.args.to_dict()
    num = int(args["pagenum"])
    size = int(args["pagesize"])
    ret = {"data": question.getAllList(num, size), "meta": {"msg": "获取成功", "status": 200}}
    return ret

'''添加回答'''
@app.route("/addAnswer", methods=["GET"])
def addAnswer():
    args = request.args.to_dict()
    ret = answer.addAnswer(args)
    return ret

@app.route("/getUserInfo", methods=["GET"])
def getUserInfo():
    args = request.args.to_dict()
    username = args["username"]
    ret = {"data": Login.getUserByName(username), "meta": {"msg": "获取成功", "status": 200}}
    return ret

@app.route("/editUser", methods=["GET"])
def editUser():
    args = request.args.to_dict()
    username = args["username"]
    data=json.loads(args["data"])
    Login.editUser(username,data)
    ret = {"meta": {"msg": "获取成功", "status": 200}}
    return ret

if __name__ == '__main__':


    app.run()
