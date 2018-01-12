#!/usr/bin/python

import os, re, sys
from stat import *
import codecs
from pycaption import WebVTTReader, SRTWriter


def convert_content(file_contents):
    '''convert_content convert vvt content to srt content using pycaption'''

    caption_set = WebVTTReader().read(file_contents)
    srt_content = SRTWriter().write(caption_set)
    return srt_content

def file_create(str_file_name, str_data):
    '''file_create create a text file'''

    try:

        f = open(str_file_name, "w", encoding="utf-8")
        f.writelines(str(str_data))
        f.close()

    except IOError:

        str_file_name = str_file_name.split(os.sep)[-1]
        f = open(str_file_name, "w")
        f.writelines(str(str_data))
        f.close()

    print("file created: " + str_file_name + "\n")

def read_text_file(str_file_name):
    f = open(str_file_name, "rb")

    print("file being read: " + str_file_name + "\n")

    return f.read().decode("utf8")

def vtt_to_srt(str_file_name):
    file_contents = read_text_file(str_file_name)

    str_data = ""

    str_data = str_data + convert_content(file_contents)

    str_file_name = str_file_name.replace(".vtt", ".srt")

    print(str_file_name)

    file_create(str_file_name, str_data)

def walktree(top_path, callback):
    '''recursively descend the directory tree rooted at top_path,
       calling the callback function for each regular file'''

    for f in os.listdir(top_path):

        pathname = os.path.join(top_path, f)
        mode = os.stat(pathname)[ST_MODE]

        if S_ISDIR(mode):

            # It's a directory, recurse into it
            walktree(pathname, callback)

        elif S_ISREG(mode):

            # It's a file, call the callback function
            callback(pathname)

        else:

            # Unknown file type, print a message
            print('Skipping %s' % pathname)

def convert_vtt_to_srt(file):
    if '.vtt' in file:
        vtt_to_srt(file)
