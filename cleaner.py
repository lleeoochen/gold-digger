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
    
# main for cleaner.py
columns = ['Quarter', 'ID', 'College', 'Unit', 'Grading', 'Day', 'Time', 'Location', 'Enrollment']
df = pd.read_csv('Data/data.csv', names=columns)

format_quarter(df)
format_course_id(df)
format_unit(df)
format_grading(df)
format_day(df)
format_location(df)
df = df.drop('Grading', 1)

df.head()