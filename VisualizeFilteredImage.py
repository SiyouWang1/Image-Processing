# https://youtu.be/ho6JXE3EbZ8
"""
@author: Sreenivas Bhattiprolu

Copying VGG16 architecture and picking the conv layers of interest 
to generate filtered responses. 
"""

import numpy as np
from matplotlib import pyplot as plt
from keras.models import Model
from tensorflow.keras.models import load_model
import cv2
  
model = load_model('11_32_512_512_canny_Tamil_and_English_artificial_and_tagged_training.h5')

print(model.summary())  
    
 
#Understand the filters in the model 
#Let us pick the first hidden layer as the layer of interest.
layer = model.layers #Conv layers at 0, 2, 4
print(layer)
filters, biases = model.layers[0].get_weights()
print(layer[0].name, filters.shape)

   
# plot filters

fig1=plt.figure(figsize=(13, 7))
columns = 8
rows = 4
n_filters = columns * rows
for i in range(1, 33, +1):
    f = filters[:, :, :, i-1]
    fig1 =plt.subplot(rows, columns, i)
    fig1.set_xticks([])  #Turn off axis
    fig1.set_yticks([])
    plt.imshow(f[:, :, 0], cmap='gray') #Show only the filters from 0th channel (R)
    #ix += 1
plt.show()    

#### Now plot filter outputs    

#Define a new truncated model to only include the conv layers of interest
conv_layer_index = [0, 2, 4]  #TO define a shorter model
outputs = [model.layers[i].output for i in conv_layer_index]
model_short = Model(inputs=model.inputs, outputs=outputs)
print(model_short.summary())

#Input shape to the model is 224 x 224. SO resize input image to this shape.
image = cv2.imread('0000013.TIF')
height, width, _ = np.shape(image)

#crop image to avoid extremely obvious borders
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.Canny(gray, 50, 120, apertureSize=3)
resized_image = cv2.resize(gray, (512, 512))

# expand dimensions to match the shape of model input
img = np.expand_dims(resized_image, axis=0)

# Generate feature output by predicting on the input image
feature_output = model_short.predict(img)


columns = 8
rows = 4
for ftr in feature_output:
    fig=plt.figure(figsize=(13, 7))
    for i in range(1, columns*rows +1):
        fig =plt.subplot(rows, columns, i)
        fig.set_xticks([])  #Turn off axis
        fig.set_yticks([])
        plt.imshow(ftr[0, :, :, i-1], cmap='gray')
        #pos += 1
    plt.show()