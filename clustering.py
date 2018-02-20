import pandas as pd
import matplotlib.pylab as plt
from sklearn import cluster
import numpy as np
from sklearn import preprocessing



file1 = pd.read_json("../house.json", lines=True)
dat = pd.DataFrame(file1)
dat.head(2)


countries =[]
for i in range(len(dat)):

    row = dat.iloc[i,:]

    if row['countrycode'] not in countries:
        print(row)

        currentdata = dat.loc[dat['countrycode']==row['countrycode'],:]

        print (currentdata.shape)

        print (currentdata.head(1))

    else:
        continue


    break