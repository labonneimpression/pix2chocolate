#!/bin/sh
time blender -b micro_displacement_test.blend -x 1 -o test -f 1
xdg-open test0001.png
