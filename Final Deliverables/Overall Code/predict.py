import requests, pickle
from collections import defaultdict
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import config

li = ['Gender','Married','Dependents','Education','Self_Employed','Property_Area']
d = defaultdict(LabelEncoder)

def encode(df):
    q = df.copy()
    ld = pickle.load(open("static/encoder.pkl", "rb"))
    for i in q:
        if(i in li):
            try:
                q[i] = ld[i].transform(q[i])
            except:
                continue     
    return q


def hloan(fields, values):
    API_KEY = config.API_KEY
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', 
                     data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}    
    
    df = pd.DataFrame([values],columns=fields)     
    df = encode(df)    
    values = list(df.loc[0])
    
    payload_scoring = {"input_data": [{"field": [fields], "values": [values]}]}
    url =  config.URL_HL
    response_scoring = requests.post(url, json=payload_scoring,
                       headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    hstatus = predictions['predictions'][0]['values'][0][0]
    return hstatus

def bloan(fields, values):   
    API_KEY = config.API_KEY
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', 
                     data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken} 
    
    df = pd.DataFrame([values],columns=fields)     
    df = encode(df)
    values = list(df.loc[0])
    payload_scoring = {"input_data": [{"field": [fields], "values": [values]}]}
    url =  config.URL_BL
    response_scoring = requests.post(url, json=payload_scoring,
                       headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    bstatus = predictions['predictions'][0]['values'][0][0]
    return bstatus

    