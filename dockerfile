FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip build-essential
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install flask flask_cors pandas psycopg2-binary pycryptodome XlsxWriter openpyxl xlrd qrcode

EXPOSE 9001

CMD ["python3", "/app/rest.py"]
