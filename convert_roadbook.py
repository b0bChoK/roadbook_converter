#! python3
import os
from turtle import right
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
    try:
        os.makedirs(page_dir)
    except OSError as error:
        pass
    try:
        os.makedirs(case_dir)
    except OSError as error:
        pass

    left_margin = 34
    right_margin = 1654 - 1608
    left_column_width = 790 - 34
    # right_column_left_border = 852 
    right_column_width = 1654 - 852
    top_margin = 238
    bottom_margin = 2130
    case_per_column = 8
    case_height = (bottom_margin - top_margin) / case_per_column

    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('output/page'+ str(i) +'.jpg', 'JPEG')
        print(images[i].size)

        # crop case 1
        case1 = images[i].crop((left_margin, top_margin, left_margin + left_column_width, top_margin + case_height))
        case1.save('output/case'+ str(i) +'.jpg', 'JPEG')


if __name__ == "__main__":
    main()