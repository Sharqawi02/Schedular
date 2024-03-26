from bottle  import  Bottle, route, template, run, static_file, request, redirect
from db import connect


app = Bottle()


@app.route('/')
def index():
     failed_login = True
     return  template('register.html', failed_login=failed_login)

@app.route('/register' , method=[ 'GET','POST'])
def register():
    if request.method == 'POST':
        firstname = request.forms.get('firstname')
        lastname = request.forms.get('Lastname')
        email = request.forms.get('Email')
        password = request.forms.get('Password')

        anslut = connect()
        cur  = anslut.cursor()

        cur.execute("INSERT INTO register (forname, lastname, email, password) VALUES(%s,%s,%s)",(firstname,lastname,email,password))
        anslut.commit()
        print ("User added")

        return redirect('/')
    else: 
        return template('register.html')




#denna ska INTE ändras
@route("/static/<filename:path>")
def static_files(filename):
    return static_file(filename, root='static')


if __name__ == '__main__':
    run(app, debug=True)