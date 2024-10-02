import pickle
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def load_pickle_volume(file_path):
    """
    Load a 3D volume image saved in pickle format.
    
    Args:
        file_path (str): Path to the pickle file containing the 3D volume.
    
    Returns:
        numpy.ndarray: 3D volume data.
    """
    with open(file_path, 'rb') as file:
        volume = pickle.load(file)
    return volume

def visualize_volume(volume, slice_dimension=0):
    """
    Visualize 3D volume image slice-by-slice.
    
    Args:
        volume (numpy.ndarray): The 3D volume data.
    """
    slices = volume.shape[slice_dimension]  # Assuming the slices are along the 3rd dimension
    fig, ax = plt.subplots(1, 1)

    # Loop through each slice and visualize
    for i in range(slices):
        if slice_dimension==0:
            slice = volume[i,:, :] 
        elif slice_dimension==1:
            slice = volume[:,i, :] 
        elif slice_dimension==2:
            slice = volume[:, :, i] 
        ax.clear()
        ax.imshow(slice, cmap='gray')  # Display each slice in grayscale
        ax.set_title(f"Slice {i+1}/{slices}")
        plt.pause(0.1)  # Pause to create an animation effect
    
    plt.show()

def visualize_volume_with_slider(volume, slice_dimension=0):
    """
    Visualize 3D volume with a slider to manually control the displayed slice.
    
    Args:
        volume (numpy.ndarray): The 3D volume data.
    """
    if volume is None:
        print("No volume data found.")
        return
    
    slices = volume.shape[slice_dimension]  # Assuming slices are along the 3rd dimension

    # Create a figure and axis for visualization
    fig, ax = plt.subplots(1, 1)
    plt.subplots_adjust(left=0.25, bottom=0.25)  # Adjust space for the slider
    
    # Display the first slice initially
    slice_idx = 0
    if slice_dimension==0:
        slice = volume[slice_idx,:, :] 
    elif slice_dimension==1:
        slice = volume[:,slice_idx, :] 
    elif slice_dimension==2:
        slice = volume[:, :, slice_idx] 

    img_display = ax.imshow(slice, cmap='gray')
    ax.set_title(f"Slice {slice_idx + 1}/{slices}")
    
    # Create a slider for slice selection
    ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slice_slider = Slider(ax_slider, 'Slice', 0, slices - 1, valinit=slice_idx, valstep=1)
    
    # Update the displayed slice when the slider is moved
    def update(val):
        slice_idx = int(slice_slider.val)
        if slice_dimension==0:
            slice = volume[slice_idx,:, :] 
        elif slice_dimension==1:
            slice = volume[:,slice_idx, :] 
        elif slice_dimension==2:
            slice = volume[:, :, slice_idx] 
        img_display.set_data(slice)
        ax.set_title(f"Slice {slice_idx + 1}/{slices}")
        fig.canvas.draw_idle()  # Update the plot

    # Attach the update function to the slider
    slice_slider.on_changed(update)
    
    plt.show()

def load_example_dataset_train(file_path =r"data\foot_50.pickle"):
    data = load_pickle_volume(file_path)
    train_data = data.get('train') # 'angles', 'projections'
    projections_train = train_data.get('projections')
    print('train dataset projection shape:', projections_train.shape)
    visualize_volume_with_slider(projections_train, slice_dimension=0)

def load_example_dataset(file_path =r"data\foot_50.pickle"):
    # Example Usage:
    
    data = load_pickle_volume(file_path)

    for key, value in data.items():
        print('key: ', key, ',' , 'value: ', value)
    # Extract metadata and image
    metadata = {key: value for key, value in data.items() if key != 'image' and key !='train' and key !='val'}

    train_data = data.get('train') # 'angles', 'projections'
    projections_train = train_data.get('projections')
    angles_train = train_data.get('angles')
    print('train dataset projection shape:', projections_train.shape)
    print('train dataset angles shape:', angles_train.shape)
    print('train dataset angles:', angles_train)
    ''' 0.06283185 = pi/50
    [0.         0.06283185 0.12566371 0.18849556 0.25132741 0.31415927
    0.37699112 0.43982297 0.50265482 0.56548668 0.62831853 0.69115038
    0.75398224 0.81681409 0.87964594 0.9424778  1.00530965 1.0681415
    1.13097336 1.19380521 1.25663706 1.31946891 1.38230077 1.44513262
    1.50796447 1.57079633 1.63362818 1.69646003 1.75929189 1.82212374
    1.88495559 1.94778745 2.0106193  2.07345115 2.136283   2.19911486
    2.26194671 2.32477856 2.38761042 2.45044227 2.51327412 2.57610598
    2.63893783 2.70176968 2.76460154 2.82743339 2.89026524 2.95309709
    3.01592895 3.0787608 ]
    '''
    '''
    val_data  = data.get('val') 
    projections_val = val_data.get('projections')
    angles_val = val_data.get('angles')
    print('val dataset projection shape:', projections_val.shape)
    visualize_volume_with_slider(projections_val, slice_dimension=0)
    
    image_volume = data.get('image')
    print('image shape:', image_volume.shape)
    # visualize_volume_with_slider(image_volume, slice_dimension=2)
    '''

def load_view_synthesis(file_path=r'G:\projects\X-Gaussian\output\foot\2024_09_19_12_51_41\test\ours_20000_view_synthesis_100\rendered_images.pickle'):
    #file_path=r'G:\projects\X-Gaussian\output\foot\2024_09_19_12_51_41\test\ours_20000_test_50\gt_images.pickle'
    data = load_pickle_volume(file_path)

    for key, value in data.items():
        print('all keys in data:', key)

    projections = data.get('projections')
    angles = data.get('angles')
    visualize_volume_with_slider(projections, slice_dimension=0)
    return projections, angles
if __name__=='__main__':
    #load_example_dataset_train(r"data\data_Th1.pickle")
    load_example_dataset(r"data\foot_50.pickle") # data\foot_50.pickle
    #_,_ = load_view_synthesis()
