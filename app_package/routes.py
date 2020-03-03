from flask import render_template, flash, redirect, url_for
from app_package import app, db,mongo
from flask_login import current_user, login_user, logout_user, login_required
from app_package.forms import LoginForm, RegistrationForm
from app_package.forms import AddAccountForm,CloseAccountForm,WithdrawForm,DepositForm,CheckBalanceForm,CustomerConfirmPage
from app_package.models import User

check=True
cus_id=0
@app.route("/",methods=["GET","POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:    
        form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()   
        if user is None or not user.check_password(form.password.data):
            flash("Invalid user")
            return redirect(url_for("index"))
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("menu"))    
    else:
        return render_template("login.html",form=form)
        
@app.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("menu")) 
    else:
        form=RegistrationForm()
        if form.validate_on_submit():
            user=User(username=form.username.data)    
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("User registered.You may login now")
            return redirect(url_for("index"))
        else:
            return render_template("register.html",form=form) 
            
@app.route("/menu")
@login_required
def menu():
    return render_template("menu.html")
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))                           


@app.route("/add_account",methods=["GET","POST"])
@login_required
def add_account():
    global cus_id,check
    form=AddAccountForm()
    if form.validate_on_submit():
        fields=["_id","accountnumber","name","customertype","balance"]
        cus_id+=1
        values=[cus_id,form.accountnumber.data,form.name.data,form.customertype.data,form.balance.data]
        customer=dict(zip(fields,values))
        cus_col=mongo.db.customers
        if check:
            check=False
            if cus_col.count()==0:
                cus_id=0
            else:
                cus=cus_col.find().sort("_id",-1).limit(1)
                tmp=cus.next()
                cus_id=tmp["_id"]
        cus_id+=1
        customer["_id"]=cus_id
        
        if form.balance.data>=50000 and form.customertype.data=="priority" or form.balance.data>=10000 and  form.customertype.data=="ordinary":      
            tmp=cus_col.insert_one(customer)
            if tmp.inserted_id==cus_id:
                flash("account added")
                return redirect(url_for("menu"))
            else:
                flash("problem adding account")
                return redirect(url_for("logout"))
        else:
            flash("minimum balance required")
            return redirect(url_for("add_account"))
           
    else:            
        return render_template("add_account.html",form=form)   
       
        
        
@app.route("/close_account",methods=["GET","POST"])
@login_required
def close_account():
    form=CloseAccountForm()
    if form.validate_on_submit():
        cus_col=mongo.db.customers
        query={"accountnumber":form.accountnumber.data} 
        cus_pro=cus_col.find(query)
        
        
        return render_template("confirmation_page.html",cus_pro=cus_pro,form=form) 
        
    else:
        return render_template("close_account.html",form=form) 
        
        
@app.route("/confirmation_page",methods=["GET","POST"])
@login_required
def confirmation_page():
    form=CustomerConfirmPage()
    if form.validate_on_submit():
        cus_col=mongo.db.customers
        query={"accountnumber":form.accountnumber.data}
        cus_col.delete_one(query)
        flash("Customer record deleted")
        return redirect(url_for("menu"))

    else:
        return render_template("confirmation_page.html",form=form)
        
        
@app.route("/deposit_account",methods=["GET","POST"])
@login_required                                            
def deposit_account():
    form=DepositForm()
    if form.validate_on_submit():
        cus_col=mongo.db.customers
        query={"accountnumber":form.accountnumber.data} 
        customers=cus_col.find_one(query)
        bal=customers["balance"]
        new_bal=bal+form.balance.data                                                           
        new_val={"$set":{"balance":new_bal}}
       
        cus_col.update_one(query,new_val)
        flash("Account deposited")
        return render_template("show_balance.html", new_bal=new_bal)
    else:
        return render_template("deposit_account.html",form=form) 
    
@app.route("/withdraw_account",methods=["GET","POST"])
@login_required                                            
def withdraw_account():
    form=WithdrawForm()
    if form.validate_on_submit():
        query={"accountnumber":form.accountnumber.data} 
        cus_col=mongo.db.customers
        
        customers=cus_col.find_one(query)
        bal=customers["balance"]
        atype=customers["customertype"]
        new_bal=int(bal)-int(form.balance.data)
        if atype=="priority" and new_bal<50000 or atype=="ordinary" and new_bal<10000:
            flash("upon withdrawal min balance is not maintained")
            return redirect(url_for("menu"))
        else:
            new_data={"$set":{"balance":new_bal}}
            cus_col.update_one(query,new_data)      
            flash("Withdrawal done")
            
            return render_template("show_balance.html", new_bal=new_bal)
    else:
        return render_template("withdraw_account.html",form=form)        
    
        
        

   
@app.route("/balance_account",methods=["GET","POST"])
@login_required                                            
def balance_account():
    form=CheckBalanceForm()
    if form.validate_on_submit():
        cus_col=mongo.db.customers
        query={"accountnumber":form.accountnumber.data} 
        customers=cus_col.find_one(query)
        bal=customers["balance"]
                                                                   
        
       
       
        return render_template("display_balance.html",customers=customers)
    else:
        return render_template("balance_account.html",form=form) 
                                                                    
        
@app.route("/display_accounts")
@login_required                                            
def display_accounts():
    cus_col=mongo.db.customers
    customers=cus_col.find()
    return render_template("display_accounts.html",customers=customers)     
    
    
@app.route("/display_balance")
@login_required                                            
def display_balance():
    cus_col=mongo.db.customers
    
    customers=cus_col.find()
    return render_template("display_balance.html",form=form,customers=customers)
    

    

                                                                                                          
