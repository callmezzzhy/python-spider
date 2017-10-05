from datafram import showdatafram    #调用datafram显示人物以及出现次数
from matalab import showline           #调用matalab画柱状图显示人物出现权重比
from yuntu import yunshow               #调用wordcloud显示关键词云图
from fencimodel import models
import gensim
with open('name.txt','r')as f:
    names=list(set(name.strip()for name in f.readlines()))          #记录小说的人物关系词并取重
with open('择天记.txt','r',encoding='utf-8')as f:
    content=list(line.strip()for line in f.readlines())             #读取每一行的小说文本并取除头尾的空格符
    #contents=''.join(content)
#print(content)

def find_peple_name(num=5):
   novel=''.join(content)
   #print(novel)
   show_num=[]
   for name in names:
       show_num.append([name,novel.count(name)])        #找到关系人物的出现次数
       #print(show_num)
   #l=dict(show_num)
   #show_num=sorted(l.items(),key=lambda v:v[1],reverse=True)
   #print(show_num)
   show_num.sort(key=lambda d:d[1],reverse=True)                    #对出现的次数进行排序，从大到小

   return show_num[:num]                                #返回出现次数最多的前5位 num=5
show_5=find_peple_name(num=5)
showdatafram(show_5)    #datafram显示

showline(show_5)        #matalab画图显示

yunshow(content)        #云图显示关键词


def made_model(contents,names):                         #训练择天记小说分析模型
    models(contents,names)
def fenxi(contents):
    #models(contents,names)
    model=gensim.models.Word2Vec.load('ztj.model')         #本地下载调用已经训练好的模型
    print('===============和长生类似的人物=================')
    for s in model.most_similar(positive=['陈长生'])[:10]:         #利用模型分析和陈长生相似的人物，返回关键词和权重比
        print(s)
fenxi(content)