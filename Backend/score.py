import json


'''用户积分奖励'''
def add_score(username):
    path = './data/users/users.json'

    with open(path, encoding='utf-8', ) as f:
        ret = json.load(f)
    oldscore = ret[username]["score"]
    newscore = oldscore + 10
    ret[username]["score"] =  newscore


    with open(path, 'wb') as f:
        ret = json.dumps(ret, ensure_ascii=False, indent=2).encode('utf-8')
        f.write(ret)

    return