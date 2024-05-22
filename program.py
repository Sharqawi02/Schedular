from bottle import Bottle, route, template, run, static_file, request, redirect, response
import psycopg2
from storage.db import connect, GetUserInfo
import json
import secrets
import os
from passlib.hash import pbkdf2_sha256
from datetime import datetime

app = Bottle()

@app.route('/')
def index():
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        return redirect("/homepage")
    else:
        return template('first-site.html', UserInfo=None)
    
@app.route('/login', method=[ 'GET','POST'])
def index():
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        return redirect("/homepage")
    else:
        if request.method == 'POST':
            email = request.forms.get('email')
            password = request.forms.get('password')

            connection = connect()
            cursor = connection.cursor()
            
            cursor.execute("""SELECT id, password, token FROM users WHERE email = %s""", (email,))
            user_id_and_password = cursor.fetchone()

            if user_id_and_password:
                if pbkdf2_sha256.verify(password, user_id_and_password[1]):
                    response.set_cookie("user_id", str(user_id_and_password[0]))
                    response.set_cookie("user_token", str(user_id_and_password[2]))

                    cursor.close()  # close cursor
                    connection.close()  # close connection

                    return redirect('/homepage')
            else:

                cursor.close()  # close cursor
                connection.close()  # close connection

                return template('login.html', wrong=True)

        return template('login.html', wrong=False)
    
@app.route('/register', method=['GET','POST'])
def register():
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        return redirect("/homepage")
    else:
        if request.method == 'POST':
            firstname = request.forms.get('firstname')
            lastname = request.forms.get('lastname')
            email = request.forms.get('email')
            password = request.forms.get('password')

            connection = connect()
            cursor  = connection.cursor()

            cursor.execute("""SELECT * FROM users WHERE email = %s""", (email,))
            MailExist = cursor.fetchone()

            if MailExist:
                
                connection = connect()
                cursor  = connection.cursor()

                return template('registrera.html', wrong=True)
            else:

                hash = pbkdf2_sha256.hash(password)
                token = f"{hash}Schedular:)"

                #profile_picture är default bilden som alla kommer få i början.
                cursor.execute("""INSERT INTO users (firstname, lastname, email, password, profile_picture, token)
                VALUES(%s,%s,%s,%s,%s,%s)""",(firstname,lastname,email,hash, 'profilbild.jpg', token))
                connection.commit()

                cursor.close()  # close cursor
                connection.close()  # close connection

                return redirect('/login')


        return template('registrera.html', wrong=False)


@app.route('/homepage')
def homepage_route():
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:

        connection = connect()

        UserInfo = GetUserInfo(connection, is_user_logged_in)

        if UserInfo is None:
            # if user is logged in this will remove the 'user_id' cookie to log the user out
            response.set_cookie('user_id', '', expires=0)
            response.set_cookie('user_token', '', expires=0)
            # redirects to the homepage
            return redirect('/')

        return template('homepage.html', UserInfo=UserInfo)
    else:
        return redirect("/")

@app.route("/get_events", method=["GET"])
def get_events():
    # 1. Hämta alla event från databasen
    connection = connect()
    cursor = connection.cursor()
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        cursor.execute(f"SELECT * FROM events AS e JOIN users AS u ON u.id = e.user_id WHERE u.id = {is_user_logged_in} ")
        events = cursor.fetchall()
        all_events = []
        for event in events:
            one_event = {
                "id": event[0],
                "title": event[1],               
                "description":event[2],
                "startdate": event[3].isoformat(),      
                "enddate": event[9].isoformat(),                
                "priority": event[4],  
                "category": event[5],
                "start":event[7].isoformat(),
                "end": event[8].isoformat()
            }
            all_events.append(one_event)

        cursor.close()  # close cursor
        connection.close()  # close connection

        return json.dumps(all_events)

