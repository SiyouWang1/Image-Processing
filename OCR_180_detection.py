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
    image180 = cv2.rotate(gray, cv2.ROTATE_180)

    # Get orientation and script detection (OSD) information
    osd_info = pytesseract.image_to_osd(gray, output_type=Output.DICT)
    osd_info2 = pytesseract.image_to_osd(image180, output_type=Output.DICT)

    # Original orientation confidence and script confidence
    O_oc = osd_info['orientation_conf']
    O_sc = osd_info['script_conf']

    # Rotated orientation confidence and script confidence
    R_oc = osd_info2['orientation_conf']
    R_sc = osd_info2['script_conf']

    if osd_info['orientation'] == 180:
        R_oc += O_oc
        O_oc = 0
        R_sc += O_sc
        O_sc = 0
    elif osd_info['orientation'] in [90, 270]:
        R_oc += O_oc / 2
        O_oc = O_oc / 2
        R_sc += O_sc / 2
        O_sc = O_sc / 2
    if osd_info2['orientation'] == 180:
        O_oc += R_oc
        R_oc = 0
        O_sc += R_sc
        R_sc = 0
    elif osd_info2['orientation'] in [90, 270]:
        O_oc += R_oc / 2
        R_oc = R_oc / 2
        O_sc += R_sc / 2
        R_sc = R_sc / 2
    
    print(O_oc, O_sc, R_oc, R_sc)
    return O_oc, O_sc, R_oc, R_sc 

start_time = time.time()
s1 = 0
f1 = 0

s2 = 0
f2 = 0

s3 = 0
f3 = 0

s4 = 0
f4 = 0

i = 0
for filename in os.listdir(src):
    imgpath = os.path.join(src, filename)
    if filename.endswith(('.jpg', '.jpeg', '.JPEG', '.JPG', '.png', '.gif', '.tif')):
        i += 1
        print(f'the {i}th image')
        try:
            # Attempt to process the image
            O_oc, O_sc, R_oc, R_sc = unpack_confidence(imgpath)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue  # Skip to the next file
        if O_oc + O_sc > R_oc + R_sc:
            s1 += 1
        else:
            f1 += 1
            # shutil.copy(imgpath, mistake_folder)
        if O_oc * O_sc > R_oc * R_sc:
            s2 += 1
        else:
            f2 += 1
            # shutil.copy(imgpath, mistake_folder)
        if O_oc > R_oc:
            s3 += 1
        else:
            f3 += 1
            # shutil.copy(imgpath, mistake_folder)
        if O_sc > R_sc:
            s4 += 1
        else:
            f4 += 1
            # shutil.copy(imgpath, mistake_folder)
    print(f'sum success rate  {s1/(s1+f1)}')
    print(f'mult success rate {s2/(s2+f2)}')
    print(f'oc success rate   {s3/(s3+f3)}')
    print(f'sc success rate   {s4/(s4+f4)}')
end_time = time.time()
time_length = end_time - start_time
print(f"Time elapsed: {time_length:.6f} seconds")