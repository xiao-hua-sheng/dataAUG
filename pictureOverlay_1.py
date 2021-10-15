import xml.dom.minidom
import os
import PIL.Image as img
import numpy as np
import random

img_path = 'sourceimgs/'
xml_path = 'Annotations/'
background_path = 'backgroundimgs/'
save_path = 'newimgs/'

img_files = os.listdir(img_path)
bimg_file = os.listdir(background_path)
leng = len(bimg_file)
print(leng)
for file in img_files:
    im = img.open(img_path+file)
    dom=xml.dom.minidom.parse(xml_path+file[:-3]+'xml')
    
    root = dom.documentElement
    width=root.getElementsByTagName('width')
    height=root.getElementsByTagName('height')
    depth=root.getElementsByTagName('depth')

    xmin = root.getElementsByTagName('xmin')
    ymin = root.getElementsByTagName('ymin')
    xmax = root.getElementsByTagName('xmax')
    ymax = root.getElementsByTagName('ymax')
    
    tmp = []
    for i in range(len(xmin)):
        box = (int(xmin[i].firstChild.data),int(ymin[i].firstChild.data),
              int(xmax[i].firstChild.data),int(ymax[i].firstChild.data))
        ng = im.crop(box)
        tmp.append(ng)
    randomindex = np.random.randint(leng,size=5)
    for j in range(5):
        im_ = img.open(background_path+bimg_file[randomindex[j]])
        width[0].firstChild.data = im_.size[0]
        height[0].firstChild.data = im_.size[1]
        depth[0].firstChild.data = 3
        for t in range(len(tmp)):
            inde_x = int(xmax[t].firstChild.data)-int(xmin[t].firstChild.data)
            inde_y = int(ymax[t].firstChild.data)-int(ymin[t].firstChild.data)
            if inde_x <= im_.size[0] or inde_y <= im_.size[1]:
                inde_x = min(inde_x,im_.size[0])
                inde_y = min(inde_y,im_.size[1])
                tmp[t] = tmp[t].resize((inde_x,inde_y))
                
            rand_x = random.randint(0,im_.size[0]-inde_x)
            rand_y = random.randint(0,im_.size[1]-inde_y)
            im_.paste(tmp[t],(rand_x,rand_y))
            xmin[t].firstChild.data=rand_x
            ymin[t].firstChild.data=rand_y
            xmax[t].firstChild.data=rand_x+inde_x
            ymax[t].firstChild.data=rand_y+inde_y
        im_.save(save_path+file[:-3]+'_%d.jpg'%j)
        with open(save_path+file[:-3]+'_%d.xml'%j,'w') as fh:
            dom.writexml(fh)