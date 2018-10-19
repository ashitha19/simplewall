#server.py file for Simple Wall example.

from flask import Flask, request, redirect, render_template, session, flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX=re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
app = Flask(__name__)
app.secret_key='myKey'
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success_reg')
def success_reg():    
    return render_template('success_registration.html')

@app.route('/success_login')
def success_login():
    debugHelp("RESERVE METHOD")
    if not session['login_flag']:
        msg = "Please login first before visiting this page!!!"   
        return render_template('success_login.html', msg = msg)
    elif session['login_flag'] == True :
        msg = "Welcome, (" + session['login_first_name'] + "). You are successfully logged in!!!"   
        return render_template('chat.html', msg = msg)    
        

@app.route('/process_registration', methods=['POST'])
def process():
    #get values from form
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    #validate each field
    #first_name validation
    if not first_name:
        flash('First name cannot be blank')
    elif len(first_name) < 3:
        flash('Minimum 3+ characters are required for first name')
    elif not first_name.isalpha():
        flash('Only alpha characters are accepeted for first name')
    #last_name validation 
    if not last_name:
        flash('last name cannot be blank')
    elif len(last_name) < 3:
        flash('Minimum 3+ characters are required for last name')
    elif not last_name.isalpha():
        flash('Only alpha characters are accepeted for last name')        
    #email validation
    if not email:
        flash('Email entered is not in a valid format')
    elif not (EMAIL_REGEX.match(request.form['email'])):
        flash('Email entered is not in a valid format')
    #password validation
    if not password:
        flash('Password cannot be blank')
    if not confirm_password:
        flash('Confirm Password cannot be blank')
    if not (password==confirm_password):
        flash('Password and Confirm Password values are not matching')
    #If there is any validations errors in registration, print all flash messages in the home page
    if '_flashes' in session.keys():
        return redirect("/")     

    #Check if email is already registered
    mysql = connectToMySQL("simplewall")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["email"] }
    result = mysql.query_db(query, data)
    if result:
        flash("Email Already exists...")
        return redirect('/')                 
            
    #bcrypt the password before storing to the database
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    #store the new record in the database
    mysql = connectToMySQL("simplewall")
    query = "INSERT INTO users (first_name, last_name, email, password, created_at) values ( %(first_name)s,%(last_name)s,%(email)s,%(password)s,now());"
    data = {    'first_name' : first_name,
                'last_name' : last_name,
                'email' : email,
                'password' : pw_hash 
            }            
    new_user_id = mysql.query_db(query,data)
    #save first-name in the session to print in the success page
    session['registered_user'] = first_name.title()
    # redirect to success page
    return redirect("/success_reg")

@app.route('/process_login', methods=['POST'])
def login_check():
    email = request.form['email']
    password = request.form['password']
    #email validation
    if not email:
        flash('Email entered is not in a valid format')
    elif not (EMAIL_REGEX.match(request.form['email'])):
        flash('Email entered is not in a valid format')
    #password validation
    if not password:
        flash('Password cannot be blank')    

    # see if the username provided exists in the database
    mysql = connectToMySQL("simplewall")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : email }
    result = mysql.query_db(query, data)
    if result:
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.check_password_hash(result[0]['password'], password):
            # if we get True after checking the password, we may put the user id in session
            session['login_userid'] = result[0]['userid']
            session['login_first_name'] = result[0]['first_name']
            session['login_flag'] = True
            # never render on a post, always redirect!
            return redirect('/display_chat')
    # if we didn't find anything in the database by searching by username or if the passwords don't match,
    # flash an error message and redirect back to a safe route
    session['login_flag'] = False
    flash("You could not be logged in")
    return redirect("/")

@app.route('/logout')
def logout():
    print("Logout")
    session.clear()
    return redirect('/')

#display list of users with the send message in the chat.html
@app.route('/display_chat')
def display_chat():
    # if not session['login_flag']:
    #     msg = "Please login first before visiting this page!!!"   
    #     return render_template('success_login.html', msg = msg)
    # if not session['login_userid']:                                                   #add this line on monday,oct 15
    #     flash("Pease login first before visiting this page!!!")
    #     return render_template('/')
    if not session['login_flag']:
        flash("Please login first before visiting this page!!!!")
        return redirect('/')
    if '_flashes' in session.keys():
        return redirect('/')
    #Get all users other than the logged in user
    mysql=connectToMySQL("simplewall")
    query="SELECT * FROM users WHERE userid not in (%(userid)s);"
    data={
        'userid' : session['login_userid']
    }
    results = mysql.query_db(query,data)

    #Get all messages fro the logged in user
    mysql=connectToMySQL("simplewall")
    #query="SELECT * FROM messages WHERE sentto_userid in (%(userid)s);"
    query = "SELECT a.first_name, b.msg_id, b.description from users a, messages b WHERE b.sentto_userid = %(userid)s AND a.userid=b.user_userid "
    data={
        'userid' : session['login_userid']
    }
    msg_results = mysql.query_db(query,data)
    print (msg_results)

    return render_template('chat.html', results=results, msg_results=msg_results)

@app.route('/delete/<id>')
def delete_msg(id):
    if not session['login_flag']:
        msg = "Please login first before visiting this page!!!"   
        return render_template('success_login.html', msg = msg)
    #Get all users other than the logged in user
    mysql=connectToMySQL("simplewall")
    query="DELETE FROM messages WHERE msg_id = %(id)s;"
    data={
        'id' : int(id)
    }
    results = mysql.query_db(query,data)    
    print ("Message delete")

    return redirect('/display_chat')


@app.route('/send_message', methods=['POST'])
def send_message():
    if not session['login_flag']:
        msg = "Please login first before visiting this page!!!"   
        return render_template('success_login.html', msg = msg)

    mysql=connectToMySQL("simplewall")
    query="INSERT INTO messages (user_userid,sentto_userid,description,created_at) VALUES(%(user_userid)s,%(sentto_userid)s,%(description)s,now());"
    data={
        'user_userid' : session['login_userid'],
        'sentto_userid' : request.form['send_to'],
        'description' : request.form['message']
    }
    results = mysql.query_db(query,data)
    flash('Message sent..')
    return redirect('/display_chat')



def debugHelp(message = ""):
    print("\n\n-----------------------", message, "--------------------")
    print('REQUEST.FORM:', request.form)
    print('SESSION:', session)


if __name__ == "__main__":
    app.run(debug=True)
