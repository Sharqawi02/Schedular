
# import psycopg2
# from bottle  import  Bottle, route, template, run, static_file, request, redirect
# from db import connect


# app = Bottle()


# @app.route('/')
# def index():
#      return template('First-Site.html')


# # Registering a new user in the database
# @app.route('/register' , method=[ 'GET','POST'])
# def register():
#     try:
#         if request.method == 'POST':
#             firstname = request.forms.get('firstname')
#             lastname = request.forms.get('lastname')
#             email = request.forms.get('email')
#             password = request.forms.get('password')

#             connection = connect()
#             cursor  = connection.cursor()

#             cursor.execute("""INSERT INTO register (firstname, lastname, email, password)
#                            VALUES(%s,%s,%s,%s)""",(firstname,lastname,email,password))
#             connection.commit()
#             print ("User added")

#             return redirect('/')
#         else: 
#             return template('register.html')
#     except psycopg2.Error as e:
#         print("ERROR CONNECTING TO POSTGREsql:", e)
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'connection' in locals():
#             connection.close()

# # login page and checking credentials from the database
# @app.route('/login', method=['POST', 'GET'])
# def login ():
#     if  request.method=='POST':
#         # Connect to your postgres
#         connection = connect ()
#         cursor = connection.cursor()
#         # Get the details from the form
#         email = request.forms.get('email')
#         password = request.forms.get('password')

#         cursor.execute("SELECT FROM register WHERE email = %s AND password = %s", (email, password))

#         registers = cursor.fetchone()


#         if registers:
#             return redirect('/First-Site')
#         else: 
#             return  template ('login.html', error="Wrong Email or Password!")
        

#     # If it is a GET Request then show the Login Page 
#     return  template ('login.html', error="Wrong Email or Password!")
    



# #denna ska INTE ändras
# @app.route('/static/<filename:path>')
# def static_files(filename):
#     return static_file(filename, root='./static')


# if __name__ == '__main__':
#     run(app, debug=True)



from psycopg2 import sql
from bottle import Bottle, route, template, request, redirect, run , static_file
from db import connect
import bcrypt
import logging

logging.basicConfig(filename='error.log', level=logging.ERROR)

app = Bottle()

@app.route('/')
def index():
    error = None
    return template('First-Site.html', error=error)


@app.route('/error')
def error():
    return template('Error.html')

# Registering a new user in the database
@app.route('/register', method=['GET','POST'])
def register():
    try:
        error = None
        if request.method == 'POST':
            firstname = request.forms.get('firstname')
            lastname = request.forms.get('lastname')
            email = request.forms.get('email')
            password = request.forms.get('password')

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            print("Hashed Password: ", hashed_password)


            connection = connect()
            cursor  = connection.cursor()


            cursor.execute(sql.SQL("SELECT * FROM register WHERE email = {}").format(sql.Literal(email)))
            existing_user = cursor.fetchone()

            # Checking for existing users with same username or email
            if existing_user:
                error = "User already exists"
                return redirect('/error')
            
            else:

                query = sql.SQL("INSERT INTO register (firstname, lastname, email, password) VALUES ({},{},{},{})").format(
                    sql.Literal(firstname),
                    sql.Literal(lastname),
                    sql.Literal(email),
                    sql.Literal(hashed_password)
            )
            

            cursor.execute(query)
            connection.commit()

            print ("User added")
            
            return redirect('/homepage.html')

        else:
            return template('First-Site.html', error=error)
    except Exception as e:
        logging.error =  "ERROR CONNECTING TO POSTGREsql: {}".format(e)
        
        print(error)
        return redirect('/error')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# login page and checking credentials from the database
@app.route('/login', method=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        connection = connect()
        cursor = connection.cursor()
        email = request.forms.get('email')
        password = request.forms.get('password')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute(sql.SQL("SELECT * FROM register WHERE email = {}").format(sql.Literal(email)))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(hashed_password, user[3].encode('utf-8')):
            return redirect('homepage.html')
            # else:
            #     error = "Felaktigt lösenord. Försök igen"
            #     return template('First-Site.html', error=error)
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