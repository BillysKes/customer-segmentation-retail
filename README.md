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

```  
