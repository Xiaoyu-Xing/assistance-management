-- use assistancemanagement;
select Donation.DonationID, Donation.UserID, Material.MaterialName, Donation.QuantityAvailable, Donation.Available, Donation.Expiration, Volunteer.Name from donation
left join material on Donation.MaterialID = Material.MaterialID
join volunteer on Donation.TitleID = Volunteer.TitleID;

insert authority values(1, "Manager"), (2, "Normal User");

insert user values(1, "JoeA", 123456789, "password", "123 Highway 1", "Iowa City", "IA", "52246",  3190000000, "Male", 55, 1);

insert user (Name, SSN, Password, Address, City, State, Zipcode, Phone, Gender, Age, AuthorityLevel) 
values("JoeC", 123456787, "password3", "125 Highway 1", "Iowa City", "IA", "52246",  3190000003, "Female", 34, 2);

INSERT INTO request (EventID, materialid, Quantity, VolunteerQuantity, TitleID, Address, UserID, Deadline, Status)                 
VALUES (1, 1, 100, 0, 15, "123 Heaven Rd.", 1, "2013-12-12", 0);