import pyodbc

server = 'host.docker.internal'
database = 'master'
username = 'sa'
password = 'AdminMicrosoft123'
driver = 'ODBC Driver 17 for SQL Server'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    cnxn = pyodbc.connect(conn_str)
    print("Connected successfully using the weird string format!")
    cnxn.close()
except pyodbc.Error as e:
    print("Connection failed with weird string format. Error message:", e)

conn_str = f'mssql+pyodbc://sa:AdminMicrosoft123@host.docker.internal/master?driver=ODBC+Driver+17+for+SQL+Server'

try:
    cnxn = pyodbc.connect(conn_str)
    print("Connected successfully using the URI format!")
    cnxn.close()
except pyodbc.Error as e:
    print("Connection failed using URI format. Error message:", e)


import sqlalchemy

server = 'host.docker.internal'
database = 'master'
username = 'sa'
password = 'AdminMicrosoft123'
driver = 'ODBC Driver 17 for SQL Server'

# Test connection using SQLAlchemy
conn_str = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

try:
    engine = sqlalchemy.create_engine(conn_str)
    with engine.connect() as connection:
        print("Connected successfully using SQLAlchemy!")
except sqlalchemy.exc.SQLAlchemyError as e:
    print("Connection failed using SQLAlchemy. Error message:", e)

# Test connection using pyodbc
import pyodbc

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    cnxn = pyodbc.connect(conn_str)
    print("Connected successfully using pyodbc!")
    cnxn.close()
except pyodbc.Error as e:
    print("Connection failed using pyodbc. Error message:", e)
