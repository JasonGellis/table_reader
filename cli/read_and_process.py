""" functions for importing and processing images. """
import re
import os
import cv2
import pandas as pd
import pytesseract


def read_images(input_dir):
    """
    Import images from a directory.

    Parameters:
        input_dir (str): Path to the directory containing images.

    Returns:
        images (list): List of imported images.
    """
    images = []
    # Iterate over files in the directory
    for filename in os.listdir(input_dir):
        # Check if the file is an image
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            # Read the image using OpenCV
            image_path = os.path.join(input_dir, filename)
            image = cv2.imread(image_path)
            if image is not None:  # Check if the image was successfully loaded
                images.append(image)
            else:  # Raise an error if the image failed to load
                raise ValueError(f"Failed to load image: {image_path}")
    return images


def convert_to_grayscale(images):
    """
    Convert imported image or list of imported images to grayscale.

    Parameters:
        images (numpy.ndarray or list): Input image or list of input images.

    Returns:
        grayscale_images (list): List of grayscale images.
    """
    if isinstance(images, list):  # Check if images is a list
        grayscale_images = []  # Initialize an empty list to store grayscale images
        for image in images:
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
            grayscale_images.append(grayscale_image)

    return grayscale_images

def normalize_images(grayscale_images):
    """
    Normalize a list of grayscale images to stretch contrast.

    Parameters:
        grayscale_images (list): List of grayscale images.

    Returns:
        normalized_images (list): List of normalized images.
    """
    # Initialize an empty list to store normalized images
    normalized_images = []

    # Iterate over each grayscale image in the input list
    for grayscale_image in grayscale_images:
        # Calculate the minimum and maximum intensity values of the image
        min_intensity = min(grayscale_image.ravel())
        max_intensity = max(grayscale_image.ravel())

        # Normalize the image to stretch contrast
        normalized_image = cv2.normalize(grayscale_image,
                                         None,
                                         min_intensity,
                                         max_intensity,
                                         cv2.NORM_MINMAX)

        normalized_images.append(normalized_image)

    return normalized_images


def perform_ocr(normalized_images):
    """
    Perform OCR (optical character recognition) on a list of images.

    Parameters:
        images (list): List of input images.

    Returns:
        extracted_text (list): List of extracted text from each image.
    """
    # Initialize an empty list to store extracted text
    extracted_text = []

    # Iterate over each image in the input list
    for normal_image in normalized_images:
        # Perform OCR on the image
        text = pytesseract.image_to_string(normal_image, lang = 'eng')
        extracted_text.append(text)

    return extracted_text

def process_text(extracted_text):
    """
    Create a data structure using extracted text from images.

    Parameters:
        extracted_text (list): List of extracted text from images.

    Returns:
        data (list): Processed data structure.
    """
    # Initialize an empty list to store processed data
    processed_data = []

    # Iterate over each extracted text
    for text in extracted_text:
        # Split the text into lines
        lines = text.strip().split('\n')

        # Split each line into words
        words = [line.split() for line in lines]

        # Append the processed data to the main list
        processed_data.append(words)

    return processed_data

def pad_columns(processed_data):
    """
    Pad rows with fewer columns to match the maximum number of columns in the data.

    Parameters:
        data (list): Processed data structure.

    Returns:
        padded_data (list): Data structure with padded rows.
    """
    # Find the maximum number of columns in the data
    max_columns = max(len(row) for row in processed_data)

    # Pad rows with fewer columns
    padded_data = [row + [''] * (max_columns - len(row)) for row in processed_data]

    return padded_data

def remove_special_characters(data, exceptions=['.', '-']):
    """
    Remove specified characters from a dataset, excluding decimal values and English letters.

    Parameters:
        data (list or DataFrame): Dataset to process.
        exceptions (list): List of characters to exempt from
        removal (default is ['.'] for decimal values).

    Returns:
        cleaned_data (list or DataFrame): Dataset with specified characters removed.
    """
    if isinstance(data, list):
        # If data is a list, process each element
        cleaned_data = [remove_special_characters(element, exceptions) for element in data]
    elif hasattr(data, 'applymap'):
        # If data is a DataFrame, process each cell
        cleaned_data = data.applymap(lambda x: remove_special_characters(x, exceptions))
    elif isinstance(data, str):
        # If data is a string, remove specified characters
        exceptions_regex = ''.join([re.escape(char) for char in exceptions])
        pattern = f'[^0-9{exceptions_regex}a-zA-Z]'
        cleaned_data = re.sub(pattern, '', data)
    else:
        # For other data types, return as is
        cleaned_data = data

    return cleaned_data


def create_dataframe(cleaned_data):
    """
    Create a DataFrame from the padded data structure.

    Parameters:
        padded_data (list): Data structure with padded rows.

    Returns:
        df (DataFrame): DataFrame created from the padded data structure.
    """

    # Flatten each sublist within padded_data and create a flat list
    flattened_data = [item for sublist in cleaned_data for item in sublist]

    # Create DataFrame from the flattened data
    df = pd.DataFrame(flattened_data, dtype='object')

    # Ensure that each value is in its own cell
    df = df.map(lambda x: x[0] if isinstance(x, list) else x)
    return df


def save_dataframe_to_directory(dataframe, output_dir, file_name):
    """
    Save a DataFrame to a file in a specified directory.

    Parameters:
        dataframe (pandas.DataFrame): The DataFrame to be saved.
        directory (str): Path to the directory where the DataFrame will be saved.
        file_name (str): Name of the file (including extension) to save the DataFrame.
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct the file path
    file_path = os.path.join(output_dir, file_name)

    # Save DataFrame to file
    dataframe.to_csv(file_path, index=False)
