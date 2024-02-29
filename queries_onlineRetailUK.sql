

#  data cleaning

select * from onlineretail
where UnitPrice=(select max(UnitPrice) from onlineretail)



#  2 rows result. to be removed(both have Quantity=80995) outliers
select * from onlineretail
where StockCode='23843'

delete from onlineretail where StockCode='23843';



#  4164 transactions where the order was canceled or the product was returned
select count(*) from onlineretail
where Quantity=-1 ; 


#  1174 different products where canceled or returned
select Quantity,StockCode,count(*)
from onlineretail
where Quantity=-1
group by Quantity,StockCode



#  1168 cases where the unit price of a product is zero
select * from onlineretail
where UnitPrice=0 and Quantity>0 ; 


# remove these rows
delete from onlineretail
	where UnitPrice=0 and Quantity>0


select CustomerID,Country,count(*) from onlineretail
group by CustomerID,Country



#
select count(*) from onlineretail
where UnitPrice=38970.00;

select avg(UnitPrice) from onlineretail
where StockCode='M' and UnitPrice!=38970.00



#  spot duplicate rows
select InvoiceNo, StockCode,Description, Quantity, InvoiceDate, UnitPrice, CustomerID,Country,count(*)
from onlineretail
group by InvoiceNo, StockCode,Description, Quantity, InvoiceDate, UnitPrice, CustomerID,Country
having count(*)>1


#  remove duplicate rows
DELETE FROM onlineretail
WHERE (InvoiceNo, StockCode,Description, Quantity, InvoiceDate, UnitPrice, CustomerID,Country) IN (
    SELECT InvoiceNo, StockCode,Description, Quantity, InvoiceDate, UnitPrice, CustomerID,Country
    FROM (
        SELECT InvoiceNo, StockCode,Description, Quantity, InvoiceDate, UnitPrice, CustomerID,Country,
               ROW_NUMBER() OVER (PARTITION BY InvoiceNo, StockCode,Description, Quantity, InvoiceDate, UnitPrice, CustomerID,Country) AS rn
        FROM onlineretail
    ) AS subquery
    WHERE rn > 1
);


#  spotting the outliers in UnitPrice

SELECT *
FROM onlineretail
WHERE ABS(UnitPrice - (SELECT AVG(UnitPrice) FROM onlineretail)) > (SELECT 2 * STDDEV(UnitPrice) FROM onlineretail);




SELECT *
FROM onlineretail
WHERE ABS(Quantity - (SELECT AVG(Quantity) FROM onlineretail)) > (SELECT 2 * STDDEV(Quantity) FROM onlineretail);


---------------------------------------
##  exploratory data analysis (EDA)





#  rows discounts 
select * from onlineretail
where Description='Discount';


#  number of transactions for each customer who have discount coupons
select CustomerID,count(*) as num_of_transactions
from onlineretail 
where Description!='Discount' and CustomerID in 
(select distinct CustomerID from onlineretail
where Description='Discount' )
group by CustomerID
order by num_of_transactions desc
