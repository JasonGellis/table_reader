import os
import cv2

def read_images(input_dir):
    """
    Read one or multiple images from an input directory.

    Parameters:
        input_dir (str): Path to the input directory containing images.

    Returns:
        images (list): List of images read from the input directory.
    """
    # Initialize an empty list to store images
    images = []

    # Check if the input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return images

    # Get a list of files in the input directory
    files = os.listdir(input_dir)

    # Iterate over each file in the input directory
    for file in files:
        # Check if the file is an image (ending with .jpg, .png, etc.)
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            # Construct the full path to the image file
            image_path = os.path.join(input_dir, file)

            # Read the image using OpenCV
            image = cv2.imread(image_path)

            # Check if the image was read successfully
            if image is not None:
                images.append(image)
            else:
                print(f"Warning: Unable to read image '{file}'.")

    return images

def convert_to_grayscale(images):
    """
    Convert list of imported images to grayscale.

    Parameters:
        images (list): List of input images.

    Returns:
        grayscale_images (list): List of grayscale images.
    """
    # Initialize an empty list to store grayscale images
    grayscale_images = []

    # Iterate over each image in the input list
    for image in images:
        # Convert the image to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
        min_intensity = grayscale_image.min()
        max_intensity = grayscale_image.max()

        # Normalize the image to stretch contrast
        normalized_image = cv2.normalize(grayscale_image, None, 0, 255, cv2.NORM_MINMAX)

        normalized_images.append(normalized_image)

    return normalized_images

import pytesseract

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

import pandas as pd

def create_dataframe(padded_data):
    """
    Create a DataFrame from the padded data structure.

    Parameters:
        padded_data (list): Data structure with padded rows.

    Returns:
        df (DataFrame): DataFrame created from the padded data structure.
    """
    # Create DataFrame from the padded data structure
    df = pd.DataFrame(padded_data)

    return df

