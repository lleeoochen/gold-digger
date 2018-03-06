import pandas as pd


# extract year and quarter number
def format_quarter(df):
    years = []
    
    for index, row in df.iterrows():
        string = str(row['Quarter'])
        start = string.find('./output/') + len('./output/')
        end = string.find('_')
        
        row['Quarter'] = string[end - 1 : end]
        years.append(string[start : end - 1])
        
    df.insert(loc=0, column='Year', value=years)        


# extract subject and course id
def format_course_id(df):
    subjects = []    

    for index, row in df.iterrows():
        string = str(row['ID']).strip()
        separator = string.rfind(' ')
        row['ID'] = string[separator + 1 :].strip()
        
        subject = string[:separator].strip()
        subject = ' '.join(subject.split())
        subjects.append(subject)

    index = df.columns.get_loc('ID')
    df.insert(loc=index, column='Subject', value=subjects)
    

# extract minUnit from unit
def format_unit(df):
    min_units = []
    
    for index, row in df.iterrows():
        string = str(row['Unit'])
        separator = string.find(' - ')
        
        if separator == -1:
            min_units.append('')
        else:
            min_unit = string[:separator]
            min_units.append(min_unit)
            row['Unit'] = string[separator + len(' - '):]

    index = df.columns.get_loc('Unit')
    df.insert(loc=index, column='MinUnit', value=min_units)
    
    
# extract grading options to Letter and PassNP
def format_grading(df):
    letter = []    
    passnp = []
    
    for index, row in df.iterrows():
        string = str(row['Grading'])
        
        if string == 'Optional':
            letter.append(1)
            passnp.append(1)
        
        elif string == 'Pass/No Pass':
            letter.append(0)
            passnp.append(1)
        
        elif string == 'Letter':
            letter.append(1)
            passnp.append(0)
        
        else:
            letter.append(0)
            letter.append(0)
    
    indexL = df.columns.get_loc('Grading')
    indexP = df.columns.get_loc('Grading')
    df.insert(loc=indexL, column='Letter', value=letter)
    df.insert(loc=indexP, column='PassNP', value=passnp)


# extract time to start and end time
def format_time(df):
    start_time = []
    end_time = []

    for index, row in df.iterrows():
        string = str(row['Time'])
        separator = string.find('-')
        start = ''
        end = ''

        if separator != -1:
            start = string[:separator].replace(' ', '').lower()
            start = to_24hr_time(start)
            start = start[:len(start) - 2]
            end = string[separator + 1:].replace(' ', '').lower()
            end = to_24hr_time(end)
            end = end[:len(end) - 2]

        start_time.append(start)
        end_time.append(end)


    index = df.columns.get_loc('Time')
    df.insert(loc=index, column='EndTime', value=end_time)
    df.insert(loc=index, column='StartTime', value=start_time)


# convert am/pm to 24 hour time
def to_24hr_time(string):
    colon = string.find(':')
    hour = int(string[:colon])
    if 'pm' in string and hour < 12:
        hour += 12
    elif 'am' in string and hour == 12:
        hour = 0
    return str(hour) + string[colon:]


# main for cleaner.py
columns = ['Quarter', 'ID', 'College', 'Unit', 'Grading', 'Day', 'Time', 'Location', 'Enrollment']
df = pd.read_csv('Data/data.csv', names=columns)
df_orig = df.copy(deep=True)

format_quarter(df)
format_course_id(df)
format_unit(df)
format_grading(df)
format_time(df)
df = df.drop('Grading', 1)
df = df.drop('Time', 1)
