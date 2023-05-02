from flask import Flask,render_template,request,url_for,flash,redirect,session
import sqlite3

import sendgrid
import os
from sendgrid.helpers.mail import *

app = Flask(__name__)
app.secret_key="1"

con = sqlite3.connect("new2.db")
con.execute("""CREATE TABLE IF NOT EXISTS 
user(pid INTEGER primary key, name TEXT, 
mobile INTEGER, email TEXT, age INTEGER, 
blood TEXT, crpassword TEXT, 
cnpassword TEXT, area TEXT,
city TEXT, district TEXT)""")
con.close()

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/success")
def success():
    return render_template('success.html')
#------------------------------------------------------

#---------------------------------------------------------

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/new",methods=["GET","POST"])
def new():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        con=sqlite3.connect("new2.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from user where email=? and crpassword=?",(email,password))
        data=cur.fetchone()

        if data:
            session["email"]=data["email"]
            session["crpassword"]=data["crpassword"]
            return redirect(url_for('afterlogin'))
        else:
            flash("Username and Password Mismatch","danger")

#---------------------------------------------------------
# After login
@app.route('/afterlogin')
def afterlogin():
    return render_template("user_profile.html")

#-------------------------------------------------------

@app.route("/register",methods = ['POST', 'GET'])
def register():
    return render_template('register.html')

@app.route("/adddata",methods = ['POST','GET'])
def adddata():
    if request.method == 'POST':
        try:
            name = request.form['name']
            mobile = request.form['mobile']
            email = request.form['email']
            age = request.form['age']
            blood = request.form['blood']
            crpassword = request.form['crpassword']
            cnpassword = request.form['cnpassword']
            area = request.form['area']
            city = request.form['city']
            district = request.form['district']
            con = sqlite3.connect("new2.db")
            cur = con.cursor()
            cur.execute("""INSERT 
            INTO user(name, mobile, 
            email, age,
            blood, crpassword, 
            cnpassword, area, 
            city, district)
            values(?,?,?,?,?,?,?,?,?,?)""",(name,mobile,email,age,blood,crpassword,cnpassword,area,
            city,district))
            con.commit()
            flash("Record Added Successfully","success")
            mailtest(email)

       
        except:
            flash("Error in Insert Operation", "error")
    
        finally:
            return redirect(url_for("success"))

def mailtest(to_email):
    sg = sendgrid.SendGridAPIClient(api_key= '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' )
    from_email = Email("chinnukool72@gmail.com")
    subject = "Integration testing3"
    content = Content("text/plain", "Sending via register page passing to_email from register page ")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

@app.route("/request_page")
def request_page():
    return render_template('request.html')

@app.route("/donor")
def donor():
    con = sqlite3.connect("new2.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT email,age,blood, area,city, district FROM user")
    user = cur.fetchall()
    con.close()
    return render_template('donor.html', user=user)

@app.route("/admin")
def admin():
    return render_template('admin_login.html')

#-----------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

#----------------------------------------------

@app.route('/dashboard',methods=['GET'])
def dashboard():
 if request.method == "GET":
     with sqlite3.connect("final2.db") as con:
             con.row_factory = sqlite3.Row  
             cur = con.cursor()
             m = con.cursor()
             cur.execute("SELECT * from user")
             rows = cur.fetchall()
             m.execute("SELECT COUNT(*) FROM user where blood='O+'") #Total O+
             Opositive = m.fetchall()
             m.execute("SELECT COUNT(*) FROM user where blood='O-'") #Total O-
             Onegative = m.fetchall()
             m.execute("SELECT COUNT(*) FROM user where blood='A+'") #Total A+
             Apositive = m.fetchall()
             m.execute("SELECT COUNT(*) FROM user where blood='A-'") #Total A-
             Anegative = m.fetchall()
             m.execute("SELECT COUNT(*) FROM user where blood='B+'") #Total B+
             Bpositive = m.fetchall() 
             m.execute("SELECT COUNT(*) FROM user where blood='B-'") #Total B-
             Bnegative = m.fetchall()
             m.execute("SELECT COUNT(*) FROM user where blood='AB+'") #Total AB+
             ABpositive = m.fetchall()
             m.execute("SELECT COUNT(*) FROM user where blood='AB-'") #Total AB-
             ABnegative = m.fetchall()
             m.execute("SELECT COUNT(name) FROM user") #Total no.of donors
             row = m.fetchall()

             return render_template('dashboard.html',Opositive = Opositive, Onegative = Onegative, Apositive = Apositive, Anegative = Anegative,Bpositive = Bpositive, Bnegative = Bnegative,ABpositive = ABpositive , ABnegative = ABnegative, rows = rows, row = row)




if __name__ == '__main__':
    app.run(debug=True)
