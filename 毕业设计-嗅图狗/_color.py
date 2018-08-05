import colorsys
import math
from PIL import Image
import numpy
  
def get_dominant_color(image,size):
    #颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')     
    #生成缩略图，减少计算量，减小cpu压力
    image.thumbnail(size)
     
    max_score = 0       #None
    dominant_color = (0,0,0)  #None……人家毕竟是元组，弄成int的0会各种问题！而且元组也要位数相等
     
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue    
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]        
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)        
        y = (y - 16.0) / (235 - 16)         
        # 忽略高亮色
        if y > 0.9:
            continue         
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
         
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
     
    return dominant_color
     


def comparecolor(img1,img2,size=(200, 200)):#颜色相似算法入口
    color1=get_dominant_color(img1,size)
    color2=get_dominant_color(img2,size)

    #以RGB作为向量，计算两个颜色的欧拉距离
    v1 = numpy.array(color1)  
    v2 = numpy.array(color2)  
    rgb= numpy.linalg.norm(v1-v2)
    #441.6729是(255-0)**2+(255-0)**2+(255-0)**2的开根号
    result=(1-rgb/441.67)*100   
    return result







def BWecolor(img1,size=(100, 100)):#专查黑白图片，true就算黑白的
    color1=get_dominant_color(img1,size)

    if color1[0]==color1[1]==color1[2]:
        return True
    else:
        return False





def ColorToBlack():#彩图转黑白【本算法用不上】
    image_file = Image.open(r'C:\Users\23216\Desktop\1.jpg') # open colour image
    image_file = image_file.convert('1') # convert image to black and white
    image_file.save('result.png')