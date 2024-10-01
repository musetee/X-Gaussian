import scipy.io
import pickle
import os 
import numpy
root = r'D:\Project\ct_data_process\matlab\Naeotom_readraw\output'
file = r'output_file_Th1.mat'
file_path = os.path.join(root, file)
# Load the .mat file
mat_data = scipy.io.loadmat(file_path)

# Extract the matrix
data = mat_data['data_Th1'].transpose(2, 0, 1)
print(data.shape)

save_root = './data'

# Save both rendered and ground truth images to a pickle file
data_to_save = {
    "train":
    {
    "projections": data,
    "angles": None
}
}

with open(os.path.join(save_root, 'data_Th1.pickle'), 'wb') as f:
    pickle.dump(data_to_save, f)