import tkinter as tk
import json
import webbrowser
from tkinter import messagebox
from tkinter import *
import pypinyin
from pypinyin import Style
import threading
import time

FONT_1 = ('微软雅黑',10,'normal')
FONT_2 = ('Arial',10,'normal')

class Application(tk.Frame): #tk.Frame 表示通过Application新类继承--窗口控件(框架)
    def __init__(self,master=None):#顶层的master为空
        #相当于调用父类---可以这么理解
        super().__init__() #通过super()函数去继承父类的初始化函数去初始化Application()--即初始化Frame
        self.master=master
        self.pack()  # 放置到屏幕上---还有一种方法是使用gird()函数继承于Frame
        #从列表文件里面获取信息
        self.urllist=self.readfromlist()
        if self.urllist:#如果list不为空
            self.creatWidgets()  #创建川口
            self.keywdbox.focus_set() #聚焦
            self.mainloop() #主循环
        else:
            messagebox.showinfo('错误','读取地址列表失败，请查看openlist.json文件是否存在并且格式正确。')

    def readfromlist(self):
        try:
            with open('openlist.json','r',encoding='utf-8') as f_obj:
                urllist=json.load(f_obj) #使用json方法load json文件返回一个字典
                print(urllist)
            return urllist
        except Exception:
            return  None
    '''
    进行窗口的布局
    pack(side,fill,expand,anchor)
    
side:按扭停靠在窗口的哪个位置
　　LEFT: 左  TOP: 上  RIGHT: 右 BUTTON: 下
fill:填充
　　　　x:水平方向填充
　　　　y:竖直方向填充
　　　　both:水平和竖直方向填充
　　　　none:不填充
expand:
　　　　yes:扩展整个空白区
　　　　no:不扩展
anchor:
　　　　N:北  下
　　　　E:东  右
　　　　S:南 下
　　　　W:西 左
　　　　CENTER:中间
padx:x方向的外边距
pady:y方向的外边距
ipadx:x方向的内边距
ipady：y方向的内边距
    '''
    def creatWidgets(self):
        # 创建搜索框
        self.frame1 = tk.Frame()
        self.frame1.pack(side=TOP, fill=X)
        self.kwlb = tk.Label(self.frame1, text='搜索：', font=FONT_2)
        self.kwlb.pack(side=LEFT)
        self.keywdbox = tk.Entry(self.frame1, font=FONT_2)
        self.keywdbox.pack(side=LEFT, fill=X, expand=YES)
        tk.Label(self.frame1, width=2).pack(side=RIGHT)  # 在最右侧添加一个空标签，占位对齐

        # 创建列表框
        self.frame2 = tk.Frame()
        self.frame2.pack(side=TOP, fill=X, pady=5)
        self.scrolly = tk.Scrollbar(self.frame2)
        self.scrolly.pack(side=RIGHT, fill=Y)
        self.listbox = tk.Listbox(self.frame2, width=60, height=15, font=FONT_1, yscrollcommand=self.scrolly.set)
        # 创建列表框并设置右侧滚动条
        self.listbox.pack(fill=BOTH, expand=YES)
        self.scrolly.config(command=self.listbox.yview)  # 设置滚动条绑定listbox

        # 创建添加、删除按钮
        self.frame3 = tk.Frame()
        self.frame3.pack(side=TOP, fill=BOTH, pady=10)
        Label(self.frame3, width=20).pack(side=LEFT, expand=YES)  # 增加空标签，为了调整按钮位置
        self.btnadd = Button(self.frame3, text='添加', command=self.additem)
        self.btnadd.pack(side=LEFT, expand=YES)  # expand使按钮左右有空白
        self.btnchange = Button(self.frame3, text='修改', command=self.changeitem)
        self.btnchange.pack(side=LEFT, expand=YES)
        self.btndel = Button(self.frame3, text='删除', command=self.deleteitem)
        self.btndel.pack(side=LEFT, expand=YES)
        Label(self.frame3, width=20).pack(side=RIGHT, expand=YES)

        # 加载地址列表
        for item in self.urllist:
            self.listbox.insert(END, item)  # 从尾部插入项目

            # 添加事件处理
            self.doevent()
    '''
    添加
    '''
    def additem(self):
        pw = Add_PopupDialog(self)
        self.wait_window(pw)  # 這一句很重要！！！

    '''
    修改
    '''
    def changeitem(self):
        print('hello')
    '''
    删除
    '''
    def deleteitem(self):
        index = self.listbox.curselection()
        try:
            item = self.listbox.get(index)
        except Exception:
            messagebox.showinfo('提示', '请选择需删除的项目！')
            return
        if messagebox.askyesno('删除', '删除 %s ？' % item):
            self.listbox.delete(index)
            del self.urllist[item]
            messagebox.showinfo('提示', '删除成功')
        else:
            return
    '''
    事件的处理
    '''
    def doevent(self):
        print('hello')


if __name__ =='__main__':
    root = tk.Tk()  #创建tk对象
    root.title("桌面-网址管理工具") #工具的标题
    root.resizable(0,0)

    app=Application(master=root)



