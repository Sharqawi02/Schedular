import psycopg2
from bottle  import  Bottle, route, template, run, static_file, request, redirect
from db import connect


app = Bottle()


@app.route('/')
def index():
     return  template('firstSide.html')


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

            return redirect('/')
        else: 
            return template('register.html')
    except psycopg2.Error as e:
        print("ERROR CONNECTING TO POSTGREsql:", e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# login page and checking credentials from the database
@app.route('/login', method=['POST', 'GET'])
def login ():
    if  request.method=='POST':

        
        
        # Connect to your postgres
        connection = connect ()
        cursor = connection.cursor()
        # Get the details from the form
        email = request.forms.get('email')
        password = request.forms.get('password')

        cursor.execute("SELECT FROM register WHERE email = %s AND password = %s", (email, password))

        registers = cursor.fetchone()


        if registers:
            return redirect('/firsslide')
        else: 
            return  template ('login.html', error="Wrong Email or Password!")
        

    # If it is a GET Request then show the Login Page 
    return  template ('login.html', error="Wrong Email or Password!")
    



#denna ska INTE ändras
@route("/static/<filename:path>")
def static_files(filename):
    return static_file(filename, root='./static')


if __name__ == '__main__':
    run(app, debug=True)