import csv

def writeToCSV(data):
    # write a new csv file
    with open('fishData.csv', 'w', newline='') as csvFile:
        fileWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(data)

def appendToCSV(data):
    with open(r'fishData.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def averageCSV():
    print("fixed CSV file")