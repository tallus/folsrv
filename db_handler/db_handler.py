#!/usr/bin/env python
'''Tool for updating the file size db.'''
import glob
import os
import sys
import argparse

class MyError(Exception):
    pass

class jsondb(dbfile):
    '''load a dictionary from a json file as a key-value store'''
    def __init__(self, dbfile)
     self.dbfile = os.path.expanduser(dbfile)
     if os.path.exists(self.dbfile):
         self.db  = self._load(open(self.dbfile)
     else:
         self.db  = {}

    def set(self, key, value):
        '''Set the (string,int,whatever) value of a key'''
        self.db[key] = value

    def get(self, key):
        '''Get the value of a key'''
        try:
            return self.db[key]
        except KeyError:
            return None

    def getall(self):
        '''return a list of all the keys'''
        return self.db.keys()

    def rem(self, key):
        '''Delete a key'''
        del self.db[key]
    
    def kexists(self, key):
        '''determine if key exists in db'''
        if key in self.db:
            return True
        else:
            return False
     
    def deldb(self):
        '''Delete everything from the database'''
        self.db= {}

    def _load(self):
        '''load db from file'''
        db  = json.load(open(self.dbfile, 'rb'))
        return db

    def dumpdb(self):
        '''write to file'''
        json.dump(self.db, open(self.dbfile, 'wb'))

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
    db = jsondb.load(dbfile)
    dirlist = get_directory_list(dpath)
    for directory in dirlist:
        dirname = os.path.basename(directory)
        if not db.get(dirname):
            dirsize = get_directory_size(directory)
            db.set(dirname, dirsize)
    db.dumpdb()

def remove_nonexistant_directories_in_db(dbfile, dpath):
    '''removes keys for directories that no longer exist'''
    db = jsondb.load(dbfile)
    direntries = db.getall()
    for directory in direntries:
        if not os.path.exists(os.path.join(dpath, directory)):
            db.rem(directory)
    db.dumpdb()


def force_reload_db(dbfile, dpath):
    '''forces reloading of db entries from scratch'''
    db = jsondb.load(dbfile)
    db.deldb()
    dirlist = get_directory_list(dpath)
    for directory in dirlist:
        dirname = os.path.basename(directory)
        dirsize = get_directory_size(directory)
        db.set(dirname, dirsize)
    db.dumpdb

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

def add_directory_sizedbfile,(dbfile, dpath, directory):
    '''update db with direxctory size'''
    dirname = sanitize(directory)
    fullpath = os.path.join(dpath, dirname)
    db = jsondb.load(dbfile)
    dirsize = get_directory_size(fullpath)
    db.set(dirname, dirsize)
    db.dumpdb

def get_size(dbfile, directory):
    '''returns the directory size from the db'''
    dirname = sanitize(directory)
    db = jsondb.load(dbfile)
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
