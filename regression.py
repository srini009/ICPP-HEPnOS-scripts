from matplotlib import pyplot as plt 
import numpy as np 
import os
import sys
from scipy.stats import pearsonr
  
pid = str(sys.argv[1])
bake_eager_write_size = open("bake_eager_write_size_"+pid+"_0","r")
bake_eager_write_latency = open("bake_eager_write_latency_"+pid+"_0","r")
bake_write_size = open("bake_write_size_"+pid+"_0","r")
bake_write_latency = open("bake_write_latency_"+pid+"_0","r")
contents1 = bake_eager_write_size.readlines()
contents2 = bake_eager_write_latency.readlines()
contents3 = bake_write_size.readlines()
contents4 = bake_write_latency.readlines()

raw_sizes = []
raw_latencies = []
for line in range(0, len(contents1)):
	size, time, _id = contents1[line].split(',')
	latency, time, _id = contents2[line].split(',')
	raw_sizes.append(float(size))
	raw_latencies.append(float(latency))

for line in range(0, len(contents3)):
	size, time, _id = contents3[line].split(',')
	latency, time, _id = contents4[line].split(',')
	raw_sizes.append(float(size))
	raw_latencies.append(float(latency))

mymodel = np.poly1d(np.polyfit(raw_sizes, raw_latencies, 3))
myline = np.linspace(1, 1000000, 100)
fig, ax = plt.subplots(figsize =(10, 7))
ax.scatter(np.array(raw_sizes), np.array(raw_latencies)) 
ax.plot(myline, mymodel(myline))
# Show plot 
plt.show() 

