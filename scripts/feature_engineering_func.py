import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import vectorize
import json
import time
import random
np.random.seed(32113)



##############################################################################
#                             Aggregated functions                           #
##############################################################################

def feature_engineering_ensemble(df):
    '''
    function:
    - aggregates multiple user defined functions to create dataframe for ensemble method modeling.
    - it also prints out how long it takes to run
    - processes google quickdraw raw data dataframe
    - after this processing, dataframe contains 404 features
    - the output of this function will be used for ensemble method modeling.

    input:
    - df = dataframe that was converted from raw_data json file
    - category = used to name output pickle file
    - sample = number of datapoints included in the final dataframe. (Used only when purpose = 'word')  
    - purpose = 'word' or 'country'. prepares data for different purposes.
        'word' for image recognition, 'country' for country prediction
    - countries = list of country code used in country prediction

    output:
    - pickled dataframe that will be used for ensemble method (404 features)
    filename: "./data/MY_feature_{}.pkl".format(category)
    '''

    print("running ... feature_engineering_ensemble")

    start_time = time.time()
    #runs feature_eng_pt1 through pt5.
    print("running ... feature_eng_pt1")
    df_test1 = feature_eng_pt1(df)
    print("finished ... feature_eng_pt1")
    df_test2 = feature_eng_pt2(df_test1)
    print("finished ... feature_eng_pt2")
    df_test3 = feature_eng_pt3(df_test2)
    print("finished ... feature_eng_pt3")
    df_subset = feature_eng_pt4(df_test3)
    print("finished ... feature_eng_pt4")
    df_subset2 = feature_eng_pt5(df_test3)
    print("finished ... feature_eng_pt5")
    df_final = pd.concat([df_test3,df_subset,df_subset2], axis=1)

    df_final = df_final.drop(['drawing', 'word', 'timestamp', 'recognized', 'X', 'Y', 'time', \
                       'X_per_stroke', 'Y_per_stroke', 'time_per_stroke', \
                       'total_time_of_stroke', 'dp_per_stroke', 'dp_percent_per_stroke', \
                       'direction'], axis=1)
    return df_final
    # # prepares final dataframe
    # #If purpose = 'word' it will randomly select 'sample' number of datapoints from df_final
    # if purpose == 'word':
    #     df_final.index = range(len(df_final))
    #     random_ind = np.random.choice(list(df_final.index), sample, replace=False)
    #     df_final = df_final.loc[list(random_ind)]
    # #if purpose = 'country', it will correct all datapoints from the selected countries.
    # elif purpose == 'country':
    #     df_final = df_final[(df_final['countrycode']==countries[0])|\
    #             (df_final['countrycode']==countries[1])|\
    #            (df_final['countrycode']==countries[2])|(df_final['countrycode']==countries[3])]
    # df_final.index = df_final['key_id']
    # df_final.to_pickle("./data/MY_feature_{}.pkl".format(category))
    # print("--- %s seconds ---" % (time.time() - start_time))


##############################################################################
#           functions for feature engineeering for ensemble methods          #
##############################################################################



