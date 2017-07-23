#!/usr/bin/env python3
#Time-stamp: <2017-07-10 19:03:51 hamada>
import numpy as np
import cv2
import aieye_find
import sys
#----------------------
start_index = 8655
class_name_src = '777'
class_name_dst = 'Hand/Goo'
is_GUI = True # False
#----------------------



def do_rename(index, dir_src, fname_src, class_name_src, class_name_dst):
    global start_index
    fname_base = fname_src.split('/')[-1]
    fname_body = fname_base.split('.')[0]
    cmd = ''
    if index == start_index:
        cmd += "mkdir -p ../rename/debug/%s\n" % class_name_dst
        cmd += "mkdir -p ../rename/images/%s\n" % class_name_dst
        cmd += "mkdir -p ../rename/labels/%s\n" % class_name_dst
        
    fname_src_debug = dir_src + '/debug/'+class_name_src+'/'+fname_body+'.jpg'
    fname_src_image = dir_src + '/images/'+class_name_src+'/'+fname_body+'.jpg'
    fname_src_label = dir_src + '/labels/'+class_name_src+'/'+fname_body+'.txt'
    fname_dst_debug = "../rename/debug/%s/image_%08d.jpg" % (class_name_dst, index)
    fname_dst_image = "../rename/images/%s/image_%08d.jpg" % (class_name_dst, index)
    fname_dst_label = "../rename/labels/%s/image_%08d.txt" % (class_name_dst, index)

    cmd += "cp %s %s;\n" % (fname_src_debug, fname_dst_debug)
    cmd += "cp %s %s;\n" % (fname_src_image, fname_dst_image)
    cmd += "cp %s %s;\n" % (fname_src_label, fname_dst_label)
    print (cmd, end='')


if (__name__ == '__main__'):
    basedir = '../log/'
    if (len(sys.argv) > 1 ):
        basedir = sys.argv[1]
    
    iflist = [] 
    for fname in aieye_find.find(basedir+'/debug/', '*.jpg'):
        iflist.append(fname)

    iflist.sort()
    ni = len(iflist)

    for i, fname in enumerate(iflist):
        do_rename(i+start_index, basedir, fname, class_name_src, class_name_dst)

        if is_GUI: 
            image = cv2.imread(fname)
            cv2.imshow("rename.py", image)
            key = cv2.waitKey(1) & 0xFF
            if key  == ord('q'): break

    if is_GUI: cv2.destroyAllWindows()
