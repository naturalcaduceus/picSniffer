from tkinter import *
from PIL import  ImageTk 
from PIL import Image
import os
import tkinter.font as tkFont 
from tkinter import ttk
from tkinter.filedialog import askdirectory,askopenfilename
import time
import datetime

Const_Image_Format = [".jpg",".jpeg",".png"]#筛选格式，局部要求的话单加

#时间转换为人话
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

#打印属性
def treePrint(tree,a,b,c,d,e,f,g,h):
    w1, h1 = f.size                                         #h不要和h1重名！！
    tree.insert('', END, values=[str(a),str(b),str(c),str(d),
                                 str(round(e/1024,2)),
                                 str(w1)+'*'+str(h1),
                                 str(TimeStampToTime(g)),
                                 str(h)])

#显示进度
def process(label,a,b):
    label.config(text=str(a)+"/"+str(b))



#都返回的是升函数，尽量是与相似度正相关的百分比
#遍历，条件（格式），算法比较，条件（相似度），输出

#图片-dHash算法（单层文件夹）
import _dhash
def startSearch01(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get();im1=Image.open(var1.get())
    global len
    len =str(len(os.listdir(path)))#显示总文件数量
    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for filename in os.listdir(path):
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=Image.open(os.path.join(path,filename))
                j=100-2.38*_dhash.classfiy_dHash(im1,im2,size=(7,6))

                count1+=1;x.set( len+'个文件中，处理了'+str(count1)+'张');root1.update()#显示处理过程

                if j>=int(var3.get()):                              #条件筛选

                    treePrint(tree,                                 #调用打印函数
                              round(j,2),
                              os.path.join(path),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(path,filename)),
                              im2,
                              os.path.getctime(os.path.join(path,filename)),
                              ""
                               )

#图片-dHash算法(多层文件夹)
import _dhash
def startSearch0(var1,var2,var3,tree,x,root1):#所有子文件夹
    count1=0;path= var2.get();im1=Image.open(var1.get())

    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                sizePingheng=51#现在只改这个就好了
                pingheng=100/(sizePingheng-1)**2
                im2=Image.open(os.path.join(root,filename))
                j=pingheng*((sizePingheng-1)**2-_dhash.classfiy_dHash(im1,im2,size=(sizePingheng,sizePingheng-1)))

                count1+=1;x.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

                if j>=int(var3.get()):                              #条件筛选

                    treePrint(tree,                                 #调用打印函数
                              round(j,2),
                              os.path.join(root),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(root,filename)),
                              im2,
                              os.path.getctime(os.path.join(root,filename)),
                              ""
                               )


#______dHash查重
import _dhash
def _S_Repeat(var2,tree,h,root1):
    count1=0;path= var2.get()

    list1=[]#获取全部特征值(直接比较会很费时间)
    list2=[]
    list3=[]#最后出重复的那些组
    list4=[]
    tupl =()
    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    #生成搜索范围list1
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=Image.open(os.path.join(root,filename))

                im2 = im2.resize(size=(7,6)).convert('L')#TMD差在这里！没转灰度？！？一天了！2018.5.9.22：30
                j=_dhash.getCode(im2,size=(7,6))

                tupl=(j,#哈希值，完整路径，root，filename
                      os.path.join(root,filename),
                      os.path.join(root),
                      filename)
                list1.append(tupl)#给列表添加（特征值，路径）的元组
                list2.append(-1)#-1为了做标记
                list4.append(-1)#记录相似度
                count1+=1;h.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

    #list2=[]#比较全部特征值
    for x in range(len(list1)):
        if list2[x]==-1:#如果list2的x1位置没有一样的，开始
            for y in range(len(list1)):
                #print(len(list1))
                if list2[y]==-1:#如果list2的y1位置还没有一样的，继续
                    k=100-2.38*_dhash.compCode(list1[x][0],list1[y][0])#比对list1里的元组的[0]的哈希值【y去找x，找到y就属于x组】~~~~~~~~~~~
                    if (k>=90):
                        list2[y]=x#组名均设为X的位置
                        list4[y]=k
                    else:
                        continue
                else:
                    continue
        else:
            continue
        #处理之后肯定没有-1，最少是自己的当前序号出现一次

    a=list2
    b = set(a) #a是另外一个列表，里面的内容是b里面的无重复项
    for zu in b:
        if a.count(zu)>=2:#print("the %d has found %d" %(zu,a.count(zu)))
            list3.append(zu)


    #现在l3有重复组号，l2是位置和组号，l1是（哈希值，路径）
    z1=0    #z1是大循环（list1的）计数变量，z是内部计数变量
    for z in list2:
        if z in list3:#如果重复2次以上（l3是重复2以上的筛选）
            similar=list4[z1]
            Prootfilename = list1[z1][1]
            Proot = list1[z1][2]
            Pfilname = list1[z1][3]
    #调用打印函数
            treePrint(tree,
                      similar,
                      Proot,
                      os.path.splitext(Pfilname)[0],
                      os.path.splitext(Pfilname)[1],
                      os.path.getsize(Prootfilename),
                      Image.open(Prootfilename),
                      os.path.getctime(Prootfilename),
                      str(z)#'组'最后排好序再输出
                      )
            # 此处开始新节点
            #for z2 in list2: #循环插入新节点
            #if z2==z  #条件
            #list2[z2]=-1#用完销毁，插入节点
        z1+=1

    #排序输出
    listS1=[]#所存列表
    for item in tree.get_children():  
        item_text = tree.item(item,"values")  
        listS1.append(item_text)#存起来所有输出项目

    listS2=sorted(listS1, key=lambda item: int(item[7]))#按组排列
    #清空表列
    x = tree.get_children()
    for item in x:
        tree.delete(item)
    #输出到tree
    for item_textS in listS2:
        tree.insert("", END, values=[item_textS[0],item_textS[1],item_textS[2],item_textS[3],item_textS[4],item_textS[5],item_textS[6],"组"+item_textS[7]])

    '''
    #按组分tree节点开始【由于与排序功能点击读取信息冲突搁置】
    newGroup='123'
    jishu=0
    for item_textS in listS2:
        jishu+=1
        if newGroup != item_textS[7]:#发现新组
            newGroup = item_textS[7]
            NG=tree.insert("",jishu,jishu,text="组"+str(newGroup),values=("1"))
        else :
            tree.insert(NG, 1, values=[item_textS[0],item_textS[1],item_textS[2],item_textS[3],item_textS[4],item_textS[5],item_textS[6],"组"+item_textS[7]])#插入同组节点
    '''




