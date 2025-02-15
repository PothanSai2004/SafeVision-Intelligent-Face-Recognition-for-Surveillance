from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import os

# Load faces data
faces_file_path = 'faces.pkl'
if os.path.exists(faces_file_path):
    with open(faces_file_path, 'rb') as f:
        try:
            FACES = pickle.load(f)
        except Exception as e:
            print("Error loading faces.pkl:", e)
            exit()
else:
    print("Error: faces.pkl not found.")
    exit()

# Load labels (names) data
names_file_path = 'names.pkl'
if os.path.exists(names_file_path):
    with open(names_file_path, 'rb') as f:
        try:
            NAMES = pickle.load(f)
        except Exception as e:
            print("Error loading names.pkl:", e)
            exit()
else:
    print("Error: names.pkl not found.")
    exit()

# Check if data is empty
if len(FACES) == 0 or len(NAMES) == 0:
    print("Error: Empty data arrays.")
    exit()

# Initialize KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)

# Train the KNN classifier
knn.fit(FACES, NAMES)

# Initialize video capture
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict_proba(resized_img)
        max_prob_index = output.argmax()  # Get index of maximum probability
        accuracy = output[0, max_prob_index] * 100
        if accuracy > 50:  # Check if the accuracy is above a certain threshold (e.g., 50%)
            label = knn.predict(resized_img)[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw rectangle around the face
            cv2.putText(frame, f'{label} ({accuracy:.2f}%)', (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Draw rectangle around the face
            cv2.putText(frame, 'Unknown', (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
