import os
from dotenv import load_dotenv
import requests as rq
import pandas as pd

def autenticate(session : rq.Session) -> bool :
    API_TOKEN : str = os.getenv("API_TOKEN")
    BASE_URL : str = os.getenv("BASE_URL")
    response : rq.Response = session.post(BASE_URL + "/Login/Autenticar?token=" + API_TOKEN)
    return response.text.strip().lower() == "true"

def get_Bus_Position(session : rq.Session) -> dict:
    BASE_URL : str = os.getenv("BASE_URL")
    response : rq.Response = session.get(BASE_URL + "/Posicao")
    data  = response.json()
    return data

    
def __parse_bus_data__(data : dict) -> pd.DataFrame:

    rows : list = []
    hora = data["hr"]

    for linha in data["l"]:
        for v in linha["vs"]:
            rows.append({
                "hora_coleta": hora,
                "linha": linha["c"],
                "codigo_linha": linha["cl"],
                "origem": linha["lt0"],
                "destino": linha["lt1"],
                "veiculo": v["p"],
                "latitude": v["py"],
                "longitude": v["px"],
                "hora_gps": v["ta"]
            })

    return pd.DataFrame(rows)

def save_data(df : pd.DataFrame) -> None :
    file_exists = os.path.isfile("data/posicao_dos_onibus.csv")
    df = __parse_bus_data__(df)
    df.to_csv("data/posicao_dos_onibus.csv",mode="a",header=not file_exists,index=False)