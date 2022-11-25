from flask import Flask, request, session, current_app, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash
from flask_mail import Message
from models import User
from app import db,create_app,login_manager, mail
from forms import LoginForm, RegisterForm, HomeApplnForm, BusinessApplnForm
from predict import bloan,hloan
import jwt, datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():    
    return redirect(url_for('index'))

app = create_app()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=1)

@app.errorhandler(404) 
def invalid_route(e): 
    return "Invalid route"

@app.route('/', methods=["GET", "POST"], strict_slashes=False)
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
                
                old_user = User.query.filter_by(email=emailid).first()
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
                e = "Error"
                if(f.errors):
                    e = list(f.errors.values())[0][0]
                raise (Exception(e)) 
     
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
        session['First_confirm'] = True
        db.session.add(user)
        db.session.commit()
        flash('Account verified. Please login.', 'success')
    
    return redirect(url_for('login'))

@app.route("/resend_email")
def resend_email():
    emailid = current_user.email
    token = jwt.encode({"email": emailid}, current_app.config["SECRET_KEY"], algorithm="HS256")
                
    # Resend verification email
    msg = Message(subject="Email Verification",recipients=[emailid])
    link = url_for('verify_email', token=token, _external=True)
    html = render_template("email_verify.html",url=link)
    msg.html = html
    mail.send(msg)
    flash('A new confirmation email has been sent.', 'info')
    return redirect(url_for("login"))

@app.route('/login',methods=['GET','POST'])
def login():  
    if request.method == "GET":
        if current_user.is_authenticated:
            if session.get('First_confirm'):
                print(session.get('First_confirm'))
                del session['First_confirm']
                return render_template("login.html")
            elif current_user.confirmed:
                return redirect(url_for('dashboard'))
            return redirect(url_for('unconfirmed'))
        
        return render_template("login.html")
    
    elif request.method == "POST":
        try:     
            f = LoginForm(request.form)
            if f.validate_on_submit():                       
                emailid = f.emailid.data
                pwd= f.pwd.data     
                
                user = User.query.filter_by(email=emailid).first()
                
                if not user :
                    flash('Account does not exist', 'error')
                    return redirect(url_for('login'))          
                
                elif not check_password_hash(user.password, pwd):
                    flash('Invalid credentials.','exception')
                    return redirect(url_for('login')) 
                          
                login_user(user)
                
                if current_user.confirmed:                    
                    return redirect(url_for('dashboard'))
                else:    
                    return redirect(url_for('unconfirmed'))
            else:
                e = "Error"
                if(f.errors):
                    e = list(f.errors.values())[0][0]
                raise (Exception(e))         
        
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

@app.route('/homeloan',methods=['GET','POST'])
@login_required
def homeloan():   
    if request.method == "GET":
        if current_user.home_applied:
            flash('Already applied for Home Loan','error')
            return redirect(url_for('dashboard')) 
        return render_template("homeloan.html")
    
    elif request.method == "POST":
        f = HomeApplnForm(request.form)        
        try:
            if f.validate_on_submit():           
                user = current_user
                user.home_applied = True
                fields = ["Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome",  "LoanAmount",  "Loan_Amount_Term",  "Credit_History","Property_Area"]
                values = []    
                values.append(f.Gender.data)
                values.append(f.Married.data)
                values.append(f.Dependents.data)
                values.append(f.Education.data)
                values.append(f.Self_Employed.data)
                values.append(f.ApplicantIncome.data)    
                values.append(f.LoanAmount.data)
                values.append(f.Loan_Amount_Term.data)
                values.append(int(f.Credit_History.data))
                values.append(f.Property_Area.data)
                #print(hloan(fields,values))
                user.home_status = hloan(fields,values)
                db.session.add(user)
                db.session.commit()
                flash('Applied for Home Loan successfully', 'success')
                return redirect(url_for('dashboard'))
            else:
                e = "Error"
                print(f.errors)
                if(f.errors):
                    e = list(f.errors.values())[0][0]
                raise (Exception(e)) 
            
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'exception')    
            return redirect(url_for("homeloan"))

@app.route('/businessloan',methods=['GET','POST'])
@login_required
def businessloan():   
    if request.method == "GET":
        if current_user.business_applied:
            flash('Already applied for Business Loan','error')
            return redirect(url_for('dashboard'))    
        return render_template("businessloan.html")
    
    elif request.method == "POST":
        f = BusinessApplnForm(request.form)        
        try:
            if f.validate_on_submit():           
                user = current_user
                user.business_applied = True
                fields = ["Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome",  "LoanAmount",  "Loan_Amount_Term",  "Credit_History","Property_Area"]
                values = []
                
                values.append(f.Gender.data)
                values.append(f.Married.data)
                values.append(f.Dependents.data)
                values.append(f.Education.data)
                values.append(f.Self_Employed.data)
                values.append(f.ApplicantIncome.data)
                values.append(f.CoapplicantIncome.data)      
                values.append(f.LoanAmount.data)
                values.append(f.Loan_Amount_Term.data)
                values.append(int(f.Credit_History.data))
                values.append(f.Property_Area.data)
                #print(bloan(fields,values))
                user.business_status = bloan(fields,values)
                db.session.add(user)
                db.session.commit()
                flash('Applied for Business Loan successfully', 'success')    
                return redirect(url_for('dashboard'))
            else:
                e = "Error"
                print(f.errors)
                if(f.errors):
                    e = list(f.errors.values())[0][0]
                raise (Exception(e))

        except Exception as e:
            db.session.rollback()
            flash(str(e), 'exception')    
            return redirect(url_for("businessloan"))

@app.route('/status',methods=['GET'])
@login_required
def status():   
    if request.method == "GET":
        if current_user.home_applied or current_user.business_applied:
            hstat = current_user.home_status
            bstat = current_user.business_status
            r1 = 'APPROVED' if(hstat=='1') else 'DENIED'
            r2 = 'APPROVED' if(bstat=='1') else 'DENIED'
            return render_template("status.html",hstat=hstat,bstat=bstat,r1=r1,r2=r2)
        else:
            flash('Not Applied for Home Loan/Business Loan', 'error')
            return redirect(url_for('dashboard'))

   
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)