def feature_eng_pt1(df_cf):

    '''
    function:
    - feature engineering pt1
      need to run this first since pt2 to pt5 uses features created
      in this function.

    - create following features:
      stroke_number = total stroke number of an image [int]
      final time = time of the last datapoints for an image (how long it took user to draw) [int]
      recognized = changed True/False response to boolean
                              (1 is true, 0 is false)[int]

    - Filtering applied:
      1: filtered out data where recognize == 0. 
          Having unrecognized images in the dataset may reduce prediction accuracy
      2: filtered out data where stroke_number is greater than 15
          After analysis, most pics were drawn under 15 strokes. 
          I'm suspecting that if stroke numbers are above 20 or 30, users might be using a graphic tablet. 
          In this project, I tried to exclude those images above 15 strokes.
          So that I keep all images that are drawn in the similar environment.
      3: filtered out data where final time is greater than 20000
          I do not know how this happens but some images have time values that are more than 20000.
          The quickdraw ask users to draw in 20sec so I am a bit puzzled how these users draw for more than 20000ms.

    input:
    df = dataframe created from Google quickdraw raw data json file

    output:
    dataframe with additional features mentioned above
    '''
    # create feature "stroke_number"
    df_cf['stroke_number']=df_cf['drawing'].str.len()

    #create feature "final_time"
    df_cf['final_time'] = [df_cf.loc[index,'drawing']\
                [df_cf.stroke_number[index]-1][2][-1] for index in df_cf.index]

    #setting boolean and changing recognized features to 1 and 0.
    b_loon = {True: 1, False:0}
    df_cf['recognized'] = df_cf['recognized'].map(b_loon)

    #filtered data by stroke number, recognized and final time features
    df_cf = df_cf[(df_cf['recognized']==1) & (df_cf['stroke_number'] <= 15)]
    df_cf = df_cf[(df_cf['final_time']<=20000)]

    # print(df_cf.shape)
    # df_cf2 = df_cf.loc[0:10,:].copy()

    ccs = np.unique(df_cf.countrycode.values)

    for c in ccs:
        rows_index = df_cf[(df_cf['countrycode']==c)].index

        if len(rows_index)>1000:
            new_index = random.sample(list(rows_index), 1000)
            todrop_index = [x for x in rows_index if x not in new_index]
            df_cf.drop(todrop_index, axis='rows',inplace=True)

    return df_cf

