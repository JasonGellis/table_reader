import os
import pytesseract
from PIL import Image
import pandas as pd
from flask import Flask

app = Flask(__name__)

@app.route("/")

def index():

    return "Congratulations, it's a web app!"

# Function to extract data from images and create DataFrame
def table_reader(input_dir, output_dir, output_file_name=None):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # List all files in the input directory
    image_files = [f for f in os.listdir(input_dir) if f.endswith('.png') or f.endswith('.jpg')]
    
    for image_file in image_files:
        # Load image using PIL
        img_path = os.path.join(input_dir, image_file)
        img = Image.open(img_path)
        
        # Use Tesseract OCR to extract text from the image
        extracted_text = pytesseract.image_to_string(img)
        
        # Preprocess the extracted text (split into rows and columns)
        rows = extracted_text.strip().split('\n')
        data = [row.split() for row in rows]
        
        # Convert the extracted data into a DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # Save DataFrame to output directory with optional custom file name
        if output_file_name is not None:
            output_file = os.path.join(output_dir, f"{output_file_name}_{os.path.splitext(image_file)[0]}.csv")
        else:
            output_file = os.path.join(output_dir, f"{os.path.splitext(image_file)[0]}.csv")
            
        df.to_csv(output_file, index=False)
        
        print(f"DataFrame saved to {output_file}")

# Example usage
# input_directory = "data_input"
# output_directory = "data_output"
# output_file_name = "extracted_data"

# extract_data_from_images(input_directory, output_directory, output_file_name)
