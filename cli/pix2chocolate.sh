#!/bin/sh


INPUTSVG=LaBonneImpressionLogoHeightmap.svg
OUTPUTPNG=LaBonneImpressionLogoHeightmap.png

# Use first parameter as SVG to use for texturing, if exists
[ "$#" -eq 1 ] && INPUTSVG="$1"


# Use ImageMagick's convert if exists, auto-rotate if width is larger than height
#command -v convert && time convert -rotate "90>" -background "#000000" -density 900 "$INPUTSVG" "$OUTPUTPNG"
inkscape "$INPUTSVG" -d 200 -C -b "#000000" -y 1.0 -o "$OUTPUTPNG"

# Run blender rendering
time blender -b micro_displacement_test.blend -x 1 -o test -f 1

# Open result in Linux desktop image viewer
xdg-open test0001.png
