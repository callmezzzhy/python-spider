import gensim
model = gensim.models.Word2Vec.load('qyn.model')
print('===============和范闲类似的人物=================')
for s in model.most_similar(positive=['吴亦凡'])[:5]:
    print(s)
print('\n\n')