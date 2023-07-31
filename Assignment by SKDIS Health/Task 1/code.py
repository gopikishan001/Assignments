import cv2
import os

dir_loc = "input/"

for file_name in os.listdir(dir_loc) :
    file_loc = os.path.join(dir_loc, file_name)

    image = cv2.imread(file_loc)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))


    for (x, y, w, h) in faces:

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]
        
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        print("file name : ",file_name)
        print("cordinates :")

        if (len(eyes)) < 1 :
            print("failed to detect")
            
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

            center = int(ex + ew/2) , int(ey + eh/2)
            print(center)

            cv2.circle(roi_color, center, 2, (255,255,0), 2)

        print("Press any key for moving to next image")
        print("----------")

        cv2.imshow(file_name , image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()




