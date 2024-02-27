# online-retail-uk










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

```  
