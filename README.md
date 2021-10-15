# dataAUG
│  pictureOverlay_1.py
│  pictureOverlay_2.py
│  pictureprocessing.py
│
├─Annotations
├─backgroundimgs
├─newimgs
├─object
│  ├─class1
│  ├─class2
│  └─class3
└─sourceimgs
Annotations：原始数据集xml文件
backgroundimgs：背景图片
newimgs：新生成的数据
object：检测物体的类别图
sourceimgs:原始数据集jpg图片

PictureOverlay_1.py用于将voc格式数据集进行扩增，方式为将原始数据集中box与背景图片随机结合，生成新的图片和下xml标签
PictureOverlay_2.py用于将voc格式数据集进行扩增，方式为将objec中的class（将需要检测的物体抠图存放在class中）与背景图片随机结合，生成新的图片和下xml标签
pictureprocessing.py 增加对比度和运动模糊，生成新的图片和下xml标签
