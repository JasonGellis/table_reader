import cv2
import pytesseract
import pandas as pd
import numpy as np

# Path to the image file
image_path = ""

# Read the image using OpenCV
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Define the minimum and maximum intensity values for stretching
min_intensity = 0
max_intensity = 255

# Calculate the minimum and maximum intensity values of the input image
min_val = np.min(gray_image)
max_val = np.max(gray_image)

# Normalize the image to stretch contrast
normalized_image = cv2.normalize(gray_image, None, min_intensity, max_intensity, cv2.NORM_MINMAX)

# Perform OCR using Tesseract
extracted_text = pytesseract.image_to_string(normalized_image, lang = 'eng')

# Preprocess the extracted text
lines = extracted_text.strip().split('\n')
data = [line.split() for line in lines]

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# remove unusual characters
# Remove « character from all columns and rows
df_cleaned = df.map(lambda x: x.replace('«', '').replace('°', '') if isinstance(x, str) else x)

ocr_message = '''
Please review the extracted table and manually verify its accuracy. 
Unusual characters may include symbols, special characters,
or unexpected text formatting that could not be accurately 
interpreted by the OCR engine.

If you continue to encounter issues or have concerns about the
accuracy of the extracted text, consider improving the image
quality to at least 300 dpi.
'''
# Display the DataFrame
print(f"{df_cleaned}\n{ocr_message}")
