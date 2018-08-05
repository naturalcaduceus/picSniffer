#from os import startfile,path,makedirs,system,walk
import os,shutil
from tkinter import * #Tk,Label,Frame,PhotoImage,Scrollbar,StringVar,Entry,Scale
from tkinter import ttk
import tkinter.messagebox
from PIL import  ImageTk 
import tkinter.font as tkFont 
from tkinter.filedialog import askdirectory,askopenfilename
from PIL import Image
import time,datetime
import threading
import tkinter.messagebox

_icon='bitbug_favicon.ico'#'_icon.ico'
_start='start.png'#'_start.png'
_pic='pic.png'#'_pic.png'

#期望图像显示的大小  
w_box = 250
h_box = 165  

#尚未实现的提示
def lack():
    tkinter.messagebox.askokcancel('啊欧','功能暂时未实现')

#将结果保存至文件夹
def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print ("copy %s -> %s"%( srcfile,dstfile))
#保存结果图片
def saveP():
    if  var2.get()=='' :
        tkinter.messagebox.askokcancel('啊欧','用此功能，【文件夹】的路径请完整填写')
        tabControl.select(0)#跳回第一个标签
        pass
    else:
        for item in tree.get_children():  
            item_text = tree.item(item,"values")  
            fileB=os.path.join(item_text[1],item_text[2]+item_text[3])#被复制
            file2B=os.path.join(var2.get(),"saveP",'fand_'+item_text[2]+item_text[3])#复制去的文件
            mycopyfile(fileB,file2B)
            tkinter.messagebox.askokcancel('成功','图片已成功加前缀fand_保存')

#函数声明

#图片缩放
def resize(w, h, w_box, h_box, pil_image):  
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
  f2 = 1.0*h_box/h  
  factor = min([f1, f2])  
  width = int(w*factor)  
  height = int(h*factor)  
  return pil_image.resize((width, height), Image.ANTIALIAS) 

#路径选择
def selectPath():
    path_ = askdirectory()
    var2.set(path_)
#图片选择
def selectPath1():
    path_ = askopenfilename()
    var1.set(path_)
#筛选函数
def sieve():
    #if 各个值不为空，继续
    if var7.get()=='' or var8_1.get()=='' or var8_2.get()=='' or var9_1.get()=='' or var9_2.get()=='' :
        tabControl.select(1)#跳回第二个标签
        tkinter.messagebox.askokcancel('啊欧','【文件限制】请完整填写')
        pass
    else :#路径合法，可以执行
        listS=[]#所存列表
        for item in tree.get_children():  
            item_text = tree.item(item,"values")  
            #print(item_text)#遍历所有元组了
            #print(datetime.datetime.strptime(str(var9_1),"%Y-%m-%d" ))
            #文件大小符合and文件尺寸符合and时间符合(注意.get())
            #文件大小；拆尺寸的横竖；日期符合
            if(float(item_text[4])>=float(var7.get()))\
                and( int(var8_1.get())<=int(item_text[5].split('*', 2)[0]) and int(var8_2.get())<=int(item_text[5].split('*', 2)[1]) )\
                and( datetime.datetime.strptime(var9_1.get(),"%Y-%m-%d" ) \
                    <=datetime.datetime.strptime(item_text[6].split(' ', 2)[0],"%Y-%m-%d" ) and \
                    datetime.datetime.strptime(item_text[6].split(' ', 2)[0],"%Y-%m-%d" )\
                    <=datetime.datetime.strptime(var9_2.get(),"%Y-%m-%d" ) \
                    ):
                #存在列表里
                listS.append(item_text)
        delButton(tree)#清空表列
        #输出到tree
        for item_textS in listS:
            tree.insert('', END, values=[item_textS[0],item_textS[1],item_textS[2],item_textS[3],item_textS[4],item_textS[5],item_textS[6],item_textS[7]])


#查找黑白图片
def SearchBW():
    if  var2.get()=='' :
        tkinter.messagebox.askokcancel('啊欧','用此功能，【文件夹】的路径请完整填写')
        tabControl.select(0)#跳回第一个标签
        pass
    else:
        label3.config(text="正在处理……")
        delButton(tree)#清空表列
        time_start=time.time()#time.time()为1970.1.1到当前时间的毫秒数  
        _S_BW(var2,tree,x,root)#调用黑白函数
        time_end=time.time();#time.time()为1970.1.1到当前时间的毫秒数   
        label3.config(text="耗时"+str(round(time_end-time_start,3))+'秒')#显示耗时 

