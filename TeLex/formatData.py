'''
This scripts is used to format the data in right format so that the data can be used as input to the TeLex alogrithm while learning the threshold. 
To use the data, the first column should be "time". This script takes the index column and rename it to "time". For our case, we also need some more column,
such as delBg, delIOB, delRate those were missing in the simulated data. This script takes the data and insert 6 more columns. For example, it inserts "bg_next" 
next to "bg" and calculates "delBg". Similarly it inserts IOB_next and rate_next to calculate delIOB and delRate respectively. Finally with all this changes,
it writes the new data to .csv file  
'''

import pandas as pd

#nameSuffix = [80,100,120,140,160]
nameSuffix = [180,200,220,240,260,280,300,320]

for i in nameSuffix: 
	fileName = "data_patientA_"+str(i)+".csv"
	updatedFileName = "patientA"+str(i)+".csv"
	data = pd.read_csv(fileName)

	data.rename( columns={'Unnamed: 0':'time'}, inplace=True )

	data.insert(2, "bg_next", 0)
	data.insert(3, "delBg", 0)
	data.insert(7, "IOB_next", 0)
	data.insert(8, "delIOB", 0)
	data.insert(10, "rate_next", 0)
	data.insert(11, "delRate", 0)

	data["bg_t"] = data["bg_next"].astype(float)
	data["delBg"] = data["delBg"].astype(float)
	data["IOB_t"] = data["IOB_next"].astype(float)
	data["delIOB"] = data["delIOB"].astype(float)
	data["rate_t"] = data["rate_next"].astype(float)
	data["delRate"] = data["delRate"].astype(float)

	for i in range(len(data.index)-1):
		data["bg_next"][i] = data["bg"][i+1]
	data["bg_next"][len(data.index)-1] = data["bg"][len(data.index)-1]

	for i in range(len(data.index)-1):
		data["delBg"][i] = data["bg_next"][i] - data["bg"][i]


	for i in range(len(data.index)-1):
		data["IOB_next"][i] = data["IOB"][i+1]
	data["IOB_next"][len(data.index)-1] = data["IOB"][len(data.index)-1]

	for i in range(len(data.index)-1):
		data["delIOB"][i] = data["IOB_next"][i] - data["IOB"][i]


	for i in range(len(data.index)-1):
		data["rate_next"][i] = data["rate"][i+1]
	data["rate_next"][len(data.index)-1] = data["rate"][len(data.index)-1]

	for i in range(len(data.index)-1):
		data["delRate"][i] = data["rate_next"][i] - data["rate"][i]
		

	data.to_csv(updatedFileName, index=False)