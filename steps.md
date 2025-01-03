# prepare pickle datset:
## read naeotom alpha raw data and save to .mat file
ct_data_process/matlab/Naeotom_readraw/TestRawDataReadXACB10.m
## stack as pickle data
python pickle_from_mat.py
## check pickle data
python eval_load_vis_pickle.py

# training:
python train.py --config config/1002.yaml 

# visualize the results:
get the ply file for example:
output\schweintest\2024_10_08_22_51_22\point_cloud\iteration_100000\point_cloud.ply

visualize by python(slowly):
python eval_Plot3D.py

or visualize in matlab:
matlab/plot3D_opacity.m

# synthesize noval views
python render.py --model_path F:\yang_Projects\X-Gaussian\output\schweintest\2024_10_22_18_50_42 --skip_test
--skip_train
--skip_test
--view_synthesis --add_vis_num 100

# reconstruct using generated noval views
python fbp_for_pickle.py

# notes about the input pickle shape:
the example given by the author has the shape (50, 500, 500), namely (angle_number, slice_number, detector_numbers)

in addition, the original output sinogram of naeotom alpha has shape: (1000, 1376, 144), 1000 is the angle, 1376 is detector numbers (width), 144 is the vertical slice number
so for every slice, sinogram should be (1000, 1376) 
so this should be transposed

at last, while checking and visualizing the pickle data, the image should be rotated around the vertical axis