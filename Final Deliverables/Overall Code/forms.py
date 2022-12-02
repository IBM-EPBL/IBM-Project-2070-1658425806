from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, IntegerField, FloatField
from wtforms.validators import InputRequired, Email, Length, EqualTo, NumberRange


class LoginForm(FlaskForm):
    emailid = StringField('emailid', validators=[InputRequired(message='Field must not be empty'), Email(), Length(min=6, max=40)])
    pwd = PasswordField('pwd', validators=[InputRequired(message='Field must not be empty'), Length(min=6, max=25)])


class RegisterForm(FlaskForm):
    name = StringField('name',validators=[InputRequired(message='Field must not be empty')])
    emailid = StringField('emailid', validators=[InputRequired(message='Field must not be empty'), Email(), Length(min=6, max=40)])
    pwd = PasswordField('pwd', validators=[InputRequired(message='Field must not be empty'), Length(min=6, max=25)])
    cpwd = PasswordField('cpwd',validators=[InputRequired(message='Field must not be empty'),EqualTo('pwd', message='Passwords must match.')])


class HomeApplnForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='Field must not be empty'), Length(min=3, max=40)])
    Gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female'),('Others','Others')], validators=[InputRequired(message='Field must not be empty')])
    Married = RadioField('Married', choices=[('Yes','Yes'),('No','No')], validators=[InputRequired(message='Field must not be empty')])
    Dependents = IntegerField('Dependents', validators=[InputRequired(message='Field must not be empty'), NumberRange(min=0)])
    Education = RadioField('Education', choices=[('Graduate','Graduate'),('Not Graduate','Not Graduate')], validators=[InputRequired(message='Field must not be empty')])
    Self_Employed = RadioField('Self_Employed', choices=[('Yes','Yes'),('No','No')], validators=[InputRequired(message='Field must not be empty')])
    ApplicantIncome = FloatField('ApplicantIncome', validators=[InputRequired(message='Field must not be empty'), NumberRange(min=0)])
    LoanAmount = FloatField('LoanAmount', validators=[InputRequired(message='Field must not be empty'), NumberRange(min=0)])
    Loan_Amount_Term = FloatField('Loan_Amount_Term', validators=[InputRequired(message='Field must not be empty'), NumberRange(min=0)])
    Credit_History = RadioField('Credit_History', choices=[('1','Yes'),('0','No')], validators=[InputRequired(message='Field must not be empty')])
    Property_Area = RadioField('Property_Area', choices=[('Urban','Urban'),('Semiurban','Semiurban'),('Rural','Rural')], validators=[InputRequired(message='Field must not be empty')])
    

class BusinessApplnForm(FlaskForm):
    Gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female'),('Others','Others')], validators=[InputRequired(message='Field must not be empty')])
    Married = RadioField('Married', choices=[('Yes','Yes'),('No','No')], validators=[InputRequired(message='Field must not be empty')])
    Dependents = IntegerField('Dependents', validators=[InputRequired(message='Field must not be empty'), NumberRange(min=0)])
    Education = RadioField('Education', choices=[('Graduate','Graduate'),('Not Graduate','Not Graduate')], validators=[InputRequired(message='Field must not be empty')])
    Self_Employed = RadioField('Self_Employed', choices=[('Yes','Yes'),('No','No')], validators=[InputRequired(message='Field must not be empty')])
    ApplicantIncome = FloatField('ApplicantIncome', validators=[InputRequired(message='Field must not be empty'), NumberRange(min=0)])
    CoapplicantIncome = FloatField('CoapplicantIncome', validators=[InputRequired(message='Field must not be empty'), NumberRange(min=0)])
    LoanAmount = FloatField('LoanAmount', validators=[InputRequired(message='Field must not be empty'), NumberRange(min=0)])
    Loan_Amount_Term = FloatField('Loan_Amount_Term', validators=[InputRequired(message='Field must not be empty'), NumberRange(min=0)])
    Credit_History = RadioField('Credit_History', choices=[('1','Yes'),('0','No')], validators=[InputRequired(message='Field must not be empty')])
    Property_Area = RadioField('Property_Area', choices=[('Urban','Urban'),('Semiurban','Semiurban'),('Rural','Rural')], validators=[InputRequired(message='Field must not be empty')])
    
    
    
    

