from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3
import bcrypt
from dotenv import load_dotenv
import os
from flask_session import Session


app = Flask(__name__, static_url_path='/static')

load_dotenv('.env')
app.secret_key = os.getenv('SECRET_KEY')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)



@app.route('/set/')
def set():
    if 'user_id' in session:
        session['key'] = session['user_id']
        session.permanent=True
        return 'ok'
    else:
        return 'User not logged in', 401

@app.route('/get/')
def get():
    return session.get('key', 'not set')


# Log In
@app.route("/")
def index():
    return render_template("index.html")
        
    
# account page
@app.route("/account", methods=["POST"])
def account():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        setcookie = request.form.get("loggedin")

        db = sqlite3.connect("passwords.db", check_same_thread=False)
        #create cursor
        cur = db.cursor()
        cur.execute('''SELECT password FROM person WHERE email_login = ?''', (email,))
        user_password = cur.fetchone()
        # check if account exists and password right
        if user_password == None:
            # prompt for wrong email or password
            return render_template("index.html", message= "wrong password, or email")
        
        # else
        if user_password is not None and bcrypt.checkpw(password.encode("utf-8"), user_password[0]):
            # if yes then get the id
            cur.execute('''SELECT id FROM person WHERE email_login = ?''', (email, ))
            user_id = cur.fetchone()
            # save the id in session
            session['user_id'] = user_id[0]
            if setcookie == '1':
                set()
            # fetch all passwords
            listoflogins = fetchlogins(user_id[0])
            return render_template("account.html", accounts = listoflogins)
        else:
            return render_template("index.html", message = "Oh oh. Something went Wrong Error 001")
    except:
        return render_template("error.html", message = 0o005) 
    finally:
        db.close()

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
            

# signin page
@app.route("/signin")
def signin():
    return render_template("signin.html")


# create account and save to db
@app.route("/createaccount", methods=["POST"])
def createaccount():
    try:
        db = sqlite3.connect("passwords.db", check_same_thread=False)
        #create cursor
        cur = db.cursor()
        cur.execute('SELECT COUNT() as count FROM person;')
        count = cur.fetchone()
        email = request.form.get("email")
        password = request.form.get("password")
        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))
        cur.execute('''INSERT INTO person (id, email_login, password) VALUES(?, ?, ?);''', (int(count[0])+1, email, hash_password))
        db.commit()
        return render_template("index.html", message = f"You have Signed In {id} ", id = count)
    except:
        return render_template("error.html", message = 0o004) 
    finally:
        db.close()



# testing tool
@app.route("/deleteall")
def deleteall():
    try:
        db = sqlite3.connect("passwords.db", check_same_thread=False)
        #create cursor
        cur = db.cursor()
        cur.execute('''DELETE FROM password''')
        cur.execute('''DELETE FROM person''')
        db.commit()
        return render_template("index.html", message= "Deleted all")
    except:
        return render_template("error.html", message = 0o003) 
    finally:
        db.close()



@app.route("/addtopassword", methods=["POST"])
def addtopassword():
    user_id = session.get('user_id')
    try:
        db = sqlite3.connect("passwords.db", check_same_thread=False)
        #create cursor
        cur = db.cursor()
        cur.execute('SELECT KEY FROM password ORDER BY KEY DESC;')
        count = cur.fetchone()
        if user_id is None:
            return render_template("index.html", message = "Please sign in again")
        else:
            website = request.form.get("website")
            email = request.form.get("email")
            password = request.form.get("password")
            if count == None:
                countupdate = 0 
            else:
                countupdate = int(count[0])
            cur.execute('INSERT INTO password(KEY, person_id, website_name, email, password) VALUES(?, ?, ?, ?, ?);', (countupdate+1, user_id, website, email, password))
            db.commit()
            listoflogins = fetchlogins(user_id)
            return render_template("account.html", accounts = listoflogins, message = "Added")
    except:
        return render_template("error.html", message = 0o002) 
    finally:
        db.close()

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # Connect to your database
    conn = sqlite3.connect("passwords.db", check_same_thread=False)
    cur = conn.cursor()
   
    cur.execute('SELECT person_id FROM password WHERE KEY= ? ', (id,))
    user_id = cur.fetchone()
    user_id = session.get('user_id')
    # Execute a query to delete the account with the given ID
    cur.execute('DELETE FROM password WHERE KEY = ?', (id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


    # Redirect the user back to the account page
    listoflogins = fetchlogins(user_id)
    return render_template('account.html', accounts = listoflogins)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Connect to your database
    conn = sqlite3.connect('passwords.db')
    cur = conn.cursor()

    if request.method == 'POST':
        # Get the updated data from the form
        website = request.form.get('website')
        email = request.form.get('email')
        password = request.form.get('password')

        # Execute a query to update the account with the given ID
        cur.execute('UPDATE password SET website_name = ?, email = ?, password = ? WHERE Key = ?', (website, email, password, id))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        user_id = session.get('user_id')
    

    # Redirect the user back to the account page
        listoflogins = fetchlogins(user_id)
        return render_template('account.html', accounts = listoflogins)

    else:
        # Execute a query to get the current data of the account
        cur.execute('SELECT KEY, website_name, email, password FROM password WHERE KEY = ?', (id,))
        account = cur.fetchone()

        # Close the connection
        conn.close()

        # Render the edit page with the current data of the account
        return render_template('edit.html', account=account)

def fetchlogins(user_id):
    
    try:
        db = sqlite3.connect("passwords.db", check_same_thread=False)
        cur = db.cursor()

        # Execute the SQL query
        cur.execute("SELECT * FROM password WHERE person_id = ?", (user_id,))

        # Fetch all the rows
        rows = cur.fetchall()

        # Close the database connection
        db.close()

        # Convert each row to a dictionary
        logins = [{"id": row[0], "website": row[2], "email": row[3], "password": row[4]} for row in rows]

        return logins
    finally:
        db.close()



def initialize_database():
    db = sqlite3.connect("passwords.db", check_same_thread=False)
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS password
            (KEY INTEGER PRIMARY KEY,
            person_id INTEGER,
            website_name TEXT NOT NULL,
            email TEXT,
            password TEXT
            );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS person
            (id INTEGER PRIMARY KEY,
            email_login TEXT NOT NULL,
            password TEXT NOT NULL
            );''')
    db.close()



def create_app():
    app = Flask(__name__)

    with app.app_context():
        initialize_database()
    return app

create_app()