import os
import json
from pathlib import Path
from typing import  List
from datetime import datetime
from sympy import not_empty_in
from distribution_inference.config import DatasetConfig, AttackConfig, BlackBoxAttackConfig, TrainConfig

class Result:
    def __init__(self,path:Path,name:str) -> None:
        self.name=name
        self.path=path
        self.start = datetime.now()
        self.dic={'name':name,'start time':str(self.start)}
    def save(self):
        self.save_t = datetime.now()
        self.dic['save time']=str(self.save_t)
        save_p = self.path.joinpath(self.name)
        with save_p.open('w') as f:
            json.dump(self.dic, f)
            
    def not_empty_dic(self,dic:dict,key):
        if not dic.has_key(key):
            dic[key]={}
    def load(self):
        raise NotImplementedError("Implement method to model for logger")

class AttackResult(Result):
    def __init__(self,path:Path,name:str,ac:AttackConfig):
        super().__init__(path,name)
        self.dic["Attack config"] = ac.__dict__
        self.dic["Attack config"]["train_config"] = ac.train_config.__dict__
        self.dic["Attack config"]["train_config"]["data_config"] = ac.train_config.data_config.__dict__
        if self.dic["Attack config"]['black_box']:
            self.dic["Attack config"]['black_box'] = ac.black_box.__dict__
        if self.dic["Attack config"]['white_box']:
            self.dic["Attack config"]['white_box'] = ac.white_box.__dict__
    
    def add_results(self,attack:str,prop,vacc,advacc):
        def check_rec(dic:dict,keys:List):
            k = keys.pop(0)
            self.not_empty_dic(dic,k)
            check_rec(dic[k],keys)
        check_rec(self.dic,['result',attack,prop])
        if self.dic['result'][attack][prop].has_key('adv_acc'):
            self.dic['result'][attack][prop]['adv acc'].append(advacc)
        else:
            self.dic['result'][attack][prop]['adv acc'] = [advacc]
        if self.dic['result'][attack][prop].has_key('victim_acc'):
            self.dic['result'][attack][prop]['victim acc'].append(vacc)
        else:
            self.dic['result'][attack][prop]['victim acc'] = [vacc]




        
    

