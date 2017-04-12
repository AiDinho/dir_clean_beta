# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 14:22:01 2017

@author: Biswarup Ghosh
"""

##create config file##
import configparser
import sys
from os.path import join
from optparse import OptionParser
import re

## a list of directories provided at run time


## check specific dirs in windows 

parser = OptionParser()
parser.add_option('--dirs',action = "store",dest="dirs")
parser.add_option('--dest',action = "store",dest="des")
opts ,args=  parser.parse_args()
print opts
folder = opts.dirs
dest = opts.des

config = configparser.SafeConfigParser()
config.add_section('Directories')
for i in folder.split(','):
    #print i
    pattern = r'([^\\]*$)'


    dir_name = re.findall(pattern,i)[0]
    print dir_name
    config.set('Directories',dir_name,i)
#config.set('Directories','Downloads','C:\\Users\\Biswarup Ghosh\\Downloads')
#config.set('Directories','Documents','C:\\Users\\Biswarup Ghosh\\Documents')
config.set('Directories',"Destination",dest)
with open("dir_clean.ini",'w') as d:
    config.write(d)
