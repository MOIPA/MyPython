'''
    图形界面，qt，gtk,这里使用tk简单演示
'''
from tkinter import *
import tkinter.messagebox as messagebox

# 产生容器，必须继承Frame


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # pack 方法将widget放入到父容器中
        # label
        self.helloLabel = Label(self, text='hello , world')
        self.helloLabel.pack()
        # input
        self.nameInput = Entry(self)
        self.nameInput.pack()
        # alertButton
        self.alertButton = Button(
            self, text='say something', comman=self.hello)
        self.alertButton.pack()
        # quit
        self.quitButton = Button(self, text='quit', command=self.quit)
        self.quitButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('message', 'hello,%s' % name)


if __name__ == '__main__':
    app = Application()
    app.master.title('hello world')
    # 主消息循环
    app.mainloop()
