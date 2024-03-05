# Table of Contents
1. [Introduction](#Introduction)
   1. [Project Overview](#project-overview)
   2. [Dataset Description](#dataset-description)
2. [Data Preparation and Cleaning](#data-cleaning)
   1. [Cleaning in python](#cleaning-python)
   2. [Cleaning in sql](#cleaning-sql)
3. [RFM Analysis](#rfm-analysis)
   1. [Recency, Frequency, and Monetary (RFM) Scores Calculation](#rfm-scores)
   2. [RFM Distribution Analysis](#rfm-distribution)
4. [Clustering Algorithm](#clustering-algorithm)
   1. [Selecting the Number of Clusters (k)](#number-of-clusters)
   	1. [Elbow Method](#elbow-method)
   2. [K-means](#k-means)
   3. [Silhouette Score](#silhouette-score)




# 1. Introduction
In the realm of retail analytics, understanding customer behavior is pivotal for strategic decision-making and targeted marketing initiatives. Customer segmentation techniques provide a structured approach to categorize customers into distinct groups based on their purchasing patterns, preferences, and overall engagement with the brand. One such powerful method is Recency, Frequency, Monetary (RFM) analysis, which evaluates customers based on the recency of their last purchase, the frequency of purchases, and the monetary value of transactions.

## 1.1 Project Overview

This project aims to leverage RFM analysis coupled with the k-means clustering algorithm to segment customers within an online transactional retail dataset. By employing RFM analysis, we can extract valuable insights regarding customer engagement and purchasing behavior. The k-means clustering algorithm, a popular unsupervised learning technique, will enable us to group customers with similar RFM characteristics into distinct segments.


## 1.2 Dataset Description

The dataset stores information about online transactions made by customers for a UK registered online retail company. All the transactions occurred between 01/12/2010 and 09/12/2011. You can find more information about the dataset here : https://www.kaggle.com/datasets/tunguz/online-retail/data





## 2. Data Preparation and Cleaning

# 2.1 Cleaning in python

### Missing values


```  
print('\ndata types : \n', df.dtypes)  # verifying that data types are all correct
print('\nmissing values : \n', df.isna().sum())  # missing values detection
print('\nduplicates :\n', df[df.duplicated()])  # duplicates detection
```
We notice that missing values exist for CustomerID(approximately a total 130k rows out of 540k rows ). Since we do not want to miss this information, which is ≈25% of the total data, we examine those rows through appropriate filtering, and we notice that the transaction ids(InvoiceNO) do not point to CustomerID. So, CustomerID is completely unknown. Missing values for Description also exist but we will handle them later.

```
nanCustomer_rows=df.loc[df['CustomerID'].isna()]
x = nanCustomer_rows.groupby('InvoiceNo')['InvoiceNo'].value_counts().reset_index(name='count')
print(x)
```

This output informs us that all these transactions made by unknown customers, have 3710 unique transaction ids. Since, every transactionID points to a unique customerID, we decide to create 3710 CustomerIDs. Hence, we manage to preserve all those 130k rows.

### Function created to create new customerIDs
```
// fill nan CustomerID values for every invoiceNo id

def fillcustomerid(df, invoiceNo_tobeFilled):
    customerid = max(df['CustomerID'])+1
    for ind in invoiceNo_tobeFilled:
        df.loc[df['InvoiceNo'] == ind, 'CustomerID'] = customerid
        customerid = customerid+1
    return df


nanCustomer_rows=df.loc[df['CustomerID'].isna()]
x = nanCustomer_rows.groupby('InvoiceNo')['InvoiceNo'].value_counts().reset_index(name='f')
sorted_x = x.sort_values(by='f' ,ascending=False)
invoiceNo_tobeFilled = x['InvoiceNo']
df = fillcustomerid(df, invoiceNo_tobeFilled)

```





### Function created to fill description
```  
//fill Description values

def fillDescription(df,stockCode,stockCodeDescription_Frequent):
    for ind in stockCode:
        descr = stockCodeDescription_Frequent.loc[
            stockCodeDescription_Frequent['StockCode'] == ind, 'Description']
        if descr.empty:
            continue
        descr = descr.iloc[0]
        df.loc[(df['StockCode'] == ind) & (df['Description'].isna()), 'Description'] = descr
    return df


missingDescr_rows=df.loc[df['Description'].isna()] //1454 rows
stockcode_rowsToEdit = missingDescr_rows.groupby('StockCode')['StockCode'].value_counts().reset_index(name='count')
filteredStockcodeAlldescr = df.groupby(['StockCode','Description'])['Description'].value_counts().reset_index(name='count')
filteredStockcodeAlldescr = filteredStockcodeAlldescr.sort_values(by=['StockCode','count'], ascending=[True,False])
max_count_rows = filteredStockcodeAlldescr.groupby('StockCode').first().reset_index()
stockCodeDescription_Frequent = max_count_rows[['StockCode', 'Description']]
stockCodeList=stockcode_rowsToEdit['StockCode'] // 960 products
df = fillDescription(df,stockCodeList,stockCodeDescription_Frequent)

```

To fill the description for those rows, we search what is the description for those products(StockCode). However, many products have multiple different descriptions. So, we decide to find the most frequent description value for each of those products fill the missing values. stockCodeDescription_Frequent parameter stores the most frequent description for every product, while stockCodeList parameter stores the StockCodeIDs we want to fill the description for.


```  
missingDescr_rows=df[df['Description'].isna()].index  # 14 rows
df.drop(missingDescr_rows , inplace=True)

```
The function didn't find any description to fill for some of the products, so we remove those rows.


# 2.2 Cleaning in sql



```  

delete from onlineretail
	where UnitPrice=0 and Quantity>0

```  


### Removing duplicate rows
```
// spot duplicate rows
select InvoiceNo, StockCode,Description, Quantity, InvoiceDate, UnitPrice, CustomerID,Country,count(*)
from onlineretail
group by InvoiceNo, StockCode,Description, Quantity, InvoiceDate, UnitPrice, CustomerID,Country
having count(*)>1;

//  remove duplicate rows
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
```  
### Removing irrelevant rows
```  
delete from onlineretail
where StockCode in ('CRUK','DOT','M','AMAZONFEE','BANK CHARGES','POST','S','C2','B','D');

delete from onlineretail
where StockCode like 'gift%';

delete from onlineretail
where Quantity<0 and  InvoiceNo not like 'C%';
```
These data is not useful for customer segmentation puproses, so we remove them.


### Outliers handling
```
  //spotting the outliers in UnitPrice

SELECT *
FROM onlineretail
WHERE ABS(UnitPrice - (SELECT AVG(UnitPrice) FROM onlineretail)) > (SELECT 2 * STDDEV(UnitPrice) FROM onlineretail);
```

### Data entry errors
```
#  noticing data entry values of unit price for stockcode 22502
select * from onlineretail
where StockCode='22502'
order by UnitPrice desc;

UPDATE onlineretail
SET Quantity = 60, UnitPrice= 10.82, Description='PICNIC BASKET WICKER SMALL'
WHERE Description = 'PICNIC BASKET WICKER 60 PIECES';
```
UnitPrice should store the price value per unit, so we correct those entry errors.

# 3. RFM Analysis


## 3.1 Recency, Frequency, and Monetary (RFM) Scores Calculation
```
INSERT INTO customersrfm
SELECT
    CustomerID,
    DATEDIFF('2011-12-09 12:50:00',MAX(InvoiceDate)) AS Recency,
    COUNT(DISTINCT InvoiceNo) AS Frequency,
    SUM(UnitPrice*Quantity) AS Monetary
FROM
    onlineretail
where Quantity>0 and UnitPrice>0
GROUP BY
    CustomerID;
```
### Distributions
![image](https://github.com/BillysKes/customer-segmentation-retail/assets/73298709/8fd19baa-319a-4405-a26f-b8c169f939a5)

80% of the customers made less than 5 transactions while 12% made between 5-10 transactions. The rest 8%(≈400 customers) have made at least 10 transactions.

![monetaryDistr](https://github.com/BillysKes/customer-segmentation-retail/assets/73298709/63d3cfb6-bc89-4b33-ad91-bd7b3194009d)


Due to the presence of outliers, we decide to winsorize the monetary variable, quantile(0.02,0.02) as a boundary.
![image](https://github.com/BillysKes/customer-segmentation-retail/assets/73298709/36c86628-1654-449b-bbb8-ee1aa0818890)

The majority of customers made a purchase recently
# 4. Clustering Algorithm

## 4.1 Selecting the number of clusters

 ### The elbow method

![elbowMethodClustering](https://github.com/BillysKes/customer-segmentation-retail/assets/73298709/d917ef7d-4f37-4c90-b479-52e016fba271)



## 4.3 K-means



![avgRecencybycluster](https://github.com/BillysKes/customer-segmentation-retail/assets/73298709/d8cb0216-e0df-4886-b110-535ab546a503)


