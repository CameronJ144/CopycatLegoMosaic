import numpy as np
from PIL import Image

# Function to load an image from a file path
def load_image(file_path):
    img = Image.open(file_path)
    return img

# Function to resize an image DOWN to (num_pixels x num_pixels) pixels
def scale_img_down(img, dimensions):
    resized_img = img.resize(dimensions, resample=Image.Resampling.NEAREST)  # Changed to NEAREST
    return resized_img

# Function to resize an image UP to original dimensions
def scale_img_up(img, dimensions):
    resized_img = img.resize(dimensions, resample=Image.Resampling.NEAREST)
    return resized_img

# Function to convert a PIL image to a numpy array
def convert_img_to_array(img):
    arr = np.array(img)
    return arr

# Function to convert a numpy array to a PIL image
def convert_array_to_img(arr):
    img = Image.fromarray(arr.astype("uint8"), "RGB")
    return img

# LEGO tile colors dictionary
lego_colors = {
    "blue": (70, 158, 209),
    "black": (47, 47, 47),
    "brown": (130, 94, 65),
    "grey": (124, 124, 124),
    "peach": (247, 188, 153),
    "white": (245, 245, 242),
    "red": (222, 20, 20)
}

# Function to calculate Euclidean distance between two RGB tuples
def get_rgb_distance(rgb1, rgb2):
    return np.sqrt(sum((rgb1[i] - rgb2[i])**2 for i in range(3)))

# Function to get the LEGO tile with the smallest Euclidean distance
def get_closest_lego_pixel(pixel):
    min_dist = float("inf")
    closest_color = None
    for color, rgb in lego_colors.items():
        dist = new_func(pixel, rgb)
        if dist < min_dist:
            min_dist = dist
            closest_color = rgb  # Store the RGB value, not the name
    return closest_color

def new_func(pixel, rgb):
    dist = get_rgb_distance(pixel, rgb)
    return dist

# Function to convert an image array to LEGO-style blocks
def get_lego_array(pixel_arr, block_size=1):
    h, w, _ = pixel_arr.shape
    lego_arr = np.zeros((h, w, 3), dtype=np.uint8)

    # Process image in block chunks
    for row in range(0, h, block_size):
        for col in range(0, w, block_size):
            block = pixel_arr[row:row+block_size, col:col+block_size]

            # Get the average color of the block
            avg_color = np.mean(block, axis=(0, 1))

            # Find the closest LEGO color
            lego_color = get_closest_lego_pixel(avg_color)

            # Fill the block with the LEGO color
            lego_arr[row:row+block_size, col:col+block_size] = lego_color

    return lego_arr

# Main procedure
if __name__ == "__main__":
    file_path = "building.jpg"  # Replace with your image file
    img = load_image(file_path)

    # Scale the image down to simplify it before LEGO processing
    small_img = scale_img_down(img, dimensions=(400, 500))  #How to create Mosaic Effect

    # Convert image to numpy array
    small_img_array = convert_img_to_array(small_img)

    # Convert the pixel array to LEGO-style block colors
    lego_array = get_lego_array(small_img_array, block_size=1)  # Bigger blocks for a stronger mosaic effect

    # Convert back to PIL image
    lego_img = convert_array_to_img(lego_array)

    # Scale the LEGO image back up to original size
    lego_img_rescaled = scale_img_up(lego_img, dimensions=img.size)

    # Display the LEGO mosaic
    lego_img_rescaled.show()