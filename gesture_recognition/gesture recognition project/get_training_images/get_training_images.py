
import cv2
import os
import sys
import time
try:
    num_of_images = int(sys.argv[1])
    image_label = sys.argv[2]
except: #nalezy podac stosowne argumenty
    print("\nInvalid syntax. Please pass the number of images to be captured and label name as arguments.")
    #pierwszy argument to ilosc zdjec
    #drugi argument to nazwa folderu skojarzona z danym gestem
    print("Sample Command: python get_training_images.py 100 mute")
    exit(-1)

font = cv2.FONT_HERSHEY_PLAIN
click = False

training_img_folder = 'training_images'

#label_name to nazwa naszego gestu np. up, down etc..
label_name = os.path.join(training_img_folder, image_label)

#licz ile zdjec nalezy wykonac
count = image_name = 0

try:
    os.mkdir(training_img_folder)
except FileExistsError:
    pass
try:
    os.mkdir(label_name)
except FileExistsError:
    #jesli juz mamy jakies zdjecia w naszym folderze, to kolejny zacznie sie numerowac
    #od ostatniej utworzonej 
    image_name=len(os.listdir(label_name))

    
#wlacz kamere VideoCapture(0)
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 2000)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)


#petla nieskonczona
while True:
    ret, image = video.read()
    image = cv2.flip(image, 1)
    
    if not ret:
        continue

    #jesli licznik doliczy do ilosci zdjec ktora podalismy w argumencie, to wychodzimy z petli
    if count == num_of_images:
        break

    #rysujemy kwadrat, w srodku ktorego umieszczamy obiekt, który chcemy "fotografowac"
    #edit 03.01.2022 -> bierzemy całą klatke zamiast kwadratu
    #cv2.rectangle(image, (200, 200), (825, 825), (255, 255, 255), 2)

    #po nacisnieciu klawisza "s" rozpoczynamy przechwytywanie
    if click:
        region_of_interest = image[::]
        save_path = os.path.join(label_name, '{}.jpg'.format(image_name + 1))
        cv2.imwrite(save_path, region_of_interest)
        image_name += 1
        count += 1


    cv2.putText(image, "Press 's' to start capturing",
            (20, 30), font, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, "Press 'q' to exit.",
            (20, 60), font, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, "Image Count: {}".format(count),
            (20, 100), font, 1, (12, 20, 200), 2, cv2.LINE_AA)
    cv2.imshow("Get Training Images", image)

    k = cv2.waitKey(10)
    if k==ord('q'):
            break
    if k == ord('s'):
        click = not click

print("\n\nDone\n\n")
video.release()
cv2.destroyAllWindows()
