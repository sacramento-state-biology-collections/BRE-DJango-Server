from flask import Flask
import pandas as pd
import json

primaryKey = "Catalog ."
searchableColumns = ['Common Name']

def sortData(df, column, search):
    return df.where(df[column] == search )


app = Flask(__name__)

@app.route('/api/v1/<collection>', methods=['GET'])
def alldata(collection):
    if collection == 'all':
        pass #add logic for all csvs later
    csvFilePath = f'./data/{collection}.csv'
    df = pd.read_csv(csvFilePath)
    parsed = json.loads(df.to_json())
    return parsed

@app.route('/api/v1/<collection>/<search>', methods=['GET'])
def showdata(collection, search):
    if collection == 'all':
        pass #add logic for all csvs later
    csvFilePath = f'./data/{collection}.csv'
    df = pd.read_csv(csvFilePath)
    for x in searchableColumns:
        df = sortData(df, x, search)
    df = df.dropna(how = 'all')
    parsed = json.loads(df.to_json())
    return parsed

app.run(host='0.0.0.0', port=105)