from flask import Flask, request, session, current_app, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash
from flask_mail import Message
from models import User
from app import db,create_app,login_manager, mail
from forms import LoginForm, RegisterForm, ChangePasswordForm

import jwt, datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():    
    return render_template("index.html")

app = create_app()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=1)

@app.errorhandler(404) 
def invalid_route(e): 
    return "Invalid route."

@app.route('/', methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html")

@app.route('/signup',methods=['GET','POST'])
def signup():       
    if request.method == "GET":
        return render_template("signup.html")
    
    elif request.method == "POST":
        f = RegisterForm(request.form)        
        try:
            if f.validate_on_submit():
                name = f.name.data
                emailid = f.emailid.data
                pwd= f.pwd.data  
                user = User(name=name,email=emailid,password=pwd,confirmed=False)
                
                old_user = User.query.filter_by(id=emailid).first()
                if old_user:
                    flash('Email address already exists','error')
                    return redirect(url_for('signup'))
                
                db.session.add(user)
                db.session.commit()

                token = jwt.encode({"email": emailid}, current_app.config["SECRET_KEY"], algorithm="HS256")
                
                # Send verification email
                msg = Message(subject="Email Verification",recipients=[emailid])
                link = url_for('verify_email', token=token, _external=True)
                html = render_template("email_verify.html",url=link)
                msg.html = html
                mail.send(msg)                
                flash('Thanks for registering!  Please check your email to confirm your email address.', 'success')
                return redirect(url_for("login"))
            else:
                raise (Exception("Error")) 
     
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'exception')    
            return redirect(url_for("signup"))

@app.route("/verify_email/<token>")
def verify_email(token):
    data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    email = data["email"]
    user = User.query.filter_by(email=email).first()

    if user.confirmed:
        flash('Account already verified. Please login.', 'info')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Account verified. Please login.', 'success')
    
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():  
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        try:     
            f = LoginForm(request.form)
            if f.validate_on_submit():                       
                emailid = f.emailid.data
                pwd= f.pwd.data     
                
                user = User.query.filter_by(email=emailid).first()

                if not user or not check_password_hash(user.password, pwd):
                    flash('Please check your login details and try again.','error')
                    return redirect(url_for('login'))
                
                flash('Successfully logged in', 'success')
                login_user(user)
                return redirect(url_for('unconfirmed'))
            else:
                raise (Exception("Error"))         
        
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'exception')    
            return redirect(url_for("login"))

@app.route('/unconfirmed',methods=['GET'])
@login_required
def unconfirmed():
    if current_user.confirmed:
        return render_template('dashboard.html')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)