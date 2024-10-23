import os
import random
import json
import imageio.v2 as iio
from utils.system_utils import searchForMaxIteration
from scene.dataset_readers import sceneLoadTypeCallbacks
from scene.gaussian_model import GaussianModel_Xray
from arguments import ModelParams
from utils.camera_utils import cameraList_from_camInfos, camera_to_JSON

class Scene:

    gaussians : GaussianModel_Xray

    def __init__(self, args : ModelParams, gaussians : GaussianModel_Xray, load_iteration=None, shuffle=True, resolution_scales=[1.0]):
        self.model_path = args.model_path
        self.loaded_iter = None
        self.volume_positions = None
        self.image_3d = None
        self.gaussians = gaussians

        if load_iteration:
            if load_iteration == -1:
                self.loaded_iter = searchForMaxIteration(os.path.join(self.model_path, "point_cloud"))
            else:
                self.loaded_iter = load_iteration
            print("Loading trained model at iteration {}".format(self.loaded_iter))

        self.train_cameras = {}
        self.test_cameras = {}
        self.add_cameras = {}


        print("Loading pickle file for X-ray rendering, ", args.source_path)
        if os.path.exists(os.path.join(args.source_path, "sparse")):
            scene_info = sceneLoadTypeCallbacks["Colmap"](args.source_path, args.images, args.eval)
        elif os.path.exists(os.path.join(args.source_path, "transforms_train.json")):
            print("Found transforms_train.json file, assuming Blender data set!")
            scene_info = sceneLoadTypeCallbacks["Blender"](args.source_path, args.white_background, args.eval)
        elif ".pickle" in args.source_path:
            print(f"Loading pickle file for X-ray rendering, train_num: {args.train_num}, add_num: {args.add_num}")
            print(f"eval mode: {args.eval}")
            scene_info, self.volume_positions, self.image_3d = sceneLoadTypeCallbacks["Xray"](path = args.source_path, eval = args.eval, interval = args.interval, add_num = args.add_num, train_num = args.train_num)
        else:
            assert False, "Could not recognize scene type!"

        print('number in scene_info.test_cameras:', len(scene_info.test_cameras), '\n',
              'number in scene_info.train_cameras:', len(scene_info.train_cameras), '\n',
              'number in scene_info.add_cameras:', len(scene_info.add_cameras), '\n' )
        if not self.loaded_iter:
            with open(scene_info.ply_path, 'rb') as src_file, open(os.path.join(self.model_path, "input.ply") , 'wb') as dest_file:
                dest_file.write(src_file.read())
            json_cams = []
            camlist = []
            if scene_info.test_cameras:
                camlist.extend(scene_info.test_cameras)
            if scene_info.train_cameras:
                camlist.extend(scene_info.train_cameras)
            #if scene_info.add_cameras:
            #    camlist.extend(scene_info.add_cameras)
            print('total cam length:', len(camlist))
            for id, cam in enumerate(camlist):
                json_cams.append(camera_to_JSON(id, cam))
            with open(os.path.join(self.model_path, "cameras.json"), 'w') as file:
                json.dump(json_cams, file)

        if shuffle:
            random.shuffle(scene_info.train_cameras)  
            random.shuffle(scene_info.test_cameras)  

        self.cameras_extent = scene_info.nerf_normalization["radius"]

        for resolution_scale in resolution_scales:
            print("Loading Training Cameras")
            self.train_cameras[resolution_scale] = cameraList_from_camInfos(scene_info.train_cameras, resolution_scale, args)
            print("Loading Test Cameras")
            self.test_cameras[resolution_scale] = cameraList_from_camInfos(scene_info.test_cameras, resolution_scale, args)
            print("Loading Additional Cameras")
            self.add_cameras[resolution_scale] = cameraList_from_camInfos(scene_info.add_cameras, resolution_scale, args)

        if self.loaded_iter:
            self.gaussians.load_ply(os.path.join(self.model_path,
                                                           "point_cloud",
                                                           "iteration_" + str(self.loaded_iter),
                                                           "point_cloud.ply"))
        else:
            self.gaussians.create_from_pcd(scene_info.point_cloud, self.cameras_extent)

    def save(self, iteration):
        point_cloud_path = os.path.join(self.model_path, "point_cloud/iteration_{}".format(iteration))
        self.gaussians.save_ply(os.path.join(point_cloud_path, "point_cloud.ply"))

    def getTrainCameras(self, scale=1.0):
        return self.train_cameras[scale]

    def getTestCameras(self, scale=1.0):
        return self.test_cameras[scale]
    
    def getAddCameras(self, scale=1.0):
        return self.add_cameras[scale]