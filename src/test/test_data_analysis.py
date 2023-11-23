import pytest
import sys,os
import json
import pandas as pd
test = os.path.dirname(os.path.realpath(__file__))
src = os.path.dirname(test)
root = os.path.dirname(src)
sys.path.append(src)
sys.path.append(root)
import data_analysis

class TestClass:
    
    
    def setup_method(self): 
        self.df= pd.read_json("./data/raw_data.json", convert_dates=False)
        self.df=self.df.head(10)
        
    def test_list_description(self):
        assert( data_analysis.list_description(['a','b','a','c'])==[['a',2],['b',1],['c',1]])
        
    def test_most_tweet_per_user(self):
        assert data_analysis.most_tweet_per_user(self.df)=='ATchelka'
        
    def test_get_all_tag(self):
        assert data_analysis.get_all_tag(self.df,True)==[['RachelBitecofer', 'Nigel_StHubbins'], ['kristine_kenyon', 'Nigel_StHubbins'], ['ckolchacksghost', 'mainetom329402'], ['dbongino', 'mainetom329402'], ['tinfoilted1', 'Biracialman76'], ['thehill', 'Biracialman76'], ['Trump_Losses', 'Gustavia_Bones'], ['Travis_in_Flint', 'ATchelka'], ['TheEXECUTlONER_', 'garyshelley7'], ['POTUS', 'bryanyou52']]
    
    def test_tag_count(self):
        assert data_analysis.tag_count(self.df,'ATcheka',True)==0
        assert data_analysis.tag_count(self.df, "Nigel_StHubbins",True)==2
    
    def test_tag_count_dict(self):
        assert data_analysis.tag_count_dict (self.df,True) == {'RachelBitecofer': [1, ['Nigel_StHubbins']], 'kristine_kenyon': [1, ['Nigel_StHubbins']], 'ckolchacksghost': [1, ['mainetom329402']], 'dbongino': [1, ['mainetom329402']], 'tinfoilted1': [1, ['Biracialman76']], 'thehill': [1, ['Biracialman76']], 'Trump_Losses': [1, ['Gustavia_Bones']], 'Travis_in_Flint': [1, ['ATchelka']], 'TheEXECUTlONER_': [1, ['garyshelley7']], 'POTUS': [1, ['bryanyou52']]}
    
    def test_graph_dict_generate(self):
        graph_file = os.path.abspath(os.path.join(root, 'data','graph_dict.txt'))
        with open(graph_file,"r") as fp:
                graph_dict=json.load(fp)
        assert data_analysis.graph_dict_generate(self.df,True)== graph_dict
    
    def test_tager_username_to_tweet_id_list(self):
        assert data_analysis.tager_username_to_tweet_id_list(self.df, "RachelBitecofer", "Nigel_StHubbins")==[1713343926189330692]
    
    def test_username_to_fake_value(self):
            assert data_analysis.username_to_fake_value(self.df,"bryanyou52")==0.0