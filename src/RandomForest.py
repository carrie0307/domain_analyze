#coding:utf-8

'''
    构建RandomForest模型
'''
from __future__ import division
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn import preprocessing
import csv
import get_features


def deal_division(num):
    return eval(num) / 10


def build_decision_tree(filename):
    """
        读取data.csv建立模型
    """
    f=open(filename,'r')
    reader=csv.reader(f)
    x=[]
    y=[]
    for index, line in enumerate(reader):
        if index != 0:
            # x.append(map(deal_division, line[1:7]))
            x.append(line[1:7])
            y.append(line[-1])
    x_train,x_test,y_train,y_test=cross_validation.train_test_split(x,y, test_size=0.2)
    # criterion='entropy',max_depth=5
    clf = RandomForestClassifier(n_estimators=10, max_depth=None,min_samples_split=2, random_state=42)
    clf=clf.fit(x_train,y_train)
    score=clf.score(x_test,y_test)
    print score
    return clf,score



def predict(domain, clf):
    # d = get_features.Domain_features(domain)
    # features = d.get_domain_features()
    features = [1, 1, 12, 1, 3, 4]
    print clf.predict([features])


if __name__ == '__main__':
    clf, score = build_decision_tree('../data/dataset-http-cmp-more.csv')
    f=open('../data/dataset-http-cmp-more.csv','r')
    reader=csv.reader(f)
    counter = 0
    print 'predicting ...'
    for index, line in enumerate(reader):
        if index != 0:
            print line[1:7]
            res = clf.predict([line[1:7]])[0] # 得到预测结果
            print res
            if res == str(line[-1]):
                counter = counter + 1
    print "正确预测:" + str(counter) + "\n"
    print "准确率：" + str(counter / index) + "\n"

    # clf, score = build_decision_tree('../data/dataset-http-cmp-more.csv')
    # predict("boda19.com", clf)
