import scipy.io
import pickle
import os 
import numpy as np

def preprocess(data, scalar):
    return (data - np.min(data))/scalar

root = r'./data'
file = r'output_file_Th1_3000_1008.mat'
save_name = 'data_Th1_3000_1008.pickle'
file_path = os.path.join(root, file)
# Load the .mat file
mat_data = scipy.io.loadmat(file_path)

# Extract the matrix
scalar = 150000.0
data = mat_data['data_Th1'].transpose(2, 1, 0)
print('train dataset projection before preprocess, min, max:', np.min(data), np.max(data))
print(data.dtype)
data = preprocess(data, scalar)
print('train dataset projection after preprocess, min, max:', np.min(data), np.max(data)) # 0 - 0.1
angles = mat_data['Angle'].squeeze() / 180 * np.pi

data_test = mat_data['data_Th1'].transpose(2, 1, 0)
data_test = preprocess(data_test, scalar)
angles_test = mat_data['Angle'].squeeze() / 180 * np.pi
print(data.shape)
print(angles.shape)

# Save both rendered and ground truth images to a pickle file
# distance from source to detector (DSD)
# distance from source to object (DSO)
data_to_save = {
    "numTrain": 50,
    "numVal": 50,
    "DSD":1100.0,
    "DSO": 610.0,
    "nDetector": [512, 512],
    "dDetector": [1.0, 1.0],
    "nVoxel": [256, 256, 256],
    "dVoxel": [1.0, 1.0, 1.0],
    "offOrigin": [0, 0, 0],
    "offDetector": [0, 0],
    "accuracy": 0.5,
    "mode": "cone",
    "filter": None,
    "totalAngle": 180.0,
    "startAngle": 0.0,
    "randomAngle": False,
    "convert": True,
    "rescale_slope": 1.0,
    "rescale_intercept": 0.0,
    "normalize": True,
    "noise": 0,
    "image": None,
    "train":
    {
    "projections": data,
    "angles": angles
    },
    "val":
    {
    "projections": data_test,
    "angles": angles_test
    },
}

with open(os.path.join(root, save_name), 'wb') as f:
    pickle.dump(data_to_save, f)
    