def feature_eng_pt2(df_cf):

    '''
    function:

    - feature engineering pt2
      need to run this after pt1. pt3 to pt5 uses features created
      in this function.

    - create following features:
      total_number_of_datapoints = total number of datapoints exist in an image [int]
      X = normalized X Ranges between 0 to 1 [list]
      Y = Y values normalized using X. Ranges between 0 and 1.5 [list]
      Ymax = maximum value of Y [int]
      time = list of time [list]
        * note: X,Y,time should have the same length for each row.

      total_time_of_stroke = time spent on each stroke [list]
      dp_per_stroke = number of datapoints exist within each stroke [list]
      dp_percent_per_stroke = data points in a stroke / total data points
                                of a drawing. displayed as percentage [list]
                                (this feature represents how much of drawing was done in each stroke)
      stroke_with_max_time = index of stroke that user spent most time drawing [int]
      stroke_with_min_time = index of stroke that user spent least time drawing [int]
      std_of_time = standard deviation of time [float]
      ave_datapoints_per_stroke = average number of data points per stroke [float]
      total_time_drawing = total amount of time that user spent on drawing[int]
                        (total time - (time user spent between strokes)) 
      ave_time_per_stroke = average time spent per stroke [float]
      stroke_with_max_dp = index of stroke that contains most data points [int]
      stroke_with_min_dp = index of stroke that contains least data points [int]
      X_per_stroke = X separated by strokes
      Y_per_stroke = Y separated by strokes
      time_per_stroke = time separated by strokes
      std_of_dp = standard deviation of all data points of a drawing [float]

    - Filtering applied:
      1: filtered out data where Ymax is greater than 1.5
         need this filter to maintain 2:3 X:Y ratio of all images.

    input:
    df_cf = output dataframe from feature_eng_pt1.

    output:
    dataframe with above features and filter.
    '''

    # process:
    # 1. make a list or int from existing features
    # 2. store contents of 1. in a new dictionary
    # 3. make new column in your dataframe with 2. dictionary
    
    #note: I figure there have to be a easier/simpler way to make these new features...
    #however, I do need to access a column that is a nested list. This complicates my situation.

    X = {}
    Y = {}
    Xperst = {}
    Yperst = {}
    Ymax ={}
    time = {}
    tperst = {}
    Tdiff = {}
    ttnum_dp = {}
    Tdiffmax = {}
    Tdiffmin = {}
    Tdiffstd = {}
    dpps = {}
    dppps = {}
    dp_max = {}
    dp_min = {}
    dp_std = {}
    sumtimeps = {}

    for i in df_cf.index:
        num = df_cf.stroke_number[i]
        #store X,Y,time of the stroke in a temp list
        Xt = [df_cf.loc[i,'drawing'][stroke][0] for stroke in range(num)]
        Yt = [df_cf.loc[i,'drawing'][stroke][1] for stroke in range(num)]
        tt = [df_cf.loc[i,'drawing'][stroke][2] for stroke in range(num)]
        # calculate the difference between final and initial time of a stroke
        Tdifftemp = [(df_cf.loc[i,'drawing'][stroke][2][-1] - df_cf.loc[i,'drawing'][stroke][2][0])\
                     for stroke in range(num)]
        # calculate the length of the stroke list
        dpps_temp = [len(df_cf.loc[i,'drawing'][stroke][2]) for stroke in range(num)]

        #store all X(or Y or time) info of an image into a list
        Xtemp = [item for stroke in Xt for item in stroke]
        Ytemp = [item for stroke in Yt for item in stroke]
        time[i] = [item for stroke in tt for item in stroke]

        #normalizing X and Y
        Xmintemp = np.min(Xtemp)-1
        Xmaxtemp = np.max(Xtemp)+1
        Ymintemp = np.min(Ytemp)-1
        #runs user defined function array_normalizer to normalize
        Xnorm = _array_normalizer(Xtemp, Xmintemp,Xmaxtemp,Xmintemp)
        Ynorm = _array_normalizer(Ytemp, Xmintemp,Xmaxtemp,Ymintemp)
        Ymax[i] = np.max(Ynorm)
        X[i] = Xnorm
        Y[i] = Ynorm
        #store X,Y and time info from each stroke as a list
        Xperst[i] = [list(_array_normalizer(Xt[stroke],Xmintemp,Xmaxtemp,Xmintemp)) for stroke in range(len(Xt))]
        Yperst[i] = [list(_array_normalizer(Yt[stroke],Xmintemp,Xmaxtemp,Ymintemp)) for stroke in range(len(Yt))]
        tperst[i] = [tt[stroke] for stroke in range(len(tt))]
        
        #total number of datapoints 
        ttnum_dp[i] = len(Xnorm)
        
        #store time spent on each stroke
        Tdiff[i] = Tdifftemp
        #store index of stroke that user spent most time
        Tdiffmax[i] = np.argmax(Tdifftemp)
        #store index of stroke that user spent least time
        Tdiffmin[i] = np.argmin(Tdifftemp)
        #time standard deviation for each stroke
        Tdiffstd[i] = np.std(Tdifftemp)
        
        #number of datapoints for each stroke
        dpps[i] = dpps_temp
        #number of datapoints stored as a percentage
        dppps[i] = np.array(dpps_temp)/float(len(Xtemp))
        #stroke with maximum number of datapoints
        dp_max[i] = np.argmax(dpps_temp)
        #stroke with minimum number of datapoints
        dp_min[i] = np.argmin(dpps_temp)
        #std. of datapoints per stroke
        dp_std[i] = np.std(dpps_temp)
        #total time spent on drawing
        sumtimeps[i] = sum(Tdifftemp)
        
    # create new features
    df_cf['total_number_of_datapoints'] = pd.Series(ttnum_dp)
    df_cf['X'] = pd.Series(X)
    df_cf['Y'] = pd.Series(Y)
    df_cf['Ymax'] = pd.Series(Ymax)
    df_cf['time'] = pd.Series(time)
    df_cf['total_time_of_stroke'] = pd.Series(Tdiff)
    df_cf['dp_per_stroke'] = pd.Series(dpps)
    df_cf['dp_percent_per_stroke'] = pd.Series(dppps)
    df_cf['stroke_with_max_time'] = pd.Series(Tdiffmax)
    df_cf['stroke_with_min_time'] = pd.Series(Tdiffmin)
    df_cf['std_of_time'] = pd.Series(Tdiffstd)
    df_cf['ave_datapoints_per_stroke'] = df_cf['total_number_of_datapoints']/(df_cf['stroke_number'])
    df_cf['total_time_drawing'] = pd.Series(sumtimeps)
    df_cf['ave_time_per_stroke'] = df_cf['total_time_drawing']/(df_cf['stroke_number'])
    df_cf['stroke_with_max_dp'] = pd.Series(dp_max)
    df_cf['stroke_with_min_dp'] = pd.Series(dp_min)
    df_cf['X_per_stroke'] = pd.Series(Xperst)
    df_cf['Y_per_stroke'] = pd.Series(Yperst)
    df_cf['time_per_stroke'] = pd.Series(tperst)
    df_cf['std_of_dp'] = pd.Series(dp_std)
    df_cf = df_cf[df_cf['Ymax']<=1.5]
    return df_cf

