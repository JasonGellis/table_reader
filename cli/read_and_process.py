"""
Functions for importing and processing images.
"""
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
    for filename in os.listdir(input_dir):
        # Check if the file is an image
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            image_path = os.path.join(input_dir, filename)
            image = cv2.imread(image_path)
            if image is not None:  # Check if the image was successfully loaded
                images.append(image)
            else:
                raise ValueError(f"Failed to load image: {image_path}")
    return images


def convert_to_grayscale(images):
    """
    Convert imported images to grayscale.

    Parameters:
        images (list or numpy.ndarray): Input images or list of images.

    Returns:
        grayscale_images (list): List of grayscale images.
    """
    if isinstance(images, list):
        grayscale_images = []
        for image in images:
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
    normalized_images = []
    for grayscale_image in grayscale_images:
        min_intensity = min(grayscale_image.ravel())
        max_intensity = max(grayscale_image.ravel())
        normalized_image = cv2.normalize(grayscale_image, None, min_intensity, max_intensity, cv2.NORM_MINMAX)
        normalized_images.append(normalized_image)

    return normalized_images


def perform_ocr(normalized_images):
    """
    Perform OCR (optical character recognition) on a list of images with enhanced
    handling for special characters and table structures.

    Parameters:
        normalized_images (list): List of input images.

    Returns:
        extracted_text (list): List of extracted text from each image.
    """
    extracted_text = []
    custom_config = (
        r'--oem 3 --psm 6 '  # Use LSTM OCR Engine and assume a block of text
        r'-c preserve_interword_spaces=1'  # Preserve spacing between words
    )

    for normal_image in normalized_images:
        text = pytesseract.image_to_string(normal_image, config=custom_config, lang='eng')
        corrected_text = correct_common_ocr_mistakes(text)
        extracted_text.append(corrected_text)

    return extracted_text


def correct_common_ocr_mistakes(text, custom_corrections=None):
    """
    Correct common OCR mistakes related to special characters, superscripts, and subscripts.

    Parameters:
        text (str): Text output from OCR.
        custom_corrections (dict): User-specified corrections for specific character combinations.

    Returns:
        corrected_text (str): Text with common OCR mistakes corrected.
    """
    corrections = {
        ',': ',',  # Ensure decimal comma is preserved
        '--': '—',  # Convert double hyphen to em dash
        '-': '-',  # Ensure standard hyphen is preserved
        '1o': '10', '2o': '20', '3o': '30', '4o': '40', '5o': '50',
        '6o': '60', '7o': '70', '8o': '80', '9o': '90', '0o': '00',
        'S1': '51', 'S2': '52', 'S3': '53', 'S4': '54', 'S5': '55',
        'S6': '56', 'S7': '57', 'S8': '58', 'S9': '59', 'S0': '50',
        '·': '.',  # Convert mid-dot to decimal point
        '–': '—',  # Ensure en dash is preserved or converted to em dash
    }

    if custom_corrections:
        corrections.update(custom_corrections)

    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)

    return text


def process_text(extracted_text):
    """
    Create a data structure using extracted text from images.

    Parameters:
        extracted_text (list): List of extracted text from images.

    Returns:
        data (list): Processed data structure.
    """
    processed_data = []
    for text in extracted_text:
        lines = text.strip().split('\n')
        words = [line.split() for line in lines]
        processed_data.append(words)

    return processed_data


def pad_columns(processed_data):
    """
    Pad rows with fewer columns to match the maximum number of columns in the data.

    Parameters:
        processed_data (list): Processed data structure.

    Returns:
        padded_data (list): Data structure with padded rows.
    """
    max_columns = max(len(row) for row in processed_data)
    padded_data = [row + [''] * (max_columns - len(row)) for row in processed_data]

    return padded_data


def remove_special_characters(data, whitelist=None, blacklist=None):
    """
    Remove or retain specified characters from a dataset based on the whitelist and blacklist.

    Parameters:
        data (list): Processed data structure (list of lists).
        whitelist (str): A string of characters to retain.
        blacklist (str): A string of characters to remove.

    Returns:
        cleaned_data (list): Data structure with specified characters removed or retained.
    """
    def process_string(text):
        if whitelist:
            text = ''.join([char for char in text if char in whitelist])
        if blacklist:
            text = ''.join([char for char in text if char not in blacklist])
        return text

    cleaned_data = []
    for row in data:
        cleaned_row = [process_string(element) for element in row]
        cleaned_data.append(cleaned_row)

    return cleaned_data


def create_dataframe(cleaned_data):
    """
    Create a DataFrame from the cleaned and padded data structure.

    Parameters:
        cleaned_data (list): Data structure with cleaned and padded rows.

    Returns:
        pd.DataFrame: DataFrame created from the data structure.
    """
    flattened_data = [item for sublist in cleaned_data for item in sublist]
    df = pd.DataFrame(flattened_data, dtype='object')
    df = df.map(lambda x: x[0] if isinstance(x, list) else x)
    return df


def save_dataframe_to_directory(dataframe, output_dir, file_name):
    """
    Save a DataFrame to a file in a specified directory.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to be saved.
        output_dir (str): Path to the directory where the DataFrame will be saved.
        file_name (str): Name of the file (including extension) to save the DataFrame.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, file_name)
    dataframe.to_csv(file_path, index=False)
