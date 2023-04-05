from flask import Flask, send_file, request
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
import os
import json
import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
settings = {
    "host": "",
    "user": "postgres",
    "password": "",
    "port": "5432",
    "database": "biologydb",
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
    databases = ['mammals', 'fish', 'herps', 'insects', 'test']
    if database not in databases:
        return "Database not valid", 500
    # BEGIN creation of xlsx file from database
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f'SELECT * FROM {database}_collection')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    dataframe = pd.DataFrame(data)
    dataframe.to_excel(f'uploads/{database}.xlsx', index=False)
    filepath = f'uploads/{database}.xlsx'
    # END creation of xlsx file from database
    return send_file(f'{filepath}', as_attachment=True)


@app.route('/api/postxlsx/<database>', methods=['POST'])
def PostXlsx(database):
    databases = ['mammals', 'fish', 'herps', 'insects', 'test']
    if database not in databases:
        return "Database not valid", 500
    if 'file' not in request.files:
        return "No file part", 500
    file = request.files['file']
    file.save(os.path.join('uploads', file.filename))
    #TODO BEGIN udate database from xlsx file
    dataframe = pd.read_excel(f'uploads/{database}.xlsx')
    columns = dataframe.columns
    sql_primary_key = f'{columns[0]} varchar(4) PRIMARY KEY,'
    columns = columns[1:]
    sql_last_text = f'{columns[-1]} TEXT'
    columns = columns[:-1]
    sql_table_text = [f'{column} TEXT,' for column in columns]
    sql_table_columns = [sql_primary_key]
    for item in sql_table_text:
        sql_table_columns.append(item)
    sql_table_columns.append(sql_last_text)
    sql_create_table = f'CREATE TABLE {database}_Collection ('
    for item in sql_table_columns:
        sql_create_table += item
    sql_create_table += ')'
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE {database}_Collection')
    print(sql_create_table)
    cursor.execute(sql_create_table)
    sql_insert_header = f"INSERT INTO {database}_Collection VALUES ("
    for index, row in dataframe.iterrows():
        sql_insert_content = []
        for column in row:
            sql_insert_content.append(f"'{column}'")
        sql_insert = sql_insert_header + ", ".join(sql_insert_content) + ")"
        cursor.execute(sql_insert)
    cursor.close()
    connection.commit()
    connection.close()
    status = 'Success'
    #! END update database from xlsx file
    if status == 'Success':
        return "Success", 200
    elif status == 'Failed':
        return "Failed", 500


@app.route('/api/<collection>/<column>/<search>', methods=['GET'])
def search_result(collection, column, search):
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT common_name,scientific_name,prep_type,drawer,catalog FROM {collection} WHERE {column} LIKE '%{search}%'")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return json.dumps(data)

@app.route('/api/<collection>/<id>', methods=['GET'])
def all_specimen_data(collection, id):
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM {collection} WHERE catalog='{id}'")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return json.dumps(data)

@app.route('/api/card/<collection>/<id>', methods=['GET'])
def card_data(collection, id):
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT common_name,scientific_name,prep_type,drawer,catalog FROM {collection} WHERE catalog='{id}'")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return json.dumps(data)

app.run(host='0.0.0.0', port=9001)