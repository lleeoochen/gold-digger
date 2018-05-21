import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys

# check if file path is valid
if len(sys.argv) == 1 or sys.argv[1] == '' or not os.path.isdir(sys.argv[1]) or not os.path.exists(os.path.dirname(sys.argv[1])):
    print ('Please specify a valid data folder containing .csv files.')
    exit()

data_dir = sys.argv[1]
quarter = data_dir[data_dir[:-1].rfind('/') + 1:-1]
cleaned_data = './DataClean/cleaned_data.csv'

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

    print ('Cleaning ' + file)    
    os.system('python cleaner.py ' + file)
    df = pd.read_csv(cleaned_data)

    for index, row in df.iterrows():
        mon = int(row['Monday'])
        tue = int(row['Tuesday'])
        wed = int(row['Wednesday'])
        thu = int(row['Thursday'])
        fri = int(row['Friday'])
        isLecture = (mon + tue + wed + thu + fri) > 1

        if isLecture:
            enrollment = round(row['RatioEnroll'], 5)
            name = str(row['Subject']) + '-' + str(row['ID'])

            if not enrollments.has_key(name):
                enrollments[name] = []

            if len(enrollments[name]) == data_length:
                enrollments[name].append(enrollment)

    data_length += 1


# plt.plot(np.arange(len(enrollments.get('PHYS-2'))), enrollments.get('PHYS-2'))
# plt.ylabel('some numbers')
# plt.show()


file = open('DataGraph/graph_' + quarter + '.csv','w')
for key in enrollments:
    output = key + ",["
    for value in enrollments[key]:
        output += str(value) + ","
    output = output + "]\n"
    file.write(output)

file.close()
