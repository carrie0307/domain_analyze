# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import csv
'''
将具有大小意义的，按照map转换;
其他保持字符串状态，由OneHotEncoder处理
'''

# 将从csv文件读取的内容转化为DataFrame形式
def generate_dataframe(filename):
    '''
    将从csv文件读取的内容转化为DataFrame形式
    :return DataFrame
    '''
    f=open(filename,'r')
    reader=csv.reader(f)
    features = []
    for index, line in enumerate(reader):
        if index != 0:
            features.append(line[0:8])
    df = pd.DataFrame(features)
    df.columns = ['domain', 'tld','email_type','spon_registrar','keyword', 'httpcode', 'locate_cmp', 'web_judge_result']
    return df


def encode_class_labes(df):
    '''
    把 类别名 也转化为 interger（由于特征项已经转化，所以这里不做转化）
    '''
    class_mapping = {label:idx for idx,label in
                 enumerate(np.unique(df['web_judge_result']))}
    # 最终把 classlabel 也转化为 interger
    df['web_judge_result'] = df['web_judge_result'].map(class_mapping)
    return df


def encode_nominal_labes(df):
    # ohe = OneHotEncoder(categorical_features=[0], sparse=False)
    df = pd.get_dummies(df[['tld','email_type','spon_registrar','keyword', 'httpcode', 'locate_cmp', 'web_judge_result']])
    # 这里一定要令df=pd.get_dummies(df[['####',...]]),否则df不变
    return df


def write_csv_file(file_path, df):
    df.to_csv(file_path, index=False)


if __name__ == '__main__':
    df = generate_dataframe('../data/dataset-http-cmp-more.csv')
    df = encode_class_labes(df)
    df = encode_nominal_labes(df)
    # print df
    write_csv_file('../data/coding-features.csv', df)
