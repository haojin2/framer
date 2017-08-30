#!/usr/bin/python
__author__ = "Hao Jin"
__copyright__ = "Copyright 2017"
__credits__ = ["Hao Jin"]
__license__ = "GNU v3.0"
__version__ = "0.0.1"
__maintainer__ = "Hao Jin"
__email__ = "haoj@andrew.cmu.edu"

import sys
import getopt

upper_left = (0, 0)
lower_right = (0, 0)


def usage():
    print """usage: python framer.py(c) -f <frame_file> -d <frame_data> """ \
          """-i <input_file> -o <output_file>"""


def main(input_file, frame, data, output_path):
    from skimage.io import imread, imshow, show, imsave
    from skimage.transform import rescale
    from skimage import img_as_float
    from skimage.transform import resize

    try:
        frame_img = imread(frame, as_float=True)
        frame_img = img_as_float(frame_img)
    except:
        print "frame image does not exist!"
        sys.exit(1)
    frame_size = frame_img.shape
    try:
        input_img = imread(input_file, as_float=True)
        input_img = img_as_float(input_img)
    except:
        print "input image does not exist!"
        sys.exit(1)
    input_size = input_img.shape
    num_lines = sum(1 for line in open(data))
    if num_lines != 1:
        print "data file of wrong format"
        sys.exit(1)
    with open(data, 'r') as data_file:
        line = data_file.readline()
        coords = line.split(' ')
        if len(coords) is not 4:
            print "coords of wrong format"
            sys.exit(1)
        try:
            upper_left = (int(coords[0]), int(coords[1]))
            lower_right = (int(coords[2]), int(coords[3]))
        except:
            print "coords of illegal format, should be integers"
    central_width = (lower_right[0] - upper_left[0])
    central_height = (lower_right[1] - upper_left[1])

    new_frame_size = (int(frame_img.shape[0] * (input_img.shape[0] * 1.0 /
                                                central_width)),
                      int(frame_img.shape[1] * (input_img.shape[1] * 1.0 /
                                                central_height)))
    new_frame = resize(frame_img, new_frame_size)
    upper = int(upper_left[0] * (new_frame_size[0] * 1.0 / frame_img.shape[0]))
    lower = int(lower_right[0] * (new_frame_size[0] * 1.0 /
                                  frame_img.shape[0]))
    left = int(upper_left[1] * (new_frame_size[1] * 1.0 / frame_img.shape[1]))
    right = int(lower_right[1] * (new_frame_size[1] * 1.0 /
                                  frame_img.shape[1]))
    for i in range(input_img.shape[0]):
        for j in range(input_img.shape[1]):
            new_frame[i + upper][j + left] = input_img[i][j]
    imsave(output_path, new_frame)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:f:d:o:",
                                   ["help", "input=", "frame=", "data=",
                                    "output="])
    except getopt.GetoptError:
        usage()
    input_file = ""
    output_path = ""
    frame = ""
    data = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-i", "--input"):
            input_file = a
        if o in ("-o", "--output"):
            output_path = a
        if o in ("-f", "--frame"):
            frame = a
        if o in ("-d", "--data"):
            data = a
    main(input_file, frame, data, output_path)
