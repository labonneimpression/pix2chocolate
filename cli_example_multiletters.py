import os
import os.path
import shutil
from xml.dom.minidom import parse
import sys
import fire

sys.path.append("cli/")
from pix2chocolate import pix2chocolate
from gmic import Gmic
G = Gmic()
DEFAULT_OUTPUT_DIR="generated"

def render_chocolate_biscuits_for_text(text="JOYEUX ANNIVERSAIRE",output_dir=DEFAULT_OUTPUT_DIR,gmic_command=""):
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
        if gmic_command:
            G.run("{} {} output {}".format(original_filename, gmic_command, final_gmic_filename))
            shutil.move(final_gmic_filename, os.path.join(output_dir, final_gmic_filename))
        shutil.move(original_filename, os.path.join(output_dir, final_filename))
        print("{} -> {}".format(letter, final_filename))
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
