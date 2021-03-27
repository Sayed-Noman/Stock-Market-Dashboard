import csv
import json

csvFilePath= 'NASDAQ.csv'
jsonFilePath = 'NASDAQ.json'

#reading csv and adding data to dictonary
data = {"symbols" :[]}

with open(csvFilePath, 'r') as csvFile:
    csvReader = csv.reader(csvFile)
    next(csvReader)
    for row in csvReader:
        data['symbols'].append({
            'serial_no': row[0],
            'company_name' : row[1],
            'company_ticker': row[2]
        })
        

#write to Json File
with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))
