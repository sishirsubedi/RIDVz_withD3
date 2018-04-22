import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import vectorize
import json
import time
import random
import feature_engineering_func
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
np.random.seed(32113)


image_object = ['house','cake','face','dog','tornado']
for item in image_object:
    filepath = str(item)+".json"
    df = pd.read_json(filepath, lines=True)
    print(str(item), df.head(1))
    df_fe = feature_engineering_func.feature_engineering_ensemble(df)
    print(str(item),df_fe.shape)
    df_fe.to_csv(str(item)+"_fe_all.csv",index=False)

for item in image_object:
    df = pd.read_csv(item + "_fe_all.csv")
    df.head(2)
    df.shape



########### lasso ############

# for item in image_object:
#     df = pd.read_csv(item + "_fe_all.csv")
#     df.head(2)
#     df.shape
#
#     count_array = pd.DataFrame(df.groupby('countrycode').count().key_id)
#     count_array.reset_index(inplace=True)
#     count_array.sort_values('key_id',ascending=False,inplace=True)
#     count_array = count_array[count_array.key_id>100]
#     countries_for_model = count_array.countrycode.unique()
#
#     countries_for_model = list(countries_for_model)
#     df = df.loc[df.countrycode.isin(countries_for_model),:]
#
#     d = dict(zip(df.countrycode.unique(),range(0,len(df.countrycode.unique()))))
#
#     df['label'] = df['countrycode'].map(d,na_action='ignore')
#
#     df = df.iloc[:,2:]
#
#     x_data = df.iloc[:, 0:df.shape[1] - 1]
#     x_scaled = pd.DataFrame(preprocessing.StandardScaler().fit(x_data).transform(x_data))
#     x_scaled.columns = x_data.columns
#     df.iloc[:, 0:df.shape[1] - 1] = x_scaled
#     df.head(10)
#
#     X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, 0:df.shape[1] - 1],
#                                                         df.iloc[:, df.shape[1] - 1],
#                                                         test_size=0.25, random_state=42)
#
#
#
#
#     model = LogisticRegression(penalty='l2',  fit_intercept=False,multi_class='multinomial',solver='newton-cg')
#     model.fit(X_train, y_train)
#     acc = model.score(X_test, y_test)
#     print(p, acc, np.count_nonzero(model.coef_[0]))
#
#     model = LogisticRegression(penalty='l1', C=0.006, fit_intercept=False)
#     model.fit(X_train, y_train)
#     predicted = pd.DataFrame(model.predict(X_test))
#     print(np.sum([1 if x == y else 0 for x, y in zip(predicted.values, y_test.values)]) / float(predicted.shape[0]))
#     model.score(X_test, y_test)
#     print(np.count_nonzero(model.coef_[0]))
#     nonzeroindex = [i for i, e in enumerate(model.coef_[0]) if e != 0]
#     lasso_features = df_all_patientdata.columns[nonzeroindex]
#     lasso_features
#

