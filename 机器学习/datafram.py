import pandas as pd
def showdatafram(data):
    show=pd.DataFrame(data,columns=['names','counts'])
    print(show)