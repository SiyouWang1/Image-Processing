from PIL import Image, ImageOps
import os
import cv2
src = 'C:\\D\\DSU\\Dragomans\\CNN-labelled-Dragomans\\CNN-labelled-Dragomans\\upside-down'
dst = src

rotate_ccw = 180
i = 1
for root, dirs, files in os.walk(src):
    for filename in files:
        if filename.endswith(('.png', '.jpg', 'gif', 'tif', 'JPG', 'JPEG', 'jpeg', 'TIF')):
            imgpath = os.path.join(src, filename)
            print(i)
            i+=1
            with Image.open(imgpath) as img:
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # some images have exif data that rotates the image. The following code corrects that. This is necessary!
                exif_data = img.getexif()
                orientation = exif_data.get(274,1)  # Tag 274 is for exif rotation, default the return value as 1 if nothing is found
                if orientation == 3:
                    rotation = 180
                elif orientation == 6:
                    rotation = 270
                elif orientation == 8:
                    rotation = 90
                else:
                    rotation = 0
                    rotated_pil = img.rotate(rotate_ccw + rotation, expand=True)
                    save_path = os.path.join(dst, filename)
                    if filename.endswith(('JPEG', 'JPG', 'jpg', 'jpeg')):
                        # JPEG/jpeg/jpg/JPG formats are quality loss image type that excel at compression
                        # this is why I have to treat these types in a special case
                        rotated_pil.save(save_path, quality=95, subsampling=0)
                    else:
                        rotated_pil.save(save_path)