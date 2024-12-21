import numpy as np
from PIL import Image

# function to load an image from a file path
def load_image(file_path):
    img = Image.open(file_path)
    return img

# function to resize an image DOWN to (num_pixels x num_pixels) pixels
def scale_img_down(img, dimensions):
    resized_img = img.resize(dimensions, resample=Image.Resampling.BILINEAR)
    return resized_img

# function to resize an image UP to (num_pixels x num_pixels) pixels
def scale_img_up(img, dimensions):
    resized_img = img.resize(dimensions, resample=Image.Resampling.NEAREST)
    return resized_img

# function to convert a PIL image to a numpy array
def convert_img_to_array(img):
    arr = np.array(img)
    return arr

# function to convert a numpy array to a PIL image
def convert_array_to_img(arr):
    img = Image.fromarray(arr.astype("uint8"), "RGB")
    return img

# dictionary with LEGO tile colors and RGB values
lego_colors = {
    "blue": (70,158,209),
    "black": (47,47,47), 
    "brown": (130,94,65), 
    "grey": (124,124,124), 
    "peach": (247,188,153),  
    "white": (245, 245, 242),
    "red": (222, 20, 20)
}

# function to calculate the (Euclidian) distance between two RGB tuples
def get_rgb_distance(rgb1, rgb2):
    # Calculate squared differences for each channel
    r_diff = (rgb1[0] - rgb2[0])**2
    g_diff = (rgb1[1] - rgb2[1])**2
    b_diff = (rgb1[2] - rgb2[2])**2

    # Calculate and return euclidean distance
    return np.sqrt(r_diff + g_diff + b_diff)

# function to get the LEGO tile with the smallest Euclidian distance from a given pixel
def get_closest_lego_pixel(pixel):
    # Find the minimum distance and corresponding LEGO color
    min_dist = np.inf
    closest_color = None
    for color, rgb in lego_colors.items():
        dist = get_rgb_distance(pixel, rgb)
        if dist < min_dist:
            min_dist = dist
            closest_color = color

    # Return the closest LEGO color
    return closest_color

# function to convert an array of pixels to an array of LEGO tiles with the closest RGB values
def get_lego_array(pixel_arr):
    # Initialize empty array for LEGO tiles
    lego_arr = np.empty_like(pixel_arr)

    # Loop through each pixel and find the closest LEGO color
    for row in range(pixel_arr.shape[0]):
        for col in range(pixel_arr.shape[1]):
            pixel = pixel_arr[row, col]
            lego_pixel = get_closest_lego_pixel(pixel)
            lego_arr[row, col] = lego_colors[lego_pixel]

    return lego_arr

# main procedure
if __name__ == "__main__":

    # load the image
    file_path = "goatjo.jpg"
    img = load_image(file_path=file_path)

    # scale the image down
    small_img = scale_img_down(img, dimensions=(800,1000))

    # convert image to numpy array
    small_img_array = convert_img_to_array(small_img)

    # get the array of LEGO RGB pixels
    lego_array = get_lego_array(small_img_array)

    # convert to PIL image
    lego_img = convert_array_to_img(lego_array)

    # scale the lego image back up to the original img dimensions
    lego_img_rescaled = scale_img_up(lego_img, dimensions=img.size)

    # view the LEGO
    lego_img_rescaled.show()