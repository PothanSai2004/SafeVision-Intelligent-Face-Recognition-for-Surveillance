import pickle
import numpy as np

# Clear the existing data in names.pkl
with open('names.pkl', 'wb') as f:
    pickle.dump([], f)

# Clear the existing data in faces_data.pkl
with open('faces_data.pkl', 'wb') as f:
    pickle.dump(np.array([]), f)
    
# Clear the existing data in faces_data.pkl
with open('faces.pkl', 'wb') as f:
    pickle.dump(np.array([]), f)

print("Data cleared successfully.")
