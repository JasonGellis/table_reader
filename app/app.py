from utils import read_images, convert_to_grayscale, normalize_images, perform_ocr, process_text,pad_columns, create_dataframe


def main():
    # Main function to orchestrate the application
    read_images()
    convert_to_grayscale()
    normalize_images()
    perform_ocr()
    process_text()
    pad_columns()
    create_dataframe()

    
# Entry point
if __name__ == "__main__":
    main()