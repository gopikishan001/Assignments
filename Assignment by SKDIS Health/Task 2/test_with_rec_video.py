
import cv2
import time
import numpy as np
from matplotlib import pyplot as plt

plt.ion()

fig, ax = plt.subplots()
line, = ax.plot([], [])
red_avg_values = [0]
time_count = [0]

start_time = time.time()

vidcap = cv2.VideoCapture("recorded_video/video.avi")

if vidcap.isOpened():
    
    while(True):
        res, frame = vidcap.read() 

        if res: 
            roi  = frame

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))



            # for (x, y, w, h) in faces[:1]:
            if len(faces) > 0 :
                x , y , w , h = faces[0]

                x += int(0.30 * w)
                y += int(0.05 * h)
                
                x1 = int(x + (0.40 * w))
                y1 = int(y + (0.15 * h))

                cv2.rectangle(frame, (x, y), (x1,y1), (0, 255, 0), 2)

                roi = frame[ y:y1 , x:x1]

                red_avg = np.mean(roi[:, :, 2])  

                red_avg_values.append(red_avg)     
                time_count.append(time.time() - start_time) 

                

                # cv2.imshow("image" , roi)

            else :
                red_avg_values.append(red_avg_values[-1])     
                time_count.append(time.time() - start_time) 

            if len(time_count) > 150 : 
                time_count =  time_count[-150 :]
                red_avg_values =  red_avg_values[-150 : ]   
                ax.clear()

            ax.set_xlabel('Time in sec')
            ax.set_ylabel('Average red ')
            ax.set_title('Average red over time')
                
            ax.plot(time_count, red_avg_values, color='red')
            ax.relim()
            ax.autoscale_view()
            plt.pause(0.001 )
            
            cv2.imshow("frame" , frame)


            frame_number = int(vidcap.get(cv2.CAP_PROP_POS_FRAMES))

            for _ in range(abs(int(((time.time() - start_time) * 30) - frame_number))):
                vidcap.read()   # skipping frames

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Capturing frame error")
            break

else:
    print("Video opening error")

vidcap.release()
cv2.destroyAllWindows()
plt.ioff()

