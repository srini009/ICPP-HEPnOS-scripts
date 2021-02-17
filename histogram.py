from matplotlib import pyplot as plt 
import numpy as np 
import os
import sys
  

f = open("putpacked_latency_204008_4","r")
contents = f.readlines()
num, min_, max_ = contents[0].split(',') 

num = int(num)
min_ = float(min_)
max_ = float(max_)

bucket_num = []
for line in range(1, len(contents)):
	bucket_num.append(int(contents[line]))
# Creating dataset 

print ("Bucket num ", bucket_num)

a = np.array(bucket_num) 

bins = []
delta = (max_ - min_)/num

print ("Delta is ", delta)

for i in range(0, num):
	bins.append(min_ + delta*i)

raw_data = []
for count, item in enumerate(bins):
	for times in range(0, bucket_num[count]):
		raw_data.append(item)
print ("Bins are ", bins)
# Creating histogram 
fig, ax = plt.subplots(figsize =(10, 7)) 
ax.hist(raw_data, bins=bins) 
  
# Show plot 
plt.show() 
