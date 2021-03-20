from matplotlib import pyplot as plt 
import numpy as np 
import os
import sys
from scipy.stats import pearsonr
import hepnos_regression as regressionmodel
from collections import defaultdict, OrderedDict



threaddict = dict()

pid = str(sys.argv[1])
sdskv_putpacked_size = open("sdskv_putpacked_data_size_"+pid+"_4","r")
sdskv_putpacked_batch_size = open("sdskv_putpacked_batch_size_"+pid+"_4","r")
sdskv_putpacked_latency = open("sdskv_putpacked_latency_"+pid+"_4","r")
sdskv_putpacked_num_entrants = open("sdskv_putpacked_num_entrants_"+pid+"_4","r")
contents3 = sdskv_putpacked_size.readlines()
contents4 = sdskv_putpacked_latency.readlines()
contents5 = sdskv_putpacked_num_entrants.readlines()
contents6 = sdskv_putpacked_batch_size.readlines()

for line in range(0, len(contents3)):
	size, time, _id = contents3[line].split(',')
	latency, time, _id = contents4[line].split(',')
	batch_size, time, _id = contents6[line].split(',')
	threaddict[int(_id)] = (float(size), float(latency), float(batch_size))

i = 0

model = regressionmodel.model()
percent_improve = defaultdict(list)
x = []
y = []

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
	
	total_latency = end_time - start_time
	total_data_size = 0.0
	avg_bw = 0.0
	for id_ in threadidlist:
		total_data_size += threaddict[id_][0]

	ideal_width = 0.0
	for id_ in threadidlist:
		per_kv_size = threaddict[id_][0]/threaddict[id_][2]
		latency_per_kv_size = threaddict[id_][1]/threaddict[id_][2]
		x.append(per_kv_size)
		y.append(latency_per_kv_size)
		latency_per_byte = latency_per_kv_size/per_kv_size
		#print("Latency per byte ", latency_per_kv_size/per_kv_size)
		ideal_width += threaddict[id_][2]*model(per_kv_size)
	percentage_improvement = ((total_latency - ideal_width)/total_latency)*100.0
	percent_improve[max_num_entrants].append(percentage_improvement)
	print("Height, percentage improvement: ", max_num_entrants, percentage_improvement)
	i = end_index + 1

#plt.plot(x)
#plt.show()
#for key, value in percent_improve.items():
#	print("In total, max_num_entrants of ", key, " decreased by ", sum(value)/len(value))

#mymodel = np.poly1d(np.polyfit(raw_sizes, raw_latencies, 3))
#myline = np.linspace(1, 1000000, 100)
#fig, ax = plt.subplots(figsize =(10, 7))
#ax.scatter(np.array(raw_sizes), np.array(raw_latencies)) 
#ax.plot(myline, mymodel(myline))
# Show plot 
#plt.show() 

