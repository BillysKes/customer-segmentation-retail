# Table of Contents
1. [Introduction]
1.1
    [Project Overview](#project-overview)

3. [Dataset Description](#dataset-description)
4. [Statistical Information](#statistical-information)
5. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
   1. [Bar-Pie Charts](#Bar-Pie-Charts)
   2. [Scatter Plots](#Scatter-Plots)
   3. [Histograms](#Histograms)
6. [Predictive modelling](predictive-modelling)
7. [Model evaluation](model-evaluation)









## Data cleaning

```  
print('\ndata types : \n', df.dtypes)  # verifying that data types are all correct
print('\nmissing values : \n', df.isna().sum())  # missing values detection
print('\nduplicates :\n', df[df.duplicated()])  # duplicates detection

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


# fill nan CustomerID values for every invoiceNo id

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


#fill unitPrice

```




