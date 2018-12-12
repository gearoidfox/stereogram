#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# Copyright 2018 Gearóid Fox
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
"""
Create random dot stereograms.
"""

import argparse
import numpy
import random
import sys
from PIL import Image


def rds(ref_image, levels = 24, parallel=False):
    """
        Create a random dot stereogram.

        args: ref_image (PIL.Image)
              greyscale image encoding depth information
              darker = lower, lighter = brighter

              levels (integer)
              levels of depth to use

              parallel (boolean)
              create a stereogram for parallel viewing

        returns: greyscale PIL.Image
    """
    xlim, ylim = ref_image.size
    left_half = numpy.zeros(shape=(xlim, ylim), dtype=int)
    right_half = numpy.zeros(shape=(xlim, ylim), dtype=int)
    
    # create random pixels:
    for i in range(xlim):
        for j in range(ylim):
            v = random.choice([0, 255])
            right_half[i, j] = v
    
    # copy right half to left half:
    ref_pixels = ref_image.load()
    for i in range(xlim):
        for j in range(ylim):
             offset = (levels * ref_pixels[i, j]) // 255
             if i < xlim - offset:
                     left_half[i, j] = right_half[i + offset, j]
             else:
                 left_half[i, j] = right_half[i, j]
   
    # create output image:
    stereogram = Image.new("L", (xlim * 2, ylim + 10))
    pixels = stereogram.load()
    for j in range(ylim):
        for i in range(xlim):
            if parallel == False:
                pixels[i, j] = int(left_half[i, j])
                pixels[i + xlim, j] = int(right_half[i, j])
            else:
                pixels[i, j] = int(right_half[i, j])
                pixels[i + xlim, j] = int(left_half[i, j])
    # Add bottom strip:
    for j in range(10):
        for i in range(3):
            pixels[xlim // 2 + i, ylim + j] = 255
            pixels[ 3 * xlim // 2 + i, ylim + j] = 255

    return stereogram


def main():
    parser = argparse.ArgumentParser(
            description="Create random dot stereograms.")
    parser.add_argument("ref_image", help="greyscale reference depth image")
    parser.add_argument("--outfile", help="output file name")
    parser.add_argument("--levels", help="levels of 3D depth", type=int)
    parser.add_argument("--parallel", action='store_true',
            help="create stereogram for parallel viewing")
    args = parser.parse_args()

    if args.levels == None:
        levels = 24
    else:
        levels = args.levels

    ref_img = Image.open(args.ref_image).convert("L")
    out_img = rds(ref_img, parallel=args.parallel, levels=levels)
    
    if args.outfile == None:
        ref_img.show()
        out_img.show()
    else:
        out_img.save(args.outfile)


if __name__ == "__main__":
    sys.exit(main())
