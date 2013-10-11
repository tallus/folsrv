#!/usr/bin/env python
'''Tool for updating the file size db.'''
import glob
import os
import pickledb

class MyError(Exception):
    pass

class json

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

def update_filesizes_in_db(dbfile, dpath):
    '''update the database with any new folders created since the last time 
    this was run. N.B. This doesn't check for changed file sizes'''
    db = jsondb.load(dbfile, False)
    dirlist = get_directory_list(dpath)
    for directory in dirlist:
        dirname = os.path.basename(directory)
        if not db.get(dirname):
            dirsize = get_directory_size(directory)
            db.set(dirname, dirsize)

def remove_nonexistant_directories_in_db(dbfile, dpath):
    '''removes keys for directories that no longer exist'''
     db = jsondb.load(dbfile, False)
     # N.B. This requires our hacked version, probably should just
     # extend pickledb
    direntries = db.getall()

#TODO complete above, write function to force reload of db
