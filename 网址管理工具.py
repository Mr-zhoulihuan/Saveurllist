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
        index = self.listbox.curselection()
        try:
            urlname = self.listbox.get(index)
        except Exception:
            messagebox.showinfo('提示', '请选择需修改的项目！')
            return
        cw = Add_PopupDialog(self, 'change', urlname)
        self.wait_window(cw)  # 這一句很重要！！！
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
<Button-1>
鼠标点击事件  1代表左键，2代表中键，3代表右键 鼠标的位置（相对于widge）x，y会被发往event对象传入handler
<B1-Motion>
鼠标拖动事件  1代表按下左键拖动，2代表中键，3代表右键。同样的，鼠标的x，y会以event对象方式被送往handler 
<ButtonRelease-1> 
 鼠标按下之后释放
<Double-Button-1>
双击鼠标
<Leave>
这里是鼠标指针进入到widget里，并不是代表按下键盘上的Enter键
<FocusIn> <FocusOut>
上面的进入对应，鼠标离开widget
 

 
    '''
    def doevent(self):
        # self.keywdbox.bind("<Return>",self.showlist) # 按回车键，显示搜索结果
        self.keywdbox.bind("<KeyRelease>", self.showlist)  # 按任意键，显示搜索结果 一定要用keyrelease 否则字符还没有输入到Enter就进入了事件处理程序
        # self.keywdbox.bind("<BackSpace>",self.showlistAll)
        # self.keywdbox.bind("<Return>", lambda e: print('enter'))
        self.keywdbox.bind("<Delete>", self.showlistAll)
        self.listbox.bind('<Double-Button-1>', self.openurl)  # 双击打开地址
        self.listbox.bind('<Return>', self.openurl)  # 按Enter键打开地址
        self.listbox.bind('<Left>', lambda e: self.keywdbox.focus_set())  # 返回搜索框
        self.listbox.bind('<Right>', lambda e: self.keywdbox.focus_set())  # 返回搜索框
        self.keywdbox.bind("<Down>", self.jump_to_result)

    def openurl(self, event):
        self.listbox.focus_set()
        if self.listbox.curselection() == tuple():
            self.listbox.select_set(0, 0)
            return
        urlname = self.listbox.get(self.listbox.curselection())
        url = self.urllist[urlname]  # 根据key值获取对应url值

        if url is not None and url != '':
            webbrowser.open(url)
        else:
            messagebox.showinfo('Error !', '打开地址失败！地址为空。')

    def jump_to_result(self, event):
        if self.listbox.size():
            self.listbox.select_clear(0, END)
            self.listbox.select_set(0)
            self.listbox.activate(0)
            # print(self.listbox.curselection())
            self.listbox.focus_set()

    def showlistAll(self, event):
        keywd = self.keywdbox.get().strip()
        # 退格清空文本框时，重新显示列表
        print(event.keycode)
        self.keywdbox.delete(0, END)
        for item in self.urllist:
            self.listbox.insert(END, item)  # 从尾部插入

    def showlist(self, event):
        keywd = self.keywdbox.get().strip()
        print(event.keycode, keywd)
        if event.keycode == 8:
            if len(keywd) == 1:
                self.listbox.delete(0, END)
                for item in self.urllist:
                    self.listbox.insert(END, item)  # 从尾部插入
        if keywd:
            self.listbox.delete(0, END)
            # print(urllist)
            for item in self.urllist:
                if (keywd.lower() in item.lower()) or (keywd.lower() in pypinyin.slug(item.lower(), separator='') or (
                        keywd.lower() in pypinyin.slug(item.lower(), style=Style.FIRST_LETTER, separator=''))):
                    self.listbox.insert(END, item)  # 加载搜索结果
        else:
            self.listbox.delete(0, END)
            for item in self.urllist:
                self.listbox.insert(END, item)  # 空字符时，加载所有列表


'''
Toplevel组件通常用在显示额外的窗口、对话框或者其他弹出窗口上
要点：
弹窗，显式地保存父窗口，显式地修改父窗口数据，显式地更新父窗口部件，最后销毁弹窗
主窗，待弹窗运行后，通过wait_window方法，返回 None

