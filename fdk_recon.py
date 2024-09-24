from eval_load_vis_pickle import load_pickle_volume, visualize_volume_with_slider
def load_dataset(file_path =r"data\foot_50.pickle"):
    # Example Usage:
    data = load_pickle_volume(file_path)

    # print('all keys in data: ' )
    # for key, value in data.items():
    #     print(key)
    # Extract metadata and image
    metadata = {key: value for key, value in data.items() if key != 'image' and key !='train' and key !='val'}
    image_volume = data.get('image')
    print('image shape:', image_volume.shape)

    train_data = data.get('train') # 'angles', 'projections'
    projections_train = train_data.get('projections')
    angles_train = train_data.get('angles')

    val_data  = data.get('val') 
    projections_val = val_data.get('projections')
    angles_val = val_data.get('angles')
    print('val dataset projection shape:', projections_val.shape)
    print('val dataset angle shape:', angles_val.shape)
    return projections_val, angles_val, image_volume
from scipy.fftpack import fft, ifft
import numpy as np

def ramp_filter(projection):
    # Apply the ramp filter in Fourier domain
    num_pixels = projection.shape[1]
    freqs = np.fft.fftfreq(num_pixels).reshape(-1, 1)
    
    # Design the ramp filter
    ramp = np.abs(freqs)
    
    # Apply the ramp filter
    filtered_proj = np.fft.ifft(np.fft.fft(projection, axis=1) * ramp, axis=1).real

    return filtered_proj

import numpy as np
from skimage.transform import iradon
from tqdm import tqdm

D = 20
start = 200

def backproject(projections, angles, sinogram_type = 2):
    """
    Back-projects the filtered projections at given angles to reconstruct the 3D volume.
    """
    # We are using skimage's iradon for back-projection
    # For cone-beam CT, you would need to modify the geometry accordingly
    print('backprojection starts')
    
    if sinogram_type == 1:
        # assume sinogram = projections[:,i,:]
        H, W = projections.shape[2], projections.shape[2]
        reconstructed_volume = np.zeros((H, W, D))
        for i in tqdm(range(D)):
            slice_recon = iradon(projections[:,i,:].T, theta=angles, circle=True, filter_name='ramp')
            reconstructed_volume[:,:,i] = slice_recon
    elif sinogram_type == 2:
        # assume sinogram = projections[:,:,i]
        H, W = projections.shape[1], projections.shape[1]
        reconstructed_volume = np.zeros((H, W, D))
        for i in tqdm(range(D)):
            slice_recon = iradon(projections[:,:,i].T, theta=angles, circle=True, filter_name='ramp')
            reconstructed_volume[:,:,i] = slice_recon
    return reconstructed_volume

projections, angles, images = load_dataset(file_path =r"data\foot_50.pickle")
print(angles)
angles = angles / np.pi * 180
# Assuming `angles` is the array of angles for each 2D projection
# angles = np.linspace(0, 180, projections.shape[0], endpoint=False)
# assume sinogram=projections[:,idx,:]

sinogram_type=1 # 1 is correct for original dataset
projections_cropped = projections[:,start:(start+D),:] if sinogram_type ==1 else projections[:,:,start:(start+D)]
VERBOSE = True
if VERBOSE:
    visualize_volume_with_slider(projections, slice_dimension=0)
    visualize_volume_with_slider(images, slice_dimension=2)
    '''
    import matplotlib.pyplot as plt
    plt.imshow(projections[:,200,:], cmap='gray')
    plt.title("sinogram slice")
    plt.show()
    '''

# Reconstruct the 3D volume using FDK
# projections shape: (50, 512, 512)
Reconstruction = True
if Reconstruction:
    volume = backproject(projections_cropped, angles, sinogram_type)
    print("Reconstructed volume shape:", volume.shape)
    visualize_volume_with_slider(volume, slice_dimension=2)
