import csv
import pygame


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
        fish(round(float(new_rows_list[frameCount].get("x-position"))), round(float(new_rows_list[frameCount].get("y-position"))))

        # run until we run out of frames
        if frameCount < totalFrames - 1:
            frameCount = frameCount + 1
        else:
            frameCount = 0

        pygame.display.update()
        clock.tick(10)

    pygame.quit()
    quit()
