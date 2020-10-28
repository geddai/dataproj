import pandas as pd

df = pd.read_csv('se_jobs.csv')


# HQ and competitor values are -1, not relevant anymore
df = df.drop(['Competitors', 'Headquarters'], axis=1)   #removes columns

# Company sector
df['Ownership'] = df.apply(lambda x: x['Type of ownership'][10:] if 'Company' in x['Type of ownership']
                                                                    else x['Type of ownership'], axis=1)

# Revenue parsing
df['Bil_Mil'] = df.Revenue.apply(lambda x: 2 if 'billion' in x.lower() else (1 if 'million' in x.lower() else 0))

# Salary changes
df = df[df['Salary Estimate'] != '-1']     #removes -1 salary values
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])      #splits to two elements between the '('
                                                        #then choose only to keep the first element by specifying [0]
no_ks = salary.apply(lambda x: x.replace('K', '').replace('$', '')) #removes 'K' and '$'
df['Min_Sal'] = no_ks.apply(lambda x: int(x.split('-')[0])) #creates a minimum salary field
df['Max_Sal'] = no_ks.apply(lambda x: int(x.split('-')[1]))
df['Avg_Sal'] = (df.Min_Sal + df.Max_Sal)/2

# Company name not laid out properly
df['Company'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-4], axis=1)
                            #removes last 4 characters in text to remove rating beside name
                            #axis=1 : as a series wasn't specified, have to let df know we do this on rows

# Company age
df['Company_Age'] = df.Founded.apply(lambda x: 2020 - x if x > -1 else 0)

# State location
df['State'] = df.Location.apply(lambda x: x.split(', ')[1])

# Job description parsing
df['Git_job'] = df['Job Description'].apply(lambda x: 1 if 'git' in x.lower() or 'github' in x.lower() else 0)
print(df.Git_job.value_counts())
df['Python_job'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
print(df.Python_job.value_counts())          #counts how many times 'python' appears
df['C_job'] = df['Job Description'].apply(lambda x: 1 if ' C,' in x or ' C/' in x or ' C ' in x
                                                        or 'C+' in x or 'C++' in x or 'C#' in x else 0)
print(df.C_job.value_counts())
df['SQL_job'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower()
                                                           or 'structured query language' in x.lower() else 0)
print(df.SQL_job.value_counts())

df.to_csv('se_cleaned.csv', index=False)
