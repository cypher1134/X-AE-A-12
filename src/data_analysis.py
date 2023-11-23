import pandas as pd
from tqdm import tqdm
import json
import numpy as np
import data
from src import parcours

def most_tweet_per_user(df):
    return df.groupby(['user'])['id'].count().sort_values(ascending=False).idxmax()
###test tweet_per_user
#print(most_tweet_per_user(df))

def get_all_tag(df,force_writing=False):
    '''renvoie une liste de tuple'''
    try:
        with open('./data/tag_list.txt',"r") as fp:
            tag_list=json.load(fp)
    except Exception as e:
        print(e)
        tag_list=None
    if force_writing or tag_list==None:#si on veut réécrire la liste des tags ou si la liste est vide
        row_number=df.shape[0]
        tag_list=[]
        index_column_username=1
        index_column_text=2
        for i in tqdm (range(row_number)):
            tweet_text=df.iloc[i,index_column_text]
            word_list=tweet_text.split(' ')
            for word in word_list:
                if word.startswith('@') and len(word)>=2:
                    tag_list.append((word[1:],df.iloc[i,index_column_username]))#(le nom du tag, le nom de l'utilisateur qui a posté le tweet)
        #---stockage : écriture de la liste de tuple pour éviter de la calculer à chaque fois---
        try :
            with open('./data/tag_list.txt',"w") as fp:
                json.dump(tag_list,fp)
                print('-----Tag_list is registered-----')
        except Exception as e:
            print(e)
    return tag_list

###test get_all_tag
#print(get_all_tag(df))



def tag_count(df,tag:str,force_writing=False):
    assert tag.startswith('@'),(f'{tag} is not a tag')
    tag_list=get_all_tag(df,force_writing)
    return tag_list.count(tag[1:])
#print('@HollyEgg',tag_count(df,'@HollyEgg'))

def tag_count_dict ( df , force_writing = False ) :
    tag_list=get_all_tag(df,force_writing)
    print('-----Finished to get all tags-----')
    tag_dict={}
    for i in tqdm(range(len(tag_list))):
        tag=tag_list[i][0]
        username=tag_list[i][1]
        if username!=None:
            if tag not in tag_dict:
                tag_dict[tag]=[1,[username]]#initialise la case dans le dict 
                if tag_dict[tag][1]==None:
                    print('Warning : tweet_id not registered')
            else:
                tag_dict[tag][0]=1+tag_dict[tag][0] #ajoute 1 au nombre de tweets avec le tag
                tag_dict[tag][1]=tag_dict[tag][1]+[username] #ajoute l'username du tweet avec le tag
    return tag_dict
    
    
    
def graph_dict_generate(df,force_writing=False):
    
    if not force_writing:
        try :
            with open('./data/graph_dict.txt',"r") as fp:
                graph_dict=json.load(fp)
        except Exception as e :
            print(e)
            graph_dict=None
    if force_writing or graph_dict==None :
        graph_dict={}
        tag_dict=tag_count_dict(df,force_writing)
        print('-----Creating graph dictionnary-----')
        for username in tqdm(tag_dict):
            tager_username_list = list_to_doublons_description( tag_dict[username][1])
            graph_dict[username] = (tag_dict[username][0],tager_username_list,username_to_fake_value(df,username))
            for tager_username in [tager_username_list[i][0] for i in range(len(tager_username_list))]:
                if tager_username not in tag_dict:
                    graph_dict[tager_username]=(0,[],username_to_fake_value(df,tager_username))
        print('-----Finished creating graph dictionnary-----')
        try :
            with open('./data/graph_dict.txt',"w") as fp:
                json.dump(graph_dict,fp)
                print('-----Graph_dict is registered-----')
        except :
            pass
    return graph_dict
    
def list_to_doublons_description(mylist):
    """renvoie une liste qui supprime les doublons avec ce format
    list_to_doublons_description(['a','b','a','c']))
    [('a',2),('b',1),('c',1)]

    """
    list_description=[]
    list_description_drop_duplicates=list(dict.fromkeys(mylist) )
    for user in  list_description_drop_duplicates:
        list_description.append((user,mylist.count(user)))
    return list_description
###test list_to_doublons_description
#print(list_to_doublons_description(['a','b','a','c']))
#>>>[('a',2),('b',1),('c',1)]

    

###test tag_count_dict
#dicto=tag_count_dict()
#print('nombre de tweet avec le tag {} :'.format(list(dicto.keys())[0]), list(dicto.values())[0][0])
#print('id des tweets avec le tag {} :'.format(list(dicto.keys())[0]), list(dicto.values())[0][1]) 

def tager_username_to_tweet_id_list(df, tag, username) :
    """renvoie la list des tweet_id des tweets qui viennent d'un username et qui contiennent le tag en argument"""
    assert type(username) == str
    n_column_id = 0  
    n_column_text = 2
    df_tweet = df.loc[df['user'] == username]
    row_number = df_tweet.shape[0]
    tweet_id_list = []
    for i in range(row_number) :
            tweet_text = df_tweet.iloc[i,n_column_text]
            tweet_id = df_tweet.iloc[i,n_column_id]
            word_list = tweet_text.split(' ')
            if '@'+ tag in word_list :
                tweet_id_list.append(int(tweet_id))
    return tweet_id_list
###test tager_username_to_tweet_id_list
#print(tager_username_to_tweet_id_list(df,'HollyEgg','maltipony'))
#>>>[14568998]



    
def username_to_fake_value(df,username):
    """renvoie la moyenne des fake values pour un username donné"""
    assert type(username)==str
    fake_value_column_id=7
    df_tweet=df.loc[df['user']== username]
    if not df_tweet.empty:
        row_number=df_tweet.shape[0]
        fake_value_list=[]
        for i in range(row_number):
                fake_value=df_tweet.iloc[i,fake_value_column_id]
                fake_value_list.append(fake_value)
        return np.mean(fake_value_list)
    else :
        return 0.0



if __name__=='__main__':  
    force_writing=False
    df = pd.read_csv("C:/Users/viann/Downloads/archive/training.1600000.processed.noemoticon.csv", sep=',',encoding="ISO-8859-1")
    df.columns=['target','id','date','flag','user','text']
    print(most_tweet_per_user(df))
    '''dicto=graph_dict_generate(df,force_writing)
    opinion_list=get_opinion_on_tag(df,'HollyEgg',force_writing)
    print('this tag has been quoted {} times'.format(len(opinion_list)))
    print('In average this tag has {} in opinion'.format(np.mean(opinion_list)))
    print('this tag has {} positive opinion'.format(opinion_list.count(4)))
    print('this tag has {} positive opinion'.format(opinion_list.count(0)))'''