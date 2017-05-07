import Queue
import threading
from configparser import ConfigParser
from os import walk,path,makedirs,chdir,remove,listdir,getcwd

from collections import defaultdict
from shutil import copy2
from datetime import datetime
import errno
import logging


def parse_dirs(dir_name):
    """
    1.show the files
    2.group the files by their category
    3.already created directories will be copied as is
    4.
    """

    root, dirs, files = walk(dir_name).next()
    x = path.split(dir_name)

    return [path.join(dir_name,f) for f in files]


def copy_files(files, destination):
    ##" try to create the directory but if it does not exist , create or raise the error "
    ## create bew
    try:
        makedirs(destination)
        # copy2(files, destination)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
            # if exception.errno == errno.

    try:
        copy2(files, destination)
        remove(files)
    except WindowsError:
        pass


def movefiles(filename, base_path):
    image_exts = [".jpeg", ".jpg", ".png", ".gif"]
    doc_exts = [".docx", ".doc", ".pdf", ".ps", ".pptx"]
    arch_exts = [".zip", ".7z", ".rar"]
    setup_exts = [".exe", ".msi"]
    time_now = datetime.date(datetime.now())
    dt = datetime.strftime(time_now, "%Y_%m")
    x = path.split(base_path)
    ext =  path.splitext(filename)[1].lower()
    #file_path = file_dict.keys()
    if ext in image_exts:
        destination = path.join(x[0], path.sep, x[1], "images", dt)
    elif ext in doc_exts:
        destination = path.join(x[0], path.sep, x[1], "docs", dt)
    elif ext in arch_exts:
        destination = path.join(x[0], path.sep, x[1], "zips", dt)
    elif ext in setup_exts:
        destination = path.join(x[0], path.sep, x[1], "exectuables", dt)
    else:
        destination = path.join(x[0], path.sep, x[1], "others", dt)
    copy_files(filename,destination)

    #remaining_files = len([name for name in listdir('.') if path.isfile(name)])
    #print_list = [no_of_files, file_path, remaining_files, datetime.strftime(time_now, "%d/%m/%y %H:%M:%S")]
    #log_Info = "{} files Copied from {} ,no of files not copied {},at-{}".format(*print_list)
    #logging.log(20, log_Info)

class FileParser(threading.Thread):
    def __init__(self,in_queue,out_queue):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
    def run(self):
        """grab a file from list of dirs
           put file in in_queue
           copy
        """

        while True:
            dirs_for_parsing = self.in_queue.get()
            files = parse_dirs(dirs_for_parsing)
            for f in files:
                self.out_queue.put(f)
            self.in_queue.task_done()

class FileMoverThread(threading.Thread):
    """grab files from out queue put it in to destination"""
    def  __init__(self,out_queue,base_path):
        threading.Thread.__init__(self)
        self.out_queue = out_queue
        self.base_path = base_path

    def run(self):
        while True:
            files = self.out_queue.get()
            #print files
            movefiles(files,self.base_path)
            self.out_queue.task_done()


def read_from_config():
    parser = ConfigParser()
    dir_list = {}

    with open('dir_clean.ini') as ip:
        parser.read_file(ip)
    for section_name in parser.sections():
        for i, j in parser.items(section_name):
            dir_list[i] = j
    return dir_list

def main():

    dir_list = read_from_config()
    backup = dir_list['destination']
    dirs = set(dir_list.keys())
    excludes = set(['destination'])
    input_dir_keys = dirs.difference(excludes)
    print input_dir_keys
    input_dirs = [dir_list[k] for k in input_dir_keys]
    print input_dirs
    print getcwd()
    in_queue = Queue.Queue(5)
    out_queue = Queue.Queue(5)

    ## thread spawning
    for i in range(2):
        f = FileParser(in_queue,out_queue)
        f.setDaemon(True)
        f.start()

    [in_queue.put(i) for i in input_dirs]
    #print in_queue.get()
    ## thread spawning
    for i in range(5):
        d = FileMoverThread(out_queue,backup)
        d.setDaemon(True)
        d.start()
    in_queue.join()
    out_queue.join()

if __name__ == "__main__":
    main()
