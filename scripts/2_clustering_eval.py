
from sklearn import cluster
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pylab as plt
from sklearn.decomposition import PCA


image_object = ['house','cake','face','dog','tornado']

cluster_eval = []
for imgobj in image_object:

    df_summary = pd.read_csv('1_'+imgobj+"_cluster.csv")
    df_summary.head(2)
    df_summary.columns

    ### geo eval
    continents = df_summary.ContinentCode.unique()
    for c in continents:
        row = df_summary[df_summary.ContinentCode ==c]
        clusters = row.groupby('Geo_Cluster').count().reset_index().CountryName
        # list(clusters).index(max(clusters))
        print(imgobj, c+'_Geo', max(clusters)/sum(clusters))
        cluster_eval.append([imgobj, c+'_Geo', max(clusters)/sum(clusters)])

    ### direction eval
    continents = df_summary.ContinentCode.unique()
    for c in continents:
        row = df_summary[df_summary.ContinentCode ==c]
        clusters = row.groupby('Direction_Cluster').count().reset_index().CountryName
        # list(clusters).index(max(clusters))
        print(imgobj, c+'_Direction', max(clusters)/sum(clusters))
        cluster_eval.append([imgobj, c+'_Direction', max(clusters)/sum(clusters)])

    ### direction eval
    continents = df_summary.ContinentCode.unique()
    for c in continents:
        row = df_summary[df_summary.ContinentCode ==c]
        clusters = row.groupby('Time_Cluster').count().reset_index().CountryName
        # list(clusters).index(max(clusters))
        print(imgobj,c +'_Time', max(clusters)/sum(clusters))
        cluster_eval.append([imgobj,c +'_Time', max(clusters)/sum(clusters)])


df_cluster_eval = pd.DataFrame(cluster_eval)
df_cluster_eval.columns=['image_object','Continent_Cluster','Score']
df_cluster_eval.to_csv('cluster_evaluation',index=False)

df_cluster_eval[df_cluster_eval.image_object=='house'].plot(kind='bar')
plt.xlabel(df_cluster_eval.Continent_Cluster)


