from flask import Flask
import psycopg2 as pg
import json

app = Flask(__name__)
settings = {
    "host": "",
    "user": "postgres",
    "password": "",
    "port": "5432",
    "database": "gremstestdb",
}

@app.route('/')
def Root():
    # Open the connection
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    # Create a Cursor
    cursor = connection.cursor()
    # Get all data from test table
    cursor.execute("SELECT * FROM test")
    # Save data as a list
    data = cursor.fetchall()
    # Close the cursor
    cursor.close()
    # Close the connection
    connection.close()
    # Send data as json
    return json.dumps(data)

@app.route('/api/status/server')
def ServerHealth():
    return "Success", 200

@app.route('/api/status/postgres')
def PostgresHealth():
    if pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    ):
        return "Success", 200
    else:
        return "Failed", 500
    

app.run(host='0.0.0.0', port=9001)