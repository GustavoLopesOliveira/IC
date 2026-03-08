import requests as rq
import pandas as pd
import time
import functions
import os
from dotenv import load_dotenv

#Para pegar dados do .env
load_dotenv()


session : rq.Session  = rq.Session()

while(True) :
    if functions.autenticate(session) :
        df: pd.DataFrame = functions.get_Bus_Position(session)
        functions.save_data(df)
    else:
        print("Falha na autenticação")
    
    time.sleep(60)