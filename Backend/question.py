import json
import datetime



'''q_id配置'''
def getId():

    '''获取已分配q_id'''
    with open('./data/id/q_id.json', encoding='utf-8', ) as f:
        file = json.load(f)
        q_id = file["q_id"]

    '''保存新的q_id'''
    newid = q_id + 1
    file["q_id"] = newid
    with open('./data/id/q_id.json', 'wb') as f:
        f.write(json.dumps(file, ensure_ascii=False, indent=2).encode('utf-8'))

    return q_id



'''获得该用户所有问题列表'''
def getList(username):

    total = 0
    with open('./data/questions/' + username + '.json', encoding='utf-8', ) as f:
        qlist = json.load(f)
    array = []
    for i in qlist:
        total += 1
        array.append(qlist[i])
    ret = {"data": array, "meta": {"msg": "获取问题列表成功", "status": 200}, "total": total}
    return ret

'''添加问题'''
def addQuestion(form):

    q_id = getId()
    q_id += 1

    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    create_time = year + '-' + month + '-' +day

    newq = {}
    newq["id"] = q_id
    newq["theme"] = form["theme"]
    newq["reward"] = form["reward"]
    newq["isfinished"] = 0
    newq["create_time"] = create_time
    newq["detail"] = form["detail"]
    newq["tag"] = form["tag"]
    username = form["username"]

    '''前置条件检测 用户账户余额是否充足'''
    with open('./data/users/users.json', encoding='utf-8', ) as f:
        newfile = json.load(f)
        if newfile[username]["balance"] < int(newq["reward"]):
            ret = {"data": "fail", "meta":{"msg": '余额不足', "status":300}}
            return ret
        else :
            newfile[username]["balance"] -= int(newq["reward"])

    with open('./data/users/users.json', 'wb') as f:
        f.write(json.dumps(newfile, ensure_ascii=False, indent=2).encode('utf-8'))

    '''添加问题到该用户文件下'''
    with open('./data/questions/' + username + '.json', encoding='utf-8', ) as f:
        newfile = json.load(f)
    newfile[q_id] = newq

    with open('./data/questions/' + username + '.json', 'wb') as f:
        f.write(json.dumps(newfile, ensure_ascii=False, indent=2).encode('utf-8'))

    '''添加问题到总问题文件下'''
    with open('./data/questions/total.json', encoding='utf-8', ) as f:
        newfile = json.load(f)
    newfile[q_id] = newq

    with open('./data/questions/total.json', 'wb') as f:
        f.write(json.dumps(newfile, ensure_ascii=False, indent=2).encode('utf-8'))

    '''还需要创建对应的回答文件'''
    newfile = {}
    with open('./data/answers/' + str(q_id) + '.json', 'wb') as f:
        f.write(json.dumps(newfile, ensure_ascii=False, indent=2).encode('utf-8'))

    ret = {"data": q_id, "meta":{"msg": '添加问题成功', "status":200}}
    return ret


'''结束问题 分配赏金'''
def endQuestion(form):
    q_user = form['q_user']
    q_id = form['q_id']
    a_user = form['a_user']
    a_id = form['a_id']

    '''修改该用户提问问题状态'''
    q_path = './data/questions/' + q_user + '.json'
    with open(q_path, encoding='utf-8') as f:
        questionlist = json.load(f)
        questionlist[q_id]['isfinished'] = 1
        '''读取该问题reward'''
        reward = questionlist[q_id]['reward']

    '''保存修改后状态'''
    with open(q_path, 'wb') as f:
        temp = json.dumps(questionlist, ensure_ascii=False, indent=2).encode('utf-8')
        f.write(temp)



    '''修改总问题文件下该问题状态'''
    q_path = './data/questions/total.json'
    with open(q_path, encoding='utf-8') as f:
        questionlist = json.load(f)
        questionlist[q_id]['isfinished'] = 1

    '''保存修改后状态'''
    with open(q_path, 'wb') as f:
        temp = json.dumps(questionlist, ensure_ascii=False, indent=2).encode('utf-8')
        f.write(temp)

    '''分配赏金到对应用户'''
    userpath = "./data/users/users.json"
    with open(userpath, encoding='utf-8') as f:
        userlist = json.load(f)

    userlist[a_user]['balance'] = userlist[a_user]['balance'] + int(reward)
    with open(userpath, 'wb') as f:
        temp = json.dumps(userlist, ensure_ascii=False, indent=2).encode('utf-8')
        f.write(temp)

    '''设置问题对应最佳答案的属性'''
    anspath = "./data/answers/" + q_id + ".json"
    with open(anspath, encoding='utf-8') as f:
        anslist = json.load(f)

    anslist[a_id]['isbest'] = 1
    with open(anspath, 'wb') as f:
        temp = json.dumps(anslist, ensure_ascii=False, indent=2).encode('utf-8')
        f.write(temp)


    ret = { "data": "success", "meta": {"msg": "结束问题并设置最佳答案成功", "status": 200}}
    return ret


'''获取全部问题委托列表'''
def getAllList(pagenum,pagesize):
    with open('./data/questions/total.json', encoding='utf-8', ) as f:
        qlist = json.load(f)
    array = []
    index=0
    for i in qlist:
        if index>=pagenum*pagesize:
            break
        if index>=(pagenum-1)*pagesize:
            array.append(qlist[i])
        index+=1
    total=len(qlist)
    ret = {"questionList": array, "pagenum": pagenum, "total": total}
    return ret