import cv2
import face_recognition
from simple_facerec import SimpleFacerec
import threading
import imutils
from imutils.video import VideoStream

rtsp_url = "rtsp://admin:admin@192.168.43.121:1935"
rtsp_url2 = "rtsp://admin:admin@192.168.43.6:1935"

video_stream = VideoStream(rtsp_url).start()
video_stream2 = VideoStream(rtsp_url2).start()

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

#
def camera_video():
    while True:
        frame = video_stream.read()
        if frame is None:
            print("none")
        frame = imutils.resize(frame, width=500)
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x1, y2, x2 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            print(name+" is at cam 1")
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        cv2.imshow("cam1", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

def camera_video2():
    while True:
        frame = video_stream2.read()
        if frame is None:
            print("none")
        frame = imutils.resize(frame, width=500)
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x1, y2, x2 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            print(name+" is at cam 2")
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        cv2.imshow("cam2", frame)

        key = cv2.waitKey(1)& 0xFF
        if key == ord('q'):
            break


if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=camera_video)
    t2 = threading.Thread(target=camera_video2)

    # starting thread 1
    t1.start()
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    t2.join()

    print("Done!")
