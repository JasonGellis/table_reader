import argparse

from read_and_process import read_images, convert_to_grayscale, \
    normalize_images, perform_ocr, process_text, pad_columns, \
        remove_special_characters, create_dataframe, save_dataframe_to_directory

from ..configs import config

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Process tables and output data frames")
    parser.add_argument("-i", "--input-dir",
                        help="Path to input directory",
                        default=config.DEFAULT_INPUT_DIR,
                        required=True)
    parser.add_argument("-o", "--output-dir",
                        help="Path to output directory",
                        default=config.DEFAULT_OUTPUT_DIR,
                        required=True)
    args = parser.parse_args()
    return args

def main():

    """
    Process images and text files according to specified input and output directories.

    Parses command-line arguments to set input and output directories. Then, reads images
    from the input directory, converts them to grayscale, normalizes them, performs OCR
    to extract text, processes the extracted text, pads columns, removes special characters,
    creates a DataFrame, and finally saves the DataFrame to the output directory as 'output.csv'.

    Args:
        None (Uses command-line arguments for input and output directories)

    Returns:
        None
    """

    args = parse_arguments()

    # Set input and output directories in config module
    config.set_input_directory(args.input_dir)
    config.set_output_directory(args.output_dir)

    # functions from read_and_process
    images = read_images(args.input_dir)
    grayscale_images = convert_to_grayscale(images)
    normalized_images = normalize_images(grayscale_images)
    extracted_text = perform_ocr(normalized_images)
    processed_text = process_text(extracted_text)
    padded_columns = pad_columns(processed_text)
    clean_data = remove_special_characters(padded_columns)
    df = create_dataframe(clean_data)
    save_dataframe_to_directory(df, args.output_dir, 'output.csv')

    # You can access the directories from other modules using config.INPUT_DIR and config.OUTPUT_DIR

if __name__ == "__main__":
    main()
