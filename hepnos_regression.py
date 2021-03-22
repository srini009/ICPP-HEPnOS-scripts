from matplotlib import pyplot as plt 
import numpy as np 
import os
import sys
from scipy.stats import pearsonr
import pandas
from sklearn import linear_model
  
#pid = str(sys.argv[1])

def multiple_linear_regr_model():
	raw_sizes = []
	raw_batch_sizes = []
	raw_latencies = []

	pidlist = ["21961", "43194", "137079"]

	for pid in pidlist:
		sdskv_putpacked_size = open("/home/srinivasan/Documents/MOCHI/hist/theta_sdskv_benchmarks/sdskv_putpacked_data_size_"+pid+"_0","r")
		sdskv_putpacked_batch_size = open("/home/srinivasan/Documents/MOCHI/hist/theta_sdskv_benchmarks/sdskv_putpacked_batch_size_"+pid+"_0","r")
		sdskv_putpacked_latency = open("/home/srinivasan/Documents/MOCHI/hist/theta_sdskv_benchmarks/sdskv_putpacked_latency_"+pid+"_0","r")
	#sdskv_putpacked_size = open("/home/srinivasan/Documents/MOCHI/hist/sdskv_putpacked_data_size_"+pid+"_4","r")
	#sdskv_putpacked_batch_size = open("/home/srinivasan/Documents/MOCHI/hist/sdskv_putpacked_batch_size_"+pid+"_4","r")
	#sdskv_putpacked_latency = open("/home/srinivasan/Documents/MOCHI/hist/sdskv_putpacked_latency_"+pid+"_4","r")
		contents1 = sdskv_putpacked_size.readlines()
		contents2 = sdskv_putpacked_latency.readlines()
		contents3 = sdskv_putpacked_batch_size.readlines()

		for line in range(0, len(contents1)):
			size, time, _id = contents1[line].split(',')
			latency, time, _id = contents2[line].split(',')
			batch_size, time, _id = contents3[line].split(',')
			raw_sizes.append(float(size))
			raw_batch_sizes.append(float(batch_size))
			raw_latencies.append(float(latency)*1000000.0)

	csv_file = open("putpacked.csv", "w")
	csv_file.write("BatchSize,DataSize,Latency\n")
	for elem in range(0, len(raw_sizes)):
		csv_file.write(str(raw_batch_sizes[elem])+","+str(raw_sizes[elem])+","+str(raw_latencies[elem])+"\n")

	csv_file.close()
	df = pandas.read_csv("putpacked.csv") 
	X = df[['BatchSize', 'DataSize']]
	y = df['Latency']
	regr = linear_model.LinearRegression()
	regr.fit(X, y)
	return regr

def linear_regr_model():
	pid = "21961"
	sdskv_putpacked_size = open("/home/srinivasan/Documents/MOCHI/hist/theta_sdskv_benchmarks/sdskv_putpacked_data_size_"+pid+"_0","r")
	sdskv_putpacked_batch_size = open("/home/srinivasan/Documents/MOCHI/hist/theta_sdskv_benchmarks/sdskv_putpacked_batch_size_"+pid+"_0","r")
	sdskv_putpacked_latency = open("/home/srinivasan/Documents/MOCHI/hist/theta_sdskv_benchmarks/sdskv_putpacked_latency_"+pid+"_0","r")
	#sdskv_putpacked_size = open("/home/srinivasan/Documents/MOCHI/hist/sdskv_putpacked_data_size_"+pid+"_4","r")
	#sdskv_putpacked_batch_size = open("/home/srinivasan/Documents/MOCHI/hist/sdskv_putpacked_batch_size_"+pid+"_4","r")
	#sdskv_putpacked_latency = open("/home/srinivasan/Documents/MOCHI/hist/sdskv_putpacked_latency_"+pid+"_4","r")
	contents1 = sdskv_putpacked_size.readlines()
	contents2 = sdskv_putpacked_latency.readlines()
	contents3 = sdskv_putpacked_batch_size.readlines()

	raw_sizes = []
	raw_batch_sizes = []
	raw_latencies = []
	for line in range(0, len(contents1)):
		size, time, _id = contents1[line].split(',')
		latency, time, _id = contents2[line].split(',')
		batch_size, time, _id = contents3[line].split(',')
		raw_sizes.append(float(size))
		raw_batch_sizes.append(float(batch_size))
		raw_latencies.append(float(latency)*1000000.0)
	regr = np.poly1d(np.polyfit(raw_batch_sizes, raw_latencies, 1))
	return regr


multiple_linear_regr_model()
