# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 15:49:34 2017

@author: Biswarup Ghosh
"""
## goal clean downloands and directories 
## read from config 
## create back up in d drive 
## basic goal two functions 1 create list of dirextories 2 which itereates over them and creates back up
##  TODOS
## take options from command line to for directories /optionally take a file which has a list of dirs
## efficent backup ,delete files rarely used or accessed ,

## todos save file meta data to
from configparser import ConfigParser
from os import walk,path,makedirs,chdir,remove,listdir
from collections import defaultdict
from shutil import copy2
from datetime import datetime
import errno
import logging




def read_from_config():
    
    parser = ConfigParser()
    dir_list = {}
    
    with open('dir_clean.ini') as ip:
        parser.read_file(ip)
    for section_name in parser.sections():
        for i,j in parser.items(section_name):
            dir_list[i]=j
    return dir_list
        

def parse_dirs(dir_name):
    """
    1.show the files
    2.group the files by their category
    3.already created directories will be copied as is 
    4.
    
    """
    image_exts = [".jpeg",".jpg",".png",".gif"]
    doc_exts = [".docx",".doc",".pdf",".ps",".pptx"]
    arch_exts = [".zip",".7z",".rar"]
    setup_exts =[".exe",".msi"]
    file_group_dict = defaultdict(list)
    #file_group_dict.set
    root,dirs,files = walk(dir_name).next()
    #print files
    for filename in files:
        ext = path.splitext(filename)[1].lower()
        #print ext
        if ext in image_exts:
            #print "1"
            file_group_dict["images"].append(filename)
        elif ext in doc_exts:
            file_group_dict["docs"].append(filename)
        elif ext in arch_exts:
            file_group_dict["zips"].append(filename)
        elif ext in setup_exts:
            file_group_dict["exectuables"].append(filename)
        else:
            file_group_dict["others"].append(filename)
      
    #print file_group_dict
    return file_group_dict

def copy_files(files,destination):
    ##" try to create the directory but if it does not exist , create or raise the error "
    try:
        makedirs(destination)
        #copy2(files, destination)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        #if exception.errno == errno.
            
    try:
        copy2(files,destination)
        remove(files)
    except WindowsError:
        pass

        
def movefiles(filedict,base_path):
    time_now = datetime.date(datetime.now())
    dt = datetime.strftime(time_now,"%Y_%m")
    x = path.split(base_path)
    file_path = file_dict.keys()
    no_of_files = len(file_dict.values())
    for j,k in filedict.iteritems():
        
        destination = path.join(x[0],path.sep,x[1],j,dt)
        [copy_files(m,destination) for m in k]
        
        
    remaining_files =  len([name for name in listdir('.') if path.isfile(name)])
    print_list = [no_of_files,file_path,remaining_files,datetime.strftime(time_now,"%d/%m/%y %H:%M:%S")]
    log_Info = "{} files Copied from {} ,no of files not copied {},at-{}".format(*print_list)
    logging.log(20,log_Info)

        #print parser.get('Directories', 'downloads')
if __name__== "__main__":
    #LOG_FILENAME = path.join(backup,'dir_clean.log')
    #logging.basicConfig()

    cdict = read_from_config()
    #print cdict
    backup = cdict['destination']
    file_dict = parse_dirs(cdict['downloads'])
    chdir(cdict['downloads'])
    LOG_FILENAME = path.join(backup, 'dir_clean.log')
    logging.basicConfig( filename=LOG_FILENAME, level=logging.INFO)
    logging.info('Started Logging')
    movefiles(file_dict,backup)
    logging.info('Finished Logging')
    
        
    
    
    

  