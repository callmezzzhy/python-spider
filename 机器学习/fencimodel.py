import jieba
import jieba.analyse
from jiebafenci import jiebatag
import gensim

def xunlian(contents,names):
    tag=jiebatag(contents)
    '''
    自定义添加词库 ta，name
    避免我们需要的关键词在jieba精准分词模式的时候不会被拆开
    '''
    for ta,x in tag:
        jieba.add_word(ta)
    for name in names:
        jieba.add_word(name)
    '''
    导入中文的标点符号以及各种停顿语气的词，
    这些词不需要我们去分析，所以在精准分词后还要进行判断这些分词是否在STOPWORD词汇里
    如果是，则去掉，分词后剩下浓缩版的小说
    '''
    with open('stopword.txt','r')as f:
        STOPWORD=[word.strip()for word in f.readlines()]

    print('开始分词中.....')
    sentence=[]
    for line in contents:
        seg_list=list(jieba.cut(line,cut_all=False))
        unique_list=[]
        #print(seg_list)
        for seg in seg_list:
            if seg not in STOPWORD:
                unique_list.append(seg)
        sentence.append(unique_list)
    print('分词完毕。')
    return sentence
def models(contents,names):
    sentences=xunlian(contents,names)   #根据文本和人物名进行分词
    print('开始训练模型....')
    model=gensim.models.Word2Vec(sentences,min_count=10,size=100,workers=4,window=5)
    print('训练完毕，保存模型到本地中...')
    model.save('ztj.model')
    print('OK')
