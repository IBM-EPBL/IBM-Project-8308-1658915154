from flask import Flask, render_template, request, redirect, url_for, session


import ibm_db


import re


app = Flask(__name__)


app.secret_key = 'a'


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSL ServerCertificate=DigiCertGlobalRootCA.crt;UID=djd71460;PWD=IhjMkjoM7EtyxzH4;",'','')

@app.route('/')


def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])


def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !' 
        else:
            insert_sql = "INSERT INTO users VALUES (?, ?, ?)" 
            prep_stmt = ibm_db.prepare(conn, insert_sql) 
            ibm_db.bind_param(prep_stmt, 1, username) 
            ibm_db.bind_param(prep_stmt, 2, email) 
            ibm_db.bind_param(prep_stmt, 3, password) 
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !' 
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)



@app.route('/login', methods=['GET', 'POST'])


def login():
    global userid
    msg = ''
    if request.method == 'POST':
        username = request.form['username']


        password = request.form['password']


        sql = "SELECT * FROM users WHERE username =? AND password=?"


        stmt = ibm_db.prepare(conn, sql)


        ibm_db.bind_param(stmt, 1, username)


        ibm_db.bind_param(stmt, 2, password)


        ibm_db.execute(stmt)


        account = ibm_db.fetch_assoc(stmt)


        print(account)


        if account:
            session['loggedin'] = True


            session['id'] = account['USERNAME']


            userid = account['USERNAME']


            session['username'] = account['USERNAME']


            msg = 'Logged in successfully !'


            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !' 
    return render_template('login.html', msg=msg)



if __name__ == '_main_':
    app.run(host='0.0.0.0')
    #app.run(debug=True)