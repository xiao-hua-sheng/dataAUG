import cv2 
import numpy as np
import os
import xml.dom.minidom
from albumentations import MotionBlur

img_path = 'sourceimgs/'
xml_path = 'Annotations/'
save_path = 'newimgs/'
# 新生成图片的初始值（000000031922.jpg）
num = 31922

#对比度
def contrast(img_path,xml_path,save_path,num):
    img_list = os.listdir(img_path)
    for name in img_list:
        img = cv2.imread(img_path+name)
        img = np.uint8(np.clip((1.8 * img + 10), 0, 255))
        
        rname = '00000000000%d'%num
        imgname = rname[-12:]+'.jpg'
        xmlname = rname[-12:]+'.xml'
        cv2.imwrite(save_path+imgname,img)
        dom=xml.dom.minidom.parse(xml_path+name[:-3]+'xml')
        root = dom.documentElement
        filename = root.getElementsByTagName('filename')
        path = root.getElementsByTagName('path')
        path[0].firstChild.data = 'D:\\coco\\datasets\\1_1628\\'+imgname
        filename[0].firstChild.data = imgname
        with open(save_path+xmlname,'w') as fh:
            dom.writexml(fh)
        num += 1
#运动模糊
def motion_filter(img_path,xml_path,save_path,num):
    img_list = os.listdir(img_path)
    for imname in img_list:
        img = cv2.imread(img_path+imname)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        image = image.astype(np.uint8)
        img_ = MotionBlur(blur_limit=35, always_apply=True, p=1)(image=image)['image']
        
        rname = '00000000000%d'%num
        imgname = rname[-12:]+'.jpg'
        xmlname = rname[-12:]+'.xml'
        cv2.imwrite(save_path+imgname,img_)
        dom=xml.dom.minidom.parse(xml_path+imname[:-3]+'xml')
        root = dom.documentElement
        filename = root.getElementsByTagName('filename')
        path = root.getElementsByTagName('path')
        path[0].firstChild.data = 'D:\\coco\\datasets\\1_1628\\'+imgname
        filename[0].firstChild.data = imgname
        with open(save_path+xmlname,'w') as fh:
            dom.writexml(fh)
        num += 1

# contrast(img_path,xml_path,save_path,num)



    

# cv2.imshow('image',img_)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# if __name__== "__main__":