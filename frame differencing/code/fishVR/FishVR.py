

import cv2


############# fish vr #############################
import pygame

pygame.init()

display_width = 1600
display_height = 400

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Fish VR')


black = (0, 0, 0)
white = (255, 255, 255)

#clock = pygame.time.Clock()
crashed = False
fishImg = pygame.image.load('zebra_fish_1.jpg')
w = fishImg.get_rect().size[0]
h = fishImg.get_rect().size[1]
#fishImg = pygame.transform.scale(fishImg, (93, 50))

#zebrafish_small

def fish(x, y):
    gameDisplay.blit(fishImg, (x, y))


x = 10
y = 50
x_change = 10

############# fish vr #############################

cap = cv2.VideoCapture(0)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# i = 1
# j = 1

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        ############# fish vr #############################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        #x = 10

        gameDisplay.fill(black)
        fish(x, y)

        # fishImg = pygame.transform.scale(fishImg, (int(w/i), int(h/i)))
        #
        # j += 1
        #
        # if j > 50:
        #     i += 1
        #     j = 1
        #
        # if i > 20:
        #     i = 1



        pygame.display.update()
        #clock.tick(60)
        ############# fish vr #############################



    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


pygame.quit()
quit()



#zebrafish_small.jpg
#
# import pygame
#
# pygame.init()
#
# display_width = 1600
# display_height = 400
#
# gameDisplay = pygame.display.set_mode((display_width, display_height))
# pygame.display.set_caption('Fish VR')
#
#
# black = (0, 0, 0)
# white = (255, 255, 255)
#
# clock = pygame.time.Clock()
# crashed = False
# carImg = pygame.image.load('zebrafish_small.jpg')
#
#
# def car(x, y):
#     gameDisplay.blit(carImg, (x, y))
#
#
# x = 10
# y = 50
# x_change = 10
#
#
# while not crashed:
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             crashed = True
#
#     if x < display_width - 400:
#         x += x_change
#
#     gameDisplay.fill(black)
#     car(x, y)
#
#     pygame.display.update()
#     clock.tick(60)
#
# pygame.quit()
# quit()