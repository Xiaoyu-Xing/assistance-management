from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

import config
import pymysql
pymysql.install_as_MySQLdb()
from exts import db
from models import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.context_processor
def context():
    username=session.get('username')
    if username:
        return {'username':username}
    else:
        return {}

@app.route('/login/',methods=['POST','GET'])
def login():
    if request.method=='GET':
       # print("get")
        return render_template('login.html')
    else:
        #print("post")
        username = request.form['Username']
        password = request.form['Password']
        #print(username,password)
        user=User.query.filter(User.name==username,User.password==password).first()
        if user:
            session['username']=username
            session.permanemt=True
           # print("success")
            return redirect(url_for('index'))
        else:
            return u'username not exist or password error'




@app.route('/regist/',methods=['POST','GET'])
def regist():
    if request.method=='GET':
        return render_template('regist.html')
    else:
        username=request.form.get('Username')
        password=request.form.get('Password')
        password1=request.form.get('Password1')
        ssn=request.form.get('SSN')
        address=request.form.get('Address')
        city=request.form.get('City')
        state=request.form.get('State')
        zipcode=request.form.get('Zipcode')
        phone=request.form.get('Phone')
        gender=request.form.get('Gender')
        age=request.form.get('Age')
        level=request.form.get('Level')
        user=User.query.filter(User.name==username).first()
        if user:
            return u'username existed'
        else:
            if password!=password1:
                return u'password is inconsistent'
            else:
                print(password)
                user=User(name=username,ssn=ssn,password=password,address=address,city=city,state=state,zipcode=zipcode,phone=phone,
                      gender=gender,age=age,authoritylevel=level)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))



if __name__ == '__main__':
    app.run()
