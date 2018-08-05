from tkinter import *
from PIL import  ImageTk 
from PIL import Image
import os,shutil,sys
import tkinter.font as tkFont 
from tkinter import ttk
from tkinter.filedialog import askdirectory,askopenfilename
import tkinter.messagebox
import time,datetime
import threading
import tkinter.messagebox

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
def saveP():
    for item in tree.get_children():  
        item_text = tree.item(item,"values")  
        fileB=os.path.join(item_text[1],item_text[2]+item_text[3])#被复制
        file2B=os.path.join(var2.get(),"saveP",'fand_'+item_text[2]+item_text[3])#复制去的文件
        mycopyfile(fileB,file2B)

#函数声明
def resize(w, h, w_box, h_box, pil_image):  #图片缩放
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
  f2 = 1.0*h_box/h  
  factor = min([f1, f2])  
  width = int(w*factor)  
  height = int(h*factor)  
  return pil_image.resize((width, height), Image.ANTIALIAS) 


def selectPath():#路径选择
    path_ = askdirectory()
    var2.set(path_)

def selectPath1():#图片选择
    path_ = askopenfilename()
    var1.set(path_)

def sieve():#筛选函数
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

def Init_dog():#图像显示初始化
    global label1,label2,image4,image5,label01
    image4 = Image.open('pic.png')  #打开
    w, h = image4.size              #获取原比例    

    pil_image_resized = resize(w, h, w_box, h_box, image4)#改成合适比例函数
    image4 = ImageTk.PhotoImage(pil_image_resized)         #转成XX对象   
    label1.configure(image = image4)
    #label2.configure(image = image4)
    
    image5 = Image.open('pic.png')  #打开(因为image4全局后，这里引用上面就用不了了)
    pil_image_resized = resize(w, h, w_box1, h_box1, image5)    #改成合适比例函数
    image5 = ImageTk.PhotoImage(pil_image_resized)              #转成XX对象   
    label01.configure(image = image5)

import recommendSingl,recommendAll
def recommend(path,path2):#根据图片路径的推荐函数
    Init_dog()
    #开始显示所选 #搜索label2.configure(image = image4)
    tabControl.select(2);label3.config(text='正在生成推荐，请勿操作！！');root.update()#跳转推荐页（序号2的tab）
    a1,a2=recommendSingl.single(path)[0],recommendSingl.single(path)[1] #尽量减少运行次数，太慢了/a1是文字、a2是id
    x1.set(str(a2)+a1);root.update()
    list = recommendAll.fandSame(a2,path2)#在范围内搜索吧
    lbExecute ( list )#清空再根据列表输出lb
    showPic3(list[0])    #显示第一张
    label3.config(text='推荐已完成');root.update()
def recommend1():
    tabControl.select(2)
def recommend2(path2):#根据随机图片路径的推荐函数
    Init_dog()
    #开始显示
    tabControl.select(2);label3.config(text='正在生成推荐，请勿操作！！');root.update()#跳转推荐页（序号2的tab）
    path=randomFilePath(path2)                              #文件夹内随机选取文件
    a1,a2=recommendSingl.single(path)[0],recommendSingl.single(path)[1] #尽量减少运行次数，太慢了/a1是文字、a2是id
    x1.set(str(a2)+a1);root.update()
    list = recommendAll.fandSame(a2,path2)#在范围内搜索吧
    lbExecute ( list )#清空再根据列表输出lb
    showPic3(list[0])    #显示第一张
    label3.config(text='推荐已完成');root.update()

import random
def randomFilePath(path):#随机挑一个文件
    Rfile = []
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in [".jpg",".gif",".png"] :#筛选格式
                Rfile.append( os.path.join(root,filename) )
                # for filename in filenames:                        #输出文件信息
                #     print("parent is" + parent)
                #     print("filename is:" + filename)
                #     print("the full name of the file is:" + os.path.join(parent, filename))
    print(Rfile)
    print(len(Rfile)-1)
    try:
        x = random.randint(0, len(Rfile)-1)#若无文件或可用文件会出错
        return Rfile[x]
    except:
        print("lack available file!")
        messagebox.askokcancel('报告''找不到推荐！')
        return 'pic.png'    #返回默认图标


