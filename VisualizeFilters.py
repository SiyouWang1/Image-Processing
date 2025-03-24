import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import load_model

# Load your saved model
model = load_model('11_32_512_512_canny_Tamil_and_English_artificial_and_tagged_training.h5')

# Define a function to plot filters
def plot_filters(layer):
    # Get the weights of the layer
    filters, _ = layer.get_weights()
    # Normalize filter values to the range 0-1 for better visualization
    f_min, f_max = filters.min(), filters.max()
    filters = (filters - f_min) / (f_max - f_min)
    
    # Plot the filters
    n_filters = filters.shape[-1]  # limit to num_filters
    width = 0
    while width*width*2 < n_filters:
        width += 1
    _, axes = plt.subplots(width, 2*width, figsize=(14, 7))
    for i in range(2*width):
        for j in range(width):
            # Get the ith filter and plot
            f = filters[:, :, :, i+(width)*(j)]
            axes[j-1, i-1].imshow(f[:, :, 0], cmap='viridis')
            axes[j-1, i-1].axis('off')
    plt.show()

# List all convolutional layers
conv_layers = [layer for layer in model.layers if 'conv' in layer.name]

# Plot filters for each convolutional layer
for i, layer in enumerate(conv_layers):
    print(f"Filters for layer {layer.name}")
    plot_filters(layer)  # Adjust num_filters to show more or fewer filters