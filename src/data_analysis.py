import pandas as pd
from tqdm import tqdm
import json
import numpy as np
import sys,os
src = os.path.dirname(os.path.realpath(__file__))
root = os.path.dirname(src)
sys.path.append(src)
sys.path.append(root)
import parcours
import data_processing

tag_file = os.path.abspath(os.path.join(root, 'data','tag_list.txt'))
graph_file = os.path.abspath(os.path.join(root, 'data','graph_dict.txt'))

def most_tweet_per_user(df):
    """Get the username of the person who posted the most tweets

    Args:
        df (pandas.Dataframe): Dataframe of all tweets

    Returns:
        str : Username of the most activ tweeter
    """
    return df.groupby(['user'])['id'].count().sort_values(ascending=False).idxmax()


def get_all_tag(df,force_writing=False):
    """Go through the text of all tweets and look for tags ('@'+'username') in it
    
    Args:
        df (pandas.Dataframe): Dataframe which contains all tweets from scrap.db
        force_writing (bool, optional): Force the writing in the json file to update the data in it.
                                        Defaults to False.

    Returns:
        tag_list(list of list) : Describe all the link between users with that format 
                                (username of the person taged, username of the person who tags)
    """
    # Load the tag_list which is regitered in the json file
    try:
        with open(tag_file,"r") as fp:
            tag_list = json.load(fp)
    except Exception as e:
        print(e)
        tag_list=None
        
    # Create and write the tag_list in the json file if needed
    if force_writing or tag_list==None:
        row_number=df.shape[0]
        tag_list=[]
        index_column_username=1
        index_column_text=2
        for i in tqdm (range(row_number)):
            tweet_text=df.iloc[i,index_column_text]
            word_list=tweet_text.split(' ')
            for word in word_list:
                if word.startswith('@') and len(word)>=2:
                    tag_list.append([word[1:],df.iloc[i,index_column_username]])
        try :
            with open(tag_file,"w") as fp:
                json.dump(tag_list,fp)
                print('-----Tag_list is registered-----')
        except Exception as e:
            print(e)
        
    return tag_list





def tag_count(df,tag:str,force_writing=False):
    """Return the number of time a person 

    Args:
        df (pandas.Dataframe): Dataframe of all tweets
        tag (str): username of the person tagged
        force_writing (bool, optional): _description_. Defaults to False.

    Returns:
        int : Count of tags
    """
    assert not tag.startswith('@'),(f'{tag} begins with a @')
    tag_list=get_all_tag(df,force_writing)
    c=0
    for e in tag_list:
        c+=e.count(tag)
    return c



def tag_count_dict ( df , force_writing = False ) :
    """From tag_list, create a dictionary that for each username 
    describes the link with the persons who taged they

    Args:
        df (pandas.Dataframe): Dataframe of all tweets
        force_writing (bool, optional): Ask to recreate the json file to update them.
        Defaults to False.

    Returns:
        tag_dict (dictionary):   Example: {'user1':[6 <number_of_tweet_that_taged_user1>,<list_of_person_who_taged_user1>['user2','user2','user1']] }
    """
    tag_list=get_all_tag(df,force_writing)
    print('-----Finished to get all tags-----')
    tag_dict={}
    for i in tqdm(range(len(tag_list))):
        tag=tag_list[i][0]
        username=tag_list[i][1]
        if username!=None:
            if tag not in tag_dict:
                tag_dict[tag]=[1,[username]] 
                if tag_dict[tag][1]==None:
                    print('Warning : tweet_id not registered')
            else:
                tag_dict[tag][0]=1+tag_dict[tag][0] 
                tag_dict[tag][1]=tag_dict[tag][1]+[username] 
    return tag_dict
    
    
    
def graph_dict_generate(df,force_writing=False):
    """Generate a dictionnary in order to build the graph 

    Args:
        df (pandas.Dataframe): Dataframe with all tweets
        force_writing (bool, optional): True if a update in json files is needed. Defaults to False.

    Returns:
        graph_dict(dictionary): Describe all nodes and link with that format
        {'user1'<name_of_a_node>:(20,                           <number_of_link_heading_towards_user1>
                                    [['user2',5],['user3',15]], <list_of_neighbors_and_number_of_link_heading_towards_user1>
                                    0.2)                        <fake_value_coefficient_of_user1>
                                    }
    """
    if not force_writing:
        try :
            with open(graph_file,"r") as fp:
                graph_dict=json.load(fp)
        except Exception as e :
            print(e)
            graph_dict=None
    if force_writing or graph_dict==None :
        graph_dict={}
        tag_dict=tag_count_dict(df,force_writing)
        print('-----Creating graph dictionnary-----')
        for username in tqdm(tag_dict):
            tager_username_list = list_description(tag_dict[username][1])
            graph_dict[username] = [tag_dict[username][0],tager_username_list,username_to_fake_value(df,username)]
            for tager_username in [tager_username_list[i][0] for i in range(len(tager_username_list))]:
                if tager_username not in tag_dict:
                    graph_dict[tager_username]=[0,[],username_to_fake_value(df,tager_username)]
        print('-----Finished creating graph dictionnary-----')
        try :
            with open(graph_file,"w") as fp:
                json.dump(graph_dict,fp)
                print('-----Graph_dict is registered-----')
        except :
            pass
    return graph_dict
    
def list_description(mylist):
    """Remove all duplicates and enumerate them in a list of tuple
    
    Example : 
        (list_description(['a','b','a','c']))
         >>>[['a',2],['b',1],['c',1]]
                
    Args:
        mylist (list): With duplicates

    Returns:
        (list of lists): Describe mylist without duplicates
        
    """
    list_description=[]
    list_description_drop_duplicates=list(dict.fromkeys(mylist) )
    for user in  list_description_drop_duplicates:
        list_description.append([user,mylist.count(user)])
    return list_description


    

def tager_username_to_tweet_id_list(df, tag, username) :
    """Return a list of tweet_id from tweets which contains the tag and that come from username
    
    Args:
        df (pandas.Dataframe): Dataframe with all tweets
        tag (str): 
        username (str): _description_

    Returns:
        _type_: _description_
    """
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



    
def username_to_fake_value(df,username):
    """Get all tweets from e specified username and their fake_value,
    then return a mean of all these values

    Args:
        df (pandas.Dataframe): Dataframe with all tweets
        username (str): username of

    Returns:
        float: mean of fake_value
    """
    assert type(username)==str
    fake_value_column_id=7
    df_tweet=df.loc[df['user']== username]
    if not df_tweet.empty:
        row_number=df_tweet.shape[0]
        fake_value_list=[]
        for i in range(row_number):
            fake_value=df_tweet.iloc[i,fake_value_column_id]
            if fake_value == "FAKE":
                fake_value = 1
            else:
                fake_value = 0
            fake_value_list.append(fake_value)
        return np.mean(fake_value_list)
    else :
        return 0.0
