import argparse
from read_and_process import read_images, convert_to_grayscale, normalize_images, \
    perform_ocr, process_text,pad_columns, create_dataframe


if __name__ == '__main__':
    # read and process images
    images = read_images
    grayscale_images = convert_to_grayscale(images)
    normalized_images = normalize_images(grayscale_images)
    extracted_text = perform_ocr(normalized_images)
    processed_data = process_text(extracted_text)
    padded_data = pad_columns(processed_data)
    df = create_dataframe(padded_data)
  
    
    # main(args.input_dir, args.output_dir)