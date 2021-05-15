#!/usr/bin/env python 
# -*- coding:utf-8 -*-

"""
we select two kinds of tokenization tools: jieba and HanLP
basic considerations:
(1)idiom  紫气东来  fool不行 pyhanlp和jieba比较好
(2)specialized noun 工藤新一 jieba不行 fool 不行  pyhannlp比较好
(3)emoji  ....
(4)internet slang 爷青结 爷的青春还在 pyhanlp fool不行 jieba比较好
-------------------------------------------------------------
(1)添加专有名词词典
(2)添加网络用语词典
(3)文档相似性的定义采用重合汉字的数量，输入文本必须要去除停用词，同时使用word2vector作为初始化
(4)可以尝试采用自注意力机制学习文本的表示向量
(5)直接采用hanLP，不用添加JieBa，可以尝试使用新词发现技术
--------------------------------------------------------------
用word2vec将文档中的单词训练成向量时要注意的点：
1. 不需要去除停用词。目前word2vec较好的方法是Negative Sampling，论文中提出该方法为了应对停用词，会进行subsampling，具体可见论文。
2. 需要去除语料库中出现次数过少的词。
3. 向量维度通常设50-200维。
4. 论文实验中显示，负采样次数取15次时效果略好于5次；Negative Sampling方法比哈夫曼树的方法准确度高。
————————————————-------------------------------
可以尝试一下使用单词的表示向量作为输入
"""

import pandas as pd
from pyhanlp import *
from jpype import *
import os
import json
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.font_manager import *


cixing=['cc','e','uj','vshi','rz','ule','vyou','p','ulian','pba',
        'rzv','pbei','usuo','uv','u','uz','ud','uzhe','r','ude1','uzhi',
        'rg','ude2','ude3','rr','ry','udh','ug','y','yg','wd','wyz','wyy','wm','wf','w','ule','d']


corpus = pd.DataFrame(columns=['id', 'progress', 'mode', 'fontsize', 'color'
    , 'midHash', 'content', 'ctime', 'idStr'])

# high-level tools for NLP tasks
CRFSegment = HanLP.newSegment("crf").enableJapaneseNameRecognize(True).enableNameRecognize(True) \
    .enableTranslatedNameRecognize(True).enableNumberQuantifierRecognize(True) \
    .enableOrganizationRecognize(True).enablePlaceRecognize(True)
PerceptronSegment = HanLP.newSegment("perceptron").enableJapaneseNameRecognize(True).enableNameRecognize(True) \
    .enableTranslatedNameRecognize(True).enableNumberQuantifierRecognize(True) \
    .enableOrganizationRecognize(True).enablePlaceRecognize(True)

StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
BasicTokenizer = JClass('com.hankcs.hanlp.tokenizer.BasicTokenizer')
IndexTokenizer = JClass('com.hankcs.hanlp.tokenizer.IndexTokenizer')
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
NotionalTokenizer = JClass('com.hankcs.hanlp.tokenizer.NotionalTokenizer')
SpeedTokenizer = JClass('com.hankcs.hanlp.tokenizer.SpeedTokenizer')

# global configuration
HanLP.Config.Normalization = True  # 大写转小写，全角转半角，繁体转简体
HanLP.Config.ShowTermNature = True  # 关闭词性


def DBC2SBC(ustring):
 rstring =""
 for uchar in ustring:
  inside_code = ord(uchar)
  if inside_code == 0x3000:
   inside_code = 0x0020
  else:
   inside_code -= 0xfee0
  if not (0x0021 <= inside_code and inside_code <= 0x7e):
   rstring += uchar
   continue
  rstring += chr(inside_code)
 return rstring


def strB2Q(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 32:  # 全角空格直接转换
                inside_code = 12288
            elif (inside_code >= 33 and inside_code <= 126):  # 全角字符（除空格）根据关系转化
                inside_code += 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)


def str_preprocess(string):
    stringlist=strB2Q(string.lower())
    return stringlist


def traverse_dir(root_dir):    # 遍历所有视频目录并保存所有视频目录路径
    dir_list = []
    list_dirs = os.walk(root_dir)
    for root, dirs, files in list_dirs:
        for d in dirs:
            dir_list.append(os.path.join(root, d))
    return dir_list


def load_from_file(path):
    """
    从词典文件加载DoubleArrayTrie
    :param path: 词典路径
    :return: 双数组trie树
    """
    map = JClass('java.util.TreeMap')()  # 创建TreeMap实例
    with open(path, encoding="UTF-8") as src:
        for word in src:
            word = word.strip()  # 去掉Python读入的\n
            map[word] = word
    return JClass('com.hankcs.hanlp.collection.trie.DoubleArrayTrie')(map)


#停用词表
#trie = load_from_file(HanLP.Config.CoreStopWordDictionaryPath)
def read_in(filepath):
    """
    从弹幕数据文件加载弹幕
    :param filepath: path of data file
    :return:dataframe format of danmaku data
    """
    f = open(filepath, "r", encoding="UTF-8")
    #print(json.load(f))
    t = json.load(f)
    #print(t)
    file = pd.DataFrame(t)
    return file


