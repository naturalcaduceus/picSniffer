from tkinter import *
from PIL import  ImageTk 
from PIL import Image
import os

#函数声明
#列出windows目录下的所有文件和文件名

#图片-dHash算法
import _dhash
def startSearch():
    im1=Image.open( var1.get())
    #遍历文件夹并传到列表
    Const_Image_Format = [".jpg",".jpeg",".bmp",".png"]
    path= var2.get()
    list1=[]
    for (root, dirs, files) in os.walk(path):  
        for filename in files:
            if os.path.splitext(filename)[1] in Const_Image_Format :
                #print(os.path.join(root,filename))
                list1.append(os.path.join(root,filename))
    #遍历比较
    list2=[]
    for i in list1:
        im2=Image.open(i)
        j=_dhash.classfiy_dHash(im1,im2,size=(9,8))
        if j<=int(var3.get()):
            print(j)
            print(i)
            list2.append(str(100-3*j)+'%')
            list2.append(i)
    #在listbox显示
    lb.delete(0, END) 
    for item in list2:
        lb.insert(END, item)    
    #====================================
    load = Image.open(var1.get()) 
    render=load.resize((300,200),Image.ANTIALIAS) 
    render_ed= ImageTk.PhotoImage(render)  
    canvas.delete('all')
    canvas.create_image(0,0,anchor=NW,image=render_ed)
    #label = tk.Label(root, image=render_ed)  
    #label.pack(padx=5, pady=5)  



#窗口开始===========================================================================
root = Tk()     # 初始旷的声明
root.title('嗅图狗')#设置窗口标题
root.geometry('800x500+500+200')#设置窗口的大小宽x高+偏移量
root.resizable(width=False, height=True) #宽不可变, 高可变,默认为True

#标题
Label(root, text='嗅图狗',  bg="yellow",font=('Arial', 20)).pack(side=TOP)
frm = Frame(root)
frm.pack(fill=BOTH)

#left左边显示给定图片
frm_L = Frame(frm,bg='gray')
frm_L.pack(side=LEFT)

frm_LT = Frame(frm_L,bg='blue')
frm_LT.pack(side=TOP)

Label(frm_LT, text='要找的图片的路径', font=(15)).pack(side=TOP)
var1 = StringVar()
e1 = Entry(frm_LT,width=30,textvariable = var1)
#var1.set("请在此处输入需要查询的图片的路径")
var1.set(r'E:\1projects\毕业设计-嗅图狗\pictures\timg (11).jpg')
e1.pack()

Label(frm_LT, text='图片文件夹路径', font=(15)).pack(side=TOP)
var2 = StringVar()
e2 = Entry(frm_LT,width=30,textvariable = var2)
#var2.set("请在此处输入需要搜索的文件夹路径")
var2.set(r'E:\1projects\毕业设计-嗅图狗\pictures')
e2.pack()

var3 = StringVar()
e3 = Entry(frm_LT,width=3,textvariable=var3)
var3.set("10")
e3.pack(side=RIGHT)

def print_select(v):
    e3.config(var3.set(str(v)))
s=Scale(frm_LT,label="误差百分比", from_=0,to=100,orient=HORIZONTAL,
        length=100,showvalue=0,tickinterval=25,resolution=10,command=print_select)
s.pack(side=RIGHT)


b1 = Button(frm_LT,text="开始搜图",bg='green',width=10,height=1,
            command=startSearch)
b1.pack(side=LEFT)




#right右边显示路径
frm_R = Frame(frm,bg='gray')
frm_R.pack()

Label(frm_R, text='所找图片预览', font=(15)).pack()
canvas=Canvas(frm_R,width=400, height=400,bg='red')
image_file=PhotoImage(file='pic.png')
canvas.create_image(0,0,anchor=NW,image=image_file)
canvas.pack(side=BOTTOM)



def print_item(event):
    print (lb.get(lb.curselection()))
    #读取图像  
    im=Image.open(lb.get(lb.curselection()))  
    #显示图像  
    im.show()  


Label(frm_L, text='找到的图片路径', font=(15)).pack()
lb = Listbox(frm_L, width=60)
lb.bind('<ButtonRelease-1>', print_item)
lb.pack(side=BOTTOM)


print(var1.get())
print(var2.get())

root.mainloop()#进入消息循环