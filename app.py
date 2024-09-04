""" Module for table reader main function and argparse"""

import argparse
import os
import cv2
from cli.read_and_process import convert_to_grayscale, \
    normalize_images, perform_ocr, process_text, pad_columns, \
    remove_special_characters, create_dataframe, save_dataframe_to_directory

import config

def parse_arguments():
    """
    Parse command-line arguments for the Table Reader application.

    This function sets up and parses the command-line arguments required
    for the application to run. It requires the user to specify the input
    directory containing images to process and the output directory where
    the results will be saved.

    Returns:
        argparse.Namespace: Parsed command-line arguments with input and output directories.
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

    args = parser.parse_args()
    return args

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

    args = parse_arguments()

    # Set input and output directories in config module
    config.set_input_directory(args.input_dir)
    config.set_output_directory(args.output_dir)

    # Read all images from the input directory
    image_files = [f for f in os.listdir(args.input_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'))]

    # Process each image separately
    for image_file in image_files:
        image_path = os.path.join(args.input_dir, image_file)

        # Read the image directly using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Unable to read image {image_path}")
            continue

        grayscale_image = convert_to_grayscale([image])[0]  # Process single image in list format
        normalized_image = normalize_images([grayscale_image])[0]
        extracted_text = perform_ocr([normalized_image])[0]
        processed_text = process_text([extracted_text])
        padded_columns = pad_columns(processed_text)
        clean_data = remove_special_characters(padded_columns)
        df = create_dataframe(clean_data)

        # Save DataFrame to output directory with a unique filename
        output_filename = f"{os.path.splitext(image_file)[0]}_output.csv"
        save_dataframe_to_directory(df, args.output_dir, output_filename)

if __name__ == "__main__":
    main()
