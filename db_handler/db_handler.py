#!/usr/bin/env python
'''Tool for updating the file size db.'''
import glob
import os
import sys
import re
import argparse
from minidb import MiniDB as minidb

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
    dirs = [os.path.join(dpath, filename) for filename in os.listdir(dpath) if (os.path.isdir(os.path.join(dpath, filename)))]
    return dirs

def update_filesizes_in_db(dbfile, dpath):
    '''update the database with any new folders created since the last time 
    this was run. N.B. This doesn't check for changed file sizes'''
    db = minidb(dbfile)
    dirlist = get_directory_list(dpath)
    for directory in dirlist:
        dirname = os.path.basename(directory)
        if not db.get(dirname):
            dirsize = get_directory_size(directory)
            db.set(dirname, dirsize)
    db.dumpdb()

def remove_nonexistant_directories_in_db(dbfile, dpath):
    '''removes keys for directories that no longer exist'''
    db = minidb(dbfile)
    direntries = db.getall()
    for directory in direntries:
        if not os.path.exists(os.path.join(dpath, directory)):
            db.rem(directory)
    db.dumpdb()


def force_reload_db(dbfile, dpath):
    '''forces reloading of db entries from scratch'''
    db = minidb(dbfile)
    db.deldb()
    dirlist = get_directory_list(dpath)
    for directory in dirlist:
        dirname = os.path.basename(directory)
        dirsize = get_directory_size(directory)
        db.set(dirname, dirsize)
    db.dumpdb()

def sanitize(spath):
    '''sanitize a path to only return valid folder names, in the form 
    that roughly corresponds to 20130101-31245, note we allow ticket numbers
    5 or greater digits in length and any date with 8 digits and any addendum'''
    folname = os.path.basename(spath)
    validname = re.compile('^[0-9]{8}-[0-9]{5,}.*')
    if validname.match(folname):
        return folname
    else:
        return None

def add_directory_sizedbfile(dbfile, dpath, directory):
    '''update db with direxctory size'''
    dirname = sanitize(directory)
    fullpath = os.path.join(dpath, dirname)
    db = minidb(dbfile)
    dirsize = get_directory_size(fullpath)
    db.set(dirname, dirsize)
    db.dumpdb()

def get_size(dbfile, directory):
    '''returns the directory size from the db'''
    dirname = sanitize(directory)
    db = minidb(dbfile)
    return db.get(dirname)

def read_options():
    '''read command line options'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", help="force a rebuild of the file size database", action="store_true")
    args = parser.parse_args()
    if args.force:
        action = "force"
    else:
        action = None
    return action


def main():
    action = read_options()
    if action == 'force':
        force_reload_db(DBFILE, DBPATH)
    else:
        remove_nonexistant_directories_in_db(DBFILE, DBPATH)
        update_filesizes_in_db(DBFILE, DBPATH)

if __name__ == "__main__":
    main()
