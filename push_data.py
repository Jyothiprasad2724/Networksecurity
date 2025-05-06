import os
import sys
import json 

from dotenv import load_dotenv

load_dotenv()

MONGO_DB = os.getenv("MONGO_DB")


import certifi 
ca = certifi.where()

import pandas as pd 
import numpy as np 
import pymongo
from Networksecurity.exception.exception import NetworksecurityException
from Networksecurity.logging.logger import logging


class NetworkData():


    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworksecurityException(e,sys)

    #Convert the csv file to Json file format
    def cv_to_json_conversion(self,filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    #conncet the mongo db and push the data
    def conncet_mongo(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
        
            self.mongo_client = pymongo.MongoClient(MONGO_DB)
        
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        
        except Exception as e:
            raise NetworksecurityException(e,sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "JYOTHIML"
    Collection = "Network_Data"
    networkobj = NetworkData()
    records=networkobj.cv_to_json_conversion(filepath=FILE_PATH)
    print(records)
    no_of_records = networkobj.conncet_mongo(records,DATABASE,Collection)
    print(no_of_records)
