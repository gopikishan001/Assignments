import cv2
import time


duration = 60


start_time = time.time()
curr_time = time.time() - start_time

fourcc = cv2.VideoWriter_fourcc(*'MJPG')

frame_width = 640
frame_height = 480
fps = 30


video_writer = cv2.VideoWriter("recorded_video/video.avi", fourcc, fps, (frame_width, frame_height))

vidcap = cv2.VideoCapture(0)


while curr_time < duration:

    res, frame = vidcap.read()
    
    if res :

        frame = cv2.putText(frame, 'time : ' + str(int(curr_time)), (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
        cv2.imshow('Video Recording', frame)
        
        video_writer.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    curr_time = time.time() - start_time

video_writer.release()
vidcap.release()

cv2.destroyAllWindows()
