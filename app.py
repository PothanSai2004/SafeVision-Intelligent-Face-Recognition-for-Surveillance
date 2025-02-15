import cv2
import pickle
import numpy as np
import os

# Load pre-trained face recognition model
with open('faces.pkl', 'rb') as f:
    faces = pickle.load(f)
with open('names.pkl', 'rb') as f:
    names = pickle.load(f)

# Initialize video capture and face detection
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    # Read frame from video stream
    ret, frame = video.read()
    
    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces_detected = facedetect.detectMultiScale(gray, 1.3, 5)
    
    # Iterate through detected faces
    for (x, y, w, h) in faces_detected:
        # Crop the detected face region
        crop_img = gray[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50))
        flattened_img = resized_img.flatten()
        
        # Ensure that the shapes are compatible for subtraction
        if faces.shape[0] > 0:
            flattened_img = flattened_img.reshape(1, -1)
            distances = np.linalg.norm(faces - flattened_img, axis=1)
            min_distance_index = np.argmin(distances)
            min_distance = distances[min_distance_index]
            
            # If minimum distance is less than a threshold, recognize the person
            if min_distance < 500:
                name = names[min_distance_index]
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 255, 50), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 255, 50), 2)
    
    # Display the frame with recognized faces
    cv2.imshow("Frame", frame)
    
    # Check for user input to exit
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

# Release video capture and close windows
video.release()
cv2.destroyAllWindows()
