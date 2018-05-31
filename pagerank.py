# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 02:10:46 2017

@author: user
"""

import os
import glob
import webbrowser
from bs4 import BeautifulSoup
import time
from collections import OrderedDict as OD
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import sys
import json
import re
from networkx import *
from networkx.drawing.nx_agraph import graphviz_layout
import numpy as np
from collections import OrderedDict as OD
from matplotlib import *
import matplotlib
import random

sys.setrecursionlimit(10000)
files1=glob.glob('wpcd\\**\\*htm',recursive=True)#Storing all the names of html files 
files=[]
i=0
#Removing images and keeping only text docs
for x in files1:
    if((x.rfind('jpg.htm')>0) or (x.rfind('png.htm')>0) or (x.rfind('gif.htm')>0)):
        i+=1
    else:
        files.append(x)
print(len(files))
print(i)     

fnames={}#Dict from file paths to file names

for x in files:
    fnames[x]=x[x.rfind('\\')+1:]
    
#Creating a list of file names
file_names=[]
for x,y in fnames.items():
    file_names.append(y)
#print(fnames)

links=OD()  #Dictionary to store all the links,Values is a "list" of file names it has links to  and key is file name
t1=time.time()
i=0
#Creating the graph network
"""
for file in files:
    links[fnames[file]]=[]
    f=open(file,encoding='ISO-8859-1')
    data=f.read()
    f.close()
    soup=BeautifulSoup(data,'lxml')
    i+=1
    for link in soup.find_all('a',attrs={'href':re.compile("^..")}):
        
        if(link.get('href').rfind("htm")>0):
            temp=link.get('href')
            check=temp[temp.rfind('/')+1:]
            if(check in file_names):
                links[fnames[file]].append(temp[temp.rfind('/')+1:])
                #print(temp[temp.rfind('/')+1:])
    print(i)
"""
t2=time.time()
print(t2-t1)    
"""    
for name,nex in link.items():
    if(len(nex)==0):
        print(name)
"""

"""
pickle.dump(links,open("net.pickle","wb"))
print("Wrote the links in pickle file")
"""
#reading the adjacency list from links


links=pickle.load(open("net.pickle","rb"))
print("Read the data from pickle")


#Constructing the graph for visualisation
DG=nx.DiGraph()


DG.add_nodes_from(file_names)#File names as nodes


edges=[]
for key,values in links.items():
    eweight={}#Storing the weight for each edge
    for v in values:
        if v in eweight:
            eweight[v]+=1
        else:
            eweight[v]=1
    for nex,weight in eweight.items():
        edges.append([key,nex,{'weight':weight}])
DG.add_edges_from(edges)
t3=time.time()
print(nx.info(DG))
#Writing the graph in memory
nx.write_weighted_edgelist(DG,'web.weighted.edgelist')
print("Wrote the edge list")
print("Time to build the full graph")
print(t3-t2)
#Reading graph from the pickle file

#DG=pickle.load(open("graph.pickle","rb"))
#Visualising the graph
"""
#Special block of code .Will be used later for drawing the graph
plt.figure(figsize=(9,9))
pos=nx.spring_layout(DG,iterations=10)
nx.draw(DG,pos,node_size=0,alpha=0.4,edge_color='r',font_size=16)
plt.savefig("link_graph.png")
"""

#Creating a new sample graph for visualisation

G=nx.DiGraph()
R=pickle.load(open("rank.pickle","rb"))#Importing Rank vector to pass as size
fi=pickle.load(open("f2i.pickle","rb"))
size=[]#For changing the size
color=[]#for changing the color
groups=[]#Storing all possible set of colours
groups.append([0.4,1,0.4])
groups.append([1,1,0.2])
groups.append([1,0.2,0.2])
groups.append([1,0.6,0])
groups.append([0,0.5,0.1])
groups.append([0,0.4,0.8])



labels={}#Dict to show as graph nodes
rlabels={}#Dict of names to indices
v_nodes=["Wayne_Rooney.htm"]
#labels["Wayne_Rooney.htm"]="Wayne_Rooney.htm"
size=[]
size.append(R[fi["Wayne_Rooney.htm"]]*300000+200)
tc=R[fi["Wayne_Rooney.htm"]]*30000000
while(tc>1):
    tc=tc/10
color.append(random.choice(groups))



for x in set(links["Wayne_Rooney.htm"]):
    v_nodes.append(x)
    size.append(R[fi[x]]*300000+200)
    
    tc=R[fi[x]]*300000
    while(tc>1):
        tc=tc/10
    color.append(random.choice(groups))
    

G=DG.subgraph(v_nodes)

#This is the actual graph to be plotted
C=nx.DiGraph()

c_nodes=[]
for i,x in enumerate(v_nodes):
    c_nodes.append(i)
    labels[i]=x
    rlabels[x]=i

edge_list=list(G.edges_iter())
c_list=[]
C.add_nodes_from(c_nodes)
for x in edge_list:
    c_list.append([rlabels[x[0]],rlabels[x[1]]])

C.add_edges_from(c_list)

print(nx.info(G))
#Writing the graph in memory
nx.write_weighted_edgelist(DG,'web.weighted.edgelist')
print("Wrote the edge list")
plt.figure(figsize=(30,30))
pos=nx.circular_layout(C)

nx.draw_networkx(C,pos,node_size=size,alpha=1.0,edge_color='r',font_size=10 ,width=0.2,node_color=color,cmap=plt.cm.jet,labels=labels)
#nx.draw(DG)

plt.show()

plt.savefig("link_graph.png")
#Stored the image
