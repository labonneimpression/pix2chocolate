import os
import shutil
from xml.dom.minidom import parse
import sys

sys.path.append("cli/")
from pix2chocolate import pix2chocolate

TEXT = "JOYEUX ANNIVERSAIRE"
SVG_TO_EDIT = "singleLetterHeightmap.svg"
TEMP_SVG = "tmp.svg"

dom = parse(SVG_TO_EDIT)

letter_id = 1
for letter in TEXT:
    print("letter")
    dom.getElementsByTagName("tspan")[0].firstChild.nodeValue = letter
    dom.writexml(open(TEMP_SVG, 'w+'))
    print("wrote", TEMP_SVG)
    pix2chocolate(PREVIEW_AFTER=False, OUTPUT_IMAGE_PREFIX="letters", DEFAULT_INPUT_IMAGE=TEMP_SVG, POST_RENDER_ROTATE=True)
    final_filename = "generated/letter" + str(letter_id).zfill(4) + ".png"
    shutil.move("letters0001.png", final_filename)
    print("{} -> {}".format(letter, final_filename))
    print("done pix2chocolate")
    letter_id += 1
    os.unlink(TEMP_SVG)