def Func1():#关闭推荐后的处理
    if (var4.get()==0):
        B0.configure(state='disabled')  
    elif (var4.get()==1):
        B0.configure(state='normal') 

def SearchBW():#查找黑白图片
    if  var2.get()=='' :
        tkinter.messagebox.askokcancel('啊欧','用此功能，【文件夹】的路径请完整填写')
        tabControl.select(0)#跳回第一个标签
        pass
    else:
        label3.config(text="正在处理……")
        delButton(tree)#清空表列
        time_start=time.time()#time.time()为1970.1.1到当前时间的毫秒数  
        Execute._S_BW(var2,tree,x,root)#调用黑白函数
        time_end=time.time();#time.time()为1970.1.1到当前时间的毫秒数   
        label3.config(text="耗时"+str(round(time_end-time_start,3))+'秒')#显示耗时 

def SearchFace():#查找人脸图片
    if  var2.get()=='' :
        tkinter.messagebox.askokcancel('啊欧','用此功能，【文件夹】的路径请完整填写')
        tabControl.select(0)#跳回第一个标签
        pass
    else:
        label3.config(text="正在处理……")
        delButton(tree)#清空表列
        time_start=time.time()#time.time()为1970.1.1到当前时间的毫秒数  
        Execute._S_Face(var2,tree,x,root)#调用黑白函数
        time_end=time.time();#time.time()为1970.1.1到当前时间的毫秒数   
        label3.config(text="耗时"+str(round(time_end-time_start,3))+'秒')#显示耗时 

def SearchRepeat():#查找重复图片
    if  var2.get()=='' :
        tkinter.messagebox.askokcancel('啊欧','用此功能，【文件夹】的路径请完整填写')
        tabControl.select(0)#跳回第一个标签
        pass
    else:
        label3.config(text="正在处理……")
        delButton(tree)#清空表列
        time_start=time.time()#time.time()为1970.1.1到当前时间的毫秒数  
        Execute._S_Repeat(var2,tree,x,root)#调用查重函数
        time_end=time.time();#time.time()为1970.1.1到当前时间的毫秒数   
        label3.config(text="耗时"+str(round(time_end-time_start,3))+'秒')#显示耗时 

import porn
def Isporn():#报告图片敏感程度
    if  var1.get()=='' :
        tkinter.messagebox.askokcancel('啊欧','用此功能，要检验的【图片】的路径请完整填写')
        tabControl.select(0)#跳回第一个标签
        pass
    else:
        label3.config(text="正在处理……")
        time_start=time.time()#time.time()为1970.1.1到当前时间的毫秒数  
        porn.main(var1.get())
        time_end=time.time();#time.time()为1970.1.1到当前时间的毫秒数   
        label3.config(text="耗时"+str(round(time_end-time_start,3))+'秒')#显示耗时 

import imp
imp.reload(sys)
#sys.setdefaultencoding('utf-8')
from PIL import Image
import pytesseract
def readEnglish():          #识别英文
    image = Image.open(var1.get())
    code = "识别结果：\n"+pytesseract.image_to_string(image)
    tkinter.messagebox.showinfo('报告',message=code )#弹框
  


def treeviewClick2(event):#右击打开目录
    print ('右击')
    for item in tree.selection():
        item_text = tree.item(item,"values")
        os.system("start explorer "+str(item_text[1]))

def treeviewClick1(event):#双击打开选定的图片
    print ('双击')
    for item in tree.selection():
        item_text = tree.item(item,"values")
        os.startfile(item_text[1]+'\\'+item_text[2]+item_text[3])     

