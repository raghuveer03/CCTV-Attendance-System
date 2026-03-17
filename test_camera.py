# quick script to test if webcam + face detection is working
# run this before starting the main app if you want to verify setup
# K.Raghuveer

import cv2

print("opening webcam... press q to quit")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: couldnt open camera. check if its connected / not in use by another app")
    exit()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

while True:
    ok, frame = cap.read()
    if not ok:
        print("frame grab failed")
        break

    # flip so it looks like a mirror
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'face detected', (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)

    label = f'{len(faces)} face(s) | q to quit'
    cv2.putText(frame, label, (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow('camera test - K.Raghuveer', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("done")
