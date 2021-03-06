#!/usr/bin/env python3

import argparse
import logging
import os
import shutil
import subprocess
import sys
import uuid


DEFAULT_INPUT_IMAGE = 'LaBonneImpressionLogoHeightmap.svg'
DEFAULT_DISPLACEMENT_TEXTURE_IMAGE = 'LaBonneImpressionLogoHeightmap.png' #todo more generic filename
DEFAULT_RENDERING_IMAGE = 'test0001.png'

def render_chocolate(image, renders_directory='.', headless=True):
    logging.info(os.listdir('.'))
    if shutil.which("convert"):
        exitcode, output = subprocess.getstatusoutput('convert -rotate "90>" -background "#000000" -density 900 {input_file} {output_file}'.format(input_file=image, output_file=DEFAULT_DISPLACEMENT_TEXTURE_IMAGE))
        logging.info(output)
    else:
        print('No prior use of ImageMagick''s convert: process not found in path.')
    
    render_filename_prefix = str(uuid.uuid1())
    render_filename_full = '{}0001.png'.format(render_filename_prefix)
    render_file_path_prefix = os.path.join(renders_directory, render_filename_prefix)
    render_file_path_full = os.path.join(renders_directory, render_filename_full)

    if shutil.which("blender"):
        exitcode, output = subprocess.getstatusoutput(
            'blender -b micro_displacement_test.blend -x 1 -o {} -f 1'.format(render_file_path_prefix))
        logging.info(output)
    else:
        print('FATAL ERROR: Blender not found!!!')
        sys.exit(1)
    
    if not headless and shutil.which("xdg-open"):
        exitcode, output = subprocess.getstatusoutput('xdg-open ' + render_file_path_full)
        logging.info(output)

    return render_file_path_full

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Picture to chocolate renderer')
    parser.add_argument('image', nargs='?', type=str, default=DEFAULT_INPUT_IMAGE,
                        help='image to render onto chocolate (default: %(default)s)')
    parser.add_argument('--verbose', '-v', action='count', default=1)
    
    args = parser.parse_args()
    args.verbose = 40 - (10*args.verbose) if args.verbose > 0 else 0
    logging.basicConfig(level=args.verbose, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    render_chocolate(args.image, headless=False)
