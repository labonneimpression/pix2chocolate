#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
import logging
import glob

DEFAULT_INPUT_IMAGE = 'LaBonneImpressionLogoHeightmap.svg'
DEFAULT_DISPLACEMENT_TEXTURE_IMAGE = 'LaBonneImpressionLogoHeightmap.png' #todo more generic filename
DEFAULT_RENDERING_IMAGE = 'test0001.png'
OUTPUT_IMAGE_PREFIX = 'test'
PREVIEW_AFTER = True

def pix2chocolate(DEFAULT_INPUT_IMAGE=DEFAULT_INPUT_IMAGE, DEFAULT_DISPLACEMENT_TEXTURE_IMAGE=DEFAULT_DISPLACEMENT_TEXTURE_IMAGE, DEFAULT_RENDERING_IMAGE=DEFAULT_RENDERING_IMAGE, OUTPUT_IMAGE_PREFIX=OUTPUT_IMAGE_PREFIX, POST_RENDER_ROTATE=False, PREVIEW_AFTER=PREVIEW_AFTER):
    if shutil.which("convert"):
        print("convert...")
        command_to_run = 'convert -rotate "90>" -background "#000000" -density 900 {input_file} {output_file}'.format(input_file=DEFAULT_INPUT_IMAGE, output_file=DEFAULT_DISPLACEMENT_TEXTURE_IMAGE)
        print(command_to_run)
        exitcode, output = subprocess.getstatusoutput(command_to_run)
        logging.info(output)
    else:
        print('No prior use of ImageMagick''s convert: process not found in path.')
    
    if shutil.which("blender"):
        exitcode, output = subprocess.getstatusoutput(
            'blender -b micro_displacement_test.blend -x 1 -o {}#### -f 1'.format(OUTPUT_IMAGE_PREFIX))
        logging.info(output)
    else:
        print('FATAL ERROR: Blender not found!!!')
        sys.exit(1)

    last_file = sorted(glob.glob(OUTPUT_IMAGE_PREFIX + "*"))
    print(last_file)
    logging.info("rendered ", last_file)

    if POST_RENDER_ROTATE:
      command_to_run = 'convert -rotate "90>" {input_file} {output_file}'.format(input_file=last_file[0], output_file=last_file[0])
      exitcode, output = subprocess.getstatusoutput(command_to_run)
      logging.info(output)

    
    if PREVIEW_AFTER and shutil.which("xdg-open"):
        exitcode, output = subprocess.getstatusoutput('xdg-open ' + last_file)
        logging.info(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Picture to chocolate renderer')
    parser.add_argument('image', nargs='?', type=str, default=DEFAULT_INPUT_IMAGE,
                        help='image to render onto chocolate (default: %(default)s)')
    parser.add_argument('--verbose', '-v', action='count', default=1)
    
    args = parser.parse_args()
    args.verbose = 40 - (10*args.verbose) if args.verbose > 0 else 0
    logging.basicConfig(level=args.verbose, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    pix2chocolate(DEFAULT_INPUT_IMAGE=args.image)
