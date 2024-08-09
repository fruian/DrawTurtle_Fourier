# DrawTurtle_Fourier
基于二维傅里叶变换原理进行海龟绘图的自建模块

# 前言
1. 本项目是基于 b站@__咕小头__ 分享的相关资源创建的，开源项目地址是: __https://gitbub.com/cereslibra/TrutleAndFourier__ 。
   
2. 本项目是本人刚开始学python面向对象时候的练手项目，旨在通过套壳大佬的代码加深对面试对象程序设计的理解，做出来后个人感觉还可以。
   
3. 在学习和使用此项目前，请先到b站观看 __咕小头__ 大佬在2020年发的两个讲解视频了解原理。本人的设计只是在大佬的基础上套个壳，方便使用者调用，实现原理没有变化。


# 项目介绍
本项目的功能是通过二维傅里叶级数，实现平面内任意封闭曲线的绘制。这个封闭曲线可以理解为一笔画，而多个封闭曲线有效组合之后，就可以完成冰墩墩这样的非一笔画项目。

因此这个项目理论上可以拟合任何非极限的图形，只要你由足够的耐心去描图。

当然，这个项目其实还是更擅长画线条简单的Q版小人，

本项目架构如下：  
DrawTurtle_Fourier
> `__init__.py`
> 
> `datas.txt`  
> 测试用的绘图数据
> 
> `Draw.py`  
> 绘图模块，需要先处理好绘图数据
> 
> `Fourier.py`  
> 绘图数据处理模块，用于生成绘图数据，需要自行获取SVG格式的原始路径信息
> 
> `rawvertexes.txt`  
> 测试用的SVG格式的原始数据


本项目主要提供了 Draw 和 Fourier 这两个功能模块，其中，Draw 模块用于画图，Fourier 模块用于生成绘图数据

# 项目使用方法
项目文件布局方面可以参考 DrawTurtle 和 DrawTurtle_Fourier 的设计，不同数据分别放在不同的文件夹下。

> 但是要特别注意的是，同一个绘图项目的绘图数据要放在同一层，不然可能会出问题。比如绘制冰墩墩所需的数据都放在`bingdundun_new`这个文件下。

Draw模块主要方法：
> draw: 绘制单个绘图数据文件的数据  
> draws: 绘制多个绘图数据文件的数据，本质是多次调用 draw 方法  
> setting_change：修改实例对象中的配置信息。这个一般用不到

Fourier模块主要方法：
> sovle: 解析SVG格式数据，生成对应绘图数据的启动接口

完成一个绘图项目的一般流程：  
`获取SVG格式的原始信息-->通过Fourier模块解析出绘图数据-->通过Draw模块进行绘图`  
详细说明：  
1. `获取SVG格式的原始信息`: 需要使用`adobe illustrator`之类的绘图软件，自己先绘制一便需要的封闭曲线，然后导出SVG格式的路径信息  
2. `通过Fourier模块解析出绘图数据`: 把导出的SVG格式的路径信息所在的文件路径（file_in）、解析出来的绘图数据的存储路径（file_out）、拟合精度（accuracy)，这个三个数据直接传入Fourier中，实例化一个对象，然后直接调用这个对象的sovle()方法即可
3. `通过Draw模块进行绘图`: 通过Draw实例化一个可操作对象，然后根据实际情况不断在调用 draw() 方法的过程中调整图形信息即可
