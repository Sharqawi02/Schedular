from bottle import Bottle, run, template
import mysql.connector

# Skapa en anslutning till din MySQL-databas
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0220561374am@",
    database="your_database"
)

app = Bottle()

# Exempelrutt för att köra en fråga mot databasen
@app.route('/query')
def query():
    # Skapa en cursor för att köra SQL-frågor
    cursor = db_connection.cursor()
    
    # Exempel på en SQL-fråga (hämtar alla rader från en tabell)
    cursor.execute("SELECT * FROM your_table")
    
    # Hämta alla rader från frågeresultatet
    result = cursor.fetchall()
    
    # Stäng cursor
    cursor.close()
    
    # Returnera resultatet som en template
    return template("query_result", rows=result)

if __name__ == "__main__":
    run(app, host='localhost', port=8080)
