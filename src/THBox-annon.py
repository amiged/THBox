#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import cv2
from datetime import datetime
import mkdir
import aieye_find
import time
import sys

class_num = 1 # annotate number for class: 001: hamada
'''
drawing = False
posi0 = [-1,-1]
posi1 = [-1,-1]
image_size = [-1, -1] # [height, width]
'''

class State(object):
    def __init__(self):
        self.is_record = False
        self.drawing = False
        self.moving = False
        self.posi0 = [-1,-1]
        self.posi1 = [-1,-1]
        self.posi2 = [-1,-1]
        self.image = -1
        self.image_size = [-1, -1] # [height, width]
        self.image_orig = -1
        self.class_num = 777
        self.image_num = 0

    def draw_rect(self):
        # print ("posi0, posi1: ", self.posi0, self.posi1)
        self.image = self.image_orig.copy()
        cv2.rectangle(self.image, (self.posi0[0], self.posi0[1]), (self.posi1[0], self.posi1[1]), (0, 255, 0), 1)

    def draw_text(self):
        if(self.is_record):
            font = cv2.FONT_HERSHEY_TRIPLEX # cv2.FONT_HERSHEY_PLAIN
            font_size = 0.8
            text = "<<%d>>"% (self.image_num)
            color = (0x0, 0x0, 0xBF)
            px = int(self.image_size[1]/2)
            py = 30
            cv2.putText(self.image, text,(px, py), font, font_size, color)

state = State()

def mouse_event(event,x,y,flags,param):
    global state

    if x < 0: x = 0
    if y < 0: y = 0
    if x >= state.image_size[1]: x = state.image_size[1] - 1
    if y >= state.image_size[0]: y = state.image_size[0] - 1

    if event == (cv2.EVENT_LBUTTONDOWN):
        state.posi0[0] = x0 = state.posi1[0]
        state.posi0[1] = y0 = state.posi1[1]
        state.posi1[0] = x
        state.posi1[1] = y
        print ("Rect: (%d, %d) - (%d, %d)"%(x0, y0, x, y) )

    if event == (cv2.EVENT_RBUTTONDOWN): 
        state.moving = True
        state.posi2[0] = x
        state.posi2[1] = y

    if event == (cv2.EVENT_RBUTTONUP): 
        state.moving = False
        state.posi2[0] = x
        state.posi2[1] = y
    

    if event == (cv2.EVENT_MOUSEMOVE):
        if state.moving == True:
            width  = abs(state.posi0[0] - state.posi1[0])
            height = abs(state.posi0[1] - state.posi1[1])
            x0 = x - int(width/2)
            x1 = x + int(width/2)
            y0 = y - int(height/2)
            y1 = y + int(height/2)

            x_min = min(x0, x1)
            x_max = max(x0, x1)
            y_min = min(y0, y1)
            y_max = max(y0, y1)

            if x_min < 0: x_min = 0
            if y_min < 0: y_min = 0
            if x_max >= state.image_size[1]: x_max = state.image_size[1] - 1
            if y_max >= state.image_size[0]: y_max = state.image_size[0] - 1

            state.posi0[0] = x_min
            state.posi0[1] = y_min
            state.posi1[0] = x_max
            state.posi1[1] = y_max

#------------------------------------------------------------------------ save_data
def save_data_bbox(image_dbg, image_orig, fnum):
    global state
    class_num = state.class_num
    posi0 = state.posi0
    posi1 = state.posi1
    basedir = '../data4bbox/'
    fname_body = "image_%08d" % fnum

    # save image_orig (for Images/)
    fname = fname_body + ".jpg"
    basedir_images = basedir+"Images/%03d/"%(class_num)
    ofname_images = mkdir.get_filename_frame_simple(basedir_images , fname)
    print (ofname_images)
    cv2.imwrite(ofname_images, image_orig)

    # save image_dbg (for Debug/)
    fname = fname_body + ".jpg"
    basedir_dbg = basedir+"Debug/%03d/"%(class_num)
    ofname_dbg  = mkdir.get_filename_frame_simple(basedir_dbg , fname)
    print (ofname_dbg)
    cv2.imwrite(ofname_dbg, image_dbg)

    # save labes
    fname = fname_body + ".txt"
    basedir_labels = basedir+"Labels/%03d/"%(class_num)
    ofname_labels  = mkdir.get_filename_frame_simple(basedir_labels , fname)
    print (ofname_labels)
    bbox_posi = []
    bbox_posi.append(min(posi0[0], posi1[0]))
    bbox_posi.append(min(posi0[1], posi1[1]))
    bbox_posi.append(max(posi0[0], posi1[0]))
    bbox_posi.append(max(posi0[1], posi1[1]))
    with open(ofname_labels, "w") as file:
        file.write("1\n")
        file.write("%d %d %d %d\n" % (tuple(bbox_posi)))

