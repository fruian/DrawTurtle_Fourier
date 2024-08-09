import math
import cmath
import re
import threading


class Fourier:
    def __init__(self, accuracy: int = 1000, file_in: str = "rawvertexes.txt", file_out: str = "datas.txt"):
        '''
        :param accuracy:  拟合精度（傅里叶系数的数量）
        :param file_in:   导入SVG信息的文件
        :param file_out:  导出计算出的坐标点集
        '''

        # 基础设置
        self._start = 0

        self._end = accuracy
        self._FileName_in = file_in
        self._FileName_out = file_out

        # 核心设置
        self._points = []  # 贝塞尔采集点
        self._out = {}  # 输出用坐标容器
        self._center = [500, 500]  # 中心点位置
        self._curWeight = []  # 各段曲线的时间权重容器
        self._trDatas = []  # 临时容器
        self._oneOver2PI = 1 / (math.pi * 2)  # 常量

    def __SVG_signal_read(self):
        with open(self._FileName_in, 'r') as f:  # 读取并解析SVG信息
            rawdata = f.readlines()
            curve = re.sub(r'\s', '', "".join(rawdata))
            cells = re.findall(r'\w[\d\,\-\.]+', curve)
            for cell in cells:
                trcdata = []
                formatString = re.sub(r'-', ',-', cell)
                trcdata.append(re.match(r'[A-Za-z]', formatString).group(0))
                rawvers = re.sub(r'[A-Za-z]\,?', '', formatString).split(',')
                for st in range(len(rawvers)):
                    rawvers[st] = float(rawvers[st])
                vergroup = []
                vercurgrp = []
                for st in range(len(rawvers)):
                    vercurgrp.append(rawvers[st])
                    if len(vercurgrp) >= 2:
                        vergroup.append(vercurgrp[0] + vercurgrp[1] * 1j)
                        vercurgrp.clear()
                if len(vercurgrp) > 0:
                    if re.match(r'v', trcdata[0], re.I):
                        vergroup.append(0 + vercurgrp[0] * 1j)
                    elif re.match(r'h', trcdata[0], re.I):
                        vergroup.append(vercurgrp[0] + 0j)
                trcdata.append(vergroup)
                self._trDatas.append(trcdata)
            print('Vertexes data have been read.')

    def __SVG_signal_analysis(self):
        for i in range(1, len(self._trDatas)):  # 解析SVG信息
            if re.match(r'[a-z]', self._trDatas[i][0]):
                for j in range(len(self._trDatas[i][1])):
                    self._trDatas[i][1][j] += self._trDatas[i - 1][1][-1]
        for i in range(len(self._trDatas)):  # 解析SVG信息
            flag = self._trDatas[i][0]
            if re.match(r'm', flag, re.I): continue
            self._trDatas[i][1].insert(0, self._trDatas[i - 1][1][-1])
            if re.match(r's', flag, re.I):
                self._trDatas[i][1].insert(1, 2 * self._trDatas[i - 1][1][-1] - self._trDatas[i - 1][1][-2])
            if re.match(r'[lvh]', flag, re.I):
                self._trDatas[i][1].insert(1, self._trDatas[i][1][0] / 3 + self._trDatas[i][1][-1] * 2 / 3)
                self._trDatas[i][1].insert(1, self._trDatas[i][1][0] * 2 / 3 + self._trDatas[i][1][-1] / 3)

        for i in range(len(self._trDatas)):  # 解析SVG信息
            flag = self._trDatas[i][0]
            if re.match(r'm', flag, re.I): continue
            self._points.append(self._trDatas[i][1])
        for i in range(len(self._points)):  # 将中心点归零
            for j in range(len(self._points[i])):
                self._points[i][j] -= self._center[0] + 1j * self._center[1]

    def __Weight_process(self):
        print("Weight process _start.")  # 计算时间权重
        wsum = 0
        for curve in self._points:  # Calculate weight
            wst = 10  # steps
            sum = 0
            for i in range(1, wst):
                sum += abs(self.__bezier(self.__linear(i, 0, wst, 0, 1), curve[0], curve[1], curve[2], curve[3]) -
                           self.__bezier(self.__linear(i - 1, 0, wst, 0, 1), curve[0], curve[1], curve[2], curve[3]))
            self._curWeight.append(sum)
            wsum += sum
        for i in range(len(self._curWeight)):
            self._curWeight[i] /= wsum
        for i in range(1, len(self._curWeight)):
            self._curWeight[i] += self._curWeight[i - 1]
        self._curWeight.insert(0, 0)
        self._curWeight[-1] = 1
        print("Weight process finished.")

    def solve(self):
        self.__SVG_signal_read()

        self.__SVG_signal_analysis()

        self.__Weight_process()

        print("Main calculation _start.")

        l = []
        for i in range(self._start, self._end + 1):
            p = threading.Thread(target=self.__produce, args=(i,))
            p.start()
            l.append(p)

        for p in l:
            p.join()

        print("Main calculation finished.")
        with open(self._FileName_out, "w") as File:
            for i in range(self._start, self._end + 1):
                File.write("{0}".format(self._out[i]))
                File.write("\n")

        print("Data saved.\n\nWork finished.\n")

    def __bezier(self, t, a, b, c, d):  # 贝塞尔函数（估测长度用）
        return (-a + 3 * b - 3 * c + d) * t * t * t + 3 * (a - 2 * b + c) * t * t + 3 * (-a + b) * t + a

    def __linear(self, x, a, b, c, d):  # 映射函数
        return (x - a) / (b - a) * (d - c) + c

    def __prSolve(self, m, cs, ce, n):  # 主要计算函数1-解析解
        if m == 0:
            return (ce - cs) * self._oneOver2PI / (n + 1)
        if n == 0:
            return 1j * self._oneOver2PI / m * (cmath.exp(-m * 1j * ce) - cmath.exp(-m * 1j * cs))
        elif n > 0:
            return 1j * self._oneOver2PI / m * cmath.exp(-m * 1j * ce) - n * 1j / ((ce - cs) * m) * self.__prSolve(m, cs,
                                                                                                                ce,
                                                                                                                n - 1)
        else:
            return 0

    def __numSolve(self, m, cs, ce, pts):  # 主要计算函数2-贝塞尔曲线方程代入
        return ((-pts[0] + 3 * pts[1] - 3 * pts[2] + pts[3]) * self.__prSolve(m, cs, ce, 3) + 3 * (
                pts[0] - 2 * pts[1] + pts[2]) * self.__prSolve(m, cs, ce, 2) + 3 * (-pts[0] + pts[1]) *
                self.__prSolve(m, cs, ce, 1) + pts[0] * self.__prSolve(m, cs, ce, 0))

    def __cpToList(self, cp):
        return [cp.real, cp.imag]

    def __produce(self, s):
        res = self.__mainCalculation(s)
        self._out[s] = res

    def __mainCalculation(self, s):
        m = 0
        if s > 0:
            m = ((s + 1) // 2) * (-1 if (s % 2 == 0) else 1)
        # print("Now working on orbit {0},m = {1}".format(s,m))
        sum = 0j
        for i in range(len(self._points)):
            cs = self.__linear(self._curWeight[i], 0, 1, 0, math.pi * 2)
            ce = self.__linear(self._curWeight[i + 1], 0, 1, 0, math.pi * 2)
            sum += self.__numSolve(m, cs, ce, self._points[i])
        return self.__cpToList(sum)


if __name__ == '__main__':
    fm = Fourier()
    fm.solve()