def treeviewClick(event):#单击展示选定的图片
    print ('单击')
    for item in tree.selection():
        item_text = tree.item(item,"values")
        showPic2(item_text[1]+'\\'+item_text[2]+item_text[3])#调用展示图片函数
    if var4.get()==1:
        try:                                                 #防止选中的没东西时报错
            recommend(item_text[1]+'\\'+item_text[2]+item_text[3],var2.get())  #根据图片,产出标签推荐
        except:
            pass

        
def showPic3(path):
    global label01,image13
    image1 = Image.open(path)           #打开
    w, h = image1.size                  #获取原比例
    image1_resized = resize(w, h, w_box1, h_box1, image1)#改成合适比例函数
    image13= ImageTk.PhotoImage(image1_resized)         #转成XX对象
    label01.configure(image = image13)


def showPic2(path):
    global label2,image12
    image1 = Image.open(path)           #打开
    w, h = image1.size                  #获取原比例
    image1_resized = resize(w, h, w_box, h_box, image1)#改成合适比例函数
    image12= ImageTk.PhotoImage(image1_resized)         #转成XX对象
    label2.configure(image = image12)

def showPic1():
    global label1,image11
    image1 = Image.open(var1.get())     #打开
    w, h = image1.size                  #获取原比例
    image1_resized = resize(w, h, w_box, h_box, image1)#改成合适比例函数
    image11= ImageTk.PhotoImage(image1_resized)         #转成XX对象
    label1.configure(image = image11)

def treeview_sort_column1(tv, col, reverse):#Treeview、列名、排列方式（桶排序）
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column1(tv, col, not reverse))

def treeview_sort_column2(tv, col, reverse):#Treeview、列名、排列方式（数字排序）
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda t: float(t[0]), reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column2(tv, col, not reverse))

def delButton(tree):#清空tree表列
    x=tree.get_children()
    for item in x:
        tree.delete(item)

def LbClick1(event):#listbox点击
    try:
        showPic3(lb.get(lb.curselection()))
    except:
        pass

def LbClick2(event):#listbox双击
    try:
        print (lb.get(lb.curselection()))
        #读取图像  
        im=Image.open(lb.get(lb.curselection()))  
        #显示图像  
        im.show() 
    except:
        pass

def lbExecute(listT):#listbox处理
    lb.delete(0, END) #先清除
    for item in listT:#再输出
        lb.insert(END, item)    


#执行搜图
import Execute
def start():
    if var1.get()=='' or var2.get()=='' :
        tkinter.messagebox.askokcancel('啊欧','用此功能，图片以及文件夹的路径请完整填写')
        tabControl.select(0)#跳回第一个标签
        pass
    else :#路径合法，可以执行
        label3.config(text="正在处理……")
        Init_dog()#初始化图像显示
        delButton(tree)#清空表列
        showPic1()#预览所找图
        time_start=time.time()#time.time()为1970.1.1到当前时间的毫秒数  
        #搜图开【新进程没啥用】
        if numberChosen.current() == 0 :
            if var5.get()==1 :
                '''
                th1=threading.Thread(target=Execute.startSearch01(var1,var2,var3,tree,x,root))
                th1.start()
                button_img.configure(state='disabled')  #万一时间长，防止按钮连续点击
                th1.join()
                button_img.configure(state='normal')
                '''
                Execute.startSearch01(var1,var2,var3,tree,x,root)#单层文件夹
            else:
                Execute.startSearch0(var1,var2,var3,tree,x,root)#多层文件夹
        elif numberChosen.current() == 1 :
            Execute.startSearch1(var1,var2,var3,tree,x,root)
        elif numberChosen.current() == 2 :
            Execute.startSearch2(var1,var2,var3,tree,x,root)
        elif numberChosen.current() == 3 :
            Execute.startSearch3(var1,var2,var3,tree,x,root)
        elif numberChosen.current() == 4 :
            Execute.startSearch4(var1,var2,var3,tree,x,root)
        elif numberChosen.current() == 5 :
            Execute.startSearch5(var1,var2,var3,tree,x,root)
        elif numberChosen.current() == 6 :
            Execute.startSearch6(var1,var2,var3,tree,x,root)
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
root.title('嗅图狗 v0.9')#设置窗口标题
root.geometry('1150x585+500+200')#设置窗口的大小宽x高+偏移量
root.resizable(width=True, height=True) #宽不可变, 高可变,默认为True
root.iconbitmap('bitbug_favicon.ico')

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

