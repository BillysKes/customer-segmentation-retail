import numpy as np
import pandas as pd


def fillcustomerid(df, invoiceNo_tobeFilled):
    customerid = max(df['CustomerID'])+1
    for ind in invoiceNo_tobeFilled:
        df.loc[df['InvoiceNo'] == ind, 'CustomerID'] = customerid
        customerid = customerid+1
    return df


def fillDescription(df,stockCode,stockCodeDescription_Frequent):
    for ind in stockCode:
        descr = stockCodeDescription_Frequent.loc[
            stockCodeDescription_Frequent['StockCode'] == ind, 'Description']
        if descr.empty:
            continue
        descr = descr.iloc[0]
        df.loc[(df['StockCode'] == ind) & (df['Description'].isna()), 'Description'] = descr
    return df


pd.set_option('display.max_columns', None)  #
pd.set_option('display.width', None)  # fit more columns
df = pd.read_csv('C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\data.csv', encoding='unicode_escape')

print('\ndata types : \n', df.dtypes)  # verifying that data types are all correct
print('\nmissing values : \n', df.isna().sum())  # missing values detection
print('\nduplicates :\n', df[df.duplicated()])  # duplicates detection
#print('\n\n', df['City'].unique().tolist())  # Inconsistencies detection - in one column

for column in df.columns:
    print("Column:", column)
    print(df[column].unique())
print("\n\n", round(df.describe(), 2))  # statistics information
print('\n\n', df.describe(include='object'))  # statistics for categorical variables

df['Description'].str.strip()
df['Country'].str.strip()
df['Description'] = df['Description'].str.replace('"', '')
for column in df.columns:
    if df[column].dtype == 'object':  # Check if the column type is object (string)
        df[column] = df[column].str.replace('"', '')

nanCustomer_rows=df.loc[df['CustomerID'].isna()]
x = nanCustomer_rows.groupby('InvoiceNo')['InvoiceNo'].value_counts().reset_index(name='f')
sorted_x = x.sort_values(by='f' ,ascending=False)
invoiceNo_tobeFilled = x['InvoiceNo']
df = fillcustomerid(df, invoiceNo_tobeFilled)

missingDescr_rows = df.loc[df['Description'].isna()]  #  1454 rows
stockcode_rowsToEdit = missingDescr_rows.groupby('StockCode')['StockCode'].value_counts().reset_index(name='count')
filteredStockcodeAlldescr = df.groupby(['StockCode','Description'])['Description'].value_counts().reset_index(name='count')
filteredStockcodeAlldescr = filteredStockcodeAlldescr.sort_values(by=['StockCode','count'], ascending=[True,False])
max_count_rows = filteredStockcodeAlldescr.groupby('StockCode').first().reset_index()
stockCodeDescription_Frequent = max_count_rows[['StockCode', 'Description']]
stockCodeList=stockcode_rowsToEdit['StockCode']  #  960 products
df = fillDescription(df, stockCodeList, stockCodeDescription_Frequent)

#df.to_csv(.\data\data2.csv', index=False)
