import psycopg2

# dbname = 'ao7325'
# user = 'ao7325'
# password = 
# host = 
# port = 

def connect():
#     conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
#     return conn

    connection = psycopg2.connect(
        host = 'pgserver.mau.se',
        port = '5432',
        user = 'ao7325',
        password = 'Ia@barca2023'
    )

    return connection