#查找重复图片
def SearchRepeat():
    if  var2.get()=='' :
        tkinter.messagebox.askokcancel('啊欧','用此功能，【文件夹】的路径请完整填写')
        tabControl.select(0)#跳回第一个标签
        pass
    else:
        label3.config(text="正在处理……")
        delButton(tree)#清空表列
        time_start=time.time()#time.time()为1970.1.1到当前时间的毫秒数  
        _S_Repeat(var2,tree,x,root)#调用查重函数
        time_end=time.time();#time.time()为1970.1.1到当前时间的毫秒数   
        label3.config(text="耗时"+str(round(time_end-time_start,3))+'秒')#显示耗时 

#右击打开目录
def treeviewClick2(event):
    print ('右击')
    for item in tree.selection():
        item_text = tree.item(item,"values")
        os.system("start explorer "+str(item_text[1]))
#双击打开选定的图片
def treeviewClick1(event):
    print ('双击')
    for item in tree.selection():
        item_text = tree.item(item,"values")
        os.startfile(item_text[1]+'\\'+item_text[2]+item_text[3])     
#单击展示选定的图片
def treeviewClick(event):
    print ('单击')
    for item in tree.selection():
        item_text = tree.item(item,"values")
        showPic2(item_text[1]+'\\'+item_text[2]+item_text[3])#调用展示图片函数



#显示选中该的图片
def showPic2(path):
    global label2,image12
    image1 = Image.open(path)           #打开
    w, h = image1.size                  #获取原比例
    image1_resized = resize(w, h, w_box, h_box, image1)#改成合适比例函数
    image12= ImageTk.PhotoImage(image1_resized)         #转成XX对象
    label2.configure(image = image12)
#显示被检索的图片
def showPic1():
    global label1,image11
    image1 = Image.open(var1.get())     #打开
    w, h = image1.size                  #获取原比例
    image1_resized = resize(w, h, w_box, h_box, image1)#改成合适比例函数
    image11= ImageTk.PhotoImage(image1_resized)         #转成XX对象
    label1.configure(image = image11)

#清空tree表列
def delButton(tree):
    x=tree.get_children()
    for item in x:
        tree.delete(item)

#Treeview、列名、排列方式（桶排序）
def treeview_sort_column1(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column1(tv, col, not reverse))
#Treeview、列名、排列方式（数字排序）
def treeview_sort_column2(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda t: float(t[0]), reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column2(tv, col, not reverse))

#算法陈列======================================================================
class Dhash:
    def getCode(img,size):
        result = []
        # print("x==",size[0])
        # print("y==",size[1]-1)	
        x_size = size[0]-1#width
        y_size = size[1] #high
        for x in range(0,x_size):
            for y in range(0,y_size):
                now_value = img.getpixel((x,y))
                next_value = img.getpixel((x+1,y))
                if next_value < now_value:
                    result.append(1)
                else:
                    result.append(0)
        return result

    def compCode(code1,code2):
        num = 0
        for index in range(0,len(code1)):
            if code1[index] != code2[index]:
                num+=1
        return num 

    def classfiy_dHash(image1,image2,size=(9,8)):
        image1 = image1.resize(size).convert("RGBA").convert('L')
        code1 = Dhash.getCode(image1, size)
        image2 = image2.resize(size).convert("RGBA").convert('L')
        code2 = Dhash.getCode(image2, size)
        assert len(code1) == len(code2),"error"	
        return Dhash.compCode(code1, code2)

class Histogram:
    def classfiy_histogram(image1,image2,size = (256,256)):
        image1 = image1.resize(size).convert("RGBA").convert("RGB")
        g = image1.histogram()
        image2 = image2.resize(size).convert("RGBA").convert("RGB")
        s = image2.histogram()
        assert len(g) == len(s),"error"
        data = []

        for index in range(0,len(g)):
            if g[index] != s[index]:
                data.append(1 - abs(g[index] - s[index])/max(g[index],s[index]) )
            else:
                data.append(1)
        return sum(data)/len(g)

import colorsys
import math
import numpy
class Colour:
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
            score = (saturation + 0.1) * count         
            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)     
        return dominant_color     


    def comparecolor(img1,img2,size=(200, 200)):#颜色相似算法入口
        color1=Colour.get_dominant_color(img1,size)
        color2=Colour.get_dominant_color(img2,size)
        #以RGB作为向量，计算两个颜色的欧拉距离
        v1 = numpy.array(color1)  
        v2 = numpy.array(color2)  
        rgb= numpy.linalg.norm(v1-v2)
        #441.6729是(255-0)**2+(255-0)**2+(255-0)**2的开根号
        result=(1-rgb/441.67)*100   
        return result

    #专查黑白图片，true就算黑白的
    def BWecolor(img1,size=(100, 100)):
        color1=Colour.get_dominant_color(img1,size)
        if color1[0]==color1[1]==color1[2]:
            return True
        else:
            return False


