
from sklearn import cluster
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pylab as plt
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture


image_object = ['house','cake','face','dog','tornado']


for imgobj in image_object:

    df_summary = pd.read_csv(imgobj + "_fe.csv")
    df_summary.head(2)
    df_summary.shape

    df_countryinfo = pd.read_csv("countries.csv")
    df_countryinfo.head(1)
    df_countryinfo.shape

    df_countryinfo.ContinentCode.unique()

    ### cluster geography
    groups =6
    kmeans = cluster.KMeans(n_clusters=groups)
    kmeans = kmeans.fit(df_summary.iloc[:,2:])
    Geo_Cluster = kmeans.predict(df_summary.iloc[:,2:])
    print(imgobj,'Geo_Cluster',groups)



    #### cluster direction
    columns_direction = df_summary.filter(like='direction').columns
    df_summary_direction = df_summary.loc[:,columns_direction]
    df_summary_direction.columns

    scores =[]
    for c in [2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
        gmm = GaussianMixture(n_components=c)
        gmm.fit(df_summary_direction.iloc[:,:])
        #print(c, gmm.bic(df_summary_direction.iloc[:,:]))
        scores.append(gmm.bic(df_summary_direction.iloc[:,:]))
    #plt.plot(scores)
    optclust = scores.index(min(scores))
    print(imgobj, 'Direction_Cluster', optclust)
    gmm = GaussianMixture(n_components=optclust)
    gmm.fit(df_summary_direction.iloc[:, :])
    Direction_Cluster = gmm.predict(df_summary_direction.iloc[:, :])


    ##### cluster time
    columns_time = df_summary.filter(like='time').columns
    df_summary_time = df_summary.loc[:,columns_time]
    df_summary_time.columns

    scores =[]
    for c in [2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
        gmm = GaussianMixture(n_components=c)
        gmm.fit(df_summary_time.iloc[:,:])
        #print(c, gmm.aic(df_summary_time.iloc[:,:]))
        scores.append(gmm.aic(df_summary_time.iloc[:,:]))
    #plt.plot(scores)
    optclust = scores.index(min(scores))
    print(imgobj, 'Time_Cluster', optclust)
    gmm = GaussianMixture(n_components=optclust)
    gmm.fit(df_summary_time.iloc[:, :])
    Time_Cluster = gmm.predict(df_summary_time.iloc[:, :])

    df_summary['Geo_Cluster']=Geo_Cluster
    df_summary['Direction_Cluster'] = Direction_Cluster
    df_summary['Time_Cluster'] = Time_Cluster

    df_summary = df_summary.loc[:,['countrycode','Geo_Cluster','Direction_Cluster','Time_Cluster'],]
    df_summary.columns = ['CountryCode','Geo_Cluster','Direction_Cluster','Time_Cluster']
    df_summary.columns
    df_countryinfo_final = pd.merge(df_countryinfo, df_summary, on='CountryCode')

    # continents = ["AF","AS","EU","NA","SA","OC"]
    # labcodes =[]
    # for i in range(len(labels)):
    #     if labels[i]==0:
    #         labcodes.append(continents[labels[i]])
    #     elif labels[i]==1:
    #         labcodes.append(continents[labels[i]])
    #     elif labels[i]==2:
    #         labcodes.append(continents[labels[i]])
    #     elif labels[i]==3:
    #         labcodes.append(continents[labels[i]])
    #     elif labels[i]==4:
    #         labcodes.append(continents[labels[i]])
    #     elif labels[i]==5:
    #         labcodes.append(continents[labels[i]])



    df_countryinfo_final.to_csv('1_'+imgobj+"_cluster.csv",index=False)


## pca analysis



pca = PCA(2)  # project from 64 to 2 dimensions
projected = pca.fit_transform(x_scaled)


#c=df_all_data.countrycode,
plt.scatter(projected[:, 0], projected[:, 1],c=df_summary.cluster,
             edgecolor='none', alpha=2.5, cmap=plt.cm.get_cmap('spectral', groups))
plt.xlabel('component 1')
plt.ylabel('component 2')
plt.colorbar()




## here we see first two components overlap heavily


pca = PCA(n_components=14)
X_train_pca = pca.fit_transform(x_scaled)
plt.bar(range(0, 14), pca.explained_variance_ratio_, alpha=0.5, align='center')
plt.step(range(0, 14), np.cumsum(pca.explained_variance_ratio_), where='mid')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.xticks([], [])
plt.show()
