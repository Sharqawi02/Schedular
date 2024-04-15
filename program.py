import psycopg2
from bottle  import  Bottle, route, template, run, static_file, request, redirect
from db import connect

app = Bottle()

@app.route('/')
def index():
     return template('First-Site.html')

@app.route('/homepage')
def homepage_route():
    return template('homepage.html')

# Registering a new user in the database
@app.route('/register' , method=[ 'GET','POST'])
def register():
    try:
        if request.method == 'POST':
            firstname = request.forms.get('firstname')
            lastname = request.forms.get('lastname')
            email = request.forms.get('email')
            password = request.forms.get('password')

            connection = connect()
            cursor  = connection.cursor()

            cursor.execute("""INSERT INTO register (firstname, lastname, email, password)
                           VALUES(%s,%s,%s,%s)""",(firstname,lastname,email,password))
            connection.commit()
            print ("User added")

            return redirect('/homepage')
        else: 
            return template('register.html')
    except psycopg2.Error as e:
        print("ERROR CONNECTING TO POSTGREsql:", e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/login', method=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        connection = connect()
        cursor = connection.cursor()
        email = request.forms.get('email')
        password = request.forms.get('password')

        cursor.execute("""SELECT * FROM register WHERE email = %s AND password = %s """,(email, password))
        user = cursor.fetchall()

        if user:
            return redirect('/homepage')
        else:
            error = "Ingen användare med den angivna epostadressen finns i systemet."
            return template('First-Site.html', error=error)

    return template('First-Site.html', error=error)

#denna ska INTE ändras
@app.route('/static/<filename:path>')
def static_files(filename):
    return static_file(filename, root='./static')

if __name__ == '__main__':
    run(app, debug=True)