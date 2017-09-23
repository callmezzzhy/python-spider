from shujuxuexi import content
from shujuxuexi import names
import jieba
import jieba.analyse
import matplotlib.pyplot as plt


print('正在分析文章关键词。。。')
tags=jieba.analyse.extract_tags(''.join(content),topK=20, withWeight=True)
print('关键词：')
for k,v in tags:
	print('关键词：{} 权重比：{:.3f}'.format(k,v))


from wordcloud import WordCloud

txt=''.join([v + ',' for v, x in tags])
wordcloud=WordCloud(background_color='white',font_path='cc.ttf', max_font_size=40).generate(txt)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
wordcloud.to_file('qun_gjc.jpg')
for tag,x in tags:
	jieba.add_word(tag)
for name in names:
	jieba.add_word(name)

with open('stopword.txt','r') as f:
	STOPWORD=[word.strip()for word in f.readlines()]

print('开始进行分词。。。')
sentence=[]
for line in content:
	seg_list=list(jieba.cut(line,cut_all=False))
	unique_list=[]
	for seg in seg_list:
		if seg not in STOPWORD:
			unique_list.append(seg)

	sentence.append(unique_list)
print('分词完毕')

from gensim import models
print('开始人工学习中。。。你可以去开会电视剧')
model=models.Word2Vec(sentence, size=100, window=5, min_count=4, workers=4)
print('智能学习完毕,正在保存模型')
model.save('qyn.model')
print('保存完毕')