button_img_gif = PhotoImage(file='start.png')  
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

pil_image = Image.open('pic.png')  #打开
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
tab3 = Frame(tabControl) 
tabControl.add(tab3, text='图片推荐')
tab4 = Frame(tabControl) 
tabControl.add(tab4, text='帮助及关于') 

#tab1 基本
frm_B0 = Frame(tab1,bg='green')
frm_B0.pack()

frm_B01 = Frame(frm_B0,bg='blue')
frm_B01.pack(side=TOP,fill=BOTH)
Label(frm_B01, text='所寻图片的路径', font=ft1).pack(side=LEFT)
Button(frm_B01, text = "图片选择",bg='yellow',command = selectPath1).pack(side=RIGHT)
var1 = StringVar()
e1 = Entry(frm_B01,width=300,textvariable = var1)
#var1.set("请在此处输入需要查询的图片的路径")
var1.set(r'E:\1projects\毕业设计-嗅图狗\pictures\timg (11).jpg')
e1.pack(side=RIGHT)

frm_B02 = Frame(frm_B0,bg='red')
frm_B02.pack(side=TOP,fill=BOTH)
Label(frm_B02, text='搜索范围文件夹', font=ft1).pack(side=LEFT)
Button(frm_B02, text = "路径选择",bg='yellow',command = selectPath).pack(side=RIGHT)
var2 = StringVar()
e2 = Entry(frm_B02,width=300,textvariable = var2)
#var2.set("请在此处输入需要搜索的文件夹路径")
var2.set(r'E:\1projects\毕业设计-嗅图狗\pictures')
e2.pack(side=RIGHT)

var3 = StringVar()
e3 = Entry(frm_B0,width=5,textvariable=var3)
s=Scale(frm_B0,label="相似程度", from_=0,to=100,orient=HORIZONTAL,
        length=1000,showvalue=0,tickinterval=5,resolution=1,
        variable=var3)
s.pack(side=LEFT,fill=BOTH)

var3.set("85")
e3.pack(side=LEFT,fill=BOTH)


#tab2 功能
frm_B1 = Frame(tab2,bg='gray')
frm_B1.pack(side=TOP,fill=BOTH)

Label(frm_B1, text='功能选项', font=ft1).grid(row=0,column=0,sticky=W)#勾选框
Button(frm_B1, text = "推荐相关",bg='gold',command = recommend1).grid(row=1,column=0,sticky=W)
var5=IntVar()
c01=Checkbutton(frm_B1,text='禁止文件夹\n穿透(仅支持\n特征码识图)',variable=var5).grid(row=2,column=0,rowspan=2,sticky=W)

Label(frm_B1, text='算法功能选择', font=ft1).grid(row=0,column=1,sticky=W)#下拉列表
number = StringVar()
numberChosen = ttk.Combobox(frm_B1, width=16, textvariable = number,state='readonly')
numberChosen['values'] = ('特征码识图（纹理）','直方图识图（灰度明暗）','主色调识图（色调）','文件名相似度（文件名）','小图找全图（SIFT特征）','画图识图（颜色位置）','相似人脸识图')     # 设置下拉列表的值
numberChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
numberChosen.current(0)                 # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
numberChosen.grid(row=1,column=1,sticky=W)

