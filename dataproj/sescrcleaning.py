#cleaning: remove unneeded text/elements and simplify to only what info is required

import pandas as pd

dataframe = pd.read_csv('gd_dsjobs.csv')

#salary parsing
dataframe = dataframe[dataframe['Salary Estimate'] != '-1']     #removes -1 salary values
salary = dataframe['Salary Estimate'].apply(lambda x: x.split('(')[0])      #splits to two elements between the '('
                                                        #then choose only to keep the first element by specifying [0]
removek = salary.apply(lambda x: x.replace('K','').replace('$','')) #removes 'K' and '$'
dataframe['minsal'] = removek.apply(lambda x: int(x.split('-')[0])) #creates a minimum salary field
dataframe['maxsal'] = removek.apply(lambda x: int(x.split('-')[1]))
dataframe['avgsal'] = (dataframe.minsal + dataframe.maxsal)/2

#company name text only
dataframe['company name'] = dataframe.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-4], axis=1)
                            #removes last 4 characters in text to remove rating beside name
                            #axis=1 : as a series wasn't specified, have to let dataframe know we do this on rows

#state field
dataframe['same state'] = dataframe.apply(lambda x: 1 if x['Headquarters'] == x['Location'] else 0, axis=1)
                            #checks if job location is in hq

#company age
dataframe['company age'] = dataframe.Founded.apply(lambda x: 2020 - x)

#parsing job description
dataframe['AI_job'] = dataframe['Job Description'].apply(lambda x: 1 if 'AI' in x or 'Artificial Intelligence' in x else 0)
print(dataframe.AI_job.value_counts())          #counts how many times 'AI' appears

print(dataframe.columns)    #prints all column keys
df_out = dataframe.drop(['Competitors'], axis=1)        #removes 'Competitors' column
df_out.to_csv('datacleaned.csv')