#原Execute开始=================================================================
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
_dhash = Dhash
#图片-dHash算法（单层文件夹）
def startSearch01(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get();im1=Image.open(var1.get())
    global len
    len =str(len(os.listdir(path)))#显示总文件数量
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
def startSearch0(var1,var2,var3,tree,x,root1):#所有子文件夹
    count1=0;path= var2.get();im1=Image.open(var1.get())
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
def _S_Repeat(var2,tree,h,root1):
    count1=0;path= var2.get()

    list1=[]#获取全部特征值(直接比较会很费时间)
    list2=[]
    list3=[]#最后出重复的那些组
    list4=[]
    tupl =()
    #生成搜索范围list1
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :#筛选格式

                im2=Image.open(os.path.join(root,filename))

                im2 = im2.resize(size=(7,6)).convert("RGBA").convert('L')#TMD差在这里！没转灰度？！？一天了！2018.5.9.22：30
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


#图片-histogram算法
_histogram = Histogram
def startSearch1(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get();im1=Image.open(var1.get())
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
_color = Colour
def startSearch2(var1,var2,var3,tree,x,root1):
    count1=0;path= var2.get();im1=Image.open(var1.get())
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
def _S_BW(var2,tree,x,root1):
    count1=0;path= var2.get()
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




#执行搜图
def start():
    if var1.get()=='' or var2.get()=='' :
        tkinter.messagebox.askokcancel('啊欧','用此功能，【图片】以及【文件夹】的路径请完整填写')
        tabControl.select(0)#跳回第一个标签
        pass
    else :#路径合法，可以执行
        label3.config(text="正在处理……")
        delButton(tree)#清空表列
        showPic1()#预览所找图
        time_start=time.time()#time.time()为1970.1.1到当前时间的毫秒数  
        #搜图开【新进程没啥用】
        if numberChosen.current() == 0 :
            if var5.get()==1 :
                startSearch01(var1,var2,var3,tree,x,root)#单层文件夹
            else:
                startSearch0(var1,var2,var3,tree,x,root)#多层文件夹
        elif numberChosen.current() == 1 :
            startSearch1(var1,var2,var3,tree,x,root)
        elif numberChosen.current() == 2 :
            startSearch2(var1,var2,var3,tree,x,root)
        elif numberChosen.current() == 3 :
            startSearch3(var1,var2,var3,tree,x,root)
        else :
            tkinter.messagebox.askokcancel('啊欧','算法未找到，也许正在制作中')
            return
        time_end=time.time();#time.time()为1970.1.1到当前时间的毫秒数   
        label3.config(text="耗时"+str(round(time_end-time_start,3))+'秒')#显示耗时 
        #自动筛选
        if (var4_1.get()==1):
            sieve()


            
#label=Label(root,textvariable = result, font=("黑体", 30, "bold"))
#label.grid(row=0,column=1,padx=20, pady=10,sticky=N)
#窗口开始===========================================================================
root = Tk()     # 初始旷的声明
root.title('嗅图狗 v0.9精简版')#设置窗口标题
root.geometry('1150x585+500+200')#设置窗口的大小宽x高+偏移量
root.resizable(width=True, height=True) #宽不可变, 高可变,默认为True
root.iconbitmap( _icon )

ft1 = tkFont.Font(family='Fixdsys', size=12)
ft2 = tkFont.Font(family='Fixdsys', size=10)


#标题
Label(root, text='欢迎使用嗅图狗',  bg="yellow",font=ft1).pack(side=TOP)

frm = Frame(root,bg='green')
frm.pack(side=TOP,fill=BOTH)

#底部公用
frm_BB = Frame(root,bg='blue')
frm_BB.pack(side=BOTTOM,fill=BOTH)

#按钮（右）
frm_BBB1 = Frame(frm_BB,bg='pink')
frm_BBB1.pack(side=RIGHT,fill=BOTH)

label3=Label(frm_BBB1, text='耗时', font=ft1)
label3.pack(fill=BOTH)
x=StringVar()
label4=Label(frm_BBB1,textvariable = x, font=ft1)
label4.pack(fill=BOTH)
x.set("无任务")

button_img_gif = PhotoImage(file= _start )  
button_img = Button(frm_BBB1,
                   image = button_img_gif,
                   text = '开始搜图'
                    ,width=100,height=100,command=start)  
button_img.pack(side=BOTTOM) 

#框架（左）
frm_BB1 = Frame(frm_BB,bg='blue')
frm_BB1.pack(side=LEFT,fill=BOTH)

#left左边显示信息
frm_L = Frame(frm,bg='gray')
frm_L.pack(side=LEFT)

Label(frm_L, text='识图的结果', font=(15)).pack()
columns=("a","b","c","d","e","f","g","h")
tree=ttk.Treeview(frm_L,height=18,show="headings",columns=columns )#表格 
for col in columns:
    if (col=='a')or(col=='e'):#数字排序
        tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column2(tree, _col, False))#重建标题，添加控件排序方法
    else :#默认排序
        tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column1(tree, _col, False))
