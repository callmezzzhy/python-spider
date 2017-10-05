import matplotlib.pyplot as plt
from pylab import mpl
'''
    data=list(show.counts)
    index=list(show.names)
'''
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x(), 8+height, '%s' % float(height))   #在柱状上方显示具体柱状高
def showline(showdata):
    mpl.rcParams['font.sans-serif']=['SimHei']   #设置字体
    l=dict(showdata)          #获取人物和出现次数的字典
    data=[]
    index=[]
    '''
    将人物名和出现次数分别提取出来做为柱状图的x，y
    '''
    for key,value in l.items():
        data.append(value)
        index.append(key)
    #print(data,index)
    rect=plt.bar(range(len(data)),data,tick_label=index)        #画柱状图
    autolabel(rect)  #显示柱状高
    plt.xlabel('出现的人物')
    plt.ylabel('出现的次数')
    plt.title('择天记人物出现频率')
    plt.savefig('分析.jpg')
    plt.show()
