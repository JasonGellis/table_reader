from flask import Flask, render_template, request
import os
from shared_utils.read_and_process import read_images, convert_to_grayscale, normalize_images, perform_ocr, process_text, pad_columns, remove_special_characters, create_dataframe, save_dataframe_to_directory

app = Flask(__name__)

# Route to upload images and process them
@app.route('/', methods=['GET', 'POST'])
def upload_and_process():
    if request.method == 'POST':
        # Get the uploaded files
        uploaded_files = request.files.getlist('file')
        if uploaded_files:
            # Save the uploaded images to a temporary directory
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)
            for file in uploaded_files:
                file_path = os.path.join(upload_dir, file.filename)
                file.save(file_path)

            # Read the uploaded images
            images = read_images(upload_dir)

            # Convert images to grayscale
            grayscale_images = convert_to_grayscale(images)

            # Normalize grayscale images
            normalized_images = normalize_images(grayscale_images)

            # Perform OCR on normalized images
            extracted_text = perform_ocr(normalized_images)

            # Process extracted text
            processed_data = process_text(extracted_text)

            # Pad columns
            padded_data = pad_columns(processed_data)

            # Remove special characters
            cleaned_data = remove_special_characters(padded_data)

            # Create DataFrame
            df = create_dataframe(cleaned_data)

            # Save DataFrame to a directory
            output_dir = 'output'
            os.makedirs(output_dir, exist_ok=True)
            save_dataframe_to_directory(df, output_dir, 'output.csv')

            # Pass processed data to the template for display
            return render_template('result.html', data=df.to_html())

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
