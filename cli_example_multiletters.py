import os
import os.path
import shutil
from xml.dom.minidom import parse
import subprocess
import sys

import fire

sys.path.append("cli/")
from pix2chocolate import pix2chocolate
from gmic import Gmic
G = Gmic()
DEFAULT_OUTPUT_DIR="generated"

def render_chocolate_biscuits_for_text(text="JOYEUX ANNIVERSAIRE",output_dir=DEFAULT_OUTPUT_DIR,gmic_command="",vectorize=True):
    SVG_TO_EDIT = "singleLetterHeightmap.svg"
    TEMP_SVG = "tmp.svg"
    dom = parse(SVG_TO_EDIT)
    letter_id = 1
    for letter in text:
        print("letter:", letter)
        dom.getElementsByTagName("tspan")[0].firstChild.nodeValue = letter
        dom.writexml(open(TEMP_SVG, 'w+'))
        print("wrote", TEMP_SVG)
        pix2chocolate(PREVIEW_AFTER=False, OUTPUT_IMAGE_PREFIX="letters", DEFAULT_INPUT_IMAGE=TEMP_SVG, POST_RENDER_ROTATE=True)
        os.makedirs(output_dir, exist_ok=True)
        original_filename = "letters0001.png"
        final_filename = "letter" + str(letter_id).zfill(4) + ".png"
        final_gmic_filename = "letter_gmic" + str(letter_id).zfill(4) + ".png"
        final_vector_filename = "letter" + str(letter_id).zfill(4) + ".svg"
        if gmic_command:
            _gmic_command = "{} {} output {}".format(original_filename, gmic_command, final_gmic_filename)
            print("gmic pass -- {}".format(_gmic_command))
            G.run(_gmic_command)

        if vectorize:
            # imitating convert + potrace Gist at https://gist.github.com/ykarikos/2892009
            # mkbitmap -x -t 0.5 -f 3 letter0001.pnm -o mk.pbm; xdg-open mk.pbm ; potrace -s -o mk.svg mk.pbm ; xdg-open mk.svg
            # reference help: http://potrace.sourceforge.net/mkbitmap.html
            pnm_filename = final_vector_filename.replace(".svg", ".pnm")
            pbm_filename = final_vector_filename.replace(".svg", ".pbm")
            _gmic_command = "{} output {}".format(final_gmic_filename if gmic_command else original_filename, final_vector_filename.replace(".svg", ".pnm"))
            print("gmic png->pnm pass -- {}".format(_gmic_command))
            G.run(_gmic_command)

            _mkbitmap_command = "mkbitmap -x -t 0.5 -f 3 {} -o {}".format(pnm_filename, pbm_filename)
            print("mkbitmap pnm->pbm pass -- {}".format(_mkbitmap_command))
            exitcode, output = subprocess.getstatusoutput(_mkbitmap_command)

            potrace_command = "potrace -s -o {} {}".format(final_vector_filename, pbm_filename)
            print("potrace vectorization -- {}".format(potrace_command))
            exitcode, output = subprocess.getstatusoutput(potrace_command)
            shutil.move(pnm_filename, os.path.join(output_dir, pnm_filename))
            shutil.move(pbm_filename, os.path.join(output_dir, pbm_filename))
            shutil.move(final_vector_filename, os.path.join(output_dir, final_vector_filename))

        if os.path.exists(final_gmic_filename):
            shutil.move(final_gmic_filename, os.path.join(output_dir, final_gmic_filename))
        shutil.move(original_filename, os.path.join(output_dir, final_filename))
        print("{} -> {}".format(letter, os.path.join(output_dir, final_filename)))
        print("done pix2chocolate")
        letter_id += 1
        os.unlink(TEMP_SVG)

if __name__ == "__main__":
    print("""
           _       ______       _                      _                 
          (_)     (_____ \     | |                    | |      _         
     ____  _ _   _  ____) )____| | _   ___   ____ ___ | | ____| |_  ____ 
    |  _ \| ( \ / )/_____// ___) || \ / _ \ / ___) _ \| |/ _  |  _)/ _  )
    | | | | |) X ( ______( (___| | | | |_| ( (__| |_| | ( ( | | |_( (/ / 
    | ||_/|_(_/ \_|_______)____)_| |_|\___/ \____)___/|_|\_||_|\___)____)
    |_|                                                                  
    """)
    fire.Fire(render_chocolate_biscuits_for_text)
