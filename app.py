"""
Table Reader - A command-line tool for processing tables from images and
outputting data frames. This script defines the CLI interface, processes images,
and applies OCR with custom options like whitelist, blacklist, and character corrections.
"""

import argparse
import os
import logging
import cv2
from cli.read_and_process import (
    convert_to_grayscale,
    normalize_images,
    perform_ocr,
    process_text,
    pad_columns,
    remove_special_characters,
    create_dataframe,
    save_dataframe_to_directory,
    correct_common_ocr_mistakes
)
import config

def setup_logging():
    """
    Set up logging configuration to output logs to the console.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def parse_arguments():
    """
    Parse command-line arguments for Table Reader, providing options
    for input/output directories, whitelist, blacklist, and character corrections.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Table Reader: A command-line tool for processing tables "
            "from images and outputting data frames."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Input and output directories
    parser.add_argument(
        "-i", "--input-dir",
        help="Path to the input directory containing images to process.",
        default=None,
        required=False
    )

    parser.add_argument(
        "-o", "--output-dir",
        help="Path to the output directory where processed data frames will be saved as CSV files.",
        default=None,
        required=False
    )

    # Whitelist and blacklist arguments
    parser.add_argument(
        "-w", "--whitelist",
        help=(
            'Restrict the OCR output to only include certain characters. '
            'For example, to only allow numeric characters and common punctuation: '
            '"0123456789.,".'
        ),
        default="",
    )

    parser.add_argument(
        "-b", "--blacklist",
        help=(
            'Remove specific characters from the OCR output. For example, to remove '
            'common punctuation marks like commas and periods: ",."'
        ),
        default="",
    )

    # Custom character corrections argument
    parser.add_argument(
        "-c", "--char-corrections",
        help="Custom character corrections in the format: wrong:correct, e.g., 'S1:51,S2:52'.",
        default="",
    )

    # Argument to show default corrections
    parser.add_argument(
        "-d", "--show-default-corrections",
        action="store_true",
        help="Show the default character corrections used by Table Reader."
    )

    args = parser.parse_args()

    # Conditionally require input-dir and output-dir unless showing default corrections
    if not args.show_default_corrections:
        if args.input_dir is None:
            parser.error("--input-dir is required unless --show-default-corrections is specified.")
        if args.output_dir is None:
            parser.error("--output-dir is required unless --show-default-corrections is specified.")

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

def show_default_corrections():
    """
    Display the default corrections used by the Table Reader.
    """
    default_corrections = {
        ',': ',',  # Ensure decimal comma is preserved
        '--': '—',  # Convert double hyphen to em dash
        '-': '-',  # Ensure standard hyphen is preserved
        '1o': '10', '2o': '20', '3o': '30', '4o': '40', '5o': '50',
        '6o': '60', '7o': '70', '8o': '80', '9o': '90', '0o': '00',
        'S1': '51', 'S2': '52', 'S3': '53', 'S4': '54', 'S5': '55',
        'S6': '56', 'S7': '57', 'S8': '58', 'S9': '59', 'S0': '50',
        '·': '.',  # Ensure mid-dot conversion to decimal
        '–': '—',  # Ensure en dash is preserved or converted to em dash
    }

    print("By default, Table Reader includes these OCR Corrections:")
    for wrong, correct in default_corrections.items():
        print(f"  '{wrong}' -> '{correct}'")
    print(
        "You can provide your own custom character corrections to Table Reader "
        "using the --char-corrections flag in the format: wrong:correct."
    )

def main():
    """
    Main function to process images and output data frames.
    It handles image preprocessing, OCR, and saving the final CSV output.
    """
    setup_logging()
    args = parse_arguments()

    # If the user requests to show default corrections, display them and exit
    if args.show_default_corrections:
        show_default_corrections()
        return

    # Parse custom character corrections
    custom_corrections = parse_char_corrections(args.char_corrections)

    # Set input and output directories in the config module
    config.set_input_directory(args.input_dir)
    config.set_output_directory(args.output_dir)

    # Check if input directory exists
    if not os.path.exists(args.input_dir):
        logging.error("Input directory %s does not exist.", args.input_dir)
        return

    # Read all valid images from the input directory
    image_files = [
        f for f in os.listdir(args.input_dir)
        if f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'))
    ]

    if not image_files:
        logging.warning("No valid image files found in the input directory: %s", args.input_dir)
        return

    # Process each image separately
    for image_file in image_files:
        image_path = os.path.join(args.input_dir, image_file)
        logging.info("Processing image: %s", image_path)

        try:
            # Read the image using OpenCV
            image = cv2.imread(image_path)
            if image is None:
                logging.warning("Unable to read image: %s", image_path)
                continue

            # Image preprocessing and OCR pipeline
            grayscale_image = convert_to_grayscale([image])[0]
            normalized_image = normalize_images([grayscale_image])[0]
            extracted_text = perform_ocr([normalized_image])[0]

            # Apply user-defined whitelist, blacklist, and corrections
            corrected_text = correct_common_ocr_mistakes(extracted_text, custom_corrections)
            processed_text = process_text([corrected_text])
            padded_columns = pad_columns(processed_text)
            clean_data = remove_special_characters(
                padded_columns,
                whitelist=args.whitelist,
                blacklist=args.blacklist
            )
            df = create_dataframe(clean_data)

            # Save DataFrame to output directory with a unique filename
            output_filename = f"{os.path.splitext(image_file)[0]}_output.csv"
            save_dataframe_to_directory(df, args.output_dir, output_filename)
            logging.info("Successfully saved processed data to %s", output_filename)

        except Exception as e:
            logging.error("Error processing image %s: %s", image_file, str(e))

if __name__ == "__main__":
    main()
