#! python3
from ast import arg
import os
import argparse
import configparser
from typing import NamedTuple

from turtle import right
from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

# Leave to None if installed on the OS or specify the bin directory
POPPLER_PATH = "poppler-22.01.0/Library/bin"

class PageConfig(NamedTuple):
    case_go_up: bool
    case_per_column: int
    column_1l_border : int
    column_1r_border : int
    column_2l_border : int
    column_2r_border : int
    top_border : int
    bottom_border: int
    case_height: int

def load_margin_configuration(conf, image_size) -> PageConfig:
    config = configparser.ConfigParser()
    config.readfp(open(conf))

    width, height = image_size
    A4 = (21, 29.7)

    case_order_go_up = config['DEFAULT']['bottom_to_top'] == 'yes'
    use_cm = config['DEFAULT']['use_cm'] == 'yes'
    case_per_column = int(config['DEFAULT']['case_per_column'])

    if use_cm:
        left_margin = float(config['CM_A4']['left_margin'])
        right_margin = float(config['CM_A4']['right_margin'])
        left_column_width = float(config['CM_A4']['left_column_width'])
        right_column_width = float(config['CM_A4']['right_column_width'])
        top_margin = float(config['CM_A4']['top_margin'])
        bottom_margin = float(config['CM_A4']['bottom_margin'])

        column_1l_border = (left_margin / A4[0]) * width
        column_1r_border = ((left_margin + left_column_width) / A4[0]) * width
        column_2l_border = ((A4[0] - right_margin - right_column_width) / A4[0]) * width
        column_2r_border = ((A4[0] - right_margin) / A4[0]) * width
        top_border = (top_margin / A4[1]) * height
        bottom_border = ((A4[1] - bottom_margin) / A4[1]) * height
        case_height = (bottom_border - top_border) / case_per_column
    else:
        left_margin = int(config['PXL']['left_margin'])
        right_margin = int(config['PXL']['right_margin'])
        left_column_width = int(config['PXL']['left_column_width'])
        right_column_width = int(config['PXL']['right_column_width'])
        top_margin = int(config['PXL']['top_margin'])
        bottom_margin = int(config['PXL']['bottom_margin'])

        column_1l_border = left_margin
        column_1r_border = left_margin + left_column_width
        column_2l_border = width - right_margin - right_column_width
        column_2r_border = width - right_margin
        top_border = top_margin
        bottom_border = height - bottom_margin
        case_height = (bottom_border - top_border) / case_per_column

    return PageConfig(case_order_go_up,
                        case_per_column,
                        int(column_1l_border), int(column_1r_border),
                        int(column_2l_border), int(column_2r_border),
                        int(top_border), int(bottom_border),
                        int(case_height))

def main():
    parser = argparse.ArgumentParser(description='Convert FFM pdf roadbook to image, 1 image per case.')
    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help='files to convert')
    parser.add_argument('-o', '--outdir', type=str, default="", help='output directory where images will be stored')
    parser.add_argument('-c', '--conf', type=str, default="page_config.toml", help='page configuration')

    args = parser.parse_args()

    outdir = args.outdir  

    for file in args.files:
        print("Convert pdf", file)
        images = convert_from_path(file, poppler_path = POPPLER_PATH)

        rb_name = os.path.basename(file).split('.')[0]
        case_dir = os.path.join(outdir, rb_name)
        
        try:
            os.makedirs(case_dir)
        except OSError as error:
            pass
        
        page_config = load_margin_configuration(args.conf, images[0].size)

        # Save the first page as images in the pdf for illustration
        if len(images) > 0:
            images[0].save(os.path.join(case_dir, 'apage_0.jpg'), 'JPEG')

        # # crop left column
        # if page_config.case_go_up:
        #     case_range = reversed(range(page_config.case_per_column))
        # else:
        #     case_range = range(page_config.case_per_column)

        cpt = 1
        for i in range(len(images)):
            # crop left column
            if page_config.case_go_up:
                case_range = reversed(range(page_config.case_per_column))
            else:
                case_range = range(page_config.case_per_column)
            
            for j in case_range:
                param = (page_config.column_1l_border,
                        page_config.top_border + (page_config.case_height * j),
                        page_config.column_1r_border,
                        page_config.top_border + (page_config.case_height * (j+1)))
                case = images[i].crop(param)
                case.save(os.path.join(case_dir, '{:03d}'.format(cpt) + "_" + rb_name +'.jpg'), 'JPEG')
                cpt+=1

            # crop left column
            if page_config.case_go_up:
                case_range = reversed(range(page_config.case_per_column))
            else:
                case_range = range(page_config.case_per_column)
            # crop right column
            for j in case_range:
                param = (page_config.column_2l_border,
                        page_config.top_border + (page_config.case_height * j),
                        page_config.column_2r_border,
                        page_config.top_border + (page_config.case_height * (j+1)))
                case = images[i].crop(param)
                case.save(os.path.join(case_dir, '{:03d}'.format(cpt) + "_" + rb_name +'.jpg'), 'JPEG')
                cpt+=1

if __name__ == "__main__":
    main()