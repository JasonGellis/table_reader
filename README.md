# Table Reader

Table Reader is a Python command-line interface (CLI) application designed to extract data values from tables in research publications and field notes. Leveraging image processing and optical character recognition (OCR) techniques, Table Reader can efficiently extract tabular data from images, enabling researchers to digitize and analyze information from various sources.

- [Table Reader](#table-reader)
  - [Key Features](#key-features)
  - [Why Use Table Reader?](#why-use-table-reader)
  - [Table Reader Installation Guide](#table-reader-installation-guide)
  - [Table Reader Instruction Guide](#table-reader-instruction-guide)
    - [***Run the CLI tool***](#run-the-cli-tool)
    - [***Available Command-Line Options***](#available-command-line-options)
  - [How to get best results from images](#how-to-get-best-results-from-images)
  - [Future updates](#future-updates)



## Key Features

- Optical character recognition (OCR) Processing: Utilizing the powerful Tesseract OCR engine, Table Reader accurately extracts text from images, including tables and tabular data.
- Data Extraction: Table Reader processes images to identify and extract tabular data, preserving the structure of tables found in the input images.
- Data Cleaning: Table Reader includes functionality to clean and pre-process extracted data, removing special characters while preserving decimal values and English letters, and ensuring consistent formatting.
- Data import: Table Reader can process one or multiple images. Images can be in .jpg, .jpeg, .png, .bmp, .gif, or .tiff formats.
- Data Export: Once the data is extracted and cleaned, Table Reader enables users to export the data to a CSV file for further analysis in statistical software or spreadsheet applications.

## Why Use Table Reader?

- Efficiency: Table Reader streamlines the process of extracting tabular data from imported images, saving researchers valuable time compared to manual transcription.
- Accuracy: By leveraging OCR technology, Table Reader greatly improves accurate extraction of data values, reducing the risk of errors introduced during manual data entry.
- Versatility: Researchers across various fields, including science, engineering, and social sciences, can benefit from Table Reader's ability to digitize and analyze tabular data from diverse sources, such as research publications and field notes.
- Automation: With its command-line interface, Table Reader supports automation and integration into existing data processing pipelines, facilitating seamless data extraction and analysis workflows.

## Table Reader Installation Guide

1. **Clone the Repository:**

   ```git clone https://github.com/your_username/table_reader.git```

2. **Navigate to the directory:**

   ```cd table_reader```

3. **Install the package locally using pip:**

   ```pip install .```

4. **Additional installation requirements**
   Table Reader uses [Pytesseract](https://pypi.org/project/pytesseract/) which requires the installation of [Google's Tesseract-OCR Engine](https://tesseract-ocr.github.io/tessdoc/Installation.html) on the user's system.

## Table Reader Instruction Guide

### ***Run the CLI tool***
   - ***be sure to include input and output directories in the command line***

   ```tablereader --input-dir /path/to/input --output-dir /path/to/output```

### ***Available Command-Line Options***

**Whitelist Certain Characters**

Use the ```--whitelist``` flag to limit the characters that are allowed in the OCR output. Any character not in the whitelist will be removed.

*Example*: To only allow numeric characters and common punctuation (like periods and commas):

```tablereader --input-dir /path/to/input --output-dir /path/to/output --whitelist "0123456789.,"```

This will ensure that only the specified characters remain in the processed output.

**Blacklist Certain Characters**

Use the ```--blacklist``` flag to remove specific characters from the OCR output. Any character in the blacklist will be stripped from the processed text.

*Example*: To remove common punctuation (like commas and periods):

```tablereader --input-dir /path/to/input --output-dir /path/to/output --blacklist ",."```

This will remove the specified characters from the final output while leaving others intact.

**Custom Character Corrections**

The ```--char-corrections``` flag allows you to specify custom corrections to OCR misinterpretations. You can provide character corrections in the format wrong:correct, separating multiple corrections with commas.

*Example*: To correct instances where S1 is misread as 51 and A1 as 41:

```tablereader --input-dir /path/to/input --output-dir /path/to/output --char-corrections "S1:51,A1:41"```

This will apply your custom corrections during the OCR processing.

**Show Default Character Corrections**

Table Reader comes with a set of default OCR corrections for common misinterpretations. You can view these default corrections without running the full processing pipeline with ```tablereader --show-default-corrections```.

**Help**

To view all available options and their usage, run: ```tablereader --help```

This will display a list of all available flags and descriptions for using Table Reader.

**Combining Flags**

You can combine these flags to further customize how Table Reader processes your images.

*Example*: To apply custom corrections, restrict the output to numeric characters and remove commas:

```tablereader --input-dir /path/to/input --output-dir /path/to/output --char-corrections "S1:51" --whitelist "0123456789" --blacklist ","```

This command will apply custom corrections, limit the output to numbers, and remove commas from the final output.

**Summary of Key Features**

- Whitelist ```(-w --whitelist)```: Restrict OCR output to specific characters.
- Blacklist ```(-b --blacklist)```: Remove unwanted characters from the OCR output.
- Custom Character Corrections ```(-c --char-corrections)```: Override OCR mistakes with your own corrections.
- Show Default Corrections ```(-d --show-default-corrections)```: View the default OCR corrections used by Table Reader.

These features give you full control over how the OCR engine processes your images and handles text extraction, allowing for precise and customizable results.

## How to get best results from images

Images with the following characteristics typically produce the best OCR (Optical Character Recognition) results:

- High Resolution: Images with higher resolution (>= 300 dpi) capture finer details, leading to more accurate text recognition.

- Clear and Sharp Text: Text should be well-defined, free from blurriness, smudges, or distortion, ensuring accurate character recognition.

- High Contrast: Images with distinct contrast between text and background enhance character segmentation and improve OCR accuracy. Table Reader will calculate the minimum and maximum intensity values of the image to adjust contrast.

- Uniform Lighting: Consistent lighting across the image minimizes shadows and variations, aiding in better text extraction.

- Minimal Noise: Images with minimal noise, artifacts, or background clutter are easier for OCR algorithms to process. Table Reader will try to process images to remove noise and sharpen text.

- Correct Orientation: Images with properly aligned text, without skew or rotation, facilitate accurate character alignment and recognition.

- Straightforward Layout: Simple and well-organized layouts with clear text arrangement simplify character segmentation and extraction. Table Reader is built to read text from tables found in scientific publications (spreadsheet format).

Optimizing images to meet these criteria before OCR processing can significantly improve the accuracy and reliability of text recognition results.

## Future updates

- Support for special and non-English characters
