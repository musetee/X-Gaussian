import scipy.io
import pickle
import os 
import numpy as np
root = r'./data'
file = r'output_file_Th1_2000_1000.mat'
save_name = 'data_Th1.pickle'
file_path = os.path.join(root, file)
# Load the .mat file
mat_data = scipy.io.loadmat(file_path)

# Extract the matrix
data = mat_data['data_Th1'].transpose(2, 1, 0)
angles = mat_data['Angle'].squeeze()
angles = angles / 180 * np.pi
print(data.shape)
print(angles.shape)

# Save both rendered and ground truth images to a pickle file
# distance from source to detector (DSD)
# distance from source to object (DSO)
data_to_save = {
    "numTrain": 50,
    "numVal": 50,
    "DSD":1500.0,
    "DSO": 1000.0,
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
    "projections": data,
    "angles": angles
    },
}

with open(os.path.join(root, save_name), 'wb') as f:
    pickle.dump(data_to_save, f)