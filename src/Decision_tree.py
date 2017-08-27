#coding:utf-8

'''
    构建决策树模型
'''
from __future__ import division
from sklearn import tree
from sklearn import cross_validation
from sklearn import preprocessing
import csv
import sys
import graphviz
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
            # x.append(map(deal_division, line[1:6]))
            x.append(line[1:])
            y.append(line[0])
    x_train,x_test,y_train,y_test=cross_validation.train_test_split(x,y, test_size=0.2)
    # criterion='entropy',max_depth=5
    clf=tree.DecisionTreeClassifier(criterion='entropy', random_state=42) # 推荐42，目前测算score最高
    clf=clf.fit(x_train,y_train)
    score=clf.score(x_test,y_test)
    print score
    return clf,score


def main(filename):
    clf, score = build_decision_tree(filename)
    # dot_data = tree.export_graphviz(clf,out_file='data-3-gini-tree.dot', feature_names=['tld','email_type','spon_registrar','keyword','locate_cmp'],
    #                      class_names=['1','2'], filled=True, rounded=True)
    # graph = graphviz.Source(dot_data)


def predict(domain,clf):
    # d = get_features.Domain_features(domain)
    # features = d.get_domain_features()
    features = [1, 1, 12, 1, 3, 4]
    print clf.predict([features])




if __name__ == '__main__':
    clf, score = build_decision_tree('../data/coding-features.csv')
    '''
    f=open('../data/dataset-http-cmp-more.csv','r')
    reader=csv.reader(f)
    counter = 0
    for index, line in enumerate(reader):
        if index != 0:
            res = clf.predict([line[1:]])[0] # 得到预测结果
            if int(res) == int(line[0]):
                counter = counter + 1
    print "正确预测:" + str(counter) + "\n"
    print "准确率：" + str(counter / index) + "\n"
'''
    # clf, score = build_decision_tree('../data/dataset-http-cmp-more.csv')
    # predict("boda19.com",clf)
