from matplotlib import pyplot as plt 
import numpy as np 
import os
import sys
from scipy.stats import pearsonr
import regression as regressionmodel



threaddict = dict()

pid = str(sys.argv[1])
bake_eager_write_size = open("bake_eager_write_size_"+pid+"_0","r")
bake_eager_write_latency = open("bake_eager_write_latency_"+pid+"_0","r")
bake_write_size = open("bake_write_size_"+pid+"_0","r")
bake_write_latency = open("bake_write_latency_"+pid+"_0","r")
bake_write_num_entrants = open("bake_write_num_entrants_"+pid+"_0","r")
contents1 = bake_eager_write_size.readlines()
contents2 = bake_eager_write_latency.readlines()
contents3 = bake_write_size.readlines()
contents4 = bake_write_latency.readlines()
contents5 = bake_write_num_entrants.readlines()

for line in range(0, len(contents1)):
	size, time, _id = contents1[line].split(',')
	latency, time, _id = contents2[line].split(',')
	threaddict[int(_id)] = (float(size), float(latency))

for line in range(0, len(contents3)):
	size, time, _id = contents3[line].split(',')
	latency, time, _id = contents4[line].split(',')
	threaddict[int(_id)] = (float(size), float(latency))


i = 0

model = regressionmodel.model()

while i < len(contents3):
	start_index = i
	end_index = i
	n, start_time, _id = contents5[i].split(',')
	start_time = float(start_time)
	end_time = float(start_time)
	threadidlist = []
	threadidlist.append(int(_id))
	max_num_entrants = float(n)
	for line_ in range (i+1, len(contents5)):
		num_entrants, time_, _id = contents5[line_].split(',')
		if float(num_entrants) == 0.00:
			end_index = line_ - 1
			end_time = float(time_)
			break
		threadidlist.append(int(_id))
		if float(num_entrants) > max_num_entrants:
			max_num_entrants =  float(num_entrants)

	expected_width = 0.0
	ideal_width = 0.0
	for id_ in threadidlist:
		expected_width += threaddict[id_][1]
		ideal_width += model(threaddict[id_][0])
	print("Height, expected width, and ideal width of region: ", max_num_entrants, expected_width, ideal_width)
	i = end_index + 1

#mymodel = np.poly1d(np.polyfit(raw_sizes, raw_latencies, 3))
#myline = np.linspace(1, 1000000, 100)
#fig, ax = plt.subplots(figsize =(10, 7))
#ax.scatter(np.array(raw_sizes), np.array(raw_latencies)) 
#ax.plot(myline, mymodel(myline))
# Show plot 
#plt.show() 

