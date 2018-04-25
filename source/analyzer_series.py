import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


data_dir = './DataCrontab/'
cleaned_data = './Output/cleaned_data.csv'

def getAllFiles(dir):
    files = []
    listing = os.listdir(dir)
    for infile in listing:
        fileName = dir + infile
        files.append(fileName)
    return files

files = getAllFiles(data_dir)
files.sort()


enrollments = {}
for file in files:
    print ('Parsing ' + file)    
    os.system('python cleaner.py ' + file)
    df = pd.read_csv(cleaned_data)

    for index, row in df.iterrows():
        
        if (int(row['Monday']) + int(row['Tuesday']) 
            + int(row['Wednesday']) + int(row['Thursday']) 
            + int(row['Friday']) > 1):
                enrollment = row['RatioEnroll']
                name = str(row['Subject']) + '-' + str(row['ID'])
                
                if not enrollments.has_key(name):
                    enrollments[name] = []
                enrollments[name].append(enrollment)
    
plt.plot(np.arange(len(enrollments.get('WRIT-50'))), enrollments.get('WRIT-50'))
plt.ylabel('some numbers')
plt.show()
