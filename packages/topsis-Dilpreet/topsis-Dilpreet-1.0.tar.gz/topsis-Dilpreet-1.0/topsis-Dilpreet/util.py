import pandas as pd
import numpy as np

def topsis(filename,weight,impact):

	w=np.array(weight)
	i=np.array(impact)

	data = pd.read_csv(filename+'.csv')
	data = data.values[:,1:]

	#print(data)

	# Taking axis=0 to sum values along column
	normalizationFactor=np.sqrt(np.sum(data**2,axis=0,dtype=float),dtype=float)

	# Broadcasting operation to divide Xij with normalization factor
	#print(normalizationFactor.shape)
	normalizedData=(data/normalizationFactor)


	#Rounding normalized data values to 3 decimal places
	normalizedData=np.round(normalizedData.astype(np.float64),decimals=3)
	#print(normalizedData)

	# Broadcasting operationn to multiply weight Xij with Wi
	#print(w.shape)
	wgtNormalizedData=normalizedData*w
	#print(wgtNormalizedData)

	idealBest=[]
	idealWorst=[]

	for x in range(data.shape[1]):
	    if i[x]==1:
	        idealBest.append(max(wgtNormalizedData[:,x]))
	        idealWorst.append(min(wgtNormalizedData[:,x]))
	    if i[x]==0:
	        idealBest.append(min(wgtNormalizedData[:,x]))
	        idealWorst.append(max(wgtNormalizedData[:,x]))

	#print("Best: ",idealBest)
	#print("Worst: ",idealWorst)

	distanceFromBest=np.sqrt(np.sum((wgtNormalizedData-idealBest)**2,axis=1,dtype=float),dtype=float)
	distanceFromBest=distanceFromBest.reshape(distanceFromBest.shape[0],-1)

	distanceFromWorst=np.sqrt(np.sum((wgtNormalizedData-idealWorst)**2,axis=1,dtype=float),dtype=float)
	distanceFromWorst=distanceFromWorst.reshape(distanceFromWorst.shape[0],-1)

	#print("DW",distanceFromWorst)
	#print("DB",distanceFromBest)

	totalDistance=distanceFromBest+distanceFromWorst
	#print("TD",totalDistance)

	performance=distanceFromWorst/totalDistance
	#print(performance)

	order = performance.argsort(axis=0)
	#print(order)
	ranks = order.argsort(axis=0)

	# Converting ranks to 1-d numpy array
	ranks=ranks.reshape(ranks.shape[0],)

	print("Item","Rank",sep="\t")
	for idx,x in enumerate(ranks):
	    print(idx+1,ranks.shape[0]-(x),sep="\t",end="\n")
