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


data_length = 0
enrollments = {}
for file in files:

    print ('Parsing ' + file)    
    os.system('python cleaner.py ' + file)
    df = pd.read_csv(cleaned_data)

    for index, row in df.iterrows():
        
        if (int(row['Monday']) + int(row['Tuesday']) + int(row['Wednesday']) + int(row['Thursday']) + int(row['Friday']) > 1):
            enrollment = round(row['RatioEnroll'], 5)
            name = str(row['Subject']) + '-' + str(row['ID'])

            if not enrollments.has_key(name):
                enrollments[name] = []

            if len(enrollments[name]) == data_length:
                enrollments[name].append(enrollment)

    data_length += 1


plt.plot(np.arange(len(enrollments.get('PHYS-2'))), enrollments.get('PHYS-2'))
plt.ylabel('some numbers')
plt.show()


file = open("DataGraph/data.csv","w")
for key in enrollments:
    output = key + ",["
    for value in enrollments[key]:
        output += str(value) + ","
    output = output[:-1] + "]\n"
    file.write(output)

file.close()
