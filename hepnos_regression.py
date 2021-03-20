from matplotlib import pyplot as plt 
import numpy as np 
import os
import sys
from scipy.stats import pearsonr
import pandas
from sklearn import linear_model
  
#pid = str(sys.argv[1])

def model():
	pid = "205993"
	sdskv_putpacked_size = open("/home/srinivasan/Documents/MOCHI/hist/theta_sdskv_benchmarks/sdskv_putpacked_data_size_"+pid+"_0","r")
	sdskv_putpacked_batch_size = open("/home/srinivasan/Documents/MOCHI/hist/theta_sdskv_benchmarks/sdskv_putpacked_batch_size_"+pid+"_0","r")
	sdskv_putpacked_latency = open("/home/srinivasan/Documents/MOCHI/hist/theta_sdskv_benchmarks/sdskv_putpacked_latency_"+pid+"_0","r")
	contents1 = sdskv_putpacked_size.readlines()
	contents2 = sdskv_putpacked_latency.readlines()
	contents3 = sdskv_putpacked_batch_size.readlines()
	csv_file = open("putpacked.csv", "w")

	raw_sizes = []
	raw_batch_sizes = []
	raw_latencies = []
	for line in range(0, len(contents1)):
		size, time, _id = contents1[line].split(',')
		latency, time, _id = contents2[line].split(',')
		batch_size, time, _id = contents3[line].split(',')
		raw_sizes.append(float(size))
		raw_batch_sizes.append(float(batch_size))
		raw_latencies.append(float(latency))

	csv_file.write("BatchSize,DataSize,Latency\n")
	for elem in range(0, len(raw_sizes)):
		csv_file.write(str(raw_batch_sizes[elem])+","+str(raw_sizes[elem])+","+str(raw_latencies[elem])+"\n")

	csv_file.close()
	df = pandas.read_csv("putpacked.csv") 
	X = df[['BatchSize', 'DataSize']]
	y = df['Latency']
	regr = linear_model.LinearRegression()
	regr.fit(X, y)
	#return mymodel
	#myline = np.linspace(1, 1000000, 100)
	#fig, ax = plt.subplots(figsize =(10, 7))
	#x.scatter(np.array(raw_sizes), np.array(raw_latencies)) 
	#x.plot(myline, mymodel(myline))
	# Show plot 
	#lt.show() 
