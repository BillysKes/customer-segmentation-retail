# Table of Contents
1. [Introduction](#Introduction)
   1. [Project Overview](#project-overview)
   2. [Dataset Description](#dataset-description)
2. [Data Preparation and Cleaning](#data-cleaning)
   1. [Cleaning in python](#cleaning-python)
   2. [Cleaning in sql](#cleaning-sql)
4. [RFM Analysis](#rfm-analysis)
   1. [Recency, Frequency, and Monetary (RFM) Scores Calculation](#rfm-scores)
   2. [RFM Segmentation](#rfm-segmentation)
   3. [RFM Distribution Analysis](#rfm-distribution)
5. [Clustering Algorithm](#clustering-algorithm)
   1. [K-means](#k-means)
   2. [Selecting the Number of Clusters (k)](#number-of-clusters)
      1. [Elbow Method](#elbow-method)
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
We notice that missing values exist for CustomerID(approximately a total 130k rows out of 540k rows ). Since we do not want to miss this information, which is ≈25% of the total data, we examine those rows through appropriate filtering, and we notice that the transaction ids(InvoiceNO) do not point to CustomerID. So, CustomerID is completely unknown.

```
nanCustomer_rows=df.loc[df['CustomerID'].isna()]
x = nanCustomer_rows.groupby('InvoiceNo')['InvoiceNo'].value_counts().reset_index(name='count')
print(x)
```

This output informs us that all these transactions made by unknown customers, have 3710 unique transaction ids. Since, every transactionID points to a unique customerID, we decide to create 3710 CustomerIDs. Hence, we manage to preserve all those 130k rows.

# Creating customerIDs Function
```
// fill nan CustomerID values for every invoiceNo id

def fillcustomerid(df, invoiceNo_tobeFilled):
    customerid = max(df['CustomerID'])+1
    for ind in invoiceNo_tobeFilled:
        df.loc[df['InvoiceNo'] == ind, 'CustomerID'] = customerid
        customerid = customerid+1
    return df
```


```  
print(df.loc[ df['Description'].isnull() & df['CustomerID'].notnull()]) # every Description missing value has a CustomerID missing value
print(df.loc[ df['Description'].isnull() & df['UnitPrice']!=0]) #every Description missing value has a UnitPrice missing value
print(df.loc[ df['Description'].isnull() & ( df['UnitPrice']!=0 | df['CustomerID'].notnull()) ])


invoice_groups = df.groupby('InvoiceNo')['CustomerID'].apply(lambda x: x.isna().any() and x.notna().any()).reset_index()
invoices_with_condition = invoice_groups[invoice_groups['CustomerID'] == True]['InvoiceNo'].tolist()
print(invoices_with_condition) # empty


filtered_df = df.groupby('StockCode')['Description'].apply(lambda x: x.isna().any() and x.str.isalpha().any()).reset_index()pandas sort
# Extract InvoiceNo values that meet the condition
stock_codes = filtered_df[filtered_df['Description'] == True]


nanCustomer_rows=df.loc[df['CustomerID'].isna()]
print(nanCustomer_rows)
print(nanCustomer_rows['InvoiceNo'].nunique()) # 3710 unique invoiceNo values
x = nanCustomer_rows.groupby('InvoiceNo')['InvoiceNo'].value_counts().reset_index(name='f')
sorted_x = x.sort_values(by='f' ,ascending=False)




nanCustomer_rows=df.loc[df['CustomerID'].isna()]
x = nanCustomer_rows.groupby('InvoiceNo')['InvoiceNo'].value_counts().reset_index(name='f')
sorted_x = x.sort_values(by='f' ,ascending=False)
invoiceNo_tobeFilled = x['InvoiceNo']
df = fillcustomerid(df, invoiceNo_tobeFilled)


#fill Description values

def fillDescription(df,stockCode,stockCodeDescription_Frequent):
    for ind in stockCode:
        descr = stockCodeDescription_Frequent.loc[
            stockCodeDescription_Frequent['StockCode'] == ind, 'Description']
        if descr.empty:
            continue
        descr = descr.iloc[0]
        df.loc[(df['StockCode'] == ind) & (df['Description'].isna()), 'Description'] = descr
    return df


missingDescr_rows=df.loc[df['Description'].isna()]
stockcode_rowsToEdit = missingDescr_rows.groupby('StockCode')['StockCode'].value_counts().reset_index(name='count')
xx = df.groupby(['StockCode','Description'])['Description'].value_counts().reset_index(name='count')
xx_sorted = xx.sort_values(by=['StockCode','count'], ascending=[True,False])
max_count_rows = xx_sorted.groupby('StockCode').first().reset_index()
stockCodeDescription_Frequent = max_count_rows[['StockCode', 'Description']]
df = fillDescription(df,stockCode,stockCodeDescription_Frequent)


missingDescr_rows=df[df['Description'].isna()].index  # 14 rows
df.drop(missingDescr_rows , inplace=True)


```  

# 2.2 Cleaning in sql








