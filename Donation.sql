-- DB name: AssistanceManagement, user/pw: cs4400project
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
  `TitleID` Int auto_increment,
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

ALTER TABLE donation
ADD FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID);

ALTER TABLE donation
ADD FOREIGN KEY (TitleID) REFERENCES Volunteer(TitleID);

-- ALTER TABLE donation
-- ADD FOREIGN KEY (UserID) REFERENCES Volunteer(UserID);