def feature_eng_pt3(df_cf):
    '''
    function:
    - feature engineering pt3
      need to run this after feature_eng_pt2 since pt4 and pt5
      uses features created in this function.

    - Create following features:
      direction = direction of stroke (from first XY points to last XY points)
                    in radian (0 to 6.28...) [float]

    input:
      df_cf = output dataframe from feature_eng_pt2

    output:
      dataframe with above features and filter

    the way I approached this is by finding the first and last x,y locations for each stroke and
    I then calculated delta x (dx) and delta y (dy).
    from there, I just calculated the direction of the stroke in radian using my user defined function "_radian_direction"
    '''
    direction = {}
    for index in df_cf.index:
        dx = [float(df_cf.drawing[index][stroke][1][-1] - df_cf.drawing[index][stroke][1][0]) \
          for stroke in range(df_cf.stroke_number[index])]
        dy = [float(df_cf.drawing[index][stroke][0][-1] - df_cf.drawing[index][stroke][0][0]) \
          for stroke in range(df_cf.stroke_number[index])]
        dx = np.array(dx)
        dy = np.array(dy)
        dx[dx==0] = 0.000001
        vecrad_direction = np.vectorize(_radian_direction)
        direction[index] = vecrad_direction(dy,dx)
    df_cf['direction'] = pd.Series(direction)
    return df_cf

def feature_eng_pt4(df_cf):
    '''
    function:
    - feature engineering pt4
      create new dataframe that need to be combined with output dataframe
      of feature_eng_pt3
    - it creates 5 features per 1 stroke.
    - this function will creates these 5 features for first 15 strokes of an image

    - Create following features:
      datapoint_percentage_stroke'i' = # of data points in stroke i divide by
                            total number of data points of an image. [float]
            * do not confuse with dp_percent_per_stroke column I previously made.
            dp_percent_per_stroke is a list. datapoint_percentage_stroke'i' is a float!
            
      direction_stroke'i' = direction of stroke 'i' [float]
      
      time_stroke'i' = total time spent on stroke'i' [int]
      
      datapoints_stroke'i' = number of data points in stroke i [int]
      
      switch_stroke'i' = boolean indicates whether stroke'i' exist in an image
                            0: stroke exist 1: stroke does not exist [int]

    input:
      df_cf = output dataframe from feature_eng_pt3

    output:
      new dataframe with 75 features (5 * 15 features)
    '''

    ar = np.zeros((len(df_cf),75))
    c = 0
    for index_ in df_cf.index:
        stroke = (df_cf.stroke_number[index_])
        ar[c][:stroke] = np.array(df_cf['dp_percent_per_stroke'][index_])
        ar[c][15:15+stroke] = np.array(df_cf['direction'][index_])
        ar[c][30:30+stroke] = np.array(df_cf['total_time_of_stroke'][index_])
        ar[c][45:45+stroke] = np.array(df_cf['dp_per_stroke'][index_])
        ar[c][60:75] = np.array([0]*stroke+[1]*(15-stroke))
        c += 1
    subset = pd.DataFrame(ar)
    subset.index = df_cf.index
    for num in range(15):
        subset = subset.rename(columns={num:"datapoint_percentage_stroke{}".format(num)})
    for num in range(15,30):
        subset = subset.rename(columns={num:"direction_stroke{}".format(num-15)})
    for num in range(30,45):
        subset = subset.rename(columns={num:"time_stroke{}".format(num-30)})
    for num in range(45,60):
        subset = subset.rename(columns={num:"datapoint_stroke{}".format(num-45)})
    for num in range(60,75):
        subset = subset.rename(columns={num:"switch_stroke{}".format(num-60)})
    return subset

