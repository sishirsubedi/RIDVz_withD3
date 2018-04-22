
from sklearn import cluster
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pylab as plt
from sklearn.decomposition import PCA


image_object = ['house','cake','face','dog','tornado']


for imgobj in image_object:

    df_summary = pd.read_csv(imgobj + "_fe.csv")
    df_summary.head(2)

    columns_withdirection = df_summary.filter(like='direction').columns

    groups =6
    kmeans = cluster.KMeans(n_clusters=groups)
    kmeans = kmeans.fit(df_summary.iloc[:,2:])
    labels = kmeans.predict(df_summary.iloc[:,2:])


    df_countryinfo = pd.read_csv("countries.csv")
    df_countryinfo.head(1)

    #df_summary['cluster'] = labels

    df_summary = df_summary.iloc[:,[0,(df_summary.shape[1]-1)]]
    df_summary.columns = ['CountryCode','Cluster']

    df_countryinfo_final = pd.merge(df_countryinfo, df_summary, on='CountryCode')


    continents = ["AF","AS","EU","NA","SA","OC"]
    labcodes =[]
    for i in range(len(labels)):
        if labels[i]==0:
            labcodes.append(continents[labels[i]])
        elif labels[i]==1:
            labcodes.append(continents[labels[i]])
        elif labels[i]==2:
            labcodes.append(continents[labels[i]])
        elif labels[i]==3:
            labcodes.append(continents[labels[i]])
        elif labels[i]==4:
            labcodes.append(continents[labels[i]])
        elif labels[i]==5:
            labcodes.append(continents[labels[i]])

    df_summary['Cluster'] = labcodes

    df_countryinfo_final['ContinentCode'] = df_countryinfo_final['Cluster']
    df_countryinfo_final.head(2)
    df_countryinfo_final =df_countryinfo_final.iloc[:,0:6]


    df_countryinfo_final.to_csv(imgobj+"_cluster.csv",index=False)
#
# cluster_result = df_summary.iloc[:,[0,df_summary.shape[1]-2,df_summary.shape[1]-1]]
# cluster_result.columns = ['country','size','cluster']
# #cluster_result.to_json("house_cluster.json",orient='records')
# cluster_result.to_csv("house_cluster_result.csv",index=False)
#


df_all_data = df_summary
#df_all_data = df_all_data.iloc[:,2:]
df_all_data.head(10)
print (df_all_data.shape)


### center data
x_data =df_all_data.iloc[:,2:df_all_data.shape[1]-1]
x_scaled = pd.DataFrame(preprocessing.scale(x_data))
x_scaled.columns = x_data.columns
df_all_data.iloc[:,2:df_all_data.shape[1]-1] = x_scaled
df_all_data.head(10)


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
