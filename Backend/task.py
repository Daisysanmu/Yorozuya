import json
import os

path = 'data/tasks'



'''新建任务'''
def createTask(id, theme, reward,  ddl, detail, owner):
    obj = {"id": id, "theme": theme, "reward": reward, "isTaken": 0, "ddl": ddl, "detail": detail,
           "owner": owner, "receiver": "", "isfinished": 0}
    return obj


'''获取已分配id'''
def getId():
    '''获取已分配t_id'''
    with open('./data/id/t_id.json', encoding='utf-8', ) as f:
        file = json.load(f)
        t_id = file["t_id"]

    '''保存新的t_id'''
    t_id = t_id + 1
    file["t_id"] = t_id
    with open('./data/id/t_id.json', 'wb') as f:
        f.write(json.dumps(file, ensure_ascii=False, indent=2).encode('utf-8'))

    return t_id


'''创建任务'''
def createTask_f(theme, price, isTaken, ddl, detail, owner):
    id = getId()
    task = createTask(id, theme, price, isTaken, ddl, detail, owner)

    with open('./data/tasks/' + str(id) + '.json', 'wb') as f:
        f.write(json.dumps(task, ensure_ascii=False, indent=2).encode('utf-8'))
    ret = {"data": task, "meta": {"msg": "创建任务成功", "status": 200}}
    return ret


'''获取所有任务列表'''
def getTaskList(pageNum, pageSize):
    taskList = []
    fileList = os.listdir("./data/tasks")
    total = len(fileList)
    index = 0
    for file in fileList:
        if file.split(".")[1] == 'json':
            if (pageNum - 1) * pageSize <= index < pageSize * pageNum:
                index += 1
                with open('./data/tasks/' + file, "r", encoding='utf-8') as f:
                    obj = json.load(f)
                    taskList.append(obj)
    data = {"taskList": taskList, "pagenum": pageNum, "total": total}
    print(data)
    return data

'''承接任务'''
def takeTask_f(id, recevier):
    fileList = os.listdir("./data/tasks")
    flag = 0
    for file in fileList:
        if file == str(id) + '.json':
            f = open('./data/tasks/' + file, "r", encoding='utf-8')
            obj = json.load(f)
            obj["isTaken"] = 1
            obj["receiver"] = recevier
            print(obj)
            f = open('./data/tasks/' + file, "wb")
            f.write(json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8'))
            break
    return flag


'''获取我的任务列表'''
def getmyTaskList(username):
    mytaskList = []
    total = 0
    fileList = os.listdir("./data/tasks")
    for file in fileList:
        with open('./data/tasks/' + file, "r", encoding='utf-8') as f:
            obj = json.load(f)
            if obj['owner'] == username :
                total += 1
                mytaskList.append(obj)
    ret= {"data": mytaskList, "meta": {"msg": "获取成功", "status":200}, "total": total}
    print(ret)
    return ret


'''确认结束我的任务 分配赏金'''
'''结束问题 分配赏金'''
def endTask(t_id):

    t_id = t_id
    '''修改该任务状态'''
    t_path = './data/tasks/' + t_id + '.json'
    with open(t_path, encoding='utf-8') as f:
        task = json.load(f)
        task['isfinished'] = 1
        '''读取该问题reward'''
        reward = task['reward']
        '''读取该问题承接用户'''
        receiver = task['receiver']


    '''保存修改后状态'''
    with open(t_path, 'wb') as f:
        temp = json.dumps(task, ensure_ascii=False, indent=2).encode('utf-8')
        f.write(temp)

    if receiver == '':
        ret = {"data": "success", "meta": {"msg": "确认结束任务成功（任务未被承接）", "status": 200}}
        return ret



    '''分配赏金到承接任务用户'''
    userpath = "./data/users/users.json"
    with open(userpath, encoding='utf-8') as f:
        userlist = json.load(f)

    userlist[receiver]['balance'] = userlist[receiver]['balance'] + int(reward)
    with open(userpath, 'wb') as f:
        temp = json.dumps(userlist, ensure_ascii=False, indent=2).encode('utf-8')
        f.write(temp)


    ret = { "data": "success", "meta": {"msg": "确认结束任务成功", "status": 200}}
    return ret


'''添加新发起的任务'''
def addTask(form):

    t_id = getId()

    username = form['owner']
    newt = createTask(t_id, form['theme'], form['reward'], form['ddl'], form['detail'], form['owner'])


    '''前置条件检测 用户账户余额是否充足'''
    with open('./data/users/users.json', encoding='utf-8', ) as f:
        newfile = json.load(f)
        if newfile[username]["balance"] < int(newt["reward"]):
            ret = {"data": "fail", "meta":{"msg": '余额不足', "status":300}}
            return ret
        else :
            newfile[username]["balance"] -= int(newt["reward"])

    with open('./data/users/users.json', 'wb') as f:
        f.write(json.dumps(newfile, ensure_ascii=False, indent=2).encode('utf-8'))


    '''写入新任务信息文件'''
    with open('./data/tasks/' + str(t_id) + '.json', 'wb') as f:
        f.write(json.dumps(newt, ensure_ascii=False, indent=2).encode('utf-8'))


    ret = {"data": 'success', "meta":{"msg": '添加问题成功', "status":200}}
    return ret