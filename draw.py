#!python

from Tkinter import *
import sys

def read_raw_data(filename):
     data_file=open(filename,"r")
     ii=0
     time_label=''
     onemin_data=[]
     raw_data=[]
     for line in data_file:
	if ii > 3: 
		d1=line.strip().split()
		if time_label != d1[0]:
			time_label=d1[0]
			if len(onemin_data) != 0:
				raw_data.append(sum(onemin_data)/len(onemin_data))
				onemin_data=[]
		onemin_data.append(float(d1[1]))
	ii=ii+1
     if len(onemin_data) !=0:
	raw_data.append(sum(onemin_data)/len(onemin_data))
     data_file.close()
     return raw_data

def calcu_ma(raw_data, length):
   ma=[]
   for jj in range(length,len(raw_data)+1):
        ma.append(sum(raw_data[(jj-length):jj])/length)
   return ma

def _draw(data, d_count, color, value_max, value_min, width, height, canvas):
    value_range=value_max-value_min
    hori_step=float(width)/d_count
    first_item=d_count-len(data)
    print first_item,color,d_count
    for jj in range(d_count-1):
	if jj>=first_item:
	   canvas.create_line(int(hori_step*jj),5+int((height-10)*(value_max-data[jj-first_item])/value_range),
	       int(hori_step*(jj+1)),5+int((height-10)*(value_max-data[jj+1-first_item])/value_range),fill=color)

def draw(data, width, height, canvas):
    ma20=calcu_ma(data,20)
    ma10=calcu_ma(data,10)
    ma5=calcu_ma(data,5)
    value_max=max(data)
    value_min=min(data)
    d_count=len(data)
    _draw(data,d_count,'white',value_max,value_min,800,300,canvas)
    _draw(ma5,d_count,'orange',value_max,value_min,800,300,canvas)
    _draw(ma10,d_count,'yellow',value_max,value_min,800,300,canvas)
    _draw(ma20,d_count,'green',value_max,value_min,800,300,canvas)

raw_data=read_raw_data(sys.argv[1])

root=Tk()
root.wm_geometry("800x300+10+30")
canvas=Canvas(root,bg='black')
canvas.pack(fill=BOTH,expand=YES)
draw(raw_data,800,300,canvas)
root.mainloop()