def save_data_darknet(image_dbg, image_orig, fnum):
    global state
    class_num = state.class_num
    posi0 = state.posi0
    posi1 = state.posi1
    basedir = '../data4darknet/'
    fname_body = "image_%08d" % fnum

    # save image_orig (for Images/)
    fname = fname_body + ".jpg"
    basedir_images = basedir+"images/%03d/"%(class_num)
    ofname_images = mkdir.get_filename_frame_simple(basedir_images , fname)
    #print (ofname_images)
    cv2.imwrite(ofname_images, image_orig)

    # save image_dbg (for Debug/)
    fname = fname_body + ".jpg"
    basedir_dbg = basedir+"debug/%03d/"%(class_num)
    ofname_dbg  = mkdir.get_filename_frame_simple(basedir_dbg , fname)
    #print (ofname_dbg)
    cv2.imwrite(ofname_dbg, image_dbg)

    # save labes
    fname = fname_body + ".txt"
    basedir_labels = basedir+"labels/%03d/"%(class_num)
    ofname_labels  = mkdir.get_filename_frame_simple(basedir_labels , fname)
    print (ofname_labels)
    bbox_posi = []
    bbox_posi.append(min(posi0[0], posi1[0]))
    bbox_posi.append(min(posi0[1], posi1[1]))
    bbox_posi.append(max(posi0[0], posi1[0]))
    bbox_posi.append(max(posi0[1], posi1[1]))
    
    label_format = 'BBox'
    label_format = 'darknet'

    if label_format == 'BBox': 
        with open(ofname_labels, "w") as file:
            file.write("1\n")
            file.write("%d %d %d %d\n" % (tuple(bbox_posi)))

    if label_format == 'darknet': 
        img_h, img_w = image_orig.shape[:2]
        dh = float(img_h)
        dw = float(img_w)
        x0 = bbox_posi[0]
        y0 = bbox_posi[1]
        x1 = bbox_posi[2]
        y1 = bbox_posi[3]
        dnet_x = (x0 + x1)/(2.0*dw)
        dnet_y = (y0 + y1)/(2.0*dh)
        dnet_w = (x1 - x0)/dw
        dnet_h = (y1 - y0)/dh
        with open(ofname_labels, "w") as file:
            file.write("0 %1.17f %1.17f %1.17f %1.17f\n" % (dnet_x, dnet_y, dnet_w, dnet_h))


def save_data(image_dbg, image_orig, fnum, label_format='darknet'):
    if False:                      save_data_bbox(image_dbg, image_orig, fnum)
    if label_format == 'darknet': save_data_darknet(image_dbg, image_orig, fnum)

#------------------------------------------------------------------------ save_data./

if '__main__' == __name__:
    basedir = '../log/'
    if (len(sys.argv) > 1 ):
        basedir = sys.argv[1]
    
    iflist = [] 
    for fname in aieye_find.find(basedir, '*.jpg'):
        iflist.append(fname)

    iflist.sort()
    ni = len(iflist)
    i = 0

    #    for i, fname in enumerate(iflist):
    while( i < ni) :
        fname = iflist[i]
        print (fname, "%d/%d (%1.3f)"%(i, ni, i/ni))

        state.image_orig = cv2.imread(fname, cv2.IMREAD_COLOR)
        state.image      = state.image_orig.copy()

        state.image_size[0], state.image_size[1] = state.image.shape[:2]

        is_next = False
        while (not is_next):

            state.draw_rect()
            state.draw_text()

            cv2.imshow("THBox-annon.py", state.image)
            cv2.namedWindow("THBox-annon.py", cv2.WINDOW_NORMAL)
            cv2.setMouseCallback("THBox-annon.py", mouse_event)
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                save_data(state.image, state.image_orig, i)
                is_next = True
            if key  == 83:  # ->
                is_next = True
            if key  == 81:  # <-
                i = i - 2
                is_next = True
            if key == ord('r'): # Reset
                i = i - 1
                is_next = True
            if key  == ord('q'): 
                i = ni
                break
        i = i+1

    cv2.destroyAllWindows()





    
