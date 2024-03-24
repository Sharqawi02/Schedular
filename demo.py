from bottle  import  Bottle, route, template, run, error, static_file, redirect, request
import _mysql_connector


app = Bottle()

@app.route('/')
def index():
     failed_login = True
     return  template('home.html', failed_login=failed_login)

@app.route("/logIn", method="post")
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    
     






    return template('home.html', failed_login=False)
























@route ('error')
def handle_error():
     return template ("Error 404: We're working on the it")




#denna ska INTE ändras
@route("/static/<filename:path>")
def static_files(filename):
    return static_file(filename, root='static')


if __name__ == '__main__':
    run(app, debug=True)