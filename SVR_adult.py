# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import  OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
from sklearn import preprocessing
from sklearn.model_selection import  train_test_split
from sklearn.preprocessing import StandardScaler
#%%
def checkvalue(df,index_title):
    a=[]
    b=[]
    for i in index_title:
        a.append(df[df[i]==' ?'].index.tolist())
    for i in a:
        if len(i)>0:
            for x in i:
                if x not in b:
                    b.append(x)
    df = df.drop(index=b)
    lens=len(b)
    return df ,lens
def norm(df):
    df_norm = (df - df.mean()) / df.std()
    return  df_norm
        
def str_transform(df):
    #數值處理 最大駔小歸一化
    #字串處理 
    labelencoder = LabelEncoder()
    df['age'] = df['age']
    df['workclass'] =labelencoder.fit_transform(df['workclass'])
    df['fnlwgt'] = norm(df['fnlwgt'])
    df['education'] = labelencoder.fit_transform(df['education'])
    df['education_num'] = df['education_num']
    df['marital_status'] = labelencoder.fit_transform(df['marital_status'])
    df['occupation'] = labelencoder.fit_transform(df['occupation'])
    df['relationship'] = labelencoder.fit_transform(df['relationship'])
    df['race'] = labelencoder.fit_transform(df['race'])
    df['sex'] = labelencoder.fit_transform(df['sex'])
    df['capital_gain'] =  norm(df['capital_gain'])
    df['capital_loss'] =  norm(df['capital_loss'])
    df['hours_per_week'] = df['hours_per_week']
    df['native_country'] = labelencoder.fit_transform(df['native_country'])
    df['salary'] = labelencoder.fit_transform(df['salary'])
    #corrdf=df.corr()
    #print(corrdf['hours_per_week'].sort_values(ascending=False))
    return df
def splt_X_Y(df):
    X = [df['age'],
    df['workclass'],
    df['education'],
    df['education_num'],
    df['sex'],
    df['capital_gain'],
    df['capital_loss'],
    df['salary'],df['native_country'], df['relationship'],df['occupation'],df['marital_status'],df['fnlwgt']]

    Y = [df['hours_per_week']]
    return X,Y
def rshape(arr):
    a=arr.shape[1]
    b=arr.shape[0]
    if a>b:
        arr=arr.reshape(a,b)
    return arr 
#%%
index_title=['age','workclass','fnlwgt','education','education_num','marital_status','occupation','relationship','race','sex','capital_gain','capital_loss','hours_per_week','native_country','salary']
df = pd.read_csv(filepath_or_buffer="adult.test.txt",header=0,names=index_title)
df2 = pd.read_csv(filepath_or_buffer="adult.train.txt",header=0,names=index_title)

print(df.isnull().sum())#確認是否有缺值
print("_____")
df , lens= checkvalue(df,index_title)
print(f'找到並刪除 {lens}')
df2,lens2 = checkvalue(df2,index_title)
print(f'找到並刪除 {lens2}')
print("_____")


#%%兩個資料合併轉換#檢查相關性刪除低相關性

X_train,y_train = splt_X_Y(str_transform(df))
X_test,y_test =  splt_X_Y(str_transform(df2))

X_train=rshape(np.array(X_train))
y_train=rshape(np.array(y_train))

X_test=rshape(np.array(X_test))
y_test=rshape(np.array(y_test))




from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

clf = SVR(kernel='rbf', degree=3, gamma='scale', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=2, max_iter=500).fit(X_train, y_train)
p = clf.predict(X_test)
s = clf.score(X_test, y_test)
print("MAPE",np.mean(np.abs((y_test - p) / y_test)) * 100)
print("RMSE",np.sqrt(metrics.mean_squared_error(y_test, p)))