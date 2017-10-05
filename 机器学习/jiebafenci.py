import jieba
import jieba.analyse
def jiebatag(content):
    print('正在分析：')
    tag=jieba.analyse.extract_tags(''.join(content),topK=50,withWeight=True)    #提取文本中的关键词，withWeight=True表示返回关键词的权重比，topK=50表示提取权重比最多的前50
    print('分析完毕')
    for k,v in tag:
        print('关键词：{}\t 权重：{}'.format(k,v))
    return tag