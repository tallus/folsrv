#!/usr/bin/env python
import glob
import os
import pickledb

class MyError(Exception):
    pass

def get_directory_size(start_path):
    '''get size of directory and contents'''
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_directory_list(dpath):
    '''returns a list of directories in a directory, 
    with fully qualified paths'''
    if not os.path.isdir(dpath):
        raise MyError('oops %s is not a directory'% dpath)
    dirs = [os.path.join(dpath, filename) for filename in os.listdir(dpath)  if (os.path.isdir(os.path.join(dpath, filename)))]
    return dirs


