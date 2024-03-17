# Table Reader

Table Reader is a Python command-line interface (CLI) application designed to extract data values from tables in research publications and field notes. Leveraging image processing and optical character recognition (OCR) techniques, Table Reader can efficiently extract tabular data from images, enabling researchers to digitize and analyze information from various sources.

## Key Features

- Optical character recognition (OCR) Processing: Utilizing the powerful Tesseract OCR engine, Table Reader accurately extracts text from images, including tables and tabular data.
- Data Extraction: Table Reader processes images to identify and extract tabular data, preserving the structure of tables found in the input images.
- Data Cleaning: Table Reader includes functionality to clean and pre-process extracted data, removing special characters while preserving decimal values and English letters, and ensuring consistent formatting.
- Data Export: Once the data is extracted and cleaned, Table Reader enables users to export the data to a structured format, such as CSV files, for further analysis in statistical software or spreadsheet applications.

## Why Use Table Reader?

- Efficiency: Table Reader streamlines the process of extracting tabular data from imported images, saving researchers valuable time compared to manual transcription.
- Accuracy: By leveraging OCR technology, Table Reader greatly improves accurate extraction of data values, reducing the risk of errors introduced during manual data entry.
- Versatility: Researchers across various fields, including science, engineering, and social sciences, can benefit from Table Reader's ability to digitize and analyze tabular data from diverse sources, such as research publications and field notes.
- Automation: With its command-line interface, Table Reader supports automation and integration into existing data processing pipelines, facilitating seamless data extraction and analysis workflows.

## Table Reader Installation Guide

### Python  and Conda Virtual Environments

1. **Clone the Repository:**

   ```git clone https://github.com/your_username/table_reader.git```

2. **Navigate to the directory:**

   ```cd table_reader```

3. **Create a Python/Conda virtual environment**

   Python: ```python3 -m venv table_reader``` \
   Conda: ```conda create --name table_reader python=3.12```

4. **Activate the virtual environment**
   - On macOS and Linux: \
     Python: ```source table_reader/bin/activate``` \
     Conda: ```conda activate table_reader```

   - On Windows: \
     Python: ```.\table_reader\Scripts\activate``` \
     Conda: ```conda activate table_reader```

5. **Install dependencies from requirements.txt**

   ```pip install -r requirements.txt```

6. **Run the application**
    - ***be sure to include input and output directories in the command line*** \


    ```python app.py -i /path/to/your/input_directory/ -o /path/to/your/output_directory/```

7. **Additional installation requirements**
   Table Reader uses [Pytesseract](https://pypi.org/project/pytesseract/) which requires the installation of [Google's Tesseract-OCR Engine](https://tesseract-ocr.github.io/tessdoc/Installation.html) on the user's system.

## Future updates

- Webapp interface
- Upload multiple images
- Ability to select/deselect image and OCR processing
- Support for special and non-English characters
- Ability to handle numbers with a "mid-dot" or "decimal comma" (e.g., writing 2.9 as 2·9).

## How to cite
