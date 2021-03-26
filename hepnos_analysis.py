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

total_error = 0.0
total_eligible = 0.0
batch_sizes = []
latencies = []
total_runtime = 0.0

model = regressionmodel.linear_regr_model()
start = 0.0
end = 0.0

for line in range(0, len(contents3)):
	size, time, _id = contents3[line].split(',')
	latency, time, _id = contents4[line].split(',')
	batch_size, time, _id = contents6[line].split(',')
	threaddict[int(_id)] = (float(size), float(latency)*1000000.0, float(batch_size))
	ideal_width = model(threaddict[int(_id)][2])
	batch_sizes.append(float(batch_size))
	latencies.append(float(latency))
	acc_pc = ((threaddict[int(_id)][1] - ideal_width)/threaddict[int(_id)][1])*100.0
	if acc_pc < 40.0 and acc_pc > -40.0:
		total_error += 1
	if acc_pc < 100.0 and acc_pc > -100.0:
		total_eligible += 1
	if line == 0:
		start = float(time)
	if line == len(contents3) - 1:
		end = float(time) 
	#print("predicted, actual latency, and acc_pc", ideal_width, threaddict[int(_id)][1], acc_pc)

#print("Error ", (total_error/total_eligible)*100.0)

#plt.hist(per_kv_size, bins=10)
#plt.scatter(batch_sizes, latencies)
#plt.show()

total_runtime = end - start
print ("Total runtime is ", total_runtime)

i = 0

model = regressionmodel.linear_regr_model()
perf_loss_factor = defaultdict(list)
percent_of_runtime = dict()

zero_total_time = 0.0
zero_start_time = 0.0
zero_end_time = 0.0
num_zeroes = 0.0

while i < len(contents5):
	start_index = i
	end_index = i
	n, start_time, _id = contents5[i].split(',')
	start_time = float(start_time)
	end_time = float(start_time)
	zero_end_time = float(start_time)
	if(zero_start_time != 0.0):
		zero_total_time += (zero_end_time - zero_start_time)
	threadidlist = set()
	threadidlist.add(int(_id))
	max_num_entrants = float(n)
	for line_ in range (i+1, len(contents5)):
		num_entrants, time_, _id = contents5[line_].split(',')
		if float(num_entrants) == 0.00:
			end_index = line_
			end_time = float(time_)
			zero_start_time = float(time_)
			break
		threadidlist.add(int(_id))
		if float(num_entrants) > max_num_entrants:
			max_num_entrants = float(num_entrants)

	total_latency = (end_time - start_time)*1000000.0
	ideal_width = 0.0
	for id_ in threadidlist:
		ideal_width += model(threaddict[id_][2])
	latency_ratio = (total_latency/ideal_width)
	perf_loss_factor[max_num_entrants].append(latency_ratio)
	percent_of_runtime[max_num_entrants] = percent_of_runtime.get(max_num_entrants, 0.0) + (end_time - start_time)
	i = end_index + 1

for key, value in perf_loss_factor.items():
	print("Height of ", key, " has a frequency ", len(value), " sees an average perf loss factor of: ", sum(value)/len(value), " and occupies ",  (percent_of_runtime[key]/total_runtime)*100.0, " percent of runtime")