def feature_eng_pt5(df_cf):
    '''
    function:
    - feature engineering pt5
      create new dataframe that need to be combined with output dataframe
      of feature_eng_pt3
    - simplifying x,y and time information of an image into 100 datapoints

      for example: if your image has 492 datapoints (492X,492Y,492time),
      this function will reduce number of data points to 100 datapoints
      (100 X,100 Y, 100 time). In order to reduce number of data points, it
      will look for 100 equally spaced indexes from 492 data and find X, Y and
      time that are associated with these 100 equally space indexes.

    - Create following features:
      X_"i" = "i"th X in simpified X datapoints
      Y_"i" = "i"th Y in simpified Y datapoints
      time_"i" = "i"th time in simpified time datapoints

    input:
      df_cf = output dataframe from feature_eng_pt3

    output:
      new dataframe with 300 features (3 * 100 features)
    '''


    #PROCESS:
    # create a numpy array with (length of df_cf, 300)dimension
    # fill in this array with simplified X, Y and time values
    # column 0-99 is for X, column 100-199 is for Y, column 200-299 is for time
    # once array is filled, convert it to dataframe and output it as a new dataframe
    ar = np.zeros((len(df_cf),300))
    c = 0
    for index_ in df_cf.index:
        Xpoints = [_value_from_stroke(df_cf['dp_per_stroke'][index_][stroke],\
                                    df_cf['dp_percent_per_stroke'][index_][stroke],\
                                    df_cf['X_per_stroke'][index_][stroke])\
                                    for stroke in range(df_cf.stroke_number[index_])]

        Ypoints = [_value_from_stroke(df_cf['dp_per_stroke'][index_][stroke],\
                                    df_cf['dp_percent_per_stroke'][index_][stroke],\
                                    df_cf['Y_per_stroke'][index_][stroke])\
                                    for stroke in range(df_cf.stroke_number[index_])]

        tpoints = [_value_from_stroke(df_cf['dp_per_stroke'][index_][stroke],\
                                    df_cf['dp_percent_per_stroke'][index_][stroke],\
                                    df_cf['time_per_stroke'][index_][stroke])\
                                    for stroke in range(df_cf.stroke_number[index_])]

        X = [item for stroke in Xpoints for item in stroke]
        Y = [item for stroke in Ypoints for item in stroke]
        time = [item for stroke in tpoints for item in stroke]

        #if the number datapoints turn out to be less than 100, it will fill
        #empty cell with it's last data points.
        if len(X)<100:
            X = X + [X[-1]]*(100-len(X))
        if len(Y)<100:
            Y = Y + [Y[-1]]*(100-len(Y))
        if len(time)<100:
            time = time + [time[-1]]*(100-len(time))

        ar[c][:100] = np.array(X[0:100])
        ar[c][100:200] = np.array(Y[0:100])
        ar[c][200:300] = np.array(time[0:100])
        c += 1

    subset = pd.DataFrame(ar)
    subset.index = df_cf.index
    for num in range(100):
        subset = subset.rename(columns={num:"X_{}".format(num)})
    for num2 in range(100,200):
        subset = subset.rename(columns={num2:"Y_{}".format(num2-100)})
    for num3 in range(200,300):
        subset = subset.rename(columns={num3:"time_{}".format(num3-200)})
    return subset

