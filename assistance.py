from flask import Flask, flash, session, redirect, url_for, escape, request, render_template
import MySQLdb
from myhelper import run_once_to_fill_data, execute_sql, get_db_data, get_new_data
from myforms import DonationForm, NewMaterialForm, Event, Request, Feedback
# rule: all the string passed to sql need in double quote


def connection():
    #connect to db
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='assistancemanagement')
    # run_once_to_fill_data(db) # used to initialize fake data in database
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
            flash("You registered a new request.", "success")
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


app.secret_key='secret_key' # a must have, and will be replaced with a real secret key for production
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

db.close()