grid()---布局
row=x,column=y：将控件放在x行，y列的位置
columnspan： 设置单元格横向跨越的列数，即控件占据的列数（宽度） 
rowspan：设置单元格纵向跨越的行数，即控件占据的行数（高度）
ipadx：设置控件里面水平方向空白区域大小
ipady：设置控件里面垂直方向空白区域大小
padx：设置控件周围水平方向空白区域保留大小
pady：设置控件周围垂直方向空白区域保留大小
sticky:默认的控件在窗口中的对齐方式是居中。
可以使用sticky选项去指定对齐方式，
可以选择的值有：N/S/E/W，分别代表上对齐/下对齐/左对齐/右对齐，
可以单独使用N/S/E/W，也可以上下和左右组合使用，达到不同的对齐效果
'''
class Add_PopupDialog(tk.Toplevel):
    def __init__(self,parent,add_or_change = 'new',aim_urlname = None):
        super().__init__()
        self.runmod = add_or_change
        self.aim_urlname = aim_urlname
        sw = self.winfo_screenwidth()  # 屏幕宽度
        sh = self.winfo_screenheight() - 100  # 屏幕高度
        ww = 400  # 窗口宽度
        wh = 120  # 窗口高度
        x = (sw - ww) / 2  # 计算窗口坐标点x
        y = (sh - wh) / 2  # 计算窗口坐标点y
        self.geometry("%dx%d+%d+%d" % (ww, wh, x, y))  # 设置窗口大小和布局位置
        self.resizable(0, 0)  # 设置 x,y方向都不可以缩放

        self.parent = parent  #显式地保留父窗口
        frame = tk.Frame(self)  # 创建一个frame
        frame.grid()  # 布置此frame

        # 第一行  名称：[输入框]
        tk.Label(frame, text='名称：').grid(row=0, column=0, sticky=E, pady=8)  # 0行0列左对齐，y方向8像素空格
        self.name = tk.StringVar()  # 创建name 字符串变量
        # 输入框 横跨4列 .在Entry中设定初始值，使用textvariable将变量与Entry绑定
        tk.Entry(frame, textvariable=self.name, width=50).grid(row=0, column=1, columnspan=4, sticky=W, pady=8)
        # 输入框0行1列跨越4列，右对齐，y方向空格8像素

        # 第二行  路径：[输入框]
        tk.Label(frame, text='路径：').grid(row=1, column=0, sticky=E, pady=8)  # 1行0列左对齐，y方向8像素空格
        self.url = tk.StringVar()  # 创建 url 字符串变量
        tk.Entry(frame, textvariable=self.url, width=50).grid(row=1, column=1, columnspan=4, sticky=W, pady=8)

        # 第三行 [确定]  [取消]
        tk.Button(frame, text="确定", command=self.ok).grid(row=2, column=2, sticky=W, pady=10)  # 确定按钮对应ok方法
        tk.Button(frame, text="取消", command=self.cancel).grid(row=2, column=3, sticky=S, pady=10)  # 取消按钮对应cancel方法

        if self.runmod == 'new':
            self.title('添加快捷路径')
        else:
            self.title('修改快捷路径')
            self.name.set(aim_urlname)
            self.url.set(self.parent.urllist[aim_urlname])

    def ok(self):  # ok键按下
        urlname=self.name.get().strip() #获取名称的并去掉首尾两边的空格
        print(urlname)
        url = self.url.get().strip() #获取需要保存的路径
        if url == "" or urlname == "":
            messagebox.showwarning('提示', '输入不能为空！')
            return
        else:
            if urlname in self.parent.urllist:
                if messagebox.askyesno('提示', '名称‘%s’已经存在，将进行覆盖，是否继续？' % urlname):
                    pass  # pass是为了直接跳转到后面进行赋值操作，将url写入urllist字典中
                else:
                    return
            # 列表字典中添加或更新项目
            print(self.parent.urllist.pop(self.aim_urlname, None))
            self.parent.urllist[urlname] = url
            # 重新加载列表字典
            self.parent.listbox.delete(0, END)  # 清空父窗口中listbox中的内容
            for item in self.parent.urllist:
                self.parent.listbox.insert(END, item)  # 循环添加项目到父窗口的listbox中
            self.destroy()  # 自己销毁自己窗口

    def cancel(self):
        self.destroy()

    def show(root):
        """"""
        root.update()
        root.deiconify()

    def hide(root):
        """"""
        root.withdraw()


if __name__ =='__main__':
    root = tk.Tk()  #创建tk对象
    root.title("桌面-网址管理工具") #工具的标题
    root.resizable(0,0)

    app=Application(master=root)

    if app.urllist:
        app.saveUrlList()
    print("taskmain end")
