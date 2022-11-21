#port 105

from flask import Flask
import pandas as pd
import json

primaryKey = "Catalog ."
searchableColumns = ['Common Name', 'Scientific Name']

def SortData(df, column, search):
    return df.where(df[column] == search )


app = Flask(__name__, static_url_path='/static')

@app.route('/')
def Root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def StaticFile(path):
    return app.send_static_file(path)

@app.route('/api/v1/<collection>', methods=['GET'])
def AllData(collection):
    if collection == 'all':
        pass #add logic for all csvs later
    csvFilePath = f'./data/{collection}.csv'
    df = pd.read_csv(csvFilePath)
    parsed = json.loads(df.to_json())
    return parsed

@app.route('/api/v1/<collection>/<search>', methods=['GET'])
def ShowData(collection, search):
    if collection == 'all':
        pass #add logic for all csvs later
    csvFilePath = f'./data/{collection}.csv'
    df = pd.read_csv(csvFilePath)

    df1 = df[(df[searchableColumns[0]] == search) | (df[searchableColumns[1]] == search)]

    parsed = json.loads(df1.to_json())
    return parsed

app.run(host='0.0.0.0', port=105)