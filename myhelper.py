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