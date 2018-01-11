#!/usr/bin/python3

# -*- coding: utf-8 -*-

import os
import threading
import time
import multiprocessing

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
    except Exception as e:
        print(e)
        exit()
        # return Image.Image()


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


def GetFiles(path):
    files_list = []
    list_dirs = os.walk(path)
    for root, dirs, files in list_dirs:
        for f in files:
            files_list.append(os.path.join(root, f))
    return files_list


def Dowork(files_list1, files_list2):
    i = 0
    for f1 in files_list1:
        for f2 in files_list2:
            # print(f1)
            # print(f2)
            hash1 = hash_String(f1)
            hash2 = hash_String(f2)

            if i % 500 == 0:
                str = time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.localtime(time.time()))
                print("compare: ", f1, " : ", f2)
            if Difference(hash1, hash2) <= 5:
                print("find: ", f1, " ==> ", f2)
            i += 1
            # print(i)


def main():
    num = multiprocessing.cpu_count()
    print("CPU number:", num)

    dir1 = "/home/user/path1"
    dir2 = "/home/user/path2"

    files_list1 = GetFiles(dir1)
    length1 = len(files_list1)

    files_list2 = GetFiles(dir2)
    length2 = len(files_list2)

    for i in range(0, multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=Dowork, args=(
            files_list1[i * (length1 // num):(i + 1) * (length1 // num)],
            files_list2[i * (length2 // num):(i + 1) * (length2 // num)])
        )
        p.start()
    print("wait...")


# ==> start
main()
