import cv2
import torch
import numpy as np
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget

def generate_gradcam_heatmap(model, input_tensor, original_image, target_class=None):
    """
    Generates a Grad-CAM heatmap for a specific disease class and overlays it.
    
    Args:
        model (nn.Module): The PyTorch model.
        input_tensor (torch.Tensor): Preprocessed image tensor [1, 3, 224, 224].
        original_image (np.ndarray): Original image in RGB float format [0, 1] shape (H, W, 3).
        target_class (int or None): Index of the target class to visualize. If None, highest predicted class.
        
    Returns:
        np.ndarray: Heatmap overlaid on the original image.
    """
    # The target layer for DenseNet121 is typically the last layer of features.
    target_layers = [model.backbone.features[-1]]
    
    # Initialize the CAM object
    cam = GradCAM(model=model, target_layers=target_layers)
    
    targets = [ClassifierOutputTarget(target_class)] if target_class is not None else None
    
    # Generate the CAM mask
    grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
    grayscale_cam = grayscale_cam[0, :]
    
    # Resize original image to match CAM output if necessary
    if original_image.shape[:2] != grayscale_cam.shape[:2]:
        original_image = cv2.resize(original_image, (grayscale_cam.shape[1], grayscale_cam.shape[0]))
        
    # Overlay heatmap
    visualization = show_cam_on_image(original_image, grayscale_cam, use_rgb=True)
    
    return visualization
