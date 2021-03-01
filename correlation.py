from matplotlib import pyplot as plt 
import numpy as np 
import os
import sys
from scipy.stats import pearsonr
  
pid = str(sys.argv[1])
f = open("bake_write_size_"+pid+"_0","r")
f2 = open("bake_write_latency_"+pid+"_0","r")
contents = f.readlines()

raw_values1 = []
for line in range(0, len(contents)):
	val, time = contents[line].split(',')
	raw_values1.append(float(val))

contents2 = f2.readlines()
raw_values2 = []
for line in range(0, len(contents2)):
	val, time = contents2[line].split(',')
	raw_values2.append(float(val)*1000000.0)
	#raw_values2.append(float(contents2[line])*1000000.0)

print ('Sum is ', sum(raw_values2))

corr, _ = pearsonr(np.array(raw_values1), np.array(raw_values2))
print('Pearsons correlation: %.3f' % corr)

fig, ax = plt.subplots(figsize =(10, 7))
ax.scatter(np.array(raw_values1), np.array(raw_values2)) 
#ax.set_ylim(0, 1000)
ax.set_xlabel("data xfer size (bytes)")
ax.set_ylabel("latency (seconds)")
  
# Show plot 
plt.show() 

