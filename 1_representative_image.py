import pandas as pd
import matplotlib.pylab as plt
from sklearn import cluster
import numpy as np
from sklearn import preprocessing



file1 = pd.read_json("../house.json", lines=True)
dat = pd.DataFrame(file1)
dat.head(2)


def get_representative(mat):
    ##calculate mean strokes
    mean_array = []
    for j in range(len(mat)):
        mean_array.append(len(mat.iloc[j, :].drawing))
    mean_strokes = int(np.mean(mean_array)) + 1

    common_strokes = []
    for k in range(len(mat)):
        if len(mat.iloc[k, :].drawing) == mean_strokes:
            common_strokes.append(mat.iloc[k, :])


    #return common_strokes[0]
    features =[]
    for row in common_strokes:
        rowfeature =[]
        for stroke in range(mean_strokes):
            rowfeature.append([
                np.min(row.drawing[stroke][0]),
                np.max(row.drawing[stroke][0]),
                np.mean(row.drawing[stroke][0]),
                np.var(row.drawing[stroke][0]),
                np.min(row.drawing[stroke][1]),
                np.max(row.drawing[stroke][1]),
                np.mean(row.drawing[stroke][1]),
                np.var(row.drawing[stroke][1])
            ])
        features.append(np.array(rowfeature).flatten())

    df_features = pd.DataFrame(features)
    feature_mean = df_features.mean()
    dotp_array =[]
    for i in range(df_features.shape[0]):
        dotp = np.dot(df_features.iloc[i,:].values,feature_mean.values)#/np.linalg.norm(df_features.iloc[1,:].values)/np.linalg.norm(feature_mean.values)
        #angle = np.arccos(np.clip(c, -1, 1))
        dotp_array.append(dotp)

    maxindex = dotp_array.index(max(dotp_array))

    return mat.iloc[maxindex,:]



summary=[]
countries =[]

for i in range(len(dat)):

    row = dat.iloc[i,:]

    if row['countrycode'] not in countries:
        countries.append(row['countrycode'])
        currentdata = dat.loc[dat['countrycode']==row['countrycode'],:]

        representive = get_representative(currentdata)
        #break
        summary.append(representive)

    else:
        continue



df_summary= pd.DataFrame(summary)
df_summary.to_json("house_rep.json",orient='records')
