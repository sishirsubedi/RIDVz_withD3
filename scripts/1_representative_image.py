import pandas as pd
import matplotlib.pylab as plt
from sklearn import cluster
import numpy as np
from sklearn import preprocessing
from scipy.spatial import distance
import json

# with open('house_rep.json') as f:
#    data = json.load(f)

file1 = pd.read_json("dog.json", lines=True)
dat = pd.DataFrame(file1)
print(dat.head(2))


def get_representative(mat):

    if mat.shape[0] <25: ## not enough data for variance
        return mat.iloc[0,:]

    ##calculate mean strokes
    mean_array = []
    for j in range(len(mat)):
        mean_array.append(len(mat.iloc[j, :].drawing))
    mean_strokes = int(np.mean(mean_array)) + 1

    common_strokes = []
    for k in range(len(mat)):
        if len(mat.iloc[k, :].drawing) == mean_strokes:
            common_strokes.append(mat.iloc[k, :])

    if len(common_strokes) == 0:
        return mat.iloc[0, :]

    #return common_strokes[0]
    features =[]
    for row in common_strokes:
        rowfeature = []
        for stroke in range(mean_strokes):

            if len(row.drawing[stroke][0]) >= 3 and len(row.drawing[stroke][1]) >= 3 and len(row.drawing[stroke][2]) >= 3  :

                rowfeature.append(np.min(row.drawing[stroke][0]))
                rowfeature.append(np.max(row.drawing[stroke][0]))
                rowfeature.append(np.mean(row.drawing[stroke][0]))
                rowfeature.append(np.std(row.drawing[stroke][0]))
                rowfeature.append(np.min(row.drawing[stroke][1]))
                rowfeature.append(np.max(row.drawing[stroke][1]))
                rowfeature.append(np.mean(row.drawing[stroke][1]))
                rowfeature.append(np.std(row.drawing[stroke][1]))


                ## distance of a stroke
                x=(row.drawing[stroke][0][0],row.drawing[stroke][0][len(row.drawing[stroke][0])-1])
                y=(row.drawing[stroke][1][0],row.drawing[stroke][1][len(row.drawing[stroke][1])-1])
                rowfeature.append(distance.euclidean(x, y))

                ## slope of a stroke
                x2x1 = float( row.drawing[stroke][0][len(row.drawing[stroke][0]) - 1] - row.drawing[stroke][0][0])
                y2y1 = float( row.drawing[stroke][1][len(row.drawing[stroke][1]) - 1] - row.drawing[stroke][1][0])
                if x2x1 != 0.0:
                    rowfeature.append(y2y1/x2x1)
                else:
                    rowfeature.append(0.0)

                ## time taken for this stroke
                rowfeature.append(row.drawing[stroke][2][len(row.drawing[stroke][2])-1])

                ## check clockwise or anticlockwise
                if row.drawing[stroke][0][0] < row.drawing[stroke][0][1] and row.drawing[stroke][0][1] < row.drawing[stroke][0][2]:
                    rowfeature.append(1)
                else:
                    rowfeature.append(-1)

                ## check up or down
                if row.drawing[stroke][1][0] < row.drawing[stroke][1][1] and row.drawing[stroke][1][1] <  row.drawing[stroke][1][2]:
                    rowfeature.append(1)
                else:
                    rowfeature.append(-1)


        features.append(np.array(rowfeature))
    df_features = pd.DataFrame(features)
    feature_mean = df_features.mean()

    dotp_array =[]
    for i in range(df_features.shape[0]):
        dotp = np.dot(df_features.iloc[i,:].values,feature_mean.values)#/np.linalg.norm(df_features.iloc[1,:].values)/np.linalg.norm(feature_mean.values)
        #angle = np.arccos(np.clip(c, -1, 1))
        dotp_array.append(dotp)

    if len(dotp_array) == 0:
        return mat.iloc[0, :]

    maxindex = dotp_array.index(max(dotp_array))

    if maxindex == '':
        return mat.iloc[0, :]

    else:
        return mat.iloc[maxindex,:]


summary=[]
countries =[]

for i in range(len(dat)):

    row = dat.iloc[i,:]


    if row['countrycode'] not in countries:

        countries.append(row['countrycode'])

        currentdata = dat.loc[dat['countrycode']==row['countrycode'],:]

        print(row['countrycode'], len(countries),currentdata.shape)

        representive = get_representative(currentdata)

        summary.append(representive)

    else:
        continue



df_summary= pd.DataFrame(summary)
df_summary.to_json("dog_rep.json",orient='records')
