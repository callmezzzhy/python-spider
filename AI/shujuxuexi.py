with open('name.txt', 'r') as f:
    names = list(set(name.strip() for name in f.readlines()))

# 读入整个庆余年文本的内容：
with open('dianying.txt', 'r', encoding='utf-8') as f:
    content = list(line.strip() for line in f.readlines())
def find_pepple_showup_cont(num=10):
    '''
    对比统计人物姓名出现的次数，
    并返回出现次数最多的前Num个人
    '''
    novel = ''.join(content)
    showup_counts = []
    for name in names:
    # 这里从文章统计处每个名词出现的次数后，保存在一个列表里返回
        showup_counts.append([name, novel.count(name)])    
    showup_counts.sort(key=lambda v: v[1], reverse=True)
    return showup_counts[:num]

# 简单的展示一下数据
showup_10 = find_pepple_showup_cont()
print(showup_10)
import pandas as pd
show = pd.DataFrame(showup_10, columns=['names', 'counts'])
print(show)
import matplotlib.pyplot as plt
from pylab import mpl
# 设置中文子字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 展示的姓名和数据
data = list(show.counts)
index = list(show.names)
# 绘制直方图
plt.bar(range(len(data)), data, tick_label=index)
plt.xlabel('出现的人物')
plt.ylabel('出现的次数')
plt.title('庆余年人物出现频次图')
plt.savefig('001.jpg')
