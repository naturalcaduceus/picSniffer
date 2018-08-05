#!/usr/bin/env python    
# encoding: utf-8    
  
import _dhash
from PIL import Image,ImageDraw  
    

#入口函数
def classify_passage(img1Path,img2Path):

    image1 = Image.open(img1Path)
    b1= image1.split()[0]  # rgb通道分离
    g1= image1.split()[1]  # rgb通道分离
    r1= image1.split()[2]  # rgb通道分离
    
    image2 = Image.open(img2Path)
    b2= image2.split()[0]  # rgb通道分离
    g2= image2.split()[1]  # rgb通道分离
    r2= image2.split()[2]  # rgb通道分离
 
    
    result = 0
    result1 = _dhash.classfiy_dHash(b1,b2,size=(11,10))
    result2 = _dhash.classfiy_dHash(g1,g2,size=(11,10))
    result3 = _dhash.classfiy_dHash(r1,r2,size=(11,10))

    #print(max(result3,result2,result1))

    #采用最大值就是省去了其他未画的部分的对比差异
    return max(result3,result2,result1)

