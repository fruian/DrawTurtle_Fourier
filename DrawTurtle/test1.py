import DrawTurtle_Fourier as df

# pd = df.Fourier(file_in='SVG格式数据/bingdundun.txt',
#                 file_out='绘图数据/bingdundun_new/bingdundun42.txt', accuracy=2000)
# pd.solve()

# dr = df.Draw(file='绘图数据/datas0.txt',points=1500)
# dr.draw()

# dr = df.Draw(file='绘图数据/pi.txt',scaling_per=(300,300,),translation=(-450,70),points=500)
# dr.draw(color_fill='green')

# 冰墩墩
dr = df.Draw(file='绘图数据/bingdundun_new',scaling_per=(100,100,),translation=(-400,0,))
dr.draws(num_files_read=6,points=400,color_fill='black')
dr.draws(num_files_read=2,points=250,color_fill='None',pensize=5)

dr.draw(points=50,pensize=2,color_fill='black')
dr.draw(pencolor='white',color_fill='white')
dr.draw(pencolor='black',color_fill='black')
dr.draw(pencolor='white',color_fill='white')

dr.draw(flip=(1,0,),translation=(-127,0,),pencolor='black',color_fill='black')
dr.draw(pencolor='white',color_fill='white')
dr.draw(pencolor='black',color_fill='black')
dr.draw(pencolor='white',color_fill='white')

dr.draw(translation=(127,0,),flip=(0,0),pencolor='black',color_fill='black')
dr.draw(pencolor='black',color_fill='black')
