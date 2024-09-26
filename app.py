from flask import Flask, render_template, request, make_response, url_for
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import abort
import sqlite3;

con = sqlite3.connect("login.db")
cursor = con.cursor() 
app = Flask(__name__)

@app.route('/<file_name>/')
def page(file_name):
    try:
        return render_template(f'{file_name}.html')
    except TemplateNotFound:
        abort(404)
        
@app.route('/create/', methods=['GET', 'POST'])
def create():
    con = sqlite3.connect("login.db")
    cursor = con.cursor()
    if request.method == 'POST':
        username = (request.form['username'])
        password = (request.form['password'])
        data = (username, password)
        cursor.execute("INSERT INTO Accaunts (username, password) VALUES (?, ?)", data)
        con.commit()
 
    return render_template('login.html')

@app.route('/login/', methods=['POST',  'GET'])
def login():
    res = make_response("")
    
    if request.method == 'POST':
        print(1)
        if request.cookies.get('username')  and request.cookies.get('password') :
            print(1.1)
            res = make_response("Your username is: {}".format(request.cookies.get('username')))
        else:
            print(1.2)
            print(request.form)
            res.set_cookie("username", request.form.get('username'), 60*60*24*15)
            res.set_cookie("password", request.form.get('password'), 60*60*24*15)
            res.headers['location'] = url_for('login')
        return res
    
    if request.cookies.get('username') != None and request.cookies.get('password') != None:
        res = make_response("Your username is: {}".format(request.cookies.get('username')))
        return res
    
    else:
        return render_template('login.html')


@app.route('/article/', methods=['POST',  'GET'])
def article():
    if request.method == 'POST':
        print(request.form)
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60*60*24*15)
        res.headers['location'] = url_for('article')
        return res, 302

    return render_template('article.html')
    

if '__main__' == __name__ :
    app.run()
    
