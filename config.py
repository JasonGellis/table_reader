""" Set up input and output directories for CLI. """

# config.py

import os

# Default input and output directories
DEFAULT_INPUT_DIR = os.path.join(os.path.dirname(__file__), "input")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Initialize global variables
INPUT_DIR = DEFAULT_INPUT_DIR
OUTPUT_DIR = DEFAULT_OUTPUT_DIR

# Function to set input directory
def set_input_directory(input_dir):
    """
    Set the input directory.

    Parameters:
        input_dir (str): The path to the input directory.

    Returns:
        None
    """
    global INPUT_DIR
    INPUT_DIR = input_dir

# Function to set output directory
def set_output_directory(output_dir):
    """
    Set the output directory.

    Parameters:
        output_dir (str): The path to the output directory.

    Returns:
        None
    """
    global OUTPUT_DIR
    OUTPUT_DIR = output_dir
