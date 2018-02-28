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
            common_strokes.append(mat.iloc[k, :].drawing)

    return common_strokes[0]



countries =[]
for i in range(len(dat)):

    row = dat.iloc[i,:]

    if row['countrycode'] not in countries:
        print(row)

        currentdata = dat.loc[dat['countrycode']==row['countrycode'],:]

        currentdata = currentdata.iloc[:,[0,1]]

        representive = get_representative(currentdata)

        countries.append([row['countrycode'],representive])

    else:
        continue


