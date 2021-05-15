import json
import os
import score


'''登录验证阶段'''

def login_f(username,password):

    res = check(username, password)

    User = {}
    User["username"] = username
    User["password"] = password
    User["token"] = username


    if res == 1:

        ret = {"data": User, "meta": {"msg": "登录成功", "status": 200}}

    elif res == 2:
        ret = {"data": -2, "meta": {"msg": "密码错误", "status": 100}}
    else:
        ret = {"data": -3, "meta": {"msg": "用户不存在", "status": 100}}

    print(ret)
    return ret


def check(username, password):

    flag = True
    with open('./data/users/users.json', encoding='utf-8', ) as f:
        users = json.load(f)
        for i in users:
            if users[i]["username"] == username and users[i]["password"] == password:
                print("密码正确")
                return 1
            elif users[i]["username"] == username and users[i]["password"] != password:
                print("密码错误")
                return 2
        print("用户不存在，请注册")
        return 3





'''注册用户阶段'''
def createUser(username, password):
    User = {
        "username": "admin",
        "password": 123456,
        "score":100,
        "token": "admin",
        "balance": 100,
        'email': '',
        'phone': '',
        'nickname': ''
    }
    User['username'] = username
    User['password'] = password
    User['token'] = username
    return User


def register_f(username,password):

    User = createUser(username,password)
    with open('./data/users/users.json', encoding='utf-8', ) as f:
        newfile = json.load(f)
        newfile[username] = User
    with open('./data/users/users.json', 'wb') as f:
        f.write(json.dumps(newfile, ensure_ascii=False, indent=2).encode('utf-8'))

    '''注册用户时创建对应用户的发起问题委托文件'''
    newfile = {}
    with open('./data/questions/' + username + '.json', 'wb') as f:
        f.write(json.dumps(newfile, ensure_ascii=False, indent=2).encode('utf-8'))

    ret = {"data": "success!", "meta": {"msg": "注册成功", "status": 200}}
    return ret

def editUser(username,values):
    with open('./data/users/users.json', encoding='utf-8', ) as f:
        newfile = json.load(f)
        newfile[username]['email']=values['email']
        newfile[username]['phone']=values['phone']
        newfile[username]['nickname']=values['nickname']
    with open('./data/users/users.json', 'wb') as f:
        f.write(json.dumps(newfile, ensure_ascii=False, indent=2).encode('utf-8'))

def getUserByName(username):
    with open('./data/users/users.json', encoding='utf-8', ) as f:
        users = json.load(f)
        return users[username]

