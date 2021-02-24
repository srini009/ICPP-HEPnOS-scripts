from matplotlib import pyplot as plt 
import numpy as np 
import os
import sys
from scipy.stats import pearsonr
  
pid = str(sys.argv[1])
f = open("bake_write_num_entrants_"+pid+"_0","r")
contents = f.readlines()

raw_values = []
raw_times = []
init_val, init_time = contents[0].split(',')
for line in range(1, len(contents)):
	val, time = contents[line].split(',')
	raw_values.append(float(val))
	raw_times.append(float(time) - float(init_time))

#print ('Sum is ', sum(raw_values1))

fig, ax = plt.subplots(figsize =(10, 7))
ax.step(np.array(raw_times), np.array(raw_values)) 
# Show plot 
plt.show() 

