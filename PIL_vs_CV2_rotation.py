import cv2
from PIL import Image
import os
import time

# Load an image path
src = 'D:\\...Special_media_image_processing\\Dragomans\\test'
dst = 'D:\\...Special_media_image_processing\\Dragomans\\test\\rotation result'

# Timing PIL (Pillow)
start_time_pil = time.time()
for filename in os.listdir(src):
    if filename.endswith(('.png', '.jpg', 'gif', 'tif', 'JPG', 'JPEG', 'jpeg')):
        imgpath = os.path.join(src, filename)
        with Image.open(imgpath) as img:
            rotated_pil = img.rotate(90, expand=True)
            save_path = os.path.join(dst, filename)    
            img_format = img.format
            
            # ensure great quality for JPEG/jpg formatted images
            if img_format in ['JPEG', 'JPG', 'jpg', 'jpeg']:
                rotated_pil.save(save_path, format=img_format, quality=92, subsampling=0)  # Maximum quality for JPEG
            else:
                rotated_pil.save(save_path, format=img_format)
end_time_pil = time.time()
pil_time = end_time_pil - start_time_pil

# Timing OpenCV
start_time_cv2 = time.time()
for filename in os.listdir(src):
    if filename.endswith(('.png', '.jpg', 'gif', 'tif', 'JPG', 'JPEG', 'jpeg')):
        imgpath = os.path.join(src, filename)
        img_cv2 = cv2.imread(imgpath)
        rotated_cv2 = cv2.rotate(img_cv2, cv2.ROTATE_90_CLOCKWISE)  # Rotate the image
        save_path = os.path.join(dst, filename)
        cv2.imwrite(save_path, rotated_cv2)  # Save the rotated image
end_time_cv2 = time.time()
cv2_time = end_time_cv2 - start_time_cv2

# Print the timing results
print(f"Pillow rotation and save time: {pil_time:.6f} seconds")
print(f"OpenCV rotation and save time: {cv2_time:.6f} seconds")