tree.column('a', width=50, anchor='center') 
tree.column('b', width=340, anchor='center') 
tree.column('c', width=80, anchor='center')
tree.column('d', width=60, anchor='center')
tree.column('e', width=75, anchor='center')
tree.column('f', width=70, anchor='center')
tree.column('g', width=140, anchor='center')
tree.column('h', width=50, anchor='center')
tree.heading('a', text='相似度')
tree.heading('b', text='路径')
tree.heading('c', text='文件名')
tree.heading('d', text='文件格式')
tree.heading('e', text='文件大小KB')
tree.heading('f', text='尺寸')
tree.heading('g', text='修改时间')
tree.heading('h', text='备注')
tree.pack(side=LEFT,fill=BOTH)
tree.bind('<ButtonRelease-1>', treeviewClick)   #单击离开
tree.bind('<Double-1>', treeviewClick1)         #双击
tree.bind('<3>', treeviewClick2)                #右键

scrollBar = Scrollbar(frm_L)#tree滚动条
scrollBar.pack(side=RIGHT, fill=Y)
scrollBar.config(command=tree.yview)


#right右边展示图片
frm_R = Frame(frm,bg='gray')
frm_R.pack(fill=BOTH)
Label(frm_R, text='图片预览', font=(15)).pack()

pil_image = Image.open( _pic )  #打开
w, h = pil_image.size              #获取原比例
pil_image_resized = resize(w, h, w_box, h_box, pil_image)#改成合适比例函数
tk_image = ImageTk.PhotoImage(pil_image_resized)         #转成XX对象

Label(frm_R, text='所找图片预览', font=("Helvetica", "10")).pack()
label1 = Label(frm_R,image=tk_image, width=w_box, height=h_box)
label1.pack()

Label(frm_R, text='所选图片预览', font=("Helvetica", "10")).pack()
label2 = Label(frm_R,image=tk_image, width=w_box, height=h_box)
label2.pack() 



#tab
tabControl = ttk.Notebook(frm_BB1) # Create Tab Control
tab1 = Frame(tabControl) # Create a tab
tabControl.pack(expand=2, fill="both") # Pack to make visible
tabControl.add(tab1, text='基础识图') # Add the tab
tab2 = Frame(tabControl) 
tabControl.add(tab2, text='更多功能') 

tab4 = Frame(tabControl) 
tabControl.add(tab4, text='帮助及关于') 

#tab1 基本
frm_B0 = Frame(tab1,bg='green')
frm_B0.pack()

frm_B01 = Frame(frm_B0,bg='blue')
frm_B01.pack(side=TOP,fill=BOTH)
Label(frm_B01, text='所寻【图片】的路径', font=ft1).pack(side=LEFT)
Button(frm_B01, text = "图片选择",bg='yellow',command = selectPath1).pack(side=RIGHT)
var1 = StringVar()
e1 = Entry(frm_B01,width=300,textvariable = var1)
e1.pack(side=RIGHT)

frm_B02 = Frame(frm_B0,bg='red')
frm_B02.pack(side=TOP,fill=BOTH)
Label(frm_B02, text='搜索范围【文件夹】', font=ft1).pack(side=LEFT)
Button(frm_B02, text = "路径选择",bg='yellow',command = selectPath).pack(side=RIGHT)
var2 = StringVar()
e2 = Entry(frm_B02,width=300,textvariable = var2)
e2.pack(side=RIGHT)

var3 = StringVar()
e3 = Entry(frm_B0,width=5,textvariable=var3)
s=Scale(frm_B0,label="相似程度筛", from_=0,to=100,orient=HORIZONTAL,
        length=1000,showvalue=0,tickinterval=5,resolution=1,
        variable=var3)
s.pack(side=LEFT,fill=BOTH)

var3.set("85")
e3.pack(side=LEFT,fill=BOTH)


#tab2 功能
frm_B1 = Frame(tab2,bg='gray')
frm_B1.pack(side=TOP,fill=BOTH)