@app.route("/create_event", method=["POST"])
def create_event():
    connection = connect()
    cursor = connection.cursor()
    # 1. Hämta alla värden som skickats från formuläret
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

    is_user_logged_in = request.get_cookie("user_id")

    # 2. Lägg in eventet (med alla värden) i databasen
    cursor.execute("""INSERT INTO events (event_start_date, event_end_date,  event_title, event_priority, event_category, event_description, user_id, events_start_time, events_end_time)
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (event_start_date,event_end_date, event_title, event_priority, event_category, event_description, is_user_logged_in, start, end))
  
    connection.commit()
    # 3. Skicka tillbaka användaren till kalendersidan
    cursor.close()  # close cursor
    connection.close()  # close connection
    return redirect("/homepage")

@app.route("/update_event/<event_id>", method=["POST"])
def update_event(event_id):
    connection = connect()
    cursor = connection.cursor()
    # 1. Hämta alla värden som skickats från formuläret
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

    is_user_logged_in = request.get_cookie("user_id")

    cursor.execute("""
        UPDATE events
        SET event_start_date = %s,
            event_end_date = %s,
            event_title = %s,
            event_priority = %s,
            event_category = %s,
            event_description = %s,
            user_id = %s,
            events_start_time = %s,
            events_end_time = %s
        WHERE id = %s
    """, (event_start_date, event_end_date, event_title, event_priority, event_category, event_description, is_user_logged_in, start, end, event_id))

    connection.commit()
    # 3. Skicka tillbaka användaren till kalendersidan
    cursor.close()  # close cursor
    connection.close()  # close connection
    return redirect("/homepage")


# Denna funktion hanterar översikten av events, när användaren trycker visa information av event. 
@app.route('/redigera/event', method=['GET', 'POST'])
def redigera_event():
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        connection = connect()
        cursor = connection.cursor()
        # 1. Hämta alla värden som skickats från formuläret
        event_id = getattr(request.forms, "event_id")

        cursor.execute('select * from events where id = %s', (event_id,))
        event_info = cursor.fetchone()

        # om user_id från händelsen matchar användarens
        if str(event_info[6]) == str(is_user_logged_in):
            # Convert full datetime strings to time-only strings
            start_time = datetime.strptime(str(event_info[7]), "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            end_time = datetime.strptime(str(event_info[8]), "%Y-%m-%d %H:%M:%S").strftime("%H:%M")

            return template('redigera_event', event_info=event_info, start_time=start_time, end_time=end_time, event_id=event_id)
        else:
            return redirect("/homepage")
        
@app.route('/radera/event/<id>', method=['GET', 'POST'])
def radera_event(id):
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        connection = connect()
        cursor = connection.cursor()
        
        cursor.execute('delete from events where id = %s', (id,))
        connection.commit()

        cursor.close()  # close cursor
        connection.close()  # close connection

        return redirect('/homepage')
# profile Routes

@app.route('/upload/profile/picture', method=['GET', 'POST'])
def upload_profile_picture():
    '''
    Denna funktion Lägger Till ProfilBild
    '''
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:

        ProfilePicture = request.files.get('ProfilePicture')
                    
        filename = ProfilePicture.filename

        connection = connect()
        cursor = connection.cursor()

        cursor.execute("update users SET profile_picture = %s where id = %s", (filename, is_user_logged_in))
        connection.commit()
        
        cursor.close()  # close cursor
        connection.close()  # close connection

        filepath = os.path.join('static/images/profile_pictures', filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        ProfilePicture.save(filepath)

        return redirect('/profilepage')
    
    else:
        # Om användaren inte är inloggad, skicka tillbaka till startsidan
        return redirect('/')

@app.route('/update/user/info', method=['GET', 'POST'])
def update_user_info():
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:
        FirstName = request.forms.get('FirstName')
        LastName = request.forms.get('LastName')
        Email = request.forms.get('Email')

        connection = connect()
        cursor = connection.cursor()

        cursor.execute("UPDATE users SET firstname = %s, lastname = %s, email = %s WHERE id = %s", 
                       (FirstName, LastName, Email, is_user_logged_in))
        connection.commit()

        cursor.close()  # close cursor
        connection.close()  # close connection

        return redirect('/profilepage') 

    else:
        # Om användaren inte är inloggad, skicka tillbaka till startsidan
        return redirect('/')

@app.route('/profilepage')
def profilepage():
    is_user_logged_in = request.get_cookie("user_id")
    if is_user_logged_in:

        connection = connect()

        UserInfo = GetUserInfo(connection, is_user_logged_in)

        
        
        return template('profilepage.html', UserInfo=UserInfo)
    else:
        # Om användaren inte är inloggad, skicka tillbaka till startsidan
        return redirect('/')
    
@app.route('/logout')
def logout():
    is_user_logged_in_cookie = request.get_cookie('user_id')
    if is_user_logged_in_cookie:
        # if user is logged in this will remove the 'user_id' cookie to log the user out
        response.set_cookie('user_id', '', expires=0)
        response.set_cookie('user_token', '', expires=0)
        # redirects to the homepage
        return redirect('/')
    else:
        return redirect('/')


@app.route('/static/<filename:path>')
def static_files(filename):
    return static_file(filename, root='./static')

if __name__ == '__main__':
    run(app, debug=True)