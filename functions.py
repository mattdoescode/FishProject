import csv
import pygame


def writeHeadCSV(filename):
    data = ["object-number", "recorded-time", "run-time", "frame-number", "x-position", "y-position", "z-position",
            "corrected-data"]
    with open(filename + ".csv", 'w', newline='') as csvFile:
        fileWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(data)


def writeToCSV(filename, data):
    # write a new csv file
    with open(filename + ".csv", 'w', newline='') as csvFile:
        fileWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(data)


def appendToCSV(filename, data):
    with open(filename + '.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def averageCSV(inputFileName, outputFileName):
    print("attempting to correct CSV file")

    # rows to be written to new file
    new_rows_list = []
    errorTime = .12
    frameTime = 0

    # read file
    with open(inputFileName + '.csv', newline='') as csvFile:
        reader = csv.DictReader(csvFile)

        # counter for each line in the CSV
        # starts at 1 because the first line is automatically recorded
        totalLines = 1

        # iterate over each row of the file looking for missing data
        for row in reader:
            previousFrameTime = frameTime
            currentFrameTime = float(row.get("run-time"))

            if previousFrameTime == 0:
                frameTime = float(row.get("run-time"))
                new_rows_list.append(row.copy())
                continue

            # figure out how many missing frames there are
            if previousFrameTime + errorTime < currentFrameTime:

                fakeFrameCount = int(abs(previousFrameTime - currentFrameTime) / 0.1) - 1

                if fakeFrameCount == 1:
                    print("adding in 1 fake record")
                else:
                    print("adding in", fakeFrameCount, "fake record")

                # our goal in the current record
                # previous record
                previousRecord = new_rows_list[totalLines - 1]

                # find the differences in between the 2
                # and average the changes
                # timeIncrement = (float(previousRecord.get("run-time")) - float(row.get("run-time"))) / fakeFrameCount - 1

                xIncrement = (float(row.get("x-position")) - float(previousRecord.get("x-position"))) / (
                        fakeFrameCount + 1)
                yIncrement = (float(row.get("y-position")) - float(previousRecord.get("y-position"))) / (
                        fakeFrameCount + 1)
                zIncrement = (float(row.get("z-position")) - float(previousRecord.get("z-position"))) / (
                        fakeFrameCount + 1)
                # print(float(row.get("x-position")))
                # print(float(previousRecord.get("x-position")))
                # print(xIncrement)

                frameCounter = 1
                # add in the missing frames
                while previousFrameTime + errorTime < currentFrameTime:
                    previousFrameTime = previousFrameTime + 0.1
                    fakeRecord = row.copy()
                    fakeRecord.update({"run-time": previousFrameTime})
                    fakeRecord.update({"recorded-time": 0})
                    fakeRecord.update({"frame-number": totalLines})
                    fakeRecord.update(
                        {"x-position": float(previousRecord.get("x-position")) + (frameCounter * xIncrement)})
                    fakeRecord.update(
                        {"y-position": float(previousRecord.get("y-position")) + (frameCounter * yIncrement)})
                    fakeRecord.update(
                        {"z-position": float(previousRecord.get("z-position")) + (frameCounter * zIncrement)})
                    fakeRecord.update({"fakeRecord": "1"})
                    totalLines = totalLines + 1
                    frameCounter = frameCounter + 1
                    new_rows_list.append(fakeRecord)

            frameTime = currentFrameTime

            tempRecord = row.copy()
            tempRecord.update({"frame-number": totalLines})
            totalLines = totalLines + 1
            new_rows_list.append(tempRecord)

    # create new file and fill it with corrected data
    with open(outputFileName + '.csv', 'w', newline='') as csvFile:
        fileWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(
            ["object-number", "recorded-time", "run-time", "frame-number", "x-position", "y-position", "z-position"])
        for i in new_rows_list:
            fileWriter.writerow(i.values())
    print("completed. new csv file")

    # to average the CSV
    # check difference in times of frame x and x+1
    # if time difference is greater than 0.15 seconds
    # make a new record for every 0.1 seconds missing
    # new record will be an average position and time


def visualizeFish(display_width, display_height):
    # image from:
    # https://www.zebrafishfilm.org/

    pygame.init()

    black = (0, 0, 0)

    # set window size and caption it
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('ZebraFish Visual')

    # load the image
    fishImg = pygame.image.load('zebrafish.png')

    def fish(x, y):
        gameDisplay.blit(fishImg, (x, y))

    clock = pygame.time.Clock()
    crashed = False

    # copy the csv to a use-able format
    new_rows_list = []

    # open and read the data from the CSV
    with open('fishDataCorrected.csv', newline='') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            new_rows_list.append(row)

    # track the frame count
    frameCount = 0

    # total number of frames we need
    totalFrames = len(new_rows_list)

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        gameDisplay.fill(black)
        print(frameCount)
        fish(round(float(new_rows_list[frameCount].get("x-position"))),
             round(float(new_rows_list[frameCount].get("y-position"))))

        # run until we run out of frames
        if frameCount < totalFrames - 1:
            frameCount = frameCount + 1
        else:
            frameCount = 0

        pygame.display.update()
        clock.tick(10)

    pygame.quit()
    quit()
