import pandas as pd
import re


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
    
def format_day(df):
    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []
    
    for index, row in df.iterrows():
        string = str(row['Day'])        
        
        if string.find('M') != -1:
            monday.append(1)
        else:
            monday.append(0)
            
        if string.find('T') != -1:
            tuesday.append(1)
        else:
            tuesday.append(0)
        
        if string.find('W') != -1:
            wednesday.append(1)
        else:
            wednesday.append(0)
            
        if string.find('R') != -1:
            thursday.append(1)
        else:
            thursday.append(0)            
            
        if string.find('F') != -1:
            friday.append(1)
        else:
            friday.append(0)
            
    indexDay = df.columns.get_loc('Day')
    df.insert(loc=indexDay, column='Friday',value=friday)
    df.insert(loc=indexDay, column='Thursday',value=thursday)
    df.insert(loc=indexDay, column='Wednesday',value=wednesday)
    df.insert(loc=indexDay, column='Tuesday',value=tuesday)
    df.insert(loc=indexDay, column='Monday', value=monday)


# extract location and building
def format_location(df):
    buildings = []
    
    for index, row in df.iterrows():
        string = str(row['Location'])
        
        m = re.search("\d", string)
        if m:
            buildings.append(string[:m.start()].strip())
        else:
            buildings.append(string)
    
    indexLoc = df.columns.get_loc('Location')
    df.insert(loc=indexLoc, column='Building', value=buildings)


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
            start = to_minutes(start)
            end = string[separator + 1:].replace(' ', '').lower()
            end = to_minutes(end)

        start_time.append(start)
        end_time.append(end)


    index = df.columns.get_loc('Time')
    df.insert(loc=index, column='EndTime', value=end_time)
    df.insert(loc=index, column='StartTime', value=start_time)


# extract enrollment status to MaxEnroll and CurEnroll
def format_enrollment(df):
    enrollment = []
    max_enrollment = []
    ratio_enrollment = []

    for index, row in df.iterrows():
        string = str(row['Enrollment'])
        separator = string.find('/')

        if separator != -1:
            each_enroll = string[:separator].strip()
            each_max = string[separator + 1:].strip()
            enrollment.append(each_enroll)
            max_enrollment.append(each_max)

            if int(each_max) != 0:
                ratio_enrollment.append(int(each_enroll) * 1.0 / int(each_max))
            else:
                ratio_enrollment.append(None)

    index = df.columns.get_loc('Enrollment')
    df.insert(loc=index, column='RatioEnroll', value=ratio_enrollment)
    df.insert(loc=index, column='MaxEnroll', value=max_enrollment)
    df.insert(loc=index, column='CurEnroll', value=enrollment)


# convert am/pm to minutes
def to_minutes(string):
    colon = string.find(':')
    hour = int(string[: colon])
    minute = int(string[colon + 1 : len(string) - 2])
    if 'pm' in string and hour < 12:
        hour += 12
    elif 'am' in string and hour == 12:
        hour = 0

    return hour * 60 + minute


# convert some column types to int
def convert_to_int(df):
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Quarter'] = pd.to_numeric(df['Quarter'], errors='coerce')
    df['MinUnit'] = pd.to_numeric(df['MinUnit'], errors='coerce')
    df['Unit'] = pd.to_numeric(df['Unit'], errors='coerce')
    df['PassNP'] = pd.to_numeric(df['PassNP'], errors='coerce')
    df['Letter'] = pd.to_numeric(df['Letter'], errors='coerce')
    df['Monday'] = pd.to_numeric(df['Monday'], errors='coerce')
    df['Tuesday'] = pd.to_numeric(df['Tuesday'], errors='coerce')
    df['Wednesday'] = pd.to_numeric(df['Wednesday'], errors='coerce')
    df['Thursday'] = pd.to_numeric(df['Thursday'], errors='coerce')
    df['Friday'] = pd.to_numeric(df['Friday'], errors='coerce')
    df['StartTime'] = pd.to_numeric(df['StartTime'], errors='coerce')
    df['EndTime'] = pd.to_numeric(df['EndTime'], errors='coerce')
    df['CurEnroll'] = pd.to_numeric(df['CurEnroll'], errors='coerce')
    df['MaxEnroll'] = pd.to_numeric(df['MaxEnroll'], errors='coerce')


# main for cleaner.py
filename = raw_input('Please specify a data file (default=Data/data.csv): ')
if filename == '':
    filename = 'Data/data.csv'

columns = ['Quarter', 'ID', 'College', 'Unit', 'Grading', 'Day', 'Time', 'Location', 'Enrollment']
df = pd.read_csv(filename, names=columns)
df_orig = df.copy(deep=True)

format_quarter(df)
format_course_id(df)
format_unit(df)
format_grading(df)
format_time(df)
format_enrollment(df)
format_day(df)
format_location(df)
df = df.drop('Grading', 1)
df = df.drop('Time', 1)
df = df.drop('Enrollment', 1)
df = df.drop('Day', 1)
df = df.drop('Location', 1)
convert_to_int(df)

plt = df.groupby('Building')['RatioEnroll'].mean()
plt.plot(kind='bar', figsize=(15, 6), logy=True)
