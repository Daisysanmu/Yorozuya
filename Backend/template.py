'''写入文件'''

'''
with open('./data/users/' + username + '.json', 'wb') as f:
    f.write(json.dumps(User, ensure_ascii=False, indent=2).encode('utf-8'))
    '''

'''读出文件'''

'''
with open('./data/users/'+ username +'.json', encoding='utf-8', ) as f:
    ret = json.load(f)
'''