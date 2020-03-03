from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,IntegerField,RadioField
from wtforms.validators import DataRequired, EqualTo
from app_package.models import User

class LoginForm(FlaskForm):
    username=StringField("Username:",validators=[DataRequired()])
    password=PasswordField("Password:",validators=[DataRequired()])
    remember_me=BooleanField("Remember Me")
    submit=SubmitField("Sign in")       
    
class RegistrationForm(FlaskForm):
    username=StringField("Username:",validators=[DataRequired()])
    password=PasswordField("Password:",validators=[DataRequired()])
    password2=PasswordField("Repeat password:",validators=[DataRequired(),EqualTo("password")])
    submit=SubmitField("Register")      
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username exists, choose another one")
            

class AddAccountForm(FlaskForm):
    accountnumber=IntegerField("Account Number:",validators=[DataRequired()]) 
    name=StringField("Name:",validators=[DataRequired()])
    customertype=RadioField('customer type:',choices=[('priority','priority'),('ordinary','ordinary')])
   
    balance=IntegerField("Balance:",validators=[DataRequired()]) 
    submit=SubmitField("Add Account")
    
    
    
class CloseAccountForm(FlaskForm):
    accountnumber=IntegerField("Account number to close account:",validators=[DataRequired()]) 
    submit=SubmitField("Close Account")
    
class CustomerConfirmPage(FlaskForm):
    accountnumber=IntegerField("Account Number: ")  
    
    submit=SubmitField("Close Account")  
            
class WithdrawForm(FlaskForm):
    accountnumber=IntegerField("Account Number:",validators=[DataRequired()]) 
    balance=IntegerField("Amount to withdraw:",validators=[DataRequired()]) 
    submit=SubmitField("Withdraw")       
    
    
class DepositForm(FlaskForm):
    accountnumber=IntegerField("Account Number:",validators=[DataRequired()]) 
    balance=IntegerField("Amount to deposit:",validators=[DataRequired()]) 
    submit=SubmitField("Deposit")  
    
    
class CheckBalanceForm(FlaskForm):
    accountnumber=IntegerField("Account Number:",validators=[DataRequired()]) 
    
    submit=SubmitField("Balance")       
