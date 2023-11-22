import pandas as pd

def parcours(dico,max):
    file,rep=[],{max}
    n=len(dico)
    visited={}
    
    for x in dico.keys():
        visited[x]=False
    file.append(max)
    while file:
        x=file.pop()
        visited[x]=True
        for y in dico[x][1]:
            if visited[y[0]]==False:
                file.append(y[0])
                visited[y[0]]=True
                rep.add(y[0])
    
    dico_modifie={}
    for element in rep :
        if not dico_modifie.get(element):
            dico_modifie[element]=dico.get(element,[])
    return dico_modifie 


def traitement(df,liste):
    df2=pd.DataFrame(['id','user','text','view','like','retweet','date','fake_value'])
    for i in range(len(liste)):
        subset_df = df[df['user'].isin([liste[i]])]
        df2 = pd.concat([df2, subset_df])
    return df2