import os
import sys
import win32api
import win32con
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QPushButton, QVBoxLayout, QMessageBox, QComboBox, \
    QSystemTrayIcon, QAction, QMenu


class MyClass(QWidget):
    def __init__(self, x, y):
        super().__init__()  # 继承父类
        self.initUI()		# 自己定义的函数，初始化类界面，里面放着自己各种定义的按钮组件及布局
        self.x = x
        self.y = y

    def initUI(self):
        self.setWindowTitle("改变分辨率程序")  # 设置界面名称
        self.setWindowIcon(QIcon('./blackground.ico'))  # 设置标题图标
        self.resize(350, 200)  # 设置界面大小

        myframe = QFrame(self)  # 实例化一个QFrame可以定义一下风格样式，相当于一个框架，可以移动，其内部组件也可以移动
        btn1 = QPushButton("自适应分辨率", self)  # 定义一个按钮，括号里需要一个self，如果需要在类内传递，则应该定义为self.btn1
        btn1.clicked.connect(self.auto_fit)  # 将点击事件与自适应的函数相连，clicked表示按钮的点击事件，还有其他的功能函数，后面连接的是一个类内函数，调用时无需加括号
        btn2 = QPushButton("强行改为1024*768", self)
        btn2.clicked.connect(self.compel_fit)  # 连接一个强行改分辨率的函数
        btn3 = QPushButton("还原分辨率", self)
        btn3.clicked.connect(self.callback_fit)  # 这里将连接还原函数，具体弹出方式在函数里说明
        btn4 = QPushButton("退出程序", self)
        btn4.clicked.connect(self.close)  # 将按钮与关闭事件相连，这个关闭事件是重写的，它自带一个关闭函数，这里重写为点击关闭之后会弹窗提示是否需要关闭

        vlo = QVBoxLayout()  # 创建一个垂直布局，需要将需要垂直布局的组件添加进去
        vlo.addWidget(btn1)
        vlo.addWidget(btn2)
        vlo.addWidget(btn3)
        vlo.addWidget(btn4)
        vlo.addStretch(1)  # 一个伸缩函数，可以一定程度上防止界面放大之后排版不协调
        hlo = QVBoxLayout(self)  # 创建整体框架布局，即主界面的布局
        hlo.addLayout(vlo)  # 将按钮布局添加到主界面的布局之中
        hlo.addWidget(myframe)  # 将框架也加入到总体布局中，当然也可以不需要这框架，直接按照整体框架布局来排版
        # 之所以这里有这个myframe，是因为尝试过很多种布局，其中一个布局就是将其他组件都放到这个myframe中，移动这个myframe
        # 其里面的组件布局相对位置不会改变，后面又尝试了多种布局，所以这个myframe最后里面其实就剩下一个下拉框
        self.show()  # 显示主界面
        self.tray()  # 程序实现托盘

    def tray(self):
        # 创建托盘程序
        ti = SystemTray(self)

    def auto_fit(self):  # 自适应函数
        dm = win32api.EnumDisplaySettings(None, 0)  # 调用可以得到显示设备所有的图形模式信息
        if 1024 <= x < 1440:  # 现在的分辨率与系数的比较
            dm.PelsHeight = 768  # 屏幕的高
            dm.PelsWidth = 1024  # 屏幕的宽
            dm.BitsPerPel = 32  # 显示设备的颜色分辨率32
            dm.DisplayFixedOutput = 0  # 设置分辨率后拉伸画面，否则切换到小分辨率时，屏幕只在中间一小块
            win32api.ChangeDisplaySettings(dm, 0) # 设置生效
        elif 1440 <= x < 1600:
            dm.PelsHeight = 900
            dm.PelsWidth = 1400
            dm.BitsPerPel = 32
            dm.DisplayFixedOutput = 0
            win32api.ChangeDisplaySettings(dm, 0)
        elif x >= 1600:
            dm.PelsHeight = 900
            dm.PelsWidth = 1600
            dm.BitsPerPel = 32
            dm.DisplayFixedOutput = 0
            win32api.ChangeDisplaySettings(dm, 0)

    def compel_fit(self):
        dm = win32api.EnumDisplaySettings(None, 0)
        dm.PelsHeight = 768
        dm.PelsWidth = 1024
        dm.BitsPerPel = 32
        dm.DisplayFixedOutput = 0
        win32api.ChangeDisplaySettings(dm, 0)

    @staticmethod
    def callback_fit():
        dm = win32api.EnumDisplaySettings(None, 0)
        dm.PelsHeight = y
        dm.PelsWidth = x
        dm.BitsPerPel = 32
        dm.DisplayFixedOutput = 0
        win32api.ChangeDisplaySettings(dm, 0)

    # def closeEvent(self, event):
    #     result = QMessageBox.question(self, "提示：", "您真的要退出程序吗", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    #     if result == QMessageBox.Yes:
    #         dm = win32api.EnumDisplaySettings(None, 0)
    #         dm.PelsHeight = y
    #         dm.PelsWidth = x
    #         dm.BitsPerPel = 32
    #         dm.DisplayFixedOutput = 0
    #         win32api.ChangeDisplaySettings(dm, 0)
    #         event.accept()
    #     else:
    #         event.ignore()


class SystemTray(object):
    # 程序托盘类
    def __init__(self, w):
        self.app = app
        self.w = w
        QApplication.setQuitOnLastWindowClosed(False)  # 禁止默认的closed方法，只能使用qapp.quit()的方法退出程序
        self.w.show()  # 不设置显示则为启动最小化到托盘
        self.tp = QSystemTrayIcon(self.w)
        self.initUI()
        self.run()

    def initUI(self):
        # 设置托盘图标

        self.tp.setIcon(QIcon('./blackground.ico'))

    def quitApp(self):
        # 退出程序
        self.w.show()  # w.hide() #设置退出时是否显示主窗口
        re = QMessageBox.question(self.w, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            MyClass.callback_fit()
            self.tp.setVisible(False)  # 隐藏托盘控件，托盘图标刷新不及时，提前隐藏
            app.quit()  # 退出程序

    def message(self):
        # 提示信息被点击方法
        print("弹出的信息被点击了")

    def act(self, reason):
        # 主界面显示方法
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            self.w.show()

    def run(self):

        a1 = QAction('&显示(Show)', triggered=self.w.show)  # 托盘菜单1
        a2 = QAction('&退出(Exit)', triggered=self.quitApp)  # 托盘菜单2

        tpMenu = QMenu()  # 托盘菜单
        tpMenu.addAction(a1)
        tpMenu.addAction(a2)
        self.tp.setContextMenu(tpMenu)
        self.tp.show()  # 不调用show不会显示系统托盘消息，图标隐藏无法调用

        # 信息提示
        # 参数1：标题
        # 参数2：内容
        # 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标
        # self.tp.showMessage('Hello', '我藏好了', icon=0)
        # 绑定提醒信息点击事件
        self.tp.messageClicked.connect(self.message)
        # 绑定托盘菜单点击事件
        self.tp.activated.connect(self.act)
        sys.exit(self.app.exec_())  # 持续对app的连接


# 创立一个主界面，并保持它，从各种按钮或者组件中接受信号完成界面功能，相当于无限循环
# 只有选择退出后才会关掉程序退出循环
if __name__ == '__main__':

    app = QApplication(sys.argv)
    x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    mc = MyClass(x, y)		# 这里相当于实例化一个主界面，myclass是自己定义的主界面类
    sys.exit(app.exec_())  # 监听退出，如果选择退出，界面就会关掉
