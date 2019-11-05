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

    # rows to be written to new file
    new_rows_list = []
    errorTime = .15
    frameTime = 0

    #read file
    with open('fishData.csv', newline='') as csvFile:
        reader = csv.DictReader(csvFile)

        # iterate over each row of the file looking for missing data
        for row in reader:
            previousFrameTime = frameTime
            currentFrameTime = float(row.get("run-time"))

            if previousFrameTime == 0:
                frameTime = float(row.get("run-time"))
                new_rows_list.append(row)
                continue

            while previousFrameTime + errorTime < currentFrameTime:
                print("error in file - adding record")
                previousFrameTime = previousFrameTime + 0.1
                fakeRecord = row
                fakeRecord.update({"run-time": previousFrameTime})
                print("previous time is: ", float(previousFrameTime))
                fakeRecord.update({"recorded-time": 0})
                # fakeRecord.update({"frame-number": 0})
                fakeRecord.update({"x-position": 0})
                fakeRecord.update({"y-position": 0})
                fakeRecord.update({"z-position": 0})
                new_rows_list.append(fakeRecord)

            frameTime = currentFrameTime
            new_rows_list.append(row)

    # create new file and fill it with corrected data
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
