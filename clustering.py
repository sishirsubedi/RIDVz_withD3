import pandas as pd
from sklearn import cluster

fmat = pd.read_csv("feature_matrix.csv")
fmat.head(2)

k_means = cluster.KMeans(n_clusters=3)
k_means.fit(fmat)
result = pd.DataFrame(fmat.index.values,columns=['id'])
result['cluster'] = k_means.labels_
result.head(2)

result.to_json("clusters.json",orient='index')