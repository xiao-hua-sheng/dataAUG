import cv2
import os

#均值哈希算法
def ahash(image):
    image = cv2.resize(image,(8,8),interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    s = 0
    ahash_str = ''
    for i in range(8):
        for j in range(8):
            s = s+gray[i, j]
    avg = s/64
    ahash_str  = ''
    for i in range(8):
        for j in range(8):
            if gray[i,j]>avg:
                ahash_str = ahash_str + '1'
            else:
                ahash_str = ahash_str + '0'
    result = ''
    for i in range(0, 64, 4):
        result += ''.join('%x' % int(ahash_str[i: i + 4], 2))
    return result
 
# 差异值哈希算法
def dhash(image):
    image = cv2.resize(image,(9,8),interpolation=cv2.INTER_CUBIC )
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    dhash_str = ''
    for i in range(8):
        for j in range(8):
            if gray[i,j]>gray[i, j+1]:
                dhash_str = dhash_str + '1'
            else:
                dhash_str = dhash_str + '0'
    result = ''
    for i in range(0, 64, 4):
        result += ''.join('%x'%int(dhash_str[i: i+4],2))
    return result

# 计算两个哈希值之间的差异
def campHash(hash1, hash2):
    n = 0
    # hash长度不同返回-1,此时不能比较
    if len(hash1) != len(hash2):
        return -1
    # 如果hash长度相同遍历长度
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n+1
    return n

img_path = 'ImgRecord/'
img_list = os.listdir(img_path)
img_list.sort()

for i in range(len(img_list)-1):
    img1 = cv2.imread(img_path+img_list[i])
    img2 = cv2.imread(img_path+img_list[i+1])
    hash1 = ahash(img1)
    hash2 = ahash(img2)
    cam = campHash(hash1,hash2)
    if  cam <= 1:
        os.remove(img_path+img_list[i])
        print(img_list[i])
    
# img1 = cv2.imread(img_path+'000000012062.jpg')
# img2 = cv2.imread(img_path+'000000012061.jpg')
# hash1 = ahash(img1)
# hash2 = ahash(img2)
# camphash1 = campHash(hash1, hash2)
# print(camphash1)



