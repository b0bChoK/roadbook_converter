#! python3
from ast import arg
import os
import argparse
import configparser

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
    parser = argparse.ArgumentParser(description='Convert FFM pdf roadbook to image, 1 image per case.')
    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help='files to convert')
    parser.add_argument('-o', '--outdir', type=str, help='output directory where image will be stored')
    parser.add_argument('-c', '--conf', type=str, default="page_config.toml", help='page configuration')

    args = parser.parse_args()

    outdir = args.outdir

    config = configparser.ConfigParser()
    config.readfp(open(args.conf))

    page_width = config['DEFAULT']['page_width']
    # page_width = 1654
    left_margin = config['DEFAULT']['left_margin']
    # left_margin = 34
    right_margin = config['DEFAULT']['right_margin']
    # right_margin = page_width - 1608
    left_column_width = config['DEFAULT']['left_column_width']
    # left_column_width = 790 - 34
    # # right_column_left_border = 852 
    right_column_width = config['DEFAULT']['right_column_width']
    # right_column_width = page_width - 852
    top_margin = config['DEFAULT']['top_margin']
    # top_margin = 238
    bottom_margin = config['DEFAULT']['bottom_margin']
    # bottom_margin = 2130
    case_per_column = config['DEFAULT']['case_per_column']
    # case_per_column = 8
    case_height = int((bottom_margin - top_margin) / case_per_column)

    for file in args.files:
        print("Convert pdf", file)
        images = convert_from_path(file, poppler_path = POPPLER_PATH)

        case_dir = os.path.join(outdir, os.path.basename(file).split('.')[0])
        try:
            os.makedirs(case_dir)
        except OSError as error:
            pass
        
        cpt = 1
        for i in range(len(images)):
            # Save pages as images in the pdf
            #images[i].save(os.path.join(case_dir, str(i) +'.jpg'), 'JPEG')
            
            # crop left column
            for j in reversed(range(case_per_column)):
                param = (left_margin, top_margin + (case_height * j), left_margin + left_column_width, top_margin + (case_height * (j+1)))
                case = images[i].crop(param)
                case.save(os.path.join(case_dir, "case_" + str(cpt) +'.jpg'), 'JPEG')
                cpt+=1

            # crop right column
            for j in reversed(range(case_per_column)):
                case = images[i].crop((page_width - right_column_width, top_margin + (case_height * j), page_width - right_margin, top_margin + (case_height * (j+1))))
                case.save(os.path.join(case_dir, "case_" + str(cpt) +'.jpg'), 'JPEG')
                cpt+=1


if __name__ == "__main__":
    main()