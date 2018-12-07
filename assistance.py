from flask import Flask, flash, session, redirect, url_for, escape, request, render_template
import MySQLdb
from myhelper import run_once_to_fill_data, execute_sql, get_db_data, get_new_data, request_match_funct, match_volunteer, match_material
from myforms import DonationForm, NewMaterialForm, Event, Request, Feedback, UserIDForm
# rule: all the string passed to sql need in double quote


def connection():
    #connect to db
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='assistancemanagement')
    #run_once_to_fill_data(db) # used to initialize fake data in database
    cursor = db.cursor()
    return db

db = connection()

app = Flask(__name__)
# flask object to initiate webpage

@app.route('/')
def home():
    return render_template('home.html')

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
        else:
            flash("Submission failed. Please check your fields or debug the code.", "danger")

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
                flash("Submission failed. Please check your fields or debug the code.", "danger")
        else:
            # update sql db into material table
            sql_new_donation = f'INSERT INTO Donation (Expiration, UserID, TitleID, Available) \
            values ("{Expiration}", {UserID}, {TitleID}, "{Available}");'
            # sql_new_donation = f'INSERT INTO Donation (Expiration, UserID, TitleID, Available) \
            #         VALUES ("{Expiration}", {UserID}, {TitleID}, "{Available}")'
            if execute_sql(db, sql_new_donation):
                flash("Thank you. We got your volunteering information. You will be contacted if there is a match for your expertise.", "success")
            else:
                flash("Submission failed. Please check your fields or debug the code.", "danger")

        return redirect(url_for('home')) # pass in the function name to url_for
    return render_template('donation.html', data=get_new_data(db), form=form)

@app.route('/event', methods=['GET', 'POST'])
def event():
    form = Event(request.form)
    if request.method == 'POST' and form.validate():
        # retreive data from user form
        country = form.country.data
        city = form.city.data
        zipcode = form.zipcode.data
        sql_new_event = f'INSERT INTO disaster (country, city, zipcode) \
                VALUES ("{country}", "{city}", "{zipcode}")'
        # execute db and notify user
        if execute_sql(db, sql_new_event):
            flash("You registered a new event/disaster. You can submit your request now.", "success")
        else:
            flash("Submission failed. Please check your fields or debug the code.", "danger")
        return redirect(url_for('request_match'))
    return render_template('event.html', form=form, data=get_db_data(db, 'select * from disaster;'))

@app.route('/request_match', methods=['GET', 'POST'])
def request_match():
    form = Request(request.form)
    if request.method == 'POST' and form.validate():
        # retreive data from user form
        UserID  = form.UserID.data
        EventID = form.EventID.data
        MaterialID = form.MaterialID.data
        MaterialQuantity = form.MaterialQuantity.data
        VolunteerQuantity = form.VolunteerQuantity.data
        Deadline = form.Deadline.data
        TitleID = form.TitleID.data
        Address = form.Address.data
        sql_new_request = f'INSERT INTO request (EventID, MaterialID, Quantity, VolunteerQuantity, TitleID, Address, UserID, Deadline, Status) \
                VALUES ({EventID}, {MaterialID}, {MaterialQuantity}, {VolunteerQuantity}, {TitleID}, "{Address}", {UserID}, "{Deadline}", 0);'
        # execute db and notify user
        if execute_sql(db, sql_new_request):
            if match_material(db, MaterialID, MaterialQuantity):
                if match_volunteer(db, TitleID, VolunteerQuantity, Deadline):
                    RequestValue = get_db_data(db, 'select RequestID FROM Request where UserID = %s and MaterialID = %s and EventID = %s and TitleID = %s' % (UserID, MaterialID, EventID, TitleID,))
                    RequestID = RequestValue[0][0]
                    request_match_funct(db, MaterialID, MaterialQuantity, TitleID, VolunteerQuantity, RequestID, Deadline)
                    flash("Your request has been matched.", "success")
                else:
                    flash("No request match, insufficient volunteers available.", "success")
            else :
                flash("No request match. Please review available materials.", "danger")
        else:
            flash("Submission failed. Please check your fields or debug the code.", "danger")
        return redirect(url_for('request_match'))
    
    return render_template('request_match.html', form=form, data=get_new_data(db))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = Feedback(request.form)
    if request.method == 'POST' and form.validate():
        # retreive data from user form
        ResponseID  = form.ResponseID.data
        Comment = form.Comment.data
        sql_new_feedback = f'INSERT INTO feedback (ResponseID, Comment) \
                VALUES ({ResponseID}, "{Comment}");'
        # execute db and notify user

        if execute_sql(db, sql_new_feedback):
            flash("You submited a new feedback, thank you.", "success")
        else:
            flash("Submission failed. Please check your fields or debug the code.", "danger")
        return redirect(url_for('home'))

    return render_template('feedback.html', form=form, data=get_new_data(db))

@app.route('/match_form', methods=['GET', 'POST'])
def match_form():
    form = UserIDForm(request.form)
    if request.method == 'POST' and form.validate():
        User = form.User.data
        sql_match_return = 'SELECT DonationID FROM Donation WHERE UserID = %s;' % (User)
        don_data = get_db_data(db, sql_match_return)
        don_list = ''
        for items in don_data:
            holder_2 = get_db_data(db, 'Select RequestID, MaterialQuantity FROM Response WHERE DonationID = %s;'%(items[0]))
            for itemss in holder_2:
                holder1 = get_db_data(db, 'SELECT MaterialID, Address, TitleID FROM Request WHERE RequestID = %s;'%(itemss[0]))
                for itemsss in holder1:
                    don_list = don_list + 'You have been matched to provide %s of material %s and assist as %s at %s. ' %(itemss[1], itemsss[0], itemsss[2], itemsss[1])
        flash (don_list, "success")
        return redirect(url_for('match_form'))
    return render_template('match.html', form=form, data=get_new_data(db))
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
        return render_template('login.html')
    else:
        username = request.form['Username']
        password = request.form['Password']
        cursor=db.cursor()
        sql="select password from user where name='%s'"%username
        cursor.execute(sql)
        results=cursor.fetchall()
        for row in results:
            pasw=row[0]
            if pasw==password:
                session['username'] = username
                session.permanemt = True
                code = get_db_data(db, 'select UserID from User where Name = "%s"' %(username))
                print(code)
                code_value = code[0]
                flash("Your User ID is %s, please record this."%(code_value), "success")
                return redirect(url_for('home'))
            else:
                flash("Username not exist or password error", "danger")
                return redirect(url_for('regist'))


               


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
        cursor = db.cursor()
        sql = "select name from user "
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                name = row[0]
                #print(name)
                if name == username:
                    flash("Username Existed, choose a different one.", "danger")
                    return redirect(url_for('regist'))
                else:
                    if password != password1:
                        flash("Two passwords do not match, try again.", "danger")
                        return redirect(url_for('regist'))
            #print(password)
            sql="insert into user(Name, SSN, Password, Address, City, State, Zipcode, Phone, Gender, Age, AuthorityLevel) values('%s',%s,'%s','%s','%s','%s','%s','%s','%s',%s,%s);"%(username,ssn,
                            password,address,city,state,zipcode,phone,gender,age,level)
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
                return redirect(url_for('login'))
            except:
                db.rollback()
                flash("Add failed.", "danger")
                return redirect(url_for('regist'))
        except:
            print("Error:unable to fetch data")


app.secret_key='secret_key' # a must have, and will be replaced with a real secret key for production
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

db.close()