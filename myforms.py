from wtforms import Form, DateField, IntegerField, StringField, validators, TextAreaField

class DonationForm(Form):
    # build form to be finised by user
    UserID = IntegerField("UserID (Your UserID)", [
        validators.DataRequired(),
        validators.NumberRange(min=0)])

    MaterialID = IntegerField('MaterialID (Choose from above list. Input "0" for volunteer)', [validators.NumberRange(min=0)])

    QuantityAvailable = IntegerField('Quantity (Integer only, check unit from above list. Input "0" for volunteer)', [validators.NumberRange(min=0)])
    
    Expiration = DateField('Material/Volunteer Expiration Date (Date format: YYYY-MM-DD)', format='%Y-%m-%d')
    Available = DateField('Material/Volunteer Available Date (Date format: YYYY-MM-DD)', format='%Y-%m-%d')
    
    TitleID = IntegerField('TitleID (Choose from below occupation list, input "15" for non-volunteer, "4" for general volunteer)', [
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

class Event(Form):
    # build form to be finised by user
    country = StringField('Country (Use full name)', [
        validators.DataRequired(),
        validators.Length(min=2, max=255)])
    city = StringField('City (Use full name)', [
        validators.DataRequired(),
        validators.Length(min=2, max=255)])
    zipcode = StringField('Zipcode', [
        validators.DataRequired(),
        validators.Length(min=2, max=20)])