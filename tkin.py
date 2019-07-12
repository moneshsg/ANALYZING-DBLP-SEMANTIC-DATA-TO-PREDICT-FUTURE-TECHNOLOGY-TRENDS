from tkinter import *
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from heapq import nlargest

def pre_start():
    future_test = pd.read_pickle('test_feature_with_rank')
    remapv=pickle.load(open('remap venue', 'rb'))

    old_rank=list(future_test['rank'])
    future_test.drop('rank',axis=1,inplace=True)


    xy=int(tx.get())

    future_test['year_data']=xy
    future_test['age']+=(xy-2017)

    clf=pickle.load(open('gba_predict', 'rb'))




    fin=future_test.copy()
    fin['new rank']=clf.predict(future_test)
    fin['old rank']=old_rank

    fin=fin.groupby('venue').agg({'new rank':np.sum,'old rank':np.sum})
    fin=fin.reset_index()
    fin['diff']=fin['new rank']-fin['old rank']
    fin=fin.nlargest(10,'diff')


    idli={}
    for i in fin['venue']:
        idli[remapv[i]]=fin['diff'][fin['venue']==i].values[0]

    trends=list(idli.keys())
    tranks=list(idli.values())


    for i in range(len(trends)):
        query=trends[i]
        stopwords = ['conference','international','arxiv:','global','on','journal','of','of','the','european','symposium','IEEE','research']
        querywords = query.split()

        resultwords  = [word for word in querywords if word.lower() not in stopwords]
        trends[i] = ' '.join(resultwords)
    
    print(list(zip(trends,tranks)))


    print('The Future Focus')




    # Fixing random state for reproducibility


    
    index = np.arange(len(trends))
    plt.barh(index,tranks)
    plt.ylabel('Discipline', fontsize=5)
    plt.xlabel('Impact', fontsize=5)
    plt.yticks(index,trends, fontsize=5, rotation=30)
    plt.title('Market Share for Each Genre 1995-2017')
    plt.show()
   


master = Tk()

master.geometry('400x200')
master.configure(background='black')



b = Button(master, text="Okay", command=pre_start)

l1 = Label(master, text="Predict the future technology trends ",font="60px")
l2 = Label(master, text="Enter Year",font="30px")

tx=Entry(master, bd =5)

l1.configure(fg='white')
l2.configure(fg='white')
l1.configure(bg='black')
l2.configure(bg='black')


l1.place(x=75,y=2)
l2.place(x=60,y=60)
tx.place(x=200,y=60)
b.place(x=170,y=130)


mainloop()