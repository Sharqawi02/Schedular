import psycopg2
from bottle import request


# dbname = 'ao7325'
# user = 'ao7325'
# password = 
# host = 
# port = 

def connect():
#     conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
#     return conn

    connection = psycopg2.connect(
        host = "pgserver.mau.se",
        port = "5432",
        user = "am2607",
        password = "l15s2krs"            
        )
    
    """
    connection = psycopg2.connect(
        host = "localhost",
        port = "5432",
        user = "postgres",
        password = "sh010101",
        dbname = "schedular"            
        )
    """
    return connection



def GetUserInfo(connection, id):

    connection = connect()
    cursor = connection.cursor()

    # Security Check
    cursor.execute('select token from users where id = %s', (id,))
    token = cursor.fetchone()

    user_token = request.get_cookie("user_token")

    if token is not None and token[0] == user_token:
        cursor.execute("SELECT * FROM users where id = %s", (id,))
        user = cursor.fetchone()
        return user
    else:
        return None