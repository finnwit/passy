# Passy

### Video Demo https://youtu.be/f5WHjpAfZZA

## Another PasswordManager. But Why
    So the whole Project idea Started last Year. 
    I was one of 14 million German citizen who's information have been leaked been leaked on Deezer.
    Since then i was constantly on my way to find the best sollutions, to be as Anonymous, as Stealth, as Secure in the World-Wide-Web.
    I started usind 1Password which worked pretty good for me. But i had to constantly export my logins from Chrome and push them to 1Password.
    So i startet to use ihe iCloud feature until i switched to Windows. So I startet do make my own password manager
    . At this time, its running loaclly on my Raspberry Pi 3.
    And i am super happy with it. I now have controll of my Data. I know where my Data is going **Finally** 😁

## Project Overview
    I build a Password-Manager for my final Project.
    It is running a Flask Instance locally on my Home Server. With it i have the power to controll where my data is going, and where not.

## Requirements
    In my Project i used Flask as my Framework. It uses bcrypt to encrypt the User logins to and sqlite3 running in the background.
    In my SQL-DB i run two Tables (one for User login, the other one for User Data). 
    For my cookies i use the Session libary. Flask is running selfmade HTML.

    **Here is a list of the Requirements:**
    bcrypt==4.1.2
    - blinker==1.7.0
    - cachelib==0.12.0
    - click==8.1.7
    - colorama==0.4.6
    - Flask==3.0.2
    - Flask-Session==0.6.0
    - Flask-WTF==1.2.1
    - itsdangerous==2.1.2
    - Jinja2==3.1.3
    - MarkupSafe==2.1.5
    - python-dotenv==1.0.1
    - Werkzeug==3.0.1
    - WTForms==3.1.2

## Code Structure
    Starting with HTML my main files can be found in the templates folder. [index.html](/templates/index.html) Here is my Home/Login page. 
    If you visit my webpage the first time, you can Sign Up using the Sign Up button on the left hand corner. You will get to /signin [signin.html](/templates/signin.html).
    If you register an account, you will be redirected to [index.html](/templates/index.html). 
    Now you can log into your account and you will be redirected to /account, wich is the file [account.html](/templates/account.html). You can now enter your first data. 
    This data will be processed by /addtopasswords. You can now edit your entry via the blue pen on the cards. For this you will be redirected to /edit/{idofentry}. 
    The HTML file behind this link is [edit.html](/templates/edit.html). You can also delete your entry via the red trashcan and you will be redirected to /delete/{idofentry}.
    You can now log out using the Logout button in the right hand corner. You will be redirectrd to the homepage / [index.html](/templates/index.html).
    Pretty much all the CSS is running through Bootstrap, and the same boilerplate [layout.html](/templates/layout.html).
    In my opinion it is easier said than done to make pretty looking websites, but with Bootrap i can use my full potential.
    But The main code goes trough [app.py](/app.py). Here i am doing all the heavy work. Mainly it is all Database query, encryption and session cookies i work with here.

## Key Functions in app.py
### createaccount
    createaccount gets an input from the Sign Up page using the post method. It uses the password and hashes it using bcrypt then stores it, together with the email_login and a Uniqe id.
### account
    account handels the User login. It copares the two hashes of the password (one tiped into the html form on [index.html](/templates/index.html) the other one from the database person).
    If everything is right, the function pulls all data of this particular user with his Uniqe id stored as person_id in the password db.
    It displays all of that in the [account.html](/templates/account.html). This goes all via post to stop leaking data from the User. If the User opted in, a server-side Session cookie is stored. 
### addtopassword
    this function stores data in my password db. It stores to every password a Unike KEY 
    and the person_id to associate it to a User.
### create_app()
    is the standard function that starts the whole programm by creating my database tables

## Data
    As stated earlier i use 2 tables
    The schema is down below:
    CREATE TABLE password
            (KEY INTEGER PRIMARY KEY,
            person_id INTEGER,
            website_name TEXT NOT NULL,
            email TEXT,
            password TEXT
            );
    CREATE TABLE person
            (id INTEGER PRIMARY KEY,
            email_login TEXT NOT NULL,
            password TEXT NOT NULL
            );
    the person Table is pretty self-explanitory i think. The only thing i have to add for the
    password Table is that person_id is linked via my app.py to id from person

## Challenges and Solutions
    Pretty much the hardest thing was to start coding. From now on i pretty puch do things
    fluently. Challenging was that the id sometimes were touple, somtimes not. That made
    it pretty hard for me to be so fluent, but it kind of worked. When i had problems i
    contacted Friends or searched through the Internet. That was also the strategie of 
    getting to know Bootstrap. Sometimes i asked CS50AI what the best sollutions were, like
    for encryption. But i think i maneged to do the most parts completly on my own

## Future Improvements
    Definately more comments. But for now i am happy. I will try to make a Chrome Ad-On, and i
    will try to also encrypt the password database. But mostly another Project.
