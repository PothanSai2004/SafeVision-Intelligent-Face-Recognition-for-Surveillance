import pickle

# Specify the path to your pickle file
file_path = 'data/faces_data.pkl'

# Load the data from the pickle file
with open(file_path, 'rb') as f:
    datas = pickle.load(f)

# Now you can inspect the contents of the 'data' variable
print(datas)

# Specify the path to your faces pickle file
file_path = 'data/faces.pkl'

# Load the data from the faces pickle file
with open(file_path, 'rb') as f:
    datea = pickle.load(f)

# Now you can inspect the contents of the 'data' variable
print(datea)

# Specify the path to your name pickle file
file_path = 'data/names.pkl'

# Load the data from the name pickle file
with open(file_path, 'rb') as f:
    data = pickle.load(f)

# Now you can inspect the contents of the 'data' variable
print(data)
