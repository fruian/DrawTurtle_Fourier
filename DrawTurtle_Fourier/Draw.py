import math
import turtle as t
import os
import queue
import time

# 隐藏海龟
t.hideturtle()


class Draw:
    # 这个 __init__ 方法现在看起来设计的非常丑陋, 但是我也没什么好的思路, 有兴趣的可以自己重构一下
    def __init__(self, points: int = 1500, file: str = "datas.txt", title: str = '',
                 pensize: int = 2, pencolor: str = 'black', color_fill: str | tuple = '',
                 scaling_per: tuple = (50, 50,), translation: tuple = (0, 0,), flip: tuple = (0, 0,)):
        '''
        :param point:  模拟的坐标点数量
        :param FileName_in:  存储傅里叶系数集的文件地址
        :param title:  设置海龟绘图窗口的名称
        :param pensize:  画笔粗细
        :param pencolor:  画笔颜色
        :param color_fill:  封闭区域填色
        :param scaling_per:  图像百分比放缩(x,y)
        :param translation:  图像平移(right,up)
        :param flip:  图片镜像反转(x,y)
        '''
        # 基础配置
        if title != '':
            t.title(title)
        self._pencolor = pencolor
        self._fillcolor = color_fill
        self._data = []
        self._points = points
        # 实例化一个队列, 用于存储目标文件夹中的所有文件路径
        self._files = queue.Queue()
        self._file = ''

        '''
        文件批处理的初始化, 可以读取一个文件夹中的所有文件, 并将其存储到实例属性 self._files 中
        往后通过对象调用 draw 和 draws 本质就是从这个队列中拿文件的路径信息, 然后直接去访问这些文件
        这样设计, 一方面是为了支持文件批处理操作, 另一方面是为了防止重复读取部分文件影响效率
        ps. 其实这里 self._files 设计为一个迭代器更合理一点, 但是我不会做QAQ
        '''
        try:
            files = os.listdir(file)
            # print(files)  # 不是很理解的话, 可以取消这行的注释自己跑一下
            for f in files:
                self._files.put(file + '/' + f)
        except:
            self._files.put(file)

        self._pensize = pensize
        self._scaling = (scaling_per[0] / 100, scaling_per[1] / 100,)
        self.translation = translation
        self.flip = (1 if flip[0] == 0 else -1,
                     -1 if flip[1] == 0 else 1,)
        self.pi = 3.1415926535  # 这个其实设计得不好, 直接用 math.pi就行, 不用实例化, 会额外占用内存空间

    def __data_read(self):
        '''
        用于读取绘图数据, 并将其存储到 self._data 中, 用于后续绘图
        '''
        with open(self._file, 'r') as f:
            while True:
                try:
                    line = eval(f.readline())
                    self._data.append(line)
                except:
                    break

    def setting_change(self, points: int, file: str, pencolor: str, color_fill: str | tuple,
                       pensize: int, scaling_per: tuple,
                       translation: tuple, flip: tuple):
        self._data.clear()
        self._points = points if points != -1 else self._points
        if file != '-2':
            f = self._files.get()
            self._file = file if file != '-1' else f
        if pencolor != '-1':
            self._pencolor = pencolor
        if color_fill != '-1':
            self._fillcolor = color_fill
        self._pensize = pensize if pensize != -1 else self._pensize
        self._scaling = (scaling_per[0] / 100, scaling_per[1] / 100,) if scaling_per != (-1, -1,) else self._scaling
        self.translation = (self.translation[0] + translation[0],
                            self.translation[1] + translation[1],)
        self.flip = (1 if flip[0] == 0 else -1,
                     -1 if flip[1] == 0 else 1,) if flip != (-1, -1,) else self.flip

    def draws(self, is_mainloop=0, num_files_read: int = -1,
              points: int = -1, file: str = "-2", pencolor='-1', color_fill='-1',
              pensize: int = -1, scaling_per: tuple = (-1, -1,),
              translation: tuple = (0, 0,), flip: tuple = (-1, -1,)
              ):
        self.setting_change(points, file, pencolor, color_fill, pensize, scaling_per, translation, flip)

        t.color(self._pencolor)

        if num_files_read == -1:
            while not self._files.empty():
                self.draw()
        else:
            for i in range(num_files_read):
                self.draw()

        if is_mainloop == 1 or self._files.empty():
            t.mainloop()

    def draw(self, is_mainloop=0,
             points: int = -1, file: str = "-1", pencolor='-1', color_fill='-1',
             pensize: int = -1, scaling_per: tuple = (-1, -1,),
             translation: tuple = (0, 0,), flip: tuple = (-1, -1,)
             ):
        if self._files.empty():
            raise '文件已全部读取,没有新文件了'
        # 配置更新
        self.setting_change(points, file, pencolor, color_fill, pensize, scaling_per, translation, flip)

        t.color(self._pencolor)
        # print(self._fillcolor)
        if self._fillcolor != 'None':
            t.fillcolor(self._fillcolor)
            t.begin_fill()
        self.__data_read()

        N = len(self._data) + 1
        x = [0] * N
        y = [0] * N

        t.penup()
        t.pensize(self._pensize)

        # 二维傅里叶级数计算
        for n in range(self._points):
            for i in range(len(self._data)):
                if i % 2 == 0:
                    x[i] = self._data[i][0] * math.cos(i / self._points * self.pi * n) - self._data[i][1] * math.sin(
                        i / self._points * self.pi * n)
                    y[i] = self._data[i][0] * math.sin(i / self._points * self.pi * n) + self._data[i][1] * math.cos(
                        i / self._points * self.pi * n)

                else:
                    x[i] = self._data[i][0] * math.cos(-(i + 1) / self._points * self.pi * n) - self._data[i][
                        1] * math.sin(-(i + 1) / self._points * self.pi * n)
                    y[i] = self._data[i][0] * math.sin(-(i + 1) / self._points * self.pi * n) + self._data[i][
                        1] * math.cos(-(i + 1) / self._points * self.pi * n)

            t.goto(self.flip[0] * int((sum(x) + self.translation[0]) * self._scaling[0]),
                   self.flip[1] * int((sum(y) - self.translation[1]) * self._scaling[1]))
            t.pendown()

        if self._fillcolor != 'None':
            t.end_fill()

        if is_mainloop or self._files.empty():
            t.mainloop()


if __name__ == '__main__':
    draw = Draw()
    draw.draw()
