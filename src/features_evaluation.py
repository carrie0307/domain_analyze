# -*- coding: UTF-8 -*-
'''
    通过随即森林评估各特征项
    其他方法详见下文
    https://yongle.gitbooks.io/datamining/content/w5-tuning-parameter/5w.html
'''
import pandas as pd
import numpy as np
import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import matplotlib.pyplot as plt


def get_pd(filename):
    '''
    读取DataFrame文件
    ：param filename:csv文件完整路径
    '''
    f=open(filename,'r')
    reader=csv.reader(f)
    features = []
    for index, line in enumerate(reader):
        if index != 0:
            features.append(line)
        else:
            columns = line
        if index > 10:
            break
    df = pd.DataFrame(features)
    df.columns = columns
    return df


def get_feature_importance_RF(df):
    '''
    用随机森林得到各特征项feature_importances
    ：param df:输入要处理数据的DataFrame
    ：return importances：各特征项feature_importances_数值
    ：return X_train：返回训练集
    :return fet_labels:特征项名
    注意：具体使用时，df.iloc位置选择值的填写，根据读入的DataFrame的格式（是否包括index、是否包括列名）调整
    '''
    X, y = df.iloc[:, 1:-1].values, df.iloc[:,-1].values
    feat_labels = df.columns[1:-1] # 得到特征项名
    X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y, test_size=0.2) # 划分测试集与训练集
    # 使用 decision tree 或 random forests 不需要 standardization或 normalization
    forest = RandomForestClassifier(n_estimators=1000,
                                    random_state=0,
                                    n_jobs=-1)
    forest.fit(X_train, y_train)
    # random forest 比较特殊, 有 feature_importances 这个 attribute
    importances = forest.feature_importances_ # 各特征项feature_importances_数值
    print importances
    indices = np.argsort(importances)
    print indices
    indices = np.argsort(importances)[::-1] # 各特征项根据feature_importances_排列大小的名次
    print indices
    '''
    若importances = [ 0.06116747  0.14034532  0.36585658  0.09692444  0.0488177   0.18988849]，
    则indices = [2 5 3 1 4 0], 即index=2的数是最大的，从大到小接下来是index为5,3,1...的数
    如果不加[::-1],则indices即为[5,3,0,2,4,1],即index=0的数从大到小排5,依次类推 ...
    '''
    # 输出各特征重要性
    for i, idx in enumerate(indices):
        print("%2d) %-*s %f" % (i + 1, 30,
                                feat_labels[idx],
                                importances[idx]))
    return importances,X_train,feat_labels


def plt_show_importance(X_train, importances,feat_labels):
    '''
    柱状图展示特征性feature_importances数值
    :param X_train：划分好的测试集数据
    :param importances：各特征项feature_importances_数值
    '''
    indices = np.argsort(importances)[::-1]
    plt.title('Feature Importances')
    plt.bar(range(X_train.shape[1]),
        importances[indices],
        color='lightblue',
        align='center')

    plt.xticks(range(X_train.shape[1]),
           feat_labels[indices], rotation=90)
    plt.xlim([-1, X_train.shape[1]])
    plt.tight_layout()
    plt.show()





if __name__ == '__main__':
    df = get_pd('../data/dataset-http-cmp-more.csv')
    importances,X_train,feat_labels = get_feature_importance_RF(df)
    plt_show_importance(X_train, importances,feat_labels)
