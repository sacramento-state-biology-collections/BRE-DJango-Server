from flask import Flask, send_file, request, redirect, url_for
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
import os
import json
import pandas as pd
from subprocess import Popen, PIPE
import base64
import qrcode as qr
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
with open('/app/config.json') as f:
    settings = json.load(f)
key = 'cscgluewaregrems'

qr_code = qr.QRCode(
    version=1,
    error_correction=qr.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)


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
    # create folder if not exist
    if not os.path.exists(f'static/history/{database}'):
        os.makedirs(f'static/history/{database}')
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
    time = pd.Timestamp.now()
    time = time.strftime("%m-%d-%Y-%H-%M-%S")
    dataframe.to_excel(f'static/history/{database}/{time}_{database}.xlsx', index=False)
    file = request.files['file']
    file.save(os.path.join('uploads', file.filename))
    # TODO BEGIN udate database from xlsx file
    dataframe = pd.read_excel(f'uploads/{database}.xlsx', engine='openpyxl')
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
    # !END update database from xlsx file
    if status == 'Success':
        return "Success", 200
    elif status == 'Failed':
        return "Failed", 500

@app.route('/api/<collection>/', methods=['GET'])
def search_all(collection):
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM {collection}")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return json.dumps(data)

@app.route('/api/edit/<collection>', methods=['GET'])
def sea(collection):
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT catalog,common_name FROM {collection}")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return json.dumps(data)

@app.route('/api/<collection>/<search>', methods=['GET'])
def search_result_multirow(collection, search):
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM {collection} WHERE common_name ILIKE '%{search}%' OR scientific_name ILIKE '%{search}%'")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return json.dumps(data)

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
    cursor.execute(f"SELECT * FROM {collection} WHERE {column}='{search}'")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return json.dumps(data)


# TODO: create route to generate QR code
@app.route('/api/<collection>/<drawer_letter>')
def drawer_search(collection_name, drawer_letter):
    column_type = "drawer"
    return redirect(
        url_for('search_result', collection=str(collection_name), column=str(column_type), search=str(drawer_letter)))


@app.route('/api/generate/<collection>/<drawer>')
def generate_qrcode(collection, drawer):
    url = f'/api/{collection}/{drawer}'
    qr_code.add_data(url)
    qr_code.make(fit=True)
    img = qr_code.make_image(fill_color="black", back_color="white")
    return send_file(img, as_attachment=True), 200


@app.route('/api/file/<collection>/<catalog>/<image>', methods=['POST', 'GET'])
def upload_file(catalog: str, collection: str, image):
    # Connect to database
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    # TODO update parent_dir variable to set correct folder pwd in linode
    parent_dir = "~/"
    # POST protocol
    if request.method == 'POST':
        ext = ['.jpg', '.jpeg']
        # check file extension
        if not image.endswith(tuple(ext)):
            return "File extension not allowed", 500
        if 'file' not in request.files:
            return "no file found", 505
        f = request.files['file']
        print(f)
        f.save(os.path.join(parent_dir, f.filename))
        collection=collection.lower()
        cursor.execute(f"UPDATE {collection} SET image={f.filename} WHERE catalog='{catalog}'")
        cursor.close()
        connection.close()
        return "file saved", 200

    # GET protocol
    elif request.method == 'GET':
        # TODO: get file from server and send it to client
        cursor.execute(f'SELECT image from {collection} WHERE catalog LIKE ' % {catalog} % ' ')
        filen = cursor.fetchall()
        pwd = Popen(f"find {parent_dir} -name {filen} 2>/dev/null", shell=True, stdout=PIPE).communicate()[0]
        pwd = pwd.decode('utf-8')
        cursor.close()
        connection.close()
        return send_file(pwd, as_attachment=True), 200


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    tmp_key = key
    enc = base64.b64decode(data['password'])
    cipher = AES.new(tmp_key.encode('utf-8'), AES.MODE_ECB)
    password = unpad(cipher.decrypt(enc), 16).decode('utf-8')
    username = data['username']
    # TODO: check if user exists in database
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(data) == 0:
        return json.dumps({'message': 'Failed'}), 500
    return json.dumps({'message': 'Success'}), 200

@app.route('/api/<collection>', methods=['GET'])
def get_collection(collection):
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT catalog,common_name FROM {collection}")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return json.dumps(data), 200

@app.route('/api/testing', methods=['GET'])
def testing():
    return app.send_static_file('test.html')

@app.route('/api/entry/<collection>/<catalog>/<column>/<data>', methods=['POST'])
def post_entry(collection, catalog, column, data):
    connection = pg.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        port=settings["port"],
        database=settings["database"]
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"UPDATE {collection} SET {column}='{data}' WHERE catalog='{catalog}'")
    cursor.close()
    connection.close()
    if 'file' in request.files:
        f = request.files['file']
        f.save(os.path.join('static', f.filename))
    return "Success", 200

@app.route('/<path>', methods=['GET'])
def StaticFile(path):
    if not os.path.isfile('static/' + path):
        return app.send_static_file('no_image.svg')
    return app.send_static_file(path)

@app.route('/api/files/history/<collection>', methods=['GET'])
def get_history_collection(collection):
    collection = collection.lower()
    if not os.path.isdir(f'/static/history/{collection}'):
        return "No history found", 500
    return json.dumps(os.listdir(f'/static/history/{collection}')), 200

@app.route('/api/file/history/<collection>/<file>', methods=['GET'])
def get_history(collection, file):
    collection = collection.lower()
    if not os.path.isfile(f'/static/history/{collection}/{file}'):
        return "No history found", 500
    return send_file(f'/static/history/{collection}/{file}', as_attachment=True), 200

# TODO: create route to generate QR code
# search query = SELECT * FROM mammals_collection WHERE drawer = 'H';

app.run(host='0.0.0.0', port=9001)
