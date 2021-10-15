import cv2
import numpy as np
import os
import random
import xml.dom.minidom


obj_path = 'object/'
save_path = 'newimgs/'
simg_path = 'backgroundimgs/'

#背景图共14张，random_min，random_max，random_num用于确定随机数的范围和大小
random_min = 0
random_max = 14 
random_num = 10  
# 新生成图片的初始值（000000031642.jpg）
num = 31642
ob_list = ['class1/','class2/','class3/']

def imgadd(img1,img2):
    row,col,ch = img2.shape
    h,w,c = img1.shape
    sc_h = (h/720)*0.6         #修改抠图比例   
    sc_w = (w/1280)*0.6
    row = int(row*sc_h)
    col = int(col*sc_w)
    img2_ = cv2.resize(img2,(col,row))
    tmp_y = img1.shape[0] - row
    tmp_x = img1.shape[1] - col
    rand_x = random.randint(0,tmp_x)
    rand_y = random.randint(0,tmp_y)
    for i in range(row):
        for j in range(col):
            if sum(img2_[i][j][:]) <= 730:
                img1[i+rand_y][j+rand_x][0] = img2_[i][j][0]
                img1[i+rand_y][j+rand_x][1] = img2_[i][j][1]
                img1[i+rand_y][j+rand_x][2] = img2_[i][j][2]
            else:
                pass
    return img1,rand_x,rand_y,img2_.shape[1],img2_.shape[0]

dom=xml.dom.minidom.parse('000000000023.xml')
root = dom.documentElement
filename = root.getElementsByTagName('filename')
path = root.getElementsByTagName('path')
width=root.getElementsByTagName('width')
height=root.getElementsByTagName('height')
depth=root.getElementsByTagName('depth')
class_name = root.getElementsByTagName('name')
xmin = root.getElementsByTagName('xmin')
ymin = root.getElementsByTagName('ymin')
xmax = root.getElementsByTagName('xmax')
ymax = root.getElementsByTagName('ymax')

for name in ob_list:
    imobj_path = obj_path+name
    imobj_list = os.listdir(imobj_path)
    for img_name in imobj_list:
        imgobj = cv2.imread(imobj_path+img_name)
        rand_list = np.random.randint(random_min,random_max,random_num)
        simg_list = os.listdir(simg_path)
        for n in rand_list:
            print(n)
            rname = '00000000000%d'%num
            imgname = rname[-12:]+'.jpg'
            xmlname = rname[-12:]+'.xml'
            imgsource = cv2.imread(simg_path+simg_list[n])
            img,rand_x,rand_y,tmp_x,tmp_y = imgadd(imgsource,imgobj)
            cv2.imwrite(save_path+imgname,img)
            
            path[0].firstChild.data = 'D:\\coco\\datasets\\1_1628\\'+imgname
            filename[0].firstChild.data = imgname
            class_name[0].firstChild.data = name[:-1]
            width[0].firstChild.data = img.shape[1]
            height[0].firstChild.data = img.shape[0]
            depth[0].firstChild.data = 3
            xmin[0].firstChild.data=rand_x
            ymin[0].firstChild.data=rand_y
            xmax[0].firstChild.data=rand_x+tmp_x
            ymax[0].firstChild.data=rand_y+tmp_y
            with open(save_path+xmlname,'w') as fh:
                dom.writexml(fh)
            num += 1