

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