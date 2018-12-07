import copy

def run_once_to_fill_data(db):
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
    # assume DB and tables are created
    # used to fill initial fake data
    fill_volunteer(db)
    fill_material(db)
    fill_donation(db)

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

def get_new_data(db):
    data={}
    # get data from sql db for web use
    data["material"] = get_db_data(db, 'select MaterialID, MaterialName, Unit, QuantityTotal from Material;')
    data["volunteer"] = get_db_data(db, 'select TitleID, Name from Volunteer;')
    data["donation"] = get_db_data(db, 'select Donation.DonationID, Donation.UserID, Material.MaterialName,\
                                    Donation.QuantityAvailable, Donation.Available, Donation.Expiration, Volunteer.Name from donation\
                                    left join material on Donation.MaterialID = Material.MaterialID\
                                    join volunteer on Donation.TitleID = Volunteer.TitleID;')
    data["disaster"] = get_db_data(db, 'select * from disaster;')
    data["user"] = get_db_data(db, 'select userID, name, zipcode from user;')
    data["response"] = get_db_data(db, 'select * from response;')
    data["feedback"] = get_db_data(db, 'select * from feedback;')
    return data

def match_material(db, mat, quant):
    t1 = get_db_data(db, 'select QuantityTotal from Material where MaterialID = %s and QuantityTotal >= %s' % (mat, quant,))
    t2 = t1[0]
    t3 = t2[0]
    if t3 > 0:
        return True
    else:
        return False
    
def match_volunteer(db, vol, quant, date):
    if vol == 15:
        return True
    t1 = get_db_data(db, 'select count(DonationID) from Donation where TitleID = "%s" and available > "%s"' % (vol, date,))
    t1 = t1[0][0]
    if t1 >= quant:
        return True
    else:
        return False
        
def request_match_funct(db, mat, quant1, vol, quant2, request, date):
    matAmount = quant1
    volAmount = quant2
    while matAmount > 0:
        data = get_db_data(db, 'select DonationID, QuantityAvailable from Donation where MaterialID = %s and QuantityAvailable > 0 Limit 1' % (mat,))
        amount = data[0][1]
        idvalue = data[0][0]
        if amount < matAmount:
            diff = matAmount - amount
            execute_sql(db, 'update Donation set QuantityAvailable = 0 where DonationID = %s', (idvalue,))
            execute_sql(db, 'insert into Response (RequestID, DonationID, MaterialQuantity) values (%s, %s, %s)'% (request, idvalue, amount,))
            matAmount = diff
            execute_sql(db, 'update Request set Quantity = %d where RequestID = %s', (matAmount, request,))
            
        else:
            diff = amount - matAmount
            execute_sql(db, 'update Donation set QuantityAvailable = %s where DonationID = %s'% (diff, idvalue,))
            execute_sql(db, 'insert into Response(RequestID, DonationID, MaterialQuantity) values (%s, %s, %s)' % (request, idvalue, matAmount,))
            execute_sql(db, 'update Request set Quantity = 0 where RequestID = %s' % (request,))
            matAmount = 0
    t5 = get_db_data(db, 'select QuantityTotal from Material where MaterialID = %s Limit 1' % (mat,))
    newAmount = t5[0][0]
    newAmount = newAmount - quant1
    try_sql = 'UPDATE Material SET QuantityTotal = %s where MaterialID= %s;' % (newAmount, mat,)
    execute_sql(db, try_sql)
    while volAmount > 0:
        data = get_db_data(db, 'select DonationID, TitleID from Donation where TitleID = "%s" and Expiration > "%s" Limit 1'% (vol,date,))
        idvalue = data[0][0]
        execute_sql(db, 'update Donation set Available = "%s" where DonationID = %s'% (date, idvalue,))
        execute_sql(db, 'insert into Response (RequestID, DonationID) values (%s, %s)'% (request, idvalue,))
        volAmount = volAmount - 1
        execute_sql(db, 'update Request set VolunteerQuantity = %s where RequestID = %s'% (volAmount, request,))
      
    execute_sql(db, 'update Request set Status = 1 where RequestID = %s'% (request,))
    return True