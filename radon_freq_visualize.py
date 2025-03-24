# given an image, do radon transform and display the magnitude
# of each row of the radon transformation
"""
Todo:
    3. test remove image strip vs filter low freq wave
"""

from skimage.transform import radon
from PIL import Image
from numpy import asarray, mean, array, blackman
import numpy as np
from numpy.fft import rfft
import matplotlib.pyplot as plt
import cv2
import warnings
import os
warnings.filterwarnings("ignore")
try:
    # More accurate peak finding from
    # https://gist.github.com/endolith/255291#file-parabolic-py
    from parabolic import parabolic

    def argmax(x):
        return parabolic(x, np.argmax(x))[0]
except ImportError:
    from numpy import argmax
    
src = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\75 sample\\freq_filter_needed'


def get_sino(imgpath, angle_interval):
    num_of_graphs = 180 // angle_interval + 3
    # determine the number of subplots and the 2d space they occupy based on the number of samples
    num_graphx = int(np.floor(np.sqrt(num_of_graphs)))
    num_graphy = int(np.floor(np.sqrt(num_of_graphs)))
    if num_graphx * num_graphy < num_of_graphs:
        num_graphx += 1
    if num_graphx * num_graphy < num_of_graphs:
        num_graphx += 1

    image = cv2.imread(imgpath)
    # image = cv2.bilateralFilter(image, d=9, sigmaColor=123, sigmaSpace=75)
    image = cv2.GaussianBlur(image, (11, 11), 4)
    height, width, _ = np.shape(image)

    #crop image to avoid extremely obvious borders
    image_cropped = image[height // 7 : 6 * height // 7, width // 7 : 6 * width // 7]
    gray = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(gray, 90, 150, apertureSize=3)
    gray = gray - mean(gray)  # Demean; make the brightness extend above and below zero
    plt.figure(1)
    plt.subplot(num_graphy, num_graphx, 1)

    # Remove the horizontal and vertical middle 5th of the gray image so that
    # It is sliced into four parts
    gray_height, gray_width = np.shape(gray)
    small_height = 5 * gray_height // 10
    small_width = 5 * gray_width // 10
    image1 = gray[0 : small_height, 0 : small_width]
    image2 = gray[0 : small_height, -small_width :]
    image3 = gray[-small_height :, 0 : small_width]
    image4 = gray[-small_height :, -small_width :]

    # Create a new canvas with double the height and width to join the 4 slices
    new_height = small_height * 2
    new_width = small_width * 2
    no_mid_gray = np.zeros((new_height, new_width))  # Initialize a black canvas

    # Place images in the new canvas
    no_mid_gray[0:small_height, 0:small_width] = image1  # Top-left
    no_mid_gray[0:small_height, small_width:] = image2  # Top-right
    no_mid_gray[small_height:, 0:small_width] = image3  # Bottom-left
    no_mid_gray[small_height:, small_width:] = image4  # Bottom-right

    plt.imshow(no_mid_gray)

    angles = np.arange(0, 180, angle_interval)
    angles = angles.tolist()
    # Do the radon transform and display the result
    sinogram = radon(no_mid_gray, angles)

    plt.subplot(num_graphy, num_graphx, 2)
    plt.imshow(sinogram, aspect='auto')
    plt.gray()
    return sinogram, no_mid_gray, num_graphy, num_graphx

def rms_flat(a):
    # Return the root mean square of all the elements of *a*, flattened out.
    return np.sqrt(np.mean(np.abs(a) ** 2))

def plot_frequency_graph(spectrums, sample_rate, ylimit, line_space):
    # Plot the frequency graph of the FFT output.
    n = len(spectrums[0])
    i = 0
    for spectrum in spectrums:
        freq = np.fft.fftfreq(n, d=1/sample_rate)[: n // 2] # Generate frequency axis values in Hz [5:n // 5]
        magnitude = np.abs(spectrum)[: n // 2]  # Only take the positive half
        title = f'Row {i}'
        try:
            if np.max(magnitude) == ylimit:
                color = 'red'
                plt.subplot(num_graphy, num_graphx, i + 3)
                i += 1
                plt.plot(sinogram[:, i-1])
                highy = np.shape(no_mid_gray)[1] - 1 - np.argmax(sinogram[:, i-1])
                # text_row = no_mid_gray[highy - line_space : highy + line_space, :]
                # plt.pause(0.1)
                # plt.figure(2)
                # plt.imshow(text_row)
                plt.pause(0.1)
                plt.figure(1)
            else:
                color = 'blue'
            plt.subplot(num_graphy, num_graphx, i + 3)
            plt.plot(freq, magnitude, color = color)
            plt.title(title, fontsize = 7)
            plt.xlabel("Frequency (Hz)", fontsize = 7)
            plt.ylabel("Magnitude", fontsize = 7)
            plt.grid(True)
            # Adjust tick label font sizes
            plt.tick_params(axis='both', which='major', labelsize=6)  # Set font size for major ticks

            # Set the y-axis limit to have a maximum value of 1000
            plt.ylim(bottom = 0, top = ylimit + 1000)  # Fix the maximum value of the y-axis to 1000
            i += 1
        except:
            i += 1

# Find the RMS value of each row and find "busiest" rotation,
# where the transform is lined up perfectly with the alternating dark
# text and white lines
def get_fourier_rows(sino):
    spectrums = []
    peaks = []
    y, x = np.shape(sino)
    Tsino = sino.transpose()
    tune_length_low = 2
    tune_length_high = 130
    # Loop through each row of the image
    for i, row in enumerate(Tsino):
        # Subtract the mean to normalize the row
        normalized_row = row - np.mean(row)
        
        # Compute the Fourier Transform of the row
        spectrum = np.abs(np.fft.fft(normalized_row)) / y
        
        # Focus on the desired frequencies y // tune_length_high : y // tune_length_low
        spectrum = spectrum[50: y // 2]
        
        # Identify the maximum peak in the spectrum
        # peak = np.max(spectrum)
        # avg_magnitude = np.mean(spectrum)
        # print(f'col {i} dominant is {peak / avg_magnitude} stronger than average')
        # Check if the peak is significantly higher than the average magnitude
        spectrums.append(spectrum)  # This row has a clear periodic pattern
        peaks.append(np.max(spectrum[:len(spectrum) // 2]))
    maxy = np.max(peaks)
    space_val = int(np.shape(no_mid_gray)[1] * 2 * (1 / (np.argmax(peaks) + y // tune_length_high)))
    return spectrums, y, maxy, space_val


for filename in os.listdir(src):
    imgpath = os.path.join(src, filename)
    print(filename)
    if filename.endswith(('.jpg', '.jpeg', '.JPEG', '.JPG', '.png', '.gif', '.TIF', '.tif')):
        sinogram, no_mid_gray, num_graphy, num_graphx = get_sino(imgpath, 30)
        rows, y, maxval, freq= get_fourier_rows(sinogram)
        plot_frequency_graph(rows, y, maxval, freq)

        # i = np.argmax(special_rows)
        # plt.axvline(i, color='r')
        plt.savefig(os.path.join(src, 'plot' + filename), format="png", dpi=300)
        plt.clf()
        plt.close()