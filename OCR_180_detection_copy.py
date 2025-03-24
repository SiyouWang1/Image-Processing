# Extract the text orientation in the pytesseract osd info
# Too slow and not reliable
from pytesseract import Output
import pytesseract
from PIL import Image
import os
import numpy as np
import shutil
import time
import cv2
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

src = 'D:\\...Special_media_image_processing\\Dragomans\\test samples'
mistake_folder = ''

def unpack_confidence(imgpath):
    # Load the image
    image = cv2.imread(imgpath)
    x, y, color = np.shape(image)
    image = image[y // 3 : 2 * y // 3 , x // 3 : 2 * x // 3]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(gray, 50, 120, apertureSize=3)

    # Get orientation and script detection (OSD) information
    osd_info = pytesseract.image_to_osd(gray, output_type=Output.DICT)

    # Original orientation confidence and script confidence
    Oo = osd_info['orientation']
    
    if Oo == 0:
        return True
    else:
        return False 

start_time = time.time()
s1 = 0
f1 = 0
i = 0
for filename in os.listdir(src):
    imgpath = os.path.join(src, filename)
    if filename.endswith(('.jpg', '.jpeg', '.JPEG', '.JPG', '.png', '.gif', '.tif')):
        i += 1
        print(f'the {i}th image')
        try:
            # Attempt to process the image
            result = unpack_confidence(imgpath)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue  # Skip to the next file
        if result:
            s1 += 1
        else:
            f1 += 1
            # shutil.copy(imgpath, mistake_folder)
    print(f'sum success rate  {s1/(s1+f1)}')
end_time = time.time()
time_length = end_time - start_time
print(f"Time elapsed: {time_length:.6f} seconds")