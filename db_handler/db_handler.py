#!/usr/bin/env python
import os
import pickledb
def get_directory_size(start_path):
    '''get size of directory and contents'''
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size
