# config.py

# Default input and output directories
INPUT_DIR = "/path/to/default_input_directory"
OUTPUT_DIR = "/path/to/default_output_directory"

# Function to set input directory
def set_input_directory(input_dir):
    """
    Set the input directory for the application.

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
    Set the output directory for the application.

    Parameters:
        output_dir (str): The path to the output directory.

    Returns:
        None
    """
    global OUTPUT_DIR
    OUTPUT_DIR = output_dir
