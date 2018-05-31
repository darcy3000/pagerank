import nltk
import math
import string
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import PorterStemmer
from nltk.corpus import stopwords
import time 
import pickle
import csv
import pandas as pd
from collections import OrderedDict as OD 
import queue as Q
from heapq_max import *
import glob
from bs4 import BeautifulSoup
import re
import numpy as np
import webbrowser

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

file_paths={}#Dict from file names to file paths:
for x,y in fnames.items():
	file_paths[y]=x





#Loading all the preprocessed data
links=pickle.load(open("net.pickle","rb"))#adjacency list
fi=pickle.load(open("f2i.pickle","rb"))#file names to index
R=pickle.load(open("rank.pickle","rb"))#Rank vector

print(len(R[1]))

#Calculatin a mapping from index to file names 
ind2f={}
for x,y in fi.items():
	ind2f[y]=x

#Now calculating a data structure to use for comparison while querying
table={}#Dict of file names to a list...
"""
for file in files:
	f=open(file,encoding='ISO-8859-1')
	data=f.read()
	soup=BeautifulSoup(data,'lxml')
	s=soup.prettify()
	
	temp=[data,R[fi[fnames[file]]][0]]
	table[fnames[file]]=temp


pickle.dump(table,open("table.pickle","wb"))
"""
#Reading data structure from pickle file

table=pickle.load(open("table.pickle","rb"))


while(1):
	query=input("Enter a query\n")
	query_tokens=query.split()

	res=[]#Going to store the final result
	score=np.zeros(len(R))
	for x in query_tokens:
		for y in files:
			temp=table[fnames[y]][0]

			if(re.search(x+"[^<]*</a",temp)!=None or re.search(x+"[^<]*</b",temp)!=None):
			#print("It has entered if")
				score[fi[fnames[y]]]+=table[fnames[y]][1]    		
			if(re.search(x+"[^<]*</h",temp)!=None):
				
				score[fi[fnames[y]]]+=0.0005
			if(re.search(x+"[^<]*</span",temp)!=None):
				score[fi[fnames[y]]]+=0.00005
			if(re.search(x+"[^<]*</b",temp)!=None):
				score[fi[fnames[y]]]+=0.00005



	for ind,x in enumerate(score):
		res.append([x,ind2f[ind]])

	#Taking the top 10 docs
	heapify_max(res)
	for x in range(15):
		temp=heappop_max(res)
		if(temp[0]==0):
			break
		print(str(temp[1])+"	"+str(temp[0]))
		#print(table[temp[1]][0])
		webbrowser.open_new_tab(file_paths[temp[1]])
	res.clear()