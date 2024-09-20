import torch
from scene import Scene
import os
from tqdm import tqdm
from os import makedirs
from gaussian_renderer import render
import torchvision
from utils.general_utils import safe_state
from argparse import ArgumentParser
from arguments import ModelParams, PipelineParams, get_combined_args
from gaussian_renderer import GaussianModel_Xray as GaussianModel
import pickle
def render_set(model_path, name, iteration, views, gaussians, pipeline, background):
    render_path = os.path.join(model_path, name, "ours_{}".format(iteration), "renders")
    gts_path = os.path.join(model_path, name, "ours_{}".format(iteration), "gt")

    makedirs(render_path, exist_ok=True)
    makedirs(gts_path, exist_ok=True)

    rendered_images = []  # List to store rendered images
    gt_images = []        # List to store ground truth images
    angles = []
    for idx, view in enumerate(tqdm(views, desc="Rendering progress")):
        rendering = render(view, gaussians, pipeline, background)["render"]
        #print("shape of original image:", view.original_image.shape)
        if view.original_image.shape[0]==1:
            gt = view.original_image[0, :, :]
        else:
            gt = view.original_image[0:3, :, :]
        #print("min, max of rendering:", torch.min(rendering), torch.max(rendering))
        #print("min, max of gt:", torch.min(gt), torch.max(gt))
        # reverse the normalization

        gt = (gt-torch.min(gt)) / (torch.max(gt)-torch.min(gt))
        

        angles.append(view.angle)
        # Append the rendered image and ground truth to lists
        rendered_images.append(rendering)
        gt_images.append(gt)

        torchvision.utils.save_image(rendering, os.path.join(render_path, '{0:05d}'.format(idx) + ".png"))
        torchvision.utils.save_image(gt, os.path.join(gts_path, '{0:05d}'.format(idx) + ".png"))

    # Convert the list of rendered images to a 3D volume by stacking along a new dimension
    rendered_images = torch.stack(rendered_images, dim=0).detach().cpu().numpy().squeeze()  # Creates a 3D volume (stack of images)
    gt_images = torch.stack(gt_images, dim=0).detach().cpu().numpy().squeeze()  # Creates a 3D volume (stack of images)
    print(rendered_images.shape)
    # Save both rendered and ground truth images to a pickle file

    rendered_data_to_save = {
        "projections": rendered_images,
        "angles": angles
    }

    gt_data_to_save = {
        "projections": gt_images,
        "angles": angles
    }
    with open(os.path.join(model_path, name, "ours_{}".format(iteration), 'rendered_images.pickle'), 'wb') as f:
        pickle.dump(rendered_data_to_save, f)

    with open(os.path.join(model_path, name, "ours_{}".format(iteration), 'gt_images.pickle'), 'wb') as f:
        pickle.dump(gt_data_to_save, f)

def render_sets(dataset : ModelParams, iteration : int, pipeline : PipelineParams, skip_train : bool, skip_test : bool, view_synthesis : bool):
    with torch.no_grad():

        gaussians = GaussianModel(dataset.sh_degree) # sh_degree = 3
        scene = Scene(dataset, gaussians, load_iteration=iteration, shuffle=False)

        bg_color = [1,1,1] if dataset.white_background else [0, 0, 0]
        background = torch.tensor(bg_color, dtype=torch.float32, device="cuda")

        if not skip_train:
             render_set(dataset.model_path, "train", scene.loaded_iter, scene.getTrainCameras(), gaussians, pipeline, background)

        if not skip_test:
             render_set(dataset.model_path, "test", scene.loaded_iter, scene.getTestCameras(), gaussians, pipeline, background)

        if view_synthesis:
             render_set(dataset.model_path, "test", scene.loaded_iter, scene.getAddCameras(), gaussians, pipeline, background)
             # for view_synthesis, because "projs = np.zeros((add_num, h, w))" is set in scene\dataset_readers.py, the output gt images are only black

if __name__ == "__main__":
    parser = ArgumentParser(description="Testing script parameters")
    model = ModelParams(parser, sentinel=True)
    pipeline = PipelineParams(parser)
    parser.add_argument("--iteration", default=-1, type=int)
    parser.add_argument("--skip_train", action="store_true")
    parser.add_argument("--skip_test", action="store_true")
    parser.add_argument("--view_synthesis", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--add_vis_num", default=100, type=int)

    #parser.add_argument("--model_path", type=str)
    args = get_combined_args(parser)
    print("Rendering " + args.model_path)
    
    safe_state(args.quiet)
    dataset = model.extract(args)
    if args.view_synthesis:
        dataset.add_num=args.add_vis_num
    #print(dataset.loaded_iter)
    render_sets(dataset, args.iteration, pipeline.extract(args), args.skip_train, args.skip_test, args.view_synthesis)
    
    # python render.py --model_path G:\projects\X-Gaussian\output\foot\2024_09_19_12_51_41 --skip_train --skip_test --view_synthesis --add_vis_num 100

    '''
    Looking for config file in G:\projects\X-Gaussian\output\foot\2024_09_19_12_51_41\cfg_args
    Config file found: G:\projects\X-Gaussian\output\foot\2024_09_19_12_51_41\cfg_args
    Rendering G:\projects\X-Gaussian\output\foot\2024_09_19_12_51_41
    Loading trained model at iteration 20000 [19/09 18:27:45]
    Loading pickle file for X-ray rendering [19/09 18:27:45]
    Reading Training Transforms [19/09 18:27:45]
    Reading Test Transforms [19/09 18:27:45]
    creating additional camera poses [19/09 18:27:45]
    Generating point cloud from uniform cube (32768) [19/09 18:27:45]
    Loading Training Cameras [19/09 18:27:46]
    Loading Test Cameras [19/09 18:27:48]
    Loading Additional Cameras [19/09 18:27:48]
    Rendering progress: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 50/50 [00:04<00:00, 12.27it/s] 
    '''