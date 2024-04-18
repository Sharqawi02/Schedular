from bottle import Bottle, route, template, run, static_file, request, redirect
import psycopg2
from storage.db import connect

app = Bottle()

@app.route('/')
def index():
     return template('First-Site.html', error="")

@app.route('/homepage')
def homepage_route():
    return template('homepage.html')

@app.route('/register' , method=[ 'GET','POST'])
def register():
    error = ""
    if request.method == 'POST':
        firstname = request.forms.get('firstname')
        lastname = request.forms.get('lastname')
        email = request.forms.get('email')
        password = request.forms.get('password')

        connection = connect()
        cursor  = connection.cursor()

        # Check if the email already exists in the database
        cursor.execute("""SELECT * FROM register WHERE email = %s""", (email,))
        user = cursor.fetchone()
        if user:
            # If the user exists, return an error message
            error = "E-postadressen är redan registrerad."
            return template('First-site.html',error=error)

        cursor.execute("""INSERT INTO register (firstname, lastname, email, password)
                       VALUES(%s,%s,%s,%s)""",(firstname,lastname,email,password))
        connection.commit()
        print ("User added")

        return redirect('/homepage')
    else: 
        return template('First-Site.html', error=error)

@app.route('/login', method=['POST', 'GET'])
def login():
    # error = ""
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
            error = "Felaktigt lösenord."
            return template('First-Site.html', error=error)

    return template('First-Site.html', error=error)



@app.route('/static/<filename:path>')
def static_files(filename):
    return static_file(filename, root='./static')

if __name__ == '__main__':
    run(app, debug=True)




'''
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
    except acopg2.Error as e:
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
'''