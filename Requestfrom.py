class NewRequestForm(Form):
    # buil form to be finished by user
    UserID = IntegerField("UserID (Your UserID)", [
        validators.DataRequired(),
        validators.NumberRange(min=1)])
        
    EventID = Integer Field('EventID (Choose from disasters on disaster page)', [validators.NumberRange(min=1)])

    MaterialID = IntegerField('MaterialID (Choose from above list. Input "0" for volunteer)', [validators.NumberRange(min=0)])

    QuantityNeeded = IntegerField('Quantity (Integer only, check unit from above list. Input "0" for volunteer)', [validators.NumberRange(min=0)])
    Volunteer Quantity = IntegerField('Quantity (Integer only. Input "o" for material)', [validators.NumberRange(min=0)])
    Deadline = DateField('Request Deadline Date (Date format: YYYY-MM-DD)', format='%Y-%m-%d')
    
    TitleID = IntegerField('TitleID (Choose from below occupation list, input "15" for non-volunteer, "4" for general volunteer)', [
        validators.DataRequired(),
        validators.NumberRange(min=2)])
    
    Address = StringField('Address (Enter full address)') [
        validators.DataRequired(),
        validators.Length(min=2)]