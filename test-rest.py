from flask import Flask, send_file, request
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
import os
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
settings = {
    "host": "",
    "user": "postgres",
    "password": "",
    "port": "5432",
    "database": "gremstestdb",
}


@app.route('/api/all')
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
    cursor = connection.cursor(cursor_factory=RealDictCursor)
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


@app.route('/api/getxlsx/<database>', methods=['GET'])
def GetXlsx(database):
    databases = ['mammals', 'fish', 'herps', 'insects']
    if database not in databases:
        return "Database not valid", 500
    # BEGIN creation of xlsx file from database
    filepath = 'test.xlsx'
    # END creation of xlsx file from database
    return send_file(f'{filepath}', as_attachment=True)


@app.route('/api/postxlsx/<database>', methods=['POST'])
def PostXlsx(database):
    databases = ['mammals', 'fish', 'herps', 'insects']
    if database not in databases:
        return "Database not valid", 500
    if 'file' not in request.files:
        return "No file part", 500
    file = request.files['file']
    if file == '':
        return "No file selected", 500
    file.save(os.path.join('uploads', file.filename))
    # BEGIN udate database from xlsx file
    status = 'Success'
    # END update database from xlsx file
    if status == 'Success':
        return "Success", 200
    elif status == 'Failed':
        return "Failed", 500


app.run(host='0.0.0.0', port=9001)