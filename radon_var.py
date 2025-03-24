# Automatically detect rotation of an image of text using
# Radon transform and fast Fourier transform
# If image is rotated by the inverse of the output, the lines will be
# horizontal (though they may be upside-down depending on the original image)
# It works with black borders because the image is pre-processed to have canny borders only

from skimage.transform import radon
from PIL import Image
import numpy as np
from numpy.fft import rfft
import matplotlib.pyplot as plt
import cv2
import warnings
warnings.filterwarnings("ignore")
try:
    # More accurate peak finding from
    # https://gist.github.com/endolith/255291#file-parabolic-py
    from parabolic import parabolic

    def argmax(x):
        return parabolic(x, np.argmax(x))[0]
except ImportError:
    print('import parabolic error')


def rms_flat(a):
    # Return the root mean square of all the elements of *a*, flattened out.
    return np.sqrt(np.mean(np.abs(a) ** 2))


imgpath = '00460!!!126 II - IMG_1714.JPG'
image = cv2.imread(imgpath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.Canny(gray, 50, 120, apertureSize=3)
# Demean; make the brightness extend above and below zero so that the
# constant component of the FFT is closer to 0
gray = gray - np.mean(gray)
plt.subplot(1, 2, 1)
plt.imshow(gray)

# apply the radon transform every 'angle_interval' degrees
angle_interval = 30
angles = np.arange(0, 180, angle_interval)
angles = angles.tolist()
# Do the radon transform and display the result
sinogram = radon(gray, angles)

plt.subplot(1, 2, 2)
plt.imshow(sinogram, aspect='auto')
plt.gray()

# apply FFT (fast fourier transform) to all rows of the radon transform result
# so that the optimal row can be selected based on its characteristic
# ideally, the nice row should have obvious and clear alternating periods
special_rows = []
y, x = np.shape(sinogram)
Tsino = sinogram.transpose()
# assumption: a 1 hz wave is a wave such that its period is y
# tune_length_low is the end (in terms of herz) of the desired frequency band.
# the two constants below are used to slice the useful frequency band.
tune_length_low = 2
tune_length_high = 90
for i, row in enumerate(Tsino):
    # Subtract the mean to normalize the row
    normalized_row = row - np.mean(row)
    
    # Compute the Fourier Transform of the row
    spectrum = np.abs(np.fft.fft(normalized_row)) / y
    
    # Focus on the desired frequencies
    spectrum = spectrum[y // tune_length_high : y // tune_length_low]
    
    # Identify the maximum peak in the spectrum
    # peak = np.max(spectrum)
    # avg_magnitude = np.mean(spectrum)
    # print(f'col {i} dominant is {peak / avg_magnitude} stronger than average')
    # Check if the peak is higher than the average magnitude
    # below: find the variance of magnitude of the frequency bands
    special_rows.append(np.var(spectrum))
    print(f'col {i} has variance {np.var(spectrum)}')

# plot a vertical red line on the radon transform output.
i = np.argmax(special_rows)
plt.axvline(i, color='r')
plt.show()