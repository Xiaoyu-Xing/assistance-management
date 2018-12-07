-- DB name: AssistanceManagement, user/pw: root
CREATE DATABASE AssistanceManagement;
USE AssistanceManagement;

CREATE TABLE `Material` (
  `MaterialID` Int auto_increment,
  `MaterialName` Varchar(255),
  `Unit` Varchar(31),
  `QuantityTotal` Int,
  PRIMARY KEY (`MaterialID`)
);

CREATE TABLE `Volunteer` (
  `TitleID` Int,
  `Name` Varchar(255),
  PRIMARY KEY (`TitleID`)
);

CREATE TABLE `Donation` (
  `DonationID` Int auto_increment,
  `MaterialID` Int,
  `QuantityAvailable` Int,
  `Expiration` Date,
  `UserID` Int,
  `TitleID` Int,
  `Available` Date,
  PRIMARY KEY (`DonationID`)
);

CREATE TABLE `Disaster` (
  `EventID` Int auto_increment,
  `Country` Varchar(255),
  `City` Varchar(255),
  `Zipcode` Varchar(20),
  PRIMARY KEY (`EventID`)
);


CREATE TABLE `Feedback` (
  `ResponseID` Int,
  `Comment` Varchar(255)
);

CREATE TABLE `Authority` (
  `AuthorLevel` Int,
  `Explanation` Varchar(255),
  PRIMARY KEY (`AuthorLevel`)
);

CREATE TABLE `Request` (
  `RequestID` Int auto_increment,
  `EventID` Int,
  `MaterialID` Int,
  `Quantity` Int,
  `VolunteerQuantity` Int,
  `TitleID` Int,
  `Status` Boolean,
  `Address` Varchar(255),
  `UserID` Int,
  `Deadline` Date,
  PRIMARY KEY (`RequestID`)
);

CREATE TABLE `User` (
  `UserID` Int auto_increment,
  `Name` Varchar(255),
  `SSN` Int,
  `Password` Varchar(255),
  `Address` Varchar(255),
  `City` Varchar(255),
  `State` Varchar(255),
  `Zipcode` Varchar(20),
  `Phone` Varchar(20),
  `Gender` Varchar(255),
  `Age` Int,
  `AuthorityLevel` Int,
  PRIMARY KEY (`UserID`)
);

CREATE TABLE `Response` (
  `ResponseID` Int auto_increment,
  `RequestID` Int,
  `DonationID` Int,
  `MaterialQuantity` Int,
  PRIMARY KEY (`ResponseID`)
);

ALTER TABLE donation
ADD FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID);

ALTER TABLE donation
ADD FOREIGN KEY (TitleID) REFERENCES Volunteer(TitleID);

ALTER TABLE donation
ADD FOREIGN KEY (UserID) REFERENCES User(UserID);

ALTER TABLE User
ADD FOREIGN KEY (AuthorityLevel) REFERENCES Authority(AuthorLevel);

ALTER TABLE Response
ADD FOREIGN KEY (RequestID) REFERENCES Request(RequestID);

ALTER TABLE Response
ADD FOREIGN KEY (DonationID) REFERENCES Donation(DonationID);

ALTER TABLE Feedback
ADD FOREIGN KEY (ResponseID) REFERENCES Response(ResponseID);

ALTER TABLE Request
ADD FOREIGN KEY (EventID) REFERENCES Disaster(EventID);

ALTER TABLE Request
ADD FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID);

ALTER TABLE Request
ADD FOREIGN KEY (TitleID) REFERENCES Volunteer(TitleID);

ALTER TABLE Request
ADD FOREIGN KEY (UserID) REFERENCES User(UserID);
