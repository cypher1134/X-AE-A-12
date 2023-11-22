import pandas as pd

def select_biggest_connected_graph(dico_tag,main_node):
    file,rep=[],[main_node]
    visited={}
    for x in dico_tag:
        visited[x]=False
    file.append(main_node)
    while len(file)>0:
        x=file.pop()
        visited[x]=True
        for y in dico_tag[x][1]:
            if visited[y[0]]==False:
                file.append(y[0])
                visited[y[0]]=True
                rep.append(y[0])
    dico_modifie={}
    for element in rep :
        if not dico_modifie.get(element):
            dico_modifie[element]=dico_tag.get(element,[])
    return dico_modifie 


def liste_to_df(df,liste):
    df2=pd.DataFrame(['id','user','text','view','like','retweet','date','fake_value'])
    for i in range(len(liste)):
        subset_df = df[df['user'].isin([liste[i]])]
        df2 = pd.concat([df2, subset_df])
    return df2