def dict_save(filename, data):
    file = open(filename,'w',encoding="UTF-8")
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存成功")


def dict_load(filename):
    file = open(filename,'r',encoding="UTF-8")
    data=file.readlines()
    for i,line in enumerate(data):
       data[i]=line.strip('\n')
    file.close()
    return data


def stralter(jstr):
    """
    Java字符串转python列表
    :param jstr:
    :return:jstr:
    """
    tmp=list(jstr)
    return [str(i) for i in tmp]


# word2vec的训练一般不需要去除停用词
def tokenization(text, tokenizer):
    """
    :param data:
    :param tokenizer:
    :return:
    """
    text=text.drop_duplicates()
    x = []
    ripedata=[str_preprocess(danmu)for danmu in text['content'].tolist()]
    for i,danmu in enumerate(ripedata):
        jstr = stralter(tokenizer.segment(danmu))
        jstr=remove_stopwords_termlist(jstr)
        if len(jstr):
         x.append(jstr)
        else:
         x.append([])
    return x


# def word_embedding(sentences):
#     """
#     :param sentences:
#     :return:
#     """
#     model = Word2Vec(sentences, vector_size=100, hs=0, min_count=1, window=5, workers=-1)
#     model.save("word2vec.model")
#     model.wv.save("word2vec.wordvectors")
#     dict_save("vocab.txt",model.wv.index_to_key)


def glove_embedding(sentences):
    pass


# def doc2vec(sentences):
#     documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(sentences)]
#     model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=-1)
#     fname = get_tmpfile("doc2vec")
#     model.save(fname)


def visulization(testword):
    wv=KeyedVectors.load("word2vec.wordvectors")
    X_tsne = TSNE(n_components=2,learning_rate=100).fit_transform(wv[testword])
    #解决负号'-'显示为方块的问题
    plt.figure(figsize=(14, 8))
    #myfont = FontProperties(fname='/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc')
    plt.scatter(X_tsne[:,0],X_tsne[:,1])
    for i in range(len(X_tsne)):
     plt.text(X_tsne[i][0] , X_tsne[i][1] ,testword[i],size = 16)
    plt.show()


def similarity_test(testword):
    wv=KeyedVectors.load("word2vec.wordvectors")
    for i in testword:
     sims = wv.most_similar(i, topn=10)
     print(sims)


def build_dict(data):
    dic=dict_load("vocab.txt")
    term_list=tokenization(data,IndexTokenizer)
    dict_save("input_danmaku.txt",term_list)
    index_list=[]
    for i,danmu in enumerate(term_list):
      tmp=[]
      for t in danmu:
        if t in dic:
         tmp.append(dic.index(t))
        else:
         tmp.append(-1)
      index_list.append(tmp)
    dict_save("input.txt",index_list)


def input_file(filepath):
    dic=dict_load("vocab.txt")
    f=open(filepath,"r",encoding="UTF-8")
    data=f.readlines()
    danmu=[]
    for i,line in enumerate(data):
       data[i]=line.strip('\n')
       tmp=list(map(int,re.findall("\d+",data[i])))
       str=""
       for index in tmp:
         str+=dic[index]
       danmu.append(str)
    f.close()
    return danmu


def remove_stopwords_termlist(termlist):
    termlist=list(termlist)
    if len(termlist):
     result = [term[:-term[::-1].index('/')-1] for term in termlist if term[-term[::-1].index('/'):]
              not in cixing or len(term)-term[::-1].index('/')-1>1]
    else:
     result=[]
    return result

def check(answer):
    temp = [{"content": answer}]
    tmp = pd.DataFrame(temp)
    tmp_list = tokenization(tmp,IndexTokenizer)
    print(tmp_list)
    s = []
    f = open("minganci.txt", "r", encoding="utf-8")
    word = f.readline()
    while word:
        t = word.split()
        s.append(t[0])
        word = f.readline()
    print(s)
    for i in range(len(tmp_list)):
        if tmp_list[i][0] in s:
            return False
    return True





# if __name__ == "__main__":
#     jstr = stralter(IndexTokenizer.segment("这个我们老师给我们放过"))
#     print(jstr)
#     #print(remove_stopwords_termlist(jstr))
#     root="data2"
#     video=os.listdir(root)
#     # for file in video:
#     #   p=os.path.join(root,file)
#     #   print(p)
#     #   if p.find("information")==-1:
#     #     data = read_in(p)
#     #     corpus = pd.concat([corpus, data], axis=0)
#     datatmp = [{"content": "我超级喜欢你"}, {"content": "这样是不对的"}]
#     tmp = pd.DataFrame(datatmp)
#     term_list = tokenization(tmp,IndexTokenizer)
#     print(term_list)
#     #word_embedding(term_list)
#     #doc2vec(term_list)

