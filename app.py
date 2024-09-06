""" Module for Table Reader main function and argparse """

import argparse
import os
import logging
import cv2
from cli.read_and_process import convert_to_grayscale, \
    normalize_images, perform_ocr, process_text, pad_columns, \
    remove_special_characters, create_dataframe, save_dataframe_to_directory

import config

def setup_logging():
    """
    Set up logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,  # Change to DEBUG for more detailed output
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Log to console
        ]
    )

def parse_arguments():
    """
    Parse command-line arguments for the Table Reader application.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Table Reader: A command-line tool for processing tables "
            "from images and outputting data frames."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-i", "--input-dir",
        help="Path to the input directory containing images to process.",
        default=config.DEFAULT_INPUT_DIR,
        required=True
    )

    parser.add_argument(
        "-o", "--output-dir",
        help="Path to the output directory where processed data frames will be saved as CSV files.",
        default=config.DEFAULT_OUTPUT_DIR,
        required=True
    )

    # New arguments
    parser.add_argument(
        "-w", "--whitelist",
        help="Characters to whitelist (preserve) in OCR output.",
        default="",  # No whitelist by default
    )

    parser.add_argument(
        "-b", "--blacklist",
        help="Characters to remove from OCR output.",
        default="",  # No blacklist by default
    )

    parser.add_argument(
        "-c", "--char-corrections",
        help="Custom character corrections for misread letters, numbers, or combinations of - e.g., 'S1:51, S2:52'.",
        default="",  # No custom corrections by default
    )

    args = parser.parse_args()
    return args

def parse_char_corrections(correction_string):
    """
    Parse the custom character corrections from the user-provided string.

    Parameters:
        correction_string (str): String containing custom character corrections
                                 in the format 'S1:51,S2:52'.

    Returns:
        dict: A dictionary mapping incorrect characters to correct ones.
    """
    corrections = {}
    if correction_string:
        for pair in correction_string.split(','):
            if ':' in pair:
                key, value = pair.split(':', 1)
                corrections[key] = value
    return corrections

def main():
    """
    Process multiple images and save output data frames to CSV files.

    Parses command-line arguments to set input and output directories.
    Reads images from the input directory, processes each image, and
    saves the extracted data to separate CSV files in the output directory.

    Args:
        None (Uses command-line arguments for input and output directories)

    Returns:
        None
    """

    setup_logging()
    args = parse_arguments()

    # Set input and output directories in config module
    config.set_input_directory(args.input_dir)
    config.set_output_directory(args.output_dir)

    # Check if input directory exists
    if not os.path.exists(args.input_dir):
        logging.error("Input directory %s does not exist.", args.input_dir)
        return

    # Read all images from the input directory
    image_files = [f for f in os.listdir(args.input_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'))]

    if not image_files:
        logging.warning("No valid image files found in the input directory: %s", args.input_dir)
        return

    # Process each image separately
    for image_file in image_files:
        image_path = os.path.join(args.input_dir, image_file)
        logging.info("Processing image: %s", image_path)

        try:
            # Read the image directly using OpenCV
            image = cv2.imread(image_path)
            if image is None:
                logging.warning("Unable to read image: %s", image_path)
                continue

            # Image preprocessing and OCR pipeline
            grayscale_image = convert_to_grayscale([image])[0]
            normalized_image = normalize_images([grayscale_image])[0]
            extracted_text = perform_ocr([normalized_image])[0]
            processed_text = process_text([extracted_text])
            padded_columns = pad_columns(processed_text)
            clean_data = remove_special_characters(padded_columns)
            df = create_dataframe(clean_data)

            # Save DataFrame to output directory with a unique filename
            output_filename = f"{os.path.splitext(image_file)[0]}_output.csv"
            save_dataframe_to_directory(df, args.output_dir, output_filename)
            logging.info("Successfully saved processed data to %s", output_filename)

        except Exception as e:
            logging.error("Error processing image %s: %s", image_file, str(e))

if __name__ == "__main__":
    main()
