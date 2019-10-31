import csv

def writeToCSV(data):
    # write a new csv file
    with open('fishData.csv', 'w', newline='') as csvFile:
        fileWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(data)

def appendToCSV(data):
    with open('fishData.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def averageCSV():
    print("attempting to correct CSV file")

    new_rows_list = []

    with open('fishData.csv', newline='') as csvFile:
        reader = csv.DictReader(csvFile)

        for row in reader:
            new_rows_list.append(row)

    with open('fishDataCorrected.csv', 'w', newline='') as csvFile:
        fileWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(["object-number", "recorded-time", "run-time", "frame-number", "x-position", "y-position", "z-position"])
        for i in new_rows_list:
            fileWriter.writerow(i.values())

    print("completed. new csv file")

    # to average the CSV
        # check difference in times of frame x and x+1
        # if time difference is greater than 0.15 seconds
        # make a new record for every 0.1 seconds missing
        # new record will be an average position and time
