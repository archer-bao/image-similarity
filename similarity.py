#!/usr/bin/python3

# -*- coding: utf-8 -*-

import os
import time

from PIL import Image  # 导入pillow库下的image模块，主要用于图片缩放、图片灰度化、获取像素灰度值

from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

# image为图片的路径，resize_width为缩放图片的宽度，resize_heith为缩放图片的高度


def grayscale_Image(image, resize_width=9, resize_heith=8):
    try:
        im = Image.open(image)  # 使用Image的open方法打开图片
        smaller_image = im.resize((resize_width, resize_heith))  # 将图片进行缩放
        grayscale_image = smaller_image.convert('L')  # 将图片灰度化
        return grayscale_image
    except:
        return tuple()


def hash_String(image, resize_width=9, resize_heith=8):
    hash_string = ""  # 定义空字符串的变量，用于后续构造比较后的字符串
    pixels = list(grayscale_Image(image, resize_width, resize_heith).getdata())
    # 上一个函数grayscale_Image()缩放图片并返回灰度化图片，.getdata()方法可以获得每个像素的灰度值，使用内置函数list()将获得的灰度值序列化
    for row in range(1, len(pixels) + 1):  # 获取pixels元素个数，从1开始遍历
        if row % resize_width:  # 因不同行之间的灰度值不进行比较，当与宽度的余数为0时，即表示当前位置为行首位，我们不进行比较
            if pixels[row - 1] > pixels[row]:  # 当前位置非行首位时，我们拿前一位数值与当前位进行比较
                hash_string += '1'  # 当为真时，构造字符串为1
            else:
                hash_string += '0'  # 否则，构造字符串为0
          # 最后可得出由0、1组64位数字字符串，可视为图像的指纹
    return int(hash_string, 2)  # 把64位数当作2进制的数值并转换成十进制数值


def Difference(dhash1, dhash2):
    difference = dhash1 ^ dhash2  # 将两个数值进行异或运算
    return bin(difference).count('1')  # 异或运算后计算两数不同的个数，即个数<5，可视为同一或相似图片

dir1 = "/home/user/mmjpg"
dir2 = "/home/user/mzitu"
i = 0
for lists1 in os.listdir(dir1):
    path1 = os.path.join(dir1, lists1)
    for lists2 in os.listdir(dir2):
        sublists = os.path.join(dir2, lists2)
        for file in os.listdir(sublists):
            path2 = os.path.join(dir2, lists2, file)
            hash1 = hash_String(path1)
            hash2 = hash_String(path2)
            i += 1
            # print(i)
            if i % 500 == 0:
                str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                os.system('echo ' + str + " >> compare.txt")
                os.system('echo ' + "compare: " + path1 +
                          " : " + path2 + " >> compare.txt")
                # print("compare: ", path1, " : ", path2)
            if Difference(hash1, hash2) <= 5:
                os.system('echo ' + "find: " + path1 +
                          " ==> " + path2 + " >> find.txt")
                # print("find: ", path1, " ==> ", path2)
