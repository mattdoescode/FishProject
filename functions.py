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
        fileWriter.writerow(["object-number", "recorded-time", "run-time", "frame-number", "x-position", "y-position", "z-position"])
        for i in new_rows_list:
            fileWriter.writerow(i.values())

    print("completed. new csv file")

    # to average the CSV
        # check difference in times of frame x and x+1
        # if time difference is greater than 0.15 seconds
        # make a new record for every 0.1 seconds missing
        # new record will be an average position and time

def visualizeFish(display_width,display_height):
    pygame.init()

    black = (0, 0, 0)
    white = (255, 255, 255)

    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('ZebraFish Visual')

    fishImg = pygame.image.load('zebra_fish.jpg')

    def fish(x, y):
        gameDisplay.blit(fishImg, (x, y))

    clock = pygame.time.Clock()
    crashed = False

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        gameDisplay.fill(white)
        fish(x, y)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()