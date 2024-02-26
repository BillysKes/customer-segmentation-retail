# online-retail-uk










## Data cleaning

```  
print('\ndata types : \n', df.dtypes)  # verifying that data types are all correct
print('\nmissing values : \n', df.isna().sum())  # missing values detection
print('\nduplicates :\n', df[df.duplicated()])  # duplicates detection

print(df.loc[ df['Description'].isnull() & df['CustomerID'].notnull()]) # every Description missing value has a CustomerID missing value
print(df.loc[ df['Description'].isnull() & df['UnitPrice']!=0]) #every Description missing value has a UnitPrice missing value

```  
