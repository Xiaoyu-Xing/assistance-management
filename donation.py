from flask import Flask, flash, session, redirect, url_for, escape, request, render_template
from hashlib import md5
from wtforms import Form, DateField, IntegerField, StringField, validators, TextAreaField
import MySQLdb
import time
import copy
from flask_mysqldb import MySQL
# rule: all the string passed to sql need in double quote

def execute_sql(db, sql):
    # execute sql for insert or update table
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        cursor.close()
        return False
def get_db_data(db, sql):
    # execute sql to get data (select)
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        data = copy.deepcopy(cursor.fetchall())
        cursor.close()
        return data
    except Exception as e:
        print(e)
        cursor.close()

def fill_volunteer(db):
    # used to fill initial fake data
    occupations = {1: "Rescuer", 2: "Community Outreach", 3: "Emergency Management", 4: "General Volunteers", 
               5: "Linesmen", 6: "First Aid", 7: "Ambulance Service", 8: "Drivers", 9: "Technicians",
               10: "Roading & Infrastructure staff", 11: "Therapists", 12: "Restoration Specialists",
              13: "Disaster Relief Workers", 14: "Mechanics", 15: "Not A Volunteer"}
    for _,occupation in occupations.items():
        sql = f'INSERT INTO Volunteer (Name) VALUES ("{occupation}");'
        execute_sql(db, sql)

def fill_material(db):
    # used to fill initial fake data
    data = [["apple", "pound", 100], ["sugar", "pound", 1000], ["flour", "pound", 200], 
            ["water", "gallon", 500], ["beef", "pound", 233], ["tent", "each", 10]]
    for name, unit, quantitytotal in data:
        sql = f'INSERT INTO Material (MaterialName, Unit, QuantityTotal) VALUES ("{name}", "{unit}", {quantitytotal})'
        execute_sql(db, sql)

def fill_donation(db):
    # used to fill initial fake data
    data = [[1, 100, "2014-11-01", 1, 15, "2013-11-01"], [2, 500, "2015-12-01", 2, 15, "2013-12-01"],
            [2, 500, "2015-12-02", 3, 15, "2013-12-02"],[3, 200, "2016-12-01", 3, 15, "2013-12-01"],
           [4, 500, "2020-12-01", 3, 15, "2013-12-01"], [5, 233, "2014-06-01", 3, 15, "2013-12-01"],
           [6, 10, "2025-01-01", 3, 15, "2013-12-20"]]
    for materialID, quantity, expiration, userID, titleID, available in data:
        sql = f'INSERT INTO Donation (MaterialID, QuantityAvailable, Expiration, UserID, TitleID, Available) VALUES ({materialID}, {quantity}, "{expiration}", {userID}, {titleID}, "{available}")'
        execute_sql(db, sql)

def run_once_to_fill_data(db):
    # assume DB and tables are created
    # used to fill initial fake data
    fill_volunteer(db)
    fill_material(db)
    fill_donation(db)

def connection():
    #connect to db
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='assistancemanagement')
    # run_once_to_fill_data(db) # used to initialize fake data in database
    cursor = db.cursor()
    return db

db = connection()

app = Flask(__name__)
# flask object to initiate webpage

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'assistancemanagement'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql_flask = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')
def get_new_data():
    data={}
    # get data from sql db for web use
    data["material"] = get_db_data(db, 'select MaterialID, MaterialName, Unit, QuantityTotal from Material;')
    data["volunteer"] = get_db_data(db, 'select TitleID, Name from Volunteer;')
    data["donation"] = get_db_data(db, 'select * from Donation;')
    return data

class DonationForm(Form):
    # build form to be finised by user
    UserID = IntegerField("UserID (Your UserID)", [
        validators.DataRequired(),
        validators.NumberRange(min=0)])

    MaterialID = IntegerField('MaterialID (Choose from above list. Input "0" for volunteer)', [validators.NumberRange(min=0)])

    QuantityAvailable = IntegerField('Quantity (Integer only, check unit from above list. Input "0" for volunteer)', [validators.NumberRange(min=0)])
    
    Expiration = DateField('Material/Volunteer Expiration Date (Date format: YYYY-MM-DD)', format='%Y-%m-%d')
    Available = DateField('Material/Volunteer Available Date (Date format: YYYY-MM-DD)', format='%Y-%m-%d')
    
    TitleID = IntegerField('TitleID (Choose from below occupation list, input "15" for non-volunteer, 4 for general volunteer)', [
        validators.DataRequired(),
        validators.NumberRange(min=0)])
class NewMaterialForm(Form):
    # build form to be finised by user
    name = StringField('Name (Lower case, singular form)', [
        validators.DataRequired(),
        validators.Length(min=2, max=255)])
    unit = StringField('Unit (lower case)', [
        validators.DataRequired(),
        validators.Length(min=2, max=10)])

@app.route('/new_material', methods=['GET', 'POST'])
def new_material():
    form = NewMaterialForm(request.form)
    if request.method == 'POST' and form.validate():
        # retreive data from user form
        name = form.name.data
        unit = form.unit.data
        # update sql db into material table
        sql_new_material = f'INSERT INTO Material (MaterialName, Unit, QuantityTotal) \
                VALUES ("{name}", "{unit}", 0)'
        # execute db and notify user
        if execute_sql(db, sql_new_material):
            flash("You registered a new material. Next please submit your donation form", "success")
        return redirect(url_for('donation'))

    return render_template('new_material.html', form=form)

@app.route('/donation', methods=['GET', 'POST'])
def donation():
    form = DonationForm(request.form)
    if request.method == 'POST' and form.validate():
        # retreive data from user form
        MaterialID = form.MaterialID.data
        QuantityAvailable = form.QuantityAvailable.data
        Expiration = form.Expiration.data
        UserID = form.UserID.data
        TitleID = form.TitleID.data
        Available = form.Available.data
        
        
        if int(TitleID) == 15:
            # get old data and for calculation of new total quantity
            old_quantity_total = get_db_data(db, f'SELECT QuantityTotal FROM Material WHERE MaterialID="{MaterialID}"')
            # update sql db into material table
            sql_new_donation = f'INSERT INTO Donation (MaterialID, QuantityAvailable, Expiration, UserID, TitleID, Available) \
                    VALUES ({MaterialID}, {QuantityAvailable}, "{Expiration}", {UserID}, {TitleID}, "{Available}")'
            sql_update_material = f'UPDATE Material SET QuantityTotal="{int(old_quantity_total[0][0])+int(QuantityAvailable)}" WHERE MaterialID="{MaterialID}"'
            # execute db and notify user
            if execute_sql(db, sql_new_donation) and execute_sql(db, sql_update_material):
                flash("Thank you. We got your donation information. You will be contacted if there is a match for your donation.", "success")
        else:
            # update sql db into material table
            sql_new_donation = 'INSERT INTO Donation (Expiration, UserID, TitleID, Available) \
            values ("2014-07-15", 11, 2, "2013-07-14");'
            # sql_new_donation = f'INSERT INTO Donation (Expiration, UserID, TitleID, Available) \
            #         VALUES ("{Expiration}", {UserID}, {TitleID}, "{Available}")'
            print("---------------------------------------------------------------")
            print(sql_new_donation)
            if execute_sql(db, sql_new_donation):
                flash("Thank you. We got your volunteering information. You will be contacted if there is a match for your expertise.", "success")
        return redirect(url_for('home')) # pass in the function name to url_for


    return render_template('donation.html', data=get_new_data(), form=form)



app.secret_key='secret_key' # a must have, and will be replaced with a real secret key for production

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

db.close()