import pandas as pd

def parcours(dico,max):
    """
    Performs a depth-first search traversal on a graph represented by the dico dictionary 
       starting the search from the point max and returns the biggest connected graph containing max
    Args :
        dico(DefaultDict): dictionnary that represents the graph
        max(String): the starting point of the research

    Returns:
        DefaultDico : updated dictionnary that represents
        the biggest connected graph containing max
    """
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


def traitement(df,list):
    """
    Creates a new dataframe that contains all the data related to users in list
    Args:
        df(DataFrame): the initial database
        list(list): List of strings (usernames) of interest
    Returns:
        DataFrame containing informations of tweets tweeted by usernames of interest
    """
    df2=pd.DataFrame(['id','user','text','view','like','retweet','date','fake_value'])
    for i in range(len(list)):
        subset_df = df[df['user'].isin([list[i]])]
        df2 = pd.concat([df2, subset_df])
    return df2