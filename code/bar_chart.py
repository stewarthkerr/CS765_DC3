import pandas as pd
import pickle
import sys
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import squarify
import altair as alt
alt.renderers.enable('notebook')


class obj:
	def __init__(self, node):
		self.node = node
		cl = []
		for child in self.node.children.keys():
			cl.append(self.node.children[child])
		cl.sort(key=lambda x:x.productCount,reverse=True)
		self.cl = cl
		self.count=0

	def onclick(self,event):
		print(event.xdata)
		if(0.5 < event.xdata <= 1.5):
			m1 = obj(self.cl[0])
			plt.close(self.fig)
			m1.make_bar()
		elif(1.5 < event.xdata <= 2.5):
			m2 = obj(self.cl[1])
			plt.close(self.fig)
			m2.make_bar()
		elif(2.5 < event.xdata <= 3.5):
			m3 = obj(self.cl[2])
			plt.close(self.fig)
			m3.make_bar()
		elif(3.5 < event.xdata <= 4.5):
			m4 = obj(self.cl[3])
			plt.close(self.fig)
			m4.make_bar()
		elif(4.5 < event.xdata <= 5.5):
			m5 = obj(self.cl[4])
			m5.make_bar()
		elif(5.5 < event.xdata <= 6.5):
			m6 = obj(self.cl[5])
			m6.make_bar()
		elif(6.5 < event.xdata <= 7.5):
			m7 = obj(self.cl[6])
			m7.make_bar()
		elif(7.5 < event.xdata <= 8.5):
			m8 = obj(self.cl[7])
			m8.make_bar()
		elif(8.5 < event.xdata <= 9.5):
			m9 = obj(self.cl[8])
			m9.make_bar()
		elif(9.5 < event.xdata <= 10.5):
			self.make_bar()
		else:
			print("Invalid input")

	def make_bar(self):
		label_l = []
		val_l = []
		i=self.count
		for i in range(self.count+9):
			label_l.append(self.cl[i].name)
			val_l.append(self.cl[i].productCount)
		i = i+1
		label_l.append("Others")
		print(val_l)
		v = 0
		while(i<len(self.cl)):
			v = v+self.cl[i].productCount
			i=i+1
		val_l.append(v)
		#self.fig = plt.figure(figsize=(15,10))
		self.fig = plt.figure(figsize=(15,10))
		print(self.fig)
		ax1 = self.fig.add_subplot(111)
		bar = ax1.bar(label_l,val_l)
		ax1.set_title("Number of product in categories")
		ax1.set_xlabel("Categories")
		ax1.set_ylabel("Number of products")
		self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
		plt.show()


with open(r"tree-all.pickle", 'rb') as file:
    rawdata = file.read()

myobj = pickle.loads(rawdata)
depth_map={}

depth_map[myobj.id]=0

def d(myobj):
    for child in myobj.children.keys():
        depth_map[myobj.children[child].id] = depth_map[myobj.children[child].parent.id] + 1
        d(myobj.children[child])

d(myobj)

fig = plt.figure(figsize=(15,10))
my_obj = obj(myobj)
my_obj.make_bar()

# def onclick(self,event):
# 	if(0.5 < event.xdata <= 1.5):
# 		make_bar(cl[0],0)
# 	elif(1.5 < event.xdata <= 2.5):
# 		make_bar(cl[1],0)
# 	elif(2.5 < event.xdata <= 3.5):
# 		make_bar(cl[2],0)
# 	elif(3.5 < event.xdata <= 4.5):
# 		make_bar(cl[3],0)
# 	elif(4.5 < event.xdata <= 5.5):
# 		make_bar(cl[4],0)
# 	elif(5.5 < event.xdata <= 5.5):
# 		make_bar(cl[5],0)
# 	elif(6.5 < event.xdata <= 5.5):
# 		make_bar(cl[6],0)
# 	elif(7.5 < event.xdata <= 5.5):
# 		make_bar(cl[7],0)
# 	elif(8.5 < event.xdata <= 5.5):
# 		make_bar(cl[8],0)
# 	elif(9.5 < event.xdata <= 5.5):
# 		make_bar(cl[],0)
# 	elif(4.5 < event.xdata <= 5.5):
# 		make_bar(cl[4],0)
# 	else:
# 		print("Invalid input")


# def make_bar(myobj,count):
#     cl = []
#     for child in myobj.children.keys():
#         cl.append(myobj.children[child])
#     cl.sort(key=lambda x:x.productCount,reverse=True)
#     label_l = []
#     val_l = []
#     i=count
#     for i in range(count+9):
#         label_l.append(cl[i].name)
#         val_l.append(cl[i].productCount)
#     i = i+1
#     label_l.append("Others")
#     print(val_l)
#     v = 0
#     while(i<len(cl)):
#         v = v+cl[i].productCount
#         i=i+1
#     val_l.append(v)
#     fig = plt.figure(figsize=(15,10))
# 	# fig.set_figheight(8)
# 	# fig.set_figwidth(10)
# 	ax1 = fig.add_subplot(211)
# 	ax2 = fig.add_subplot(212)
# 	bar = ax1.bar(label_l,val_l)
# 	ax1.set_title("Number of product in categories")
# 	ax1.set_xlabel("Categories")
# 	ax1.set_ylabel("Number of products")
# 	self.cid = fig.canvas.mpl_connect('button_press_event', onclick)




# tup = make_bar(myobj,0)
# fig = plt.figure(figsize=(15,10))
# # fig.set_figheight(8)
# # fig.set_figwidth(10)
# ax1 = fig.add_subplot(211)
# ax2 = fig.add_subplot(212)
# bar = ax1.bar(tup[0],tup[1])
# ax1.set_title("Number of product in categories")
# ax1.set_xlabel("Categories")
# ax1.set_ylabel("Number of products")
# self.cid = fig.canvas.mpl_connect('button_press_event', self.onclick)