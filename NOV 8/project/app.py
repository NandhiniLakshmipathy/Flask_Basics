from flask import Flask,render_template,request,url_for,flash,redirect,session
import sqlite3

app = Flask(__name__)
app.secret_key="1"

con = sqlite3.connect("final2.db")
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

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        con=sqlite3.connect("final2.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from user where email=? and crpassword=?",(email,password))
        data=cur.fetchone()

        if data:
            session["email"]=data["email"]
            session["crpassword"]=data["crpassword"]
            return redirect(url_for('after_login'))
        else:
            flash("Username and Password Mismatch","danger")
    
    return render_template('login.html')

#---------------------------------------------------------
# After login
@app.route('/afterlogin',methods=["GET","POST"])
def after_login():
    return render_template("user_profile.html")

#-------------------------------------------------------

@app.route("/register",methods = ['POST', 'GET'])
def register():
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
            con = sqlite3.connect("final2.db")
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
       
        except:
            flash("Error in Insert Operation", "error")
    
        finally:
            return redirect(url_for("success"))
    return render_template('register.html')

@app.route("/request")
def request_page():
    return render_template('request.html')

@app.route("/donor")
def request_donor():
    return render_template('donor.html')

@app.route("/admin")
def admin():
    return render_template('admin_login.html')

#-----------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)