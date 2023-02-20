from flask import Flask
import psycopg2 as pg
import json

app = Flask(__name__)
connection = pg.connect(
    host="",
    user="postgres",
    password="",
    port="5432",
    database="gremstestdb",
)
cursor = connection.cursor()

@app.route('/')
def Root():
    # get all table data from test table and return it for react front end
    cursor.execute("SELECT * FROM test")
    data = cursor.fetchall()
    # send data as json
    return json.dumps(data)

app.run(host='0.0.0.0', port=9001)