#图片-histogram算法
import _histogram
def startSearch1(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get();im1=Image.open(var1.get())

    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=Image.open(os.path.join(root,filename))
                j=100*_histogram.classfiy_histogram(im1,im2,size=(256,256))
                
                count1+=1;x.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

                if j>=int(var3.get()):                              #条件筛选

                    treePrint(tree,                                 #调用打印函数
                              round(j,2),
                              os.path.join(root),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(root,filename)),
                              im2,
                              os.path.getctime(os.path.join(root,filename)),
                              ""
                               )

#图片提取比对主色调
import _color
def startSearch2(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get();im1=Image.open(var1.get())

    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=Image.open(os.path.join(root,filename))
                j=_color.comparecolor(im1,im2,size=(200,200))
                
                count1+=1;x.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

                if j>=int(var3.get()):                              #条件筛选

                    treePrint(tree,                                 #调用打印函数
                              round(j,2),
                              os.path.join(root),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(root,filename)),
                              im2,
                              os.path.getctime(os.path.join(root,filename)),
                              ""
                               )

#_____查黑白图
import _color
def _S_BW(var2,tree,x,root1):
    count1=0;path= var2.get()

    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=Image.open(os.path.join(root,filename))
                j=_color.BWecolor(im2,size=(100,100))
                #print(str(_color.get_dominant_color(im2,size=(100,100)))+"\n"+str(os.path.join(root,filename)))#显示一下遍历的图片的rgb值
                
                count1+=1;x.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

                if j==True:                              #条件筛选

                    treePrint(tree,                                 #调用打印函数
                              "--",
                              os.path.join(root),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(root,filename)),
                              im2,
                              os.path.getctime(os.path.join(root,filename)),
                              "黑白"
                               )



#文件名相似度
import difflib
def startSearch3(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get()
    Sim1=os.path.splitext(os.path.basename(var1.get()))[0]

    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式
                
                im2=Image.open(os.path.join(root,filename))
                Sim2=os.path.splitext(os.path.join(filename))[0]
                j=100*difflib.SequenceMatcher(None, Sim1, Sim2).quick_ratio()
                
                count1+=1;x.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

                if j>=int(var3.get()):                              #条件筛选

                    treePrint(tree,                                 #调用打印函数
                              round(j,2),
                              os.path.join(root),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(root,filename)),
                              im2,
                              os.path.getctime(os.path.join(root,filename)),
                              ""
                               )


#=========================================================================================基于库-EX

#基于opencv的人脸
import _Face
def startSearch6(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get();im1=Image.open(var1.get())

    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=Image.open(os.path.join(root,filename))
                j= 100-_Face.classify_faces(im1,im2)
                #print(j)#看看相似度
                
                count1+=1;x.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

                if j>=int(var3.get()):                              #条件筛选

                    treePrint(tree,                                 #调用打印函数
                              round(j,2),
                              os.path.join(root),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(root,filename)),
                              im2,
                              os.path.getctime(os.path.join(root,filename)),
                              ""
                               )

#_____查含人脸的图
import _Face
def _S_Face(var2,tree,x,root1):
    count1=0;path= var2.get()

    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=Image.open(os.path.join(root,filename))
                j=_Face.Dface(im2)#识别人脸
                
                count1+=1;x.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

                if j:                              #列表里有东西就是有人脸

                    treePrint(tree,                                 #调用打印函数
                              "--",
                              os.path.join(root),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(root,filename)),
                              im2,
                              os.path.getctime(os.path.join(root,filename)),
                              "人脸"
                               )

                    
#sift算法局部找整体
import _locality
def startSearch4(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get();im1=var1.get()

    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=os.path.join(root,filename)
                #print(im2)
                j= _locality.classify_locality(im1,im2)
                
                count1+=1;x.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

                if j==1:                              #条件筛选

                    treePrint(tree,                                 #调用打印函数
                              '--',
                              os.path.join(root),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(root,filename)),
                              Image.open(im2),
                              os.path.getctime(os.path.join(root,filename)),
                              "包含"
                               )

#基于np的画图识图
import _draw
def startSearch5(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get();im1=var1.get()

    #Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=os.path.join(root,filename)
                #print(im2)
                j =_draw.classify_passage(im1,im2)
                
                count1+=1;x.set('已处理'+str(count1)+'张');root1.update()#显示处理过程

                if j>=int(var3.get()):                               #条件筛选

                    treePrint(tree,                                 #调用打印函数
                              round(j,2),
                              os.path.join(root),
                              os.path.splitext(filename)[0],
                              os.path.splitext(filename)[1],
                              os.path.getsize(os.path.join(root,filename)),
                              Image.open(im2),
                              os.path.getctime(os.path.join(root,filename)),
                              ""
                               )