# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 14:44:01 2017

@author: matt.slevin
"""

# Script that allows the access to the mapped server directory. In order to set
# this up on a different machine ensure that the directory test records is mapped
# to the computer it is running from.

import os

save_dir= "T:"

os.chdir(save_dir)

folders=os.listdir()
#save_path=os.getcwd()+save_dir