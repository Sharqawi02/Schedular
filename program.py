from bottle import Bottle, route, template, run, static_file, request, redirect, response
import psycopg2
from storage.db import connect
import json

app = Bottle()


@app.route('/')
def index():
     return template('First-Site.html', error={})

@app.route('/homepage')
def homepage_route():
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        return template('homepage.html', is_user_logged_in=is_user_logged_in)
    else:
        return redirect("/")

@app.route('/register' , method=[ 'GET','POST'])
def register():
    if request.method == 'POST':
        firstname = request.forms.get('firstname')
        lastname = request.forms.get('lastname')
        email = request.forms.get('email')
        password = request.forms.get('password')

        connection = connect()
        cursor  = connection.cursor()

        # Check if the email already exists in the database
        cursor.execute("""SELECT * FROM users WHERE email = %s""", (email,))
        user = cursor.fetchone()
        if user:
            # If the user exists, return an error message
            error_message = "E-postadressen är redan registrerad."
            return template('First-site.html',error={
                "email_already_registered": error_message,
            })
        else:
            cursor.execute("""INSERT INTO users (firstname, lastname, email, password)
                        VALUES(%s,%s,%s,%s)""",(firstname,lastname,email,password))
            connection.commit()

            return redirect('/homepage')
    else: 
        return template('First-site.html',error={})

@app.route('/login', method=['POST', 'GET'])
def login():
    if request.method == 'POST':
        connection = connect()
        cursor = connection.cursor()
        email = request.forms.get('email')
        password = request.forms.get('password')

        cursor.execute("""SELECT id FROM users WHERE email = %s AND password = %s """,(email, password))
        user_id = cursor.fetchall()

        if user_id:
            response.set_cookie("user_id", str(user_id[0]))
            return redirect('/homepage')
        else:
            error_message = "E-postadressen eller lösenordet är fel."
            return template('First-site.html',error={
                "wrong_password": error_message
            })
    else:
        return template('First-site.html',error={})

@app.route("/get_events", method=["GET"])
def get_events():
    # 1. Hämta alla event från databasen

    # 2. Gör om strukturen så att varje event får följande struktur
    # {
    #    "title": "Min titel"
    #    "start": "2024-04-24"
    # }
    return json.dumps([
        {
            "title": "Test",
            "start": "2024-05-24"
        }
    ])

@app.route("/create_event", method=["POST"])
def create_event():
    # 1. Hämta alla värden som skickats från formuläret
    task_date = getattr(request.forms, "task_date")

    # 2. Lägg in eventet (med alla värden) i databasen

    # 3. Skicka tillbaka användaren till kalendersidan
    redirect("/homepage")



@app.route('/forgot-password', method=['GET', 'POST'])
def forgot_password():
   error = ""
   if request.method == 'POST':
       email = request.forms.get('email')
       new_password = request.forms.get('new_password')


       # Check if the email exists in the database
       connection = connect()
       cursor = connection.cursor()


       cursor.execute("""SELECT * FROM users WHERE email = %s""", (email,))
       user = cursor.fetchone()


       if user:
           # Generate a new password
           import secrets
           # new_password = secrets.token_urlsafe(10) 


           # Update the user's password in the database
           cursor.execute("""UPDATE users SET password = %s WHERE email = %s""", (new_password, email))
           connection.commit()


          
           new = f"New password for {email}: {new_password}"


           return template('First-Site.html', new=new, error=None)
       else:
           error = "Email not found."
           return template('forgot-password.html', error=error, new=None)


   return template('forgot-password.html', error=error, new=None)

@app.route('/profilepage')
def profilepage():
    return template('profilepage.html')


@app.route('/static/<filename:path>')
def static_files(filename):
    return static_file(filename, root='./static')

if __name__ == '__main__':
    run(app, debug=True)


