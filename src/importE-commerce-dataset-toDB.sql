

InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country


CREATE TABLE OnlineRetail (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description VARCHAR(255),
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(10, 2),
    CustomerID INT,
    Country VARCHAR(100)
);
----------------------------------------------------------------


CREATE table CustomersRFM(
CustomerID VARCHAR(20),
Recency INT,
Frequency INT,
Monetary DECIMAL(10, 2)
)


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/data4.csv'
IGNORE 
INTO TABLE onlineretail
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(InvoiceNo, StockCode, Description, Quantity, @InvoiceDate, UnitPrice, CustomerID, Country)        
SET InvoiceDate = STR_TO_DATE(@InvoiceDate, '%m/%d/%Y %H:%i');





