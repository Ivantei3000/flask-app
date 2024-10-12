from flask import Flask, render_template, request, make_response, url_for, redirect, session
from werkzeug.security import generate_password_hash,  check_password_hash
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import abort
import sqlite3;

app = Flask(__name__)
con = sqlite3.connect("My_DB.db")
cursor = con.cursor()
         
@app.route('/<file_name>/')
def page(file_name):
    try:
        return render_template(f'{file_name}.html')
    except TemplateNotFound:
        abort(404)
        
@app.route('/create/', methods=['GET', 'POST'])
def create():
    con = sqlite3.connect("My_DB.db")
    cursor = con.cursor()
    unic_username = True
    if request.method == 'POST':
        username = (request.form['username'])
        password = (request.form['password'])
        cursor.execute("SELECT username FROM Accaunts")
        result = cursor.fetchall()
        print(result)
        for i in result:
            if i[0] == username:
                unic_username = False
                print("exist")
                return render_template('create.html',message="Account is already exist")
            else:
                pass
                
        if unic_username:
            print("unic")
            password_hash = generate_password_hash(password)
            data = (username,password_hash)
            cursor.execute("INSERT INTO Accaunts (username,password_hash) VALUES (?, ?)", data)
            con.commit()
            unic_username = False
            return redirect(url_for("login"))
        
    
    return render_template('create.html')



@app.route('/login/', methods=['POST',  'GET'])    
def login():
    con = sqlite3.connect("My_DB.db")
    cursor = con.cursor()
    if request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('username')
        
        cursor.execute("SELECT username FROM Accaunts")
    for i in cursor:
        if i[0] == username:
            cursor.execute("SELECT password_hash FROM Accaunts")
            for i in cursor:
                if check_password_hash(i[0], password):
                    return make_response("Your username is:{}".format(username))
                
    return render_template('login.html')
    
    

@app.route('/login_with_sesions/', methods=['POST',  'GET'])    
def login_with_sessions():
    print(request.method)
    if request.method == 'POST':
        session['password'] = request.form.get('password')
        session['username'] = request.form.get('username')
        return render_template('login.html')
    
    if session['password'] != None and sesion['username'] != None:
        res =("Your username is: {}".format(sessions.get('username')))
        return res
    
    else:
        return render_template('login.html')

#def login():
    #print(request.method)
    #if request.method == 'POST':
       #res = make_response(redirect('/login'))
        #res.set_cookie("username", request.form.get('username'), 60*60*24*15)
        #res.set_cookie("password", request.form.get('password'), 60*60*24*15)
        #return res
    
    #if request.cookies.get('username') != None and request.cookies.get('password') != None:
        #res = make_response("Your username is: {}".format(request.cookies.get('username')))
        #return res
    
    #else:
        #return render_template('login.html')

if '__main__' == __name__ :
    app.run()
    
