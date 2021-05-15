import json
import preprocessing
import score

'''a_id配置'''
def getId():
    '''获取已分配a_id'''
    with open('./data/id/a_id.json', encoding='utf-8', ) as f:
        file = json.load(f)
        a_id = file["a_id"]

    '''保存新的a_id'''
    newid = a_id + 1
    file["a_id"] = newid
    with open('./data/id/a_id.json', 'wb') as f:
        f.write(json.dumps(file, ensure_ascii=False, indent=2).encode('utf-8'))

    return a_id

def getAnswer(q_id):

    with open('./data/answers/' + q_id + '.json', encoding='utf-8', ) as f:
        alist = json.load(f)
    rets = []
    for i in alist:
        rets.append(alist[i])
    ret = {"data": rets, "meta": {"msg": "获取问题列表成功", "status": 200}}
    return ret

def addAnswer(form):
    a_id = getId()
    a_id += 1

    newa = {}
    newa["id"] = a_id
    newa["username"] = form["username"]
    newa["detail"] = form["detail"]
    newa["q_id"] = form["q_id"]
    newa["isbest"] = 0
    q_id = form["q_id"]

    '''检测有无敏感词汇'''
    content = form['detail']
    if not preprocessing.check(content):
        msg = "添加回答失败，有敏感词"
        status = 101
        ret = {"data": a_id, "meta": {"msg": msg, "status": status}}
        return ret

    '''增加回答用户的积分'''
    score.add_score(form['username'])

    '''添加回答到该问题文件下'''
    with open('./data/answers/' + q_id + '.json', encoding='utf-8', ) as f:
        newfile = json.load(f)
    newfile[a_id] = newa

    with open('./data/answers/' + q_id + '.json', 'wb') as f:
        f.write(json.dumps(newfile, ensure_ascii=False, indent=2).encode('utf-8'))

    ret = {"data": a_id, "meta":{"msg": '添加回答成功', "status":200}}
    return ret
