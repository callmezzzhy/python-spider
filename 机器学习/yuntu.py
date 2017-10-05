from wordcloud import WordCloud
import matplotlib.pyplot as plt
from jiebafenci import jiebatag
from pylab import mpl
def yunshow(content):
    tag=jiebatag(content)
    mpl.rcParams['font.sans-serif']=['SimHei']
    #print(type(tag))
    txt=''.join([v+','for v,x in tag])
    #print(txt)
    wordcloud=WordCloud(background_color='white',font_path='cc.ttf',max_font_size=40).generate(txt)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    wordcloud.to_file('云分析.jpg')