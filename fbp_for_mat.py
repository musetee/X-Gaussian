import scipy.io
import numpy as np
from skimage.transform import iradon
import matplotlib.pyplot as plt

def load_sino_from_mat(file_path):
    mat_data = scipy.io.loadmat(file_path)

    # Extract the matrix
    sino_with_calibration = mat_data['sino_with_calibration']#.transpose(2, 1, 0)
    sino_without_calibration = mat_data['sino_with_calibration']#.transpose(2, 1, 0)
    angles = mat_data['Angle'].squeeze()
    print('sino_with_calibration', sino_with_calibration.shape, sino_with_calibration.dtype)
    print('angles', angles[0:10])
    return sino_with_calibration, sino_without_calibration, angles

if __name__ == '__main__':
    sino_with_calibration, sino_without_calibration, angles = load_sino_from_mat(r'F:\yang_Projects\X-Gaussian\data\sino_Th1_3000_1008_1.mat')
    projections=sino_with_calibration
    slice_recon = iradon(projections, theta=angles, circle=True, filter_name='ramp')
    print('reconstruction',slice_recon.shape)
    # Create a figure and axis for visualization
    fig, ax = plt.subplots(1, 1)
    plt.subplots_adjust(left=0.25, bottom=0.25)  # Adjust space for the slider
    ax.imshow(slice_recon, cmap='gray')
    plt.show()
    