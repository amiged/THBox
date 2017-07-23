#!/usr/bin/env python3
#Time-stamp: <2017-06-19 19:56:35 hamada>
import argparse
import numpy as np
import cv2
from datetime import datetime
import mkdir
import aieye_find
import time
import sys
import random
import shutil

# Usage: ./shuffle.py ../data4darknet/
# !!! data4darknet must have debug/777/, images/777/ and labels/777/ !!!

if (__name__ == '__main__'):
    random.seed(0x19740526)
    basedir = '../log/'
    if (len(sys.argv) > 1 ):
        basedir = sys.argv[1]
    
    iflist = [] 
    for fname in aieye_find.find(basedir+'/debug/777/', '*.jpg'):
        iflist.append(fname)

    iflist.sort()
    random.shuffle(iflist)

    ni = len(iflist)
    i = 0

    mkdir.create_dir(basedir+"/images/888/")
    mkdir.create_dir(basedir+"/labels/888/")
    mkdir.create_dir(basedir+"/debug/888/")

    #    for i, fname in enumerate(iflist):
    while( i < ni) :
        # basedir: xxx/debug/777/
        fname  = iflist[i]
        fname0 = fname.split('/')[-1]
        fname_body = fname0.split('.')[0]
        fname_body_new = "image_%08d"%(i)
        shutil.copy2(basedir+'/debug/777/'+fname_body+".jpg",    basedir+'/debug/888/'+fname_body_new+".jpg")  # copy debug
        shutil.copy2(basedir+'/images/777/'+fname_body+".jpg",   basedir+'/images/888/'+fname_body_new+".jpg") # copy images
        shutil.copy2(basedir+'/labels/777/'+fname_body+".txt",   basedir+'/labels/888/'+fname_body_new+".txt") # copy labels


        print (basedir, fname_body, i, ni, i/ni)
        image = cv2.imread(fname)
        cv2.imshow("play.py", image)

        key = cv2.waitKey(1) & 0xFF
        if key != 255:  print (key, "%d/%d"% (i, ni))

        if key  == ord('q'): break


        i = i + 1

    cv2.destroyAllWindows()
