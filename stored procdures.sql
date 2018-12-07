CREATE PROCEDURE Getalldonation 
AS 
    SELECT donation.donationid, 
           donation.userid, 
           material.materialname, 
           donation.quantityavailable, 
           donation.available, 
           donation.expiration, 
           volunteer.NAME 
    FROM   donation 
           LEFT JOIN material 
                  ON donation.materialid = material.materialid 
           JOIN volunteer 
             ON donation.titleid = volunteer.titleid; 

GO; 

EXEC Getalldonation; -- to run the stored procedure



CREATE PROCEDURE Getallmaterial
AS
	SELECT MaterialID, MaterialName, Unit, QuantityTotal 
	FROM Material

GO;

EXEC Getallmaterial; -- to run the stored procedure

CREATE PROCEDURE Getmaterialmatch @ID int @Quantity int
AS 
  SELECT quantitytotal 
  FROM   material 
  WHERE  materialid = ID 
  AND    quantitytotal = Quantity
GO;

EXEC Getmaterialmatch; -- to run the stored procedure

