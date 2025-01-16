import pandas as pd
df = pd.read_excel('sentence.xlsx')
N=2
dic={}
for row in df.head(10).itertuples():
    print(row.abstract[:100])
    words=row.abstract[:100].split(" ")
    print(words)
    for j in range(len(words)):
        pre_word=[]
        for k in range(max(0,j-N),j):
            pre_word.append(words[k])
        dic={pre_word:words[j]}
        #dic.append(words[j]:pre_word)
        print(dic)
    
