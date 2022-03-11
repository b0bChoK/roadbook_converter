#! python3
import os
from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

# Leave to None if installed on the OS or specify the bin directory
POPPLER_PATH = "poppler-22.01.0/Library/bin"

def main():
    print("Convert pdf")

    images = convert_from_path('pdf/test.pdf', poppler_path = POPPLER_PATH)

    page_dir = "output/pages"
    case_dir = "output/cases"
    os.makedirs(page_dir)
    os.makedirs(case_dir)

    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('output/page'+ str(i) +'.jpg', 'JPEG')

if __name__ == "__main__":
    main()