Label(frm_B1, text='功能选项', font=ft1).grid(row=0,column=0,sticky=W)#勾选框
var5=IntVar()
c01=Checkbutton(frm_B1,text='禁止文件夹\n穿透(仅支持\n特征码识图)',variable=var5).grid(row=2,column=0,rowspan=2,sticky=W)

Label(frm_B1, text='算法功能选择', font=ft1).grid(row=0,column=1,sticky=W)#下拉列表
number = StringVar()
numberChosen = ttk.Combobox(frm_B1, width=16, textvariable = number,state='readonly')
numberChosen['values'] = ('特征码识图（纹理）','直方图识图（灰度明暗）','主色调识图（色调）','文件名相似度（文件名）')     # 设置下拉列表的值
numberChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
numberChosen.current(0)                 # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
numberChosen.grid(row=1,column=1,sticky=W)

Label(frm_B1, text='图像甄别与其他功能', font=ft1).grid(row=0,column=2,sticky=W)#下拉列表
Button(frm_B1, text = "找出路径内所有黑白图片",bg='yellow',command = SearchBW).grid(row=1,column=2,sticky=W)
Button(frm_B1, text = "查路径内所有重复图片（纹理）",bg='yellow',command = SearchRepeat).grid(row=2,column=2,sticky=W)
Button(frm_B1, text = "保存所有结果至【文件夹】路径下‘saveP’文件夹",bg='red',command = saveP).grid(row=3,column=2,sticky=W)

#筛选
Label(frm_B1, text='文件筛选', font=ft1).grid(row=0,column=4,sticky=W)#范围:时间、大小
var4_1=IntVar()
c11=Checkbutton(frm_B1,text='go！自动执行筛选',variable = var4_1).grid(row=1,column=4,sticky=W)
Button(frm_B1, text = "开始筛选上方表格",bg='yellow',command = sieve).grid(row=2,column=4,sticky=E)

Label(frm_B1, text='图片大小', font=ft1).grid(row=1,column=5,sticky=W)#范围:大小
Label(frm_B1, text='最小尺寸', font=ft1).grid(row=2,column=5,sticky=W)#范围:尺寸
Label(frm_B1, text='日期区间', font=ft1).grid(row=3,column=5,sticky=W)#范围:时间

var7 = StringVar()
en1=Entry(frm_B1,width=22,textvariable = var7).grid(row=1,column=6,sticky=E)
var7.set("100")
var8_1 = StringVar()
var8_2 = StringVar()
Entry(frm_B1,width=5,textvariable = var8_1).grid(row=2,column=6,sticky=W)
Label(frm_B1, text='（横*竖）', font=ft1).grid(row=2,column=6)#范围:大小
Entry(frm_B1,width=5,textvariable = var8_2).grid(row=2,column=6,sticky=E)
var8_1.set("60")
var8_2.set("40")
var9_1 = StringVar()
var9_2 = StringVar()
Entry(frm_B1,width=10,textvariable = var9_1).grid(row=3,column=6,sticky=W)
Entry(frm_B1,width=10,textvariable = var9_2).grid(row=3,column=6,sticky=E)
var9_1.set(str((datetime.datetime.now()-datetime.timedelta(days=7)).strftime('%Y-%m-%d')))
var9_2.set(str(datetime.datetime.now().strftime('%Y-%m-%d')))



#tab4
frm_B3 = Frame(tab4,bg='green')
frm_B3.pack(side=TOP,fill=BOTH)
t=Text(frm_B3)
t.pack(fill=BOTH)
t.insert(1.0,'【能力有限，查询结果可能有误；本软件禁止商用】\n')
t.insert(END,'【本软件作者：csdn @超自然祈祷；大部分图像算法来源于：segmentfault @肥肥的兔子】 \n帮助：\n')
t.insert(END,'选定要找的图片，选定搜索的路径，单击“go按钮（注意更多功能中的筛选功能）”\n')
t.insert(END,'在“识图的结果”一栏中：【单击展示选定的图片，双击用系统默认软件打开选定的图片，右击打开目录】\n')
t.insert(END,'画图识图是你随便用画图工具画一个草图，算法能找出大致符合的图片 \n')
t.insert(END,'技巧：（想找特定主色调图片请自行油漆桶+色调识图）(文件筛选不多的话排序就好了) \n')
t.insert(END,'说明：\n')
t.insert(END,'格式不符请自行【格式工厂】处理后来搜，默认支持格式：jpg、png、bmp、gif \n')
t.insert(END,'自己做个工具图个方便，放出来大家一起方便~\n')
t.config(state="disabled")#禁止修改




print(var1.get())
print(var2.get())

root.mainloop()#进入消息循环

#灰色会出毛病；opencv的人脸会出毛病