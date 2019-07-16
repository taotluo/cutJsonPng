# -*- coding: utf-8 -*-

# split atlas created by TexturePacker
# created by AdamWu(calvinmankor@gmail.com)

import os
import json
import cv2
import numpy as np

root = os.getcwd()
dst = root + "/result"
dPath = "sheets"

def makedirs(dir):
    if os.path.exists(dir):
        return
    os.makedirs(dir)

def atlas_split(folder, filename, dst):
    print folder,filename
    with open(os.path.join(folder,filename),'r') as load_f:
        data = json.load(load_f)
    n, e = os.path.splitext(filename)
    pngName = n + ".png" #对应的png名字
    print "Atlas", pngName
    colorImg = cv2.imread(os.path.join(folder, pngName), cv2.IMREAD_UNCHANGED)
    print colorImg.ndim
    print colorImg.shape

    
    n1, e1 = os.path.splitext(data["meta"]["image"])
    makedirs(os.path.join(dst, n1))
    #print data
    for k in data["frames"]:
#        print k
        d = k["filename"] + ".png"
        print "\n", k
        v = k
        
        # source size
        width = int(v["sourceSize"]["w"])
        height = int(v["sourceSize"]["h"])
        print "size:", width, height
        
        # frame size
        frame = v["frame"]
        x = int(frame["x"])
        y = int(frame["y"])
        w = int(frame["w"])
        h = int(frame["h"])
        print "frame:", x, y, w, h
        
        # offset (trim mode:trim or crop)
        # just avaliable in mode crop
        offset_x = 0
        offset_y = 0
        print "offset:", offset_x, offset_y
        
        # rotated
        rotated = v["rotated"]
        print "rotated:", rotated
        
        # source rect(can be calculated)
        source_rect = v["spriteSourceSize"]
        source_x = int(source_rect["x"])
        source_y = int(source_rect["y"])
        
        # new img
        frameImg = np.zeros((height, width, 4), np.uint8)
        
        # calculate rect
        if rotated:
            ox = int(0.5*(width - w) + offset_x)
            oy = int(0.5*(height - h) + offset_y)
        else:
            ox = int(0.5*(width - w) + offset_x)
            oy = int(0.5*(height - h) - offset_y)
        
        print h ,w, ox, oy
        for i in range(h):
            for j in range(w):
                if rotated:
                    #frameImg[height-1-(source_y+i), source_x+j] = colorImg[y+j, x+i]
                    frameImg[height-1-(oy+i), ox+j] = colorImg[y+j, x+i]
                else:
                    #frameImg[source_y+i, source_x+j] = colorImg[y+i, x+j]
                    frameImg[oy+i, ox+j] = colorImg[y+i, x+j]
        
        # write to file
        print d
        cv2.imwrite(os.path.join(dst, n1, d), frameImg)

rootdir = root + "/" + dPath
if not os.path.exists(rootdir):
    print u"当前目录没有sheets目录！！！"
else:
    if not os.path.exists(dst):
        os.makedirs(dst)

    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
        fName = list[i]
        path = os.path.join(rootdir, fName)
        if os.path.isfile(path):
            #你想对文件的操作
            na, ea = os.path.splitext(fName)
            if (ea == ".json"):
                print na,ea
                atlas_split(root, dPath + "/" + fName, dst)
