from email.headerregistry import DateHeader
import pandas as pd
pd.set_option('display.max_rows', None)

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
df.head(10)

#dates are in number
dates_extracted = df.str.extractall(r'(?P<origin>(?P<month>\d?\d)[/|-](?P<day>\d?\d)[/|-](?P<year>\d{4}))')
#index_left = ~df.index.isin([x[0] for x in dates_extracted.index])
dates_extracted = dates_extracted.append(df.str.extractall(r'(?P<origin>(?P<month>\d?\d)[/|-](?P<day>([0-2]?[0-9])|([3][01]))[/|-](?P<year>\d{2}))'))
#index_left = ~df.index.isin([x[0] for x in dates_extracted.index])
del dates_extracted[3]
del dates_extracted[4]
dates_extracted = dates_extracted.append(df.str.extractall(r'(?P<origin>(?P<day>\d?\d) ?(?P<month>[a-zA-Z]{3,})\.?,? (?P<year>\d{4}))'))
#index_left = ~df.index.isin([x[0] for x in dates_extracted.index])
dates_extracted = dates_extracted.append(df.str.extractall(r'(?P<origin>(?P<month>[a-zA-Z]{3,})\.?-? ?(?P<day>\d\d?)(th|nd|st)?,?-? ?(?P<year>\d{4}))'))
del dates_extracted[3]
#index_left = ~df.index.isin([x[0] for x in dates_extracted.index])

# Only year
only_year = df.str.extractall(r'(?P<origin>(?P<year>\d{4}))')
only_year['day'] = 1
only_year['month'] = 1
dates_extracted = dates_extracted.append(only_year)
# index_left = ~df.index.isin([x[0] for x in dates_extracted.index])

#without month
without_month = df.str.extractall(r'(?P<origin>(?P<day>\d\d?)/(?P<year>\d{4}))')
without_month['month'] = 1
dates_extracted = dates_extracted.append(without_month)

#without day
without_day = df.str.extractall('(?P<origin>(?P<month>[A-Z][a-z]{2,}),?\.? (?P<year>\d{4}))')
without_day['day'] = 1
dates_extracted = dates_extracted.append(without_day)

#Year
dates_extracted['year'] = dates_extracted['year'].apply(lambda x: '19' + x if len(x) == 2 else x)
dates_extracted['year'] = dates_extracted['year'].apply(lambda x: str(x))

#Month
dates_extracted['month'] = dates_extracted['month'].apply(lambda x: x[1:] if type(x) is str and x.startswith('0') else x)
month_dict = dict({'September': 9, 'Mar': 3, 'November': 11, 'Jul': 7, 'January': 1, 'December': 12,
                    'Feb': 2, 'May': 5, 'Aug': 8, 'Jun': 6, 'Sep': 9, 'Oct': 10, 'June': 6, 'March': 3,
                    'February': 2, 'Dec': 12, 'Apr': 4, 'Jan': 1, 'Janaury': 1,'August': 8, 'October': 10,
                    'July': 7, 'Since': 1, 'Nov': 11, 'April': 4, 'Decemeber': 12, 'Age': 8})
dates_extracted.replace({"month": month_dict}, inplace=True)
dates_extracted['month'] = dates_extracted['month'].apply(lambda x: str(x))

#Day
dates_extracted['day'] = dates_extracted['day'].apply(lambda x: str(x))

#Cleaned date
dates_extracted['Date'] = dates_extracted['day'] + '-' + dates_extracted['month'] + '-' + dates_extracted['year']
dates_extracted['Date'] = pd.to_datetime(dates_extracted['Date'], errors = 'coerce')
# print(dates_extracted['Date'].sort_values(ascending=True))
dates_extracted = dates_extracted['Date'].sort_values(ascending=True)
dates_extracted = dates_extracted.dropna()
print(dates_extracted)
a = []
for i, j in list (dates_extracted.index):
    a.append(i)
print(pd.Series(a))
