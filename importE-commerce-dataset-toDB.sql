

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
CREATE TABLE Transactions (
    InvoiceNo INT,
    StockCode INT,
    Description VARCHAR(255),
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(10, 2),
    CustomerID INT,
    Country VARCHAR(100),
    PRIMARY KEY (InvoiceNo)
);


CREATE TABLE Products (
    StockCode INT PRIMARY KEY,
    Description VARCHAR(255),
    UnitPrice DECIMAL(10, 2)
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Country VARCHAR(100)
);

CREATE TABLE Transactions_Details (
    TransactionID INT,
    StockCode INT,
    Quantity INT,
    FOREIGN KEY (TransactionID) REFERENCES Transactions(InvoiceNo),
    FOREIGN KEY (StockCode) REFERENCES Products(StockCode)
);


CREATE TABLE Cancelled_Transactions (
    CancelledInvoiceNo INT PRIMARY KEY,
    OriginalInvoiceNo INT,
    FOREIGN KEY (OriginalInvoiceNo) REFERENCES Transactions(InvoiceNo)
);




LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/data4.csv'
IGNORE 
INTO TABLE onlineretail
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(InvoiceNo, StockCode, Description, Quantity, @InvoiceDate, UnitPrice, CustomerID, Country)        
SET InvoiceDate = STR_TO_DATE(@InvoiceDate, '%m/%d/%Y %H:%i');