def _array_normalizer(array1,Xmin,Xmax,array_min):
    '''
    function:
        - normalize X,Y array by range of X
        - used in feature_eng_pt2
    input:
        array1 = array that you want to normalize (1D array or list)
        Xmin = minimum value of your X array (int)
        Xmax = maximum value of your X array (int)
        array_min = minimum value of array1

    output:
        normalized array of array1
    '''
    return (np.array(array1)-np.array([array_min]*len(array1)))/float(Xmax-Xmin)

def _radian_direction(dy,dx):
    '''
    function:
        - based on given dy and dx it calculates direction in radian.
        - used in feature_eng_pt3
    input:
        dy = change in y
        dx = change in x

    output:
        returns radian value (0 to 6.28)
    '''
    if dy < 0.0 and dx > 0.0:
        return (2*np.pi + np.arctan(dy/dx))
    elif dy >=0.0 and dx > 0.0:
        return (np.arctan(dy/dx))
    else:
        return np.pi + np.arctan(dy/dx)

def _value_from_stroke(stroke_length,percentage,xperstroke):
    '''
    function:
        - generates list of equally spaced x,y or time using input values.
        - used in feature_eng_pt5
        - for example: if your stroke_length is 60 and percentage is 0.4,
        it will create a list of indexes that equally spaced
        40(=0.4*100) datapoints from 60 data points.
        Using this list of index, it will create a list of X,Y, or time.
    input:
        stroke_length = length of the stroke
        percentage = number of data points of the stroke/total number of data points
        xperstroke =  data points in a stroke
                        (the list of data points should be in chronological order)
    output:
        list of data point (x,y,time) that
        return np.linspace array which represents index of datapoints in each stroke

    '''
    idxs = np.around(np.linspace(0,stroke_length-1,int(np.around(percentage*100))))
    return [xperstroke[int(ind)] for ind in idxs]



############### analysis @@@@@@@@@@@@@@@@@@


ccode = pd.read_csv("cc_2_3.csv")
ccode.head(1)

image_object = ['dog','tornado']

for item in image_object:
    filepath = str(item)+".json"
    df = pd.read_json(filepath, lines=True)
    print(str(item), df.head(1))

    df_fe = feature_engineering_ensemble(df)

    print(str(item),df_fe.shape)
    #df_fe.to_csv((str(item)+"_fe.csv"),index=False)

    ccs = np.unique(df_fe.countrycode.values)

    best_rep = []
    for c in ccs:
        rows = df_fe[(df_fe['countrycode']==c)]

        mean_vec = rows.iloc[:,2:].mean(axis=0)

        dotp_array = []
        for i in range(rows.shape[0]):
            dotp = np.dot(rows.iloc[i, 2:].values,  mean_vec.values)
            dotp_array.append(dotp)

        maxindex = dotp_array.index(max(dotp_array))

        best_rep.append(rows.iloc[maxindex, :].values)

    df_best_rep = pd.DataFrame(best_rep)
    df_best_rep.columns = df_fe.columns
    #df_best_rep.to_csv((str(item)+"_fe.csv"),index=False)

    temp_df_columns = list(df.columns)
    temp_df_columns.append('cc3')
    best_rep_drawing =pd.DataFrame(index=np.arange(0, len(df_best_rep.countrycode.values)),columns=temp_df_columns)

    i = 0
    for c in df_best_rep.countrycode.values:

        row = df_best_rep[df_best_rep.countrycode == c]

        new_row = df[df.key_id == row.key_id.values[0]]

        newcode = new_row.countrycode.values[0]

        code3 =''
        if newcode in ccode.cc2.values:
            code3 = ccode[ccode.cc2==new_row.countrycode.values[0]].cc3.values[0]
        else:
            code3 = 'XYZ'

        new_row['cc3'] = code3

        best_rep_drawing.iloc[i,:]=new_row.values
        i += 1


    best_rep_drawing.to_json((str(item) + "_rep.json"), orient='records')

    print ('completed for -- ',(str(item) ))

