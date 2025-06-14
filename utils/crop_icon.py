from PIL import Image
import os

def crop_image_to_square(input_path, output_path, start_top=50):
    """
    Crops the center of a square region from an image.
    The top of the square starts at 2/5 of the image height.
    
    Args:
        input_path (str): Path to the source image.
        output_path (str): Path to save the cropped image.
    """
    with Image.open(input_path) as img:
        width, height = img.size

        crop_size = min(width, height)

        left = (width - crop_size) // 2
        top = start_top
        top = min(top, height - crop_size)

        box = (left, top, left + crop_size, top + crop_size)
        
        # Crop and save
        cropped_img = img.crop(box)
        cropped_img.save(output_path)
        print(f"Cropped image saved to {output_path}")
        

