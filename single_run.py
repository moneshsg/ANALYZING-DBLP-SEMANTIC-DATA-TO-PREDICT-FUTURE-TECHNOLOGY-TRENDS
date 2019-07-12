import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from heapq import nlargest

future_test = pd.read_pickle('test_feature_with_rank')
remid=pickle.load(open('re_map_id', 'rb'))
df = pd.read_pickle('all_data')

old_rank=list(future_test['rank'])
future_test.drop('rank',axis=1,inplace=True)


xy=int(input('Enter the year that you want to predict '))

future_test['year_data']=xy
future_test['age']+=(xy-2017)

rf=pickle.load(open('rf_predict', 'rb'))

#print(len(future_test))
#future_test.head()

#pd.Series(remid)
#remid[1200]


fin=future_test.copy()
fin['new rank']=rf.predict(future_test)
fin['old rank']=old_rank
fin['diff']=fin['new rank']-fin['old rank']

fin=fin.nlargest(30,'diff')

#pd.Series(remid).iloc[1200]
idli={}
for i in fin['id']:
    idli[remid[i]]=fin['diff'][fin['id']==i].values[0]

top=df[df['id'].isin(idli.keys())]
top=top.drop_duplicates(subset='venue', keep='first')
top.drop(['abstract','references','title'],axis=1,inplace=True)
top['rank']=top['id'].map(idli)
trends=list(top['venue'])
tranks=list(top['rank'])

for i in range(len(trends)):
    query=trends[i]
    stopwords = ['conference','international','arxiv:','global']
    querywords = query.split()

    resultwords  = [word for word in querywords if word.lower() not in stopwords]
    trends[i] = ' '.join(resultwords)


print('The Future Focus')
print(top)


# Fixing random state for reproducibility
np.random.seed(19680801)


plt.rcdefaults()
fig, ax = plt.subplots()

# Example data
people = trends
y_pos = np.arange(len(tranks))
performance = tranks

ax.barh(y_pos, performance, align='center',
        color='orange', ecolor='black')
ax.set_yticks(y_pos)
ax.set_yticklabels(people)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Performance')
ax.set_title('Future Progress')

plt.show()