Label(frm_B1, text='图像甄别与其他功能', font=ft1).grid(row=0,column=2,sticky=W)#下拉列表
Button(frm_B1, text = "找出路径内所有黑白图片",bg='yellow',command = SearchBW).grid(row=1,column=2,sticky=W)
Button(frm_B1, text = "查路径内所有重复图片（纹理）",bg='yellow',command = SearchRepeat).grid(row=2,column=2,sticky=W)
Button(frm_B1, text = "识别图片英文",bg='green',command = readEnglish).grid(row=3,column=2,sticky=W)
#Button(frm_B1, text = "标签试图",bg='yellow',command =lambda : recommend2(ID=var6.get())).grid(row=3,column=2,sticky=W)
#var6 = StringVar()
#Entry(frm_B1,width=16,textvariable = var6).grid(row=3,column=2,sticky=E)
#var6.set("输入标签试试看")
Button(frm_B1, text = "查看所选单张图片敏感程度",bg='yellow',command = Isporn).grid(row=1,column=3,sticky=W)
Button(frm_B1, text = "扫描路径内所有人脸",bg='yellow',command = SearchFace).grid(row=2,column=3,sticky=W)
Button(frm_B1, text = "保存所有结果至搜索路径下‘saveP’文件夹",bg='red',command = saveP).grid(row=3,column=3,sticky=W)

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



#tab3 推荐
frm_B2 = Frame(tab3,bg='green')
frm_B2.pack(side=TOP,fill=BOTH)
w_box1=205
h_box1=109

var4=IntVar()
c02=Checkbutton(frm_B2,text='开启推荐\n（路径下图太多则建议关闭）\n需要纯净的点击预览请去掉勾！',variable=var4,command=Func1)
#c02.select()#生成时默认开启一下（推荐太耗时间、太费事了!）
c02.grid(row=0,column=1,sticky=N)

B0=Button(frm_B2, text = "随机标签\n随便看看",bg='gold',width=8,height=3,command =lambda : recommend2(path2 = var2.get() ))
B0.grid(row=0,column=0,sticky=W)
B0.configure(state='disabled') 

Label(frm_B2, text = "可能的标签：" ).grid(row=1,column=0,sticky=W)
x1=StringVar()
label5=Label(frm_B2, text = "暂无" ,textvariable = x1)
label5.grid(row=1,column=1,sticky=W)
x1.set("暂无")

pil_image = Image.open('pic.png')  #打开
w, h = pil_image.size              #获取原比例
pil_image_resized = resize(w, h, w_box1, h_box1, pil_image) #改成合适比例函数
tk_image1 = ImageTk.PhotoImage(pil_image_resized)           #转成XX对象
label01 = Label(frm_B2,image=tk_image1, width=w_box1, height=h_box1)
label01.grid(row=0,column=2, rowspan=2,sticky=W)

lb=Listbox(frm_B2, width=81,height=6)           #初始化listbox
lb.bind('<ButtonRelease-1>', LbClick1)          #单击
lb.bind('<Double-Button-1>', LbClick2)          #双击
lb.grid(row=0,column=5, rowspan=2,sticky=W)


#tab4
frm_B3 = Frame(tab4,bg='green')
frm_B3.pack(side=TOP,fill=BOTH)
t=Text(frm_B3)
t.pack(fill=BOTH)
t.insert(1.0,'帮助：\n')
t.insert(END,'选定要找的图片，选定搜索的路径，单击“go按钮”\n')
t.insert(END,'在“识图的结果”一栏中：单击展示选定的图片，双击用系统默认软件打开选定的图片，右击打开目录\n')
t.insert(END,'画图识图是你随便用画图工具画一个草图，算法能找出大致符合的图片 \n')
t.insert(END,'技巧：（想找特定主色调图片请自行油漆桶+色调识图）(文件筛选不多的话排序就好了) \n')
t.insert(END,'说明：\n')
t.insert(END,'格式不符请自行【格式工厂】处理后来搜，默认支持格式：jpg、png、bmp、gif \n')
t.insert(END,'自己做个工具图个方便，放出来大家一起方便~ \n')
t.insert(END,'本软件作者：csdn 超自然祈祷；部分图像算法来源于：segmentfault 肥肥的兔子 \n')
t.config(state="disabled")#禁止修改




print(var1.get())
print(var2.get())

root.mainloop()#进入消息循环

#灰色会出毛病；opencv的人脸会出毛病