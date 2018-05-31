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
from heapq_max import *


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
Special block of code .Will be used later for drawing the graph
plt.figure(figsize=(9,9))
pos=nx.spring_layout(DG,iterations=10)
nx.draw(DG,pos,node_size=0,alpha=0.4,edge_color='r',font_size=16)
plt.savefig("link_graph.png")
"""

#Creating a new sample graph for visualisation
"""
G=nx.DiGraph()
v_names=file_names[40:43].copy()
G.add_nodes_from(v_names)

v_edges=[]
for x in v_names:
    temp=links[x]
    for y in temp:
        v_edges.append([x,y])
    for z in temp:
        temp2=links[z]
        for a in temp:
            if( a in temp2):
                v_edges.append([z,a])



G.add_edges_from(v_edges)




print(nx.info(G))
#Writing the graph in memory
nx.write_weighted_edgelist(DG,'web.weighted.edgelist')
print("Wrote the edge list")
plt.figure(figsize=(20,20))
pos=nx.circular_layout(G)
nx.draw_networkx(G,pos,node_size=300,alpha=1.0,edge_color='r',font_size=10 ,width=0.2)
#nx.draw(DG)

plt.show()
print("GHFCGHJ")
plt.savefig("link_graph.png")
Stored the image
"""

#Calculating top 50 trusted docs for trust propogation
tr=[]
for x in file_names:
    tr.append([DG.in_degree(x),x])

heapify_max(tr)
trust=[]
for x in range(500):
    temp=heappop_max(tr)
    
for x in range(50):
    temp=heappop_max(tr)
    trust.append(temp[1])
#Storing the SEED documents
pickle.dump(trust,open("trust.pickle","wb"))
print("trust is")
#print(trust)




#Now computation of PAGERANK starts!!:
nx=len(fnames)#number of nodes
print("It is going to allocate transition matrix")
T=np.matrix(np.zeros((nx,nx)))

fi=OD((fn,i) for i,fn in enumerate (file_names))#Dict for mapping from file names to numbers to access in numpy operations
#Writing into pickle file
pickle.dump(fi,open("f2i.pickle","wb"))


print("It is going to create transition matrix")
#Creating the transition matrix from adjacency list

for row,col in DG.adj.items():
    for des,wt in col.items():
        if ((des in fi)):
            T[fi[des],fi[row]]=1/DG.out_degree(row)
        
        

print("Transition matrix created")
print(np.sum(T[:,fi["c-list.htm"]]))
t4=time.time()
print(t4-t3)

#Now adding another "RANDOM" matrix to handle spider traps and dead ends
beta=0.5
E=np.random.random(T.shape)/nx
for x in file_names:
    if (x in trust):
        for y in range(nx):
            E[fi[x],y]+=1/50

A=(beta)*T+(1-beta)*E#This is not stochastic
F=np.matrix(np.zeros(A.shape))#This will be column stochastic
for i in range(nx):
    F[:,i]=A[:,i]/np.sum(A[:,i])

pi=np.ones(nx)/nx#initialising the rank vector with random values
pi=pi/np.sum(pi)#Normalising the rank vector
R=[]
for x in pi:
    R.append([x])
print(len(R))
print("Going into main step")
evolution=[]
for i in range(10):#Taking dot product 1000 times
    print(str(i)+"  "+str(np.sum(R)))
    R=np.dot(F,R)
    evolution.append(R)

#evolution =[np.dot(F**i,pi) for i in range(50)]
plt.figure()
for i in range(10):
    plt.plot([step[i,0] for step in evolution],label=file_names[i],lw=2)
    print(str(R[fi["c-list.htm"]])+"   "+str(DG.out_degree("c-list.htm")))
plt.draw()
plt.xlabel('iterations')
plt.ylabel('rank')
plt.legend()
plt.draw()
plt.show()

pickle.dump(R,open("rank.pickle","wb"))

t5=time.time()
print(t5-t4)