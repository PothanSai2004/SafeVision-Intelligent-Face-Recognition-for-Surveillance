import cv2
import pickle
import numpy as np
import os

def add_faces(name):
    video = cv2.VideoCapture(0)
    facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    faces_data = []

    i = 0

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w, :]
            resized_img = cv2.resize(crop_img, (50, 50))
            if len(faces_data) <= 100 and i % 10 == 0:
                faces_data.append(resized_img.flatten())
            i += 1
            cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1)
        if k == ord('q') or len(faces_data) == 100:
            break

    video.release()
    cv2.destroyAllWindows()

    faces_data = np.asarray(faces_data)

    # Check if faces.pkl exists
    if 'faces.pkl' in os.listdir('/'):
        # Load existing faces data
        with open('faces.pkl', 'rb') as f:
            faces = pickle.load(f)
        # Check if faces array is empty
        if faces.size == 0:
            faces = faces_data
        else:
            # Append new faces data to existing faces data
            faces = np.append(faces, faces_data, axis=0)
    else:
        # Create new faces data
        faces = faces_data

    # Save updated faces data to faces.pkl
    with open('faces.pkl', 'wb') as f:
        pickle.dump(faces, f)

    # Save labels (names) to names.pkl
    if 'names.pkl' not in os.listdir('/'):
        names = [name] * 100
        with open('names.pkl', 'wb') as f:
            pickle.dump(names, f)
    else:
        with open('names.pkl', 'rb') as f:
            names = pickle.load(f)
        names += [name] * 100
        with open('names.pkl', 'wb') as f:
            pickle.dump(names, f)

if __name__ == "__main__":
    name = input("Enter Your Name: ")
    add_faces(name)
