import pandas as pd
import matplotlib.pylab as plt
from sklearn import cluster
import numpy as np
from sklearn import preprocessing
from scipy.spatial import distance


file1 = pd.read_json("../house.json", lines=True)
dat = pd.DataFrame(file1)
print(dat.head(2))


def get_meanrep(mat):

    ##calculate mean strokes
    mean_array = []
    for j in range(len(mat)):
        mean_array.append(len(mat.iloc[j, :].drawing))
    mean_strokes = int(np.mean(mean_array)) + 1

    common_strokes = []
    for k in range(len(mat)):
        if len(mat.iloc[k, :].drawing) == mean_strokes:
            common_strokes.append(mat.iloc[k, :])

    if len(common_strokes)<2:
        return "error"

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
    return df_features.mean()


summary=[]
countries =[]

for i in range(len(dat)):

    row = dat.iloc[i,:]

    features =[]

    if row['countrycode'] == 'BS':
        break

    if row['countrycode'] not in countries:

        countries.append(row['countrycode'])

        currentdata = dat.loc[dat['countrycode']==row['countrycode'],:]

        if currentdata.shape[0]<10:
            continue

        print(row['countrycode'], len(countries), currentdata.shape)
        representive = get_meanrep(currentdata)

        features.append(row['countrycode'])
        for val in representive:
            features.append(val)

    else:
        continue
    summary.append(features)

df_summary = pd.DataFrame(summary)
df_summary.fillna(0,inplace=True)

kmeans = cluster.KMeans(n_clusters=7)
kmeans = kmeans.fit(df_summary.iloc[:,1:])
labels = kmeans.predict(df_summary.iloc[:,1:])
df_summary['size'] = 5
df_summary['cluster'] = labels

cluster_result = df_summary.iloc[:,[0,df_summary.shape[1]-2,df_summary.shape[1]-1]]
cluster_result.columns = ['country','size','cluster']
#cluster_result.to_json("house_cluster.json",orient='records')
cluster_result.to_csv("house_cluster2.csv",index=False)

