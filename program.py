from bottle import Bottle, route, template, run, static_file, request, redirect, response
import psycopg2
from storage.db import connect
import json
import secrets

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
            cursor.close()  # close cursor
            connection.close()  # close connection
            return template('First-site.html',error={
                "email_already_registered": error_message,
            })
        else:
            cursor.execute("""INSERT INTO users (firstname, lastname, email, password)
                        VALUES(%s,%s,%s,%s)""",(firstname,lastname,email,password))
            connection.commit()
           
            cursor.execute("""SELECT * FROM users where firstname = %s and lastname = %s and email = %s and password = %s""", (firstname,lastname,email,password))
            user_id = cursor.fetchone()

            response.set_cookie("user_id", str(user_id[0]))

            cursor.close()  # close cursor
            connection.close()  # close connection

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
        user_id = cursor.fetchone()
        if user_id:
            user_id = user_id[0]
            response.set_cookie("user_id", str(user_id))

            cursor.close()  # close cursor
            connection.close()  # close connection

            return redirect('/homepage')
        else:
            error_message = "E-postadressen eller lösenordet är fel."
            cursor.close()  # close cursor
            connection.close()  # close connection
            return template('First-site.html',error={
                "wrong_password": error_message
            })
    else:
        return template('First-site.html',error={})
    
@app.route("/get_events", method=["GET"])
def get_events():
    # 1. Hämta alla event från databasen
    connection = connect()
    cursor = connection.cursor()
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        cursor.execute(f"SELECT * FROM events AS e JOIN users AS u ON u.id = e.user_id WHERE u.id = {is_user_logged_in} ")
        events = cursor.fetchall()
        print(events)
        all_events = []
        for event in events:
            one_event = {
                "title": event[1],               
                "description":event[2],
                "date": event[3].isoformat(),                
                "startdate": event[3].isoformat(),      
                "enddate": event[9].isoformat(),                
                "priority": event[4],  
                "category": event[5],
                "start":event[7].isoformat(),
                "end": event[8].isoformat()
            }
            all_events.append(one_event)
            print(event)
        print(all_events)

        cursor.close()  # close cursor
        connection.close()  # close connection

        return json.dumps(all_events)

@app.route("/create_event", method=["POST"])
def create_event():
    connection = connect()
    cursor = connection.cursor()
    # 1. Hämta alla värden som skickats från formuläret
    event_date = getattr(request.forms, "event_date")
    event_title = getattr(request.forms, "event_title")
    event_start_date = getattr(request.forms, "event_start_date")
    event_end_date = getattr(request.forms, "event_end_date")
    event_priority = getattr(request.forms, "event_priority")
    event_category = getattr(request.forms, "event_category")
    event_description = getattr(request.forms, "event_description") 
    events_start_time = getattr(request.forms, "events_start_time")
    events_end_time = getattr(request.forms, "events_end_time")

    #python tar inte emot timestamp så detta löses genom att kombinera date och timestamp för att få fram det
    #korrekta formatet (åååå-mm-dd-hh-mm-ss)
    start = f"{event_start_date} {events_start_time}"
    end = f"{event_end_date} {events_end_time}"
    start = f"{event_start_date} {events_start_time}"
    end = f"{event_end_date} {events_end_time}"

    is_user_logged_in = request.get_cookie("user_id")

    # 2. Lägg in eventet (med alla värden) i databasen
    cursor.execute("""INSERT INTO events (event_start_date, event_end_date,  event_title, event_priority, event_category, event_description, user_id, events_start_time, events_end_time)
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (event_start_date,event_end_date, event_title, event_priority, event_category, event_description, is_user_logged_in, start, end))
  
    connection.commit()
    # 3. Skicka tillbaka användaren till kalendersidan
    cursor.close()  # close cursor
    connection.close()  # close connection
    redirect("/homepage")

@app.route('/forgot-password', method=['GET', 'POST'])
def forgot_password():
    error = {}
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
            # new_password = secrets.token_urlsafe(10) 
            # Update the user's password in the database
            cursor.execute("""UPDATE users SET password = %s WHERE email = %s""", (new_password, email))
            connection.commit()

            new = f"New password for {email}: {new_password}"
            cursor.close()  # close cursor
            connection.close()  # close connection
            return template('First-Site.html', new=new, error=error)
        else:
            error["email_not_found"] = "Email not found."
            cursor.close()  # close cursor
            connection.close()  # close connection
            return template('forgot-password.html', error=error, new=None)

    return template('forgot-password.html', error=error, new=None)
@app.route('/profilepage')
def profilepage():
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        print (is_user_logged_in)
        # User logged in, getting their information from database
        connection = connect()
        cursor = connection.cursor()
        user_id = eval(is_user_logged_in) #extrakting user_id 
        cursor.execute("""SELECT firstname, lastname, email FROM users WHERE id = %s""", (user_id,))
        user_data = cursor.fetchone()  # fetches the user information from database
        connection.close()  # closes the connection
        cursor.close()  # close cursor
        connection.close()  # close connection
        return template('profilepage.html', firstname=user_data[0], lastname=user_data[1], email=user_data[2])
    else:
        # Om användaren inte är inloggad, skicka tillbaka till startsidan
        return redirect('/')
@app.route('/redirect_to_profilepage', method='GET')
def redirect_to_profilepage():
    return redirect('/profilepage')
@app.route('/logout')
def logout():
    is_user_logged_in_cookie = request.get_cookie('user_id')
    if is_user_logged_in_cookie:
        # if user is logged in this will remove the 'user_id' cookie to log the user out
        response.set_cookie('user_id', '', expires=0)
        # redirects to the homepage
        return redirect('/')
    else:
        return redirect('/')
@app.route('/static/<filename:path>')
def static_files(filename):
    return static_file(filename, root='./static')

if __name__ == '__main__':
    run(app, debug=True)