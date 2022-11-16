from flask import Flask
import pandas as pd
import json

jsonFilePath = "./rest.json"
primaryKey = "Catalog ."

app = Flask(__name__)

@app.route('/api/v1/<collection>', methods=['GET'])
def tabledata(collection):
    if collection == 'all':
        pass #add logic for all csvs later
    csvFilePath = f'./data/{collection}.csv'
    df = pd.read_csv(csvFilePath)
    parsed = json.loads(df.to_json())
    return parsed

app.run(host='0.0.0.0', port=105)
