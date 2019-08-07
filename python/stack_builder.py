#!/usr/bin/env python3

"""
==============================================================================
==============================================================================
=======================          Stack Builder          ======================
==============================================================================
==============================================================================

This script is built to speed the process of making FIJI (ImageJ) stacks for
pollen microscopy experiments.
"""

import os
import glob
import argparse
import tifffile as tiff

"""
========================
Setting up the arguments
========================
"""

parser = argparse.ArgumentParser(description="Given some images and a series of ranges, build stacks")

parser.add_argument('-i', '--input_image_directory', type=str, help="Path to directory for input images.")
parser.add_argument('-r', '--image_ranges', type=str, help=("Series of ranges for stacks, as well as names "
                                                            "of the stacks. Format: "
                                                            "A 1:32 B 33:47..."))

args = parser.parse_args()

"""
===================
List files function
===================
"""


def list_files(input_directory):
    input_dir_string = input_directory + '*.tif'
    file_list = []
    for file in glob.glob(input_dir_string):
        file_list.append(file)
    file_list.sort()
    return file_list


"""
=============================
Process input ranges function
=============================
"""


def process_input_ranges(input_ranges):
    # Making the long string a list based on spaces
    input_ranges = input_ranges.split()
    # Getting the trial names
    names = input_ranges[::2]
    # Getting the trial ranges
    ranges = input_ranges[1::2]

    output_list = []

    # Goes through the names and trial lists and makes a list of lists where
    # each sublist has the name of the trial and the actual index range, which
    # will be used later to pull the correct image files for each trial from
    # the file list.
    for x in range(len(names)):
        range_list = ranges[x].split(':')
        proper_range = [int(i) for i in range_list]
        proper_range[0] = proper_range[0] - 1
        proper_range = slice(proper_range[0], proper_range[1])
        sublist = [names[x], proper_range]
        output_list.append(sublist)
    return output_list


"""
====================
Make stacks function
====================
"""


def make_stacks(input_image_directory, file_list, input_ranges):
    # Making a directory for the stack output inside of the input directory
    directory_path = input_image_directory + 'stacks/'
    try:
        os.mkdir(directory_path)
    except OSError:
        print("...stacks directory exists")

    for x in input_ranges:
        trial_name = x[0]
        trial_range = x[1]

        print("\n...building stack: " + trial_name)
        files_in_trial = file_list[trial_range]
        print("...images in stack:\n" + "\n".join(files_in_trial))

        # Reading in the images
        trial_images = tiff.imread(files_in_trial)

        # Writing out the images in a stack
        tiff.imwrite(input_image_directory + 'stacks/' + trial_name + ".tif", trial_images)
        print("...stack write complete\n")


"""
=================
The main function
=================
"""


def main():
    file_list = list_files(args.input_image_directory)
    input_ranges = process_input_ranges(args.image_ranges)
    make_stacks(args.input_image_directory, file_list, input_ranges)


if __name__ == "__main__":
    main()
