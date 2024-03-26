import psycopg2
from bottle  import  Bottle, route, template, run, static_file, request, redirect
from db import connect


app = Bottle()


@app.route('/')
def index():
     return  template('register.html')

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

            cursor.close()

            return redirect('/')
        else: 
            return template('register.html')
    except psycopg2.Error as e:
        print("ERROR CONNECTING TO POSTGREsql:", e)



#denna ska INTE ändras
@route("/static/<filename:path>")
def static_files(filename):
    return static_file(filename, root='static')


if __name__ == '__main__':
    run(app, debug=True)