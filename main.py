#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/20/17 4:57 PM
# @Author  : Tony Cao
# @File    : main.py

import csv
import random
import math
import operator


# 处理数据 训练数据集数据量/测试数据集数据量的比值取67/33是一个常用的惯例
def loadDataset(filename, split, trainingSet=[], testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset) - 1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])


# trainingSet = []
# testSet = []
# loadDataset('iris.data', 0.66, trainingSet, testSet)
# print('Train: ' + repr(len(trainingSet)))
# print('Test: ' + repr(len(testSet)))


# 相似度
def euclideanDistance(instance1, instance2, length):
    distance = 0
    # 差的平方和
    for x in range(length):
        distance += pow(instance1[x] - instance2[x], 2)
    return math.sqrt(distance)


# data1 = [2, 2, 2, 'a']
# data2 = [4, 4, 4, 'b']
# distance = euclideanDistance(data1, data2, 3)
# print(repr(distance))


# 临近元素
def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        # 根据前2个数据计算相似度
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        # 实验数据和相似度的集合数组
        distances.append((trainingSet[x], dist))
    # 根据相似度排序
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    # 取出前k个
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


# trainingSet = [[2, 2, 2, 'a'], [4, 4, 4, 'b']]
# testInstance = [5, 5, 5]
# k = 1
# neighbors = getNeighbors(trainingSet, testInstance, k)
# print(neighbors)


# 预测结果  投票
def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


# neighbors = [[1, 1, 1, 'a'], [2, 2, 2, 'a'], [3, 3, 3, 'c']]
# response = getResponse(neighbors)
# print(response)


# 准确度
# 计算在测试数据集中算法正确预测的比例，这个比例叫分类准确度。
def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        test = testSet[x][-1]
        pred = predictions[x]
        print('test:'+test+', pred:'+pred)
        if test == pred:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


# testSet = [[1, 1, 1, 'a'], [2, 2, 2, 'a'], [3, 3, 3, 'c']]
# predictions = ['a', 'a', 'a']
# accuracy = getAccuracy(testSet, predictions)
# print(accuracy)

def main():
    # prepare data
    trainingSet = []
    testSet = []
    split = 0.66
    loadDataset('iris.data', split, trainingSet, testSet)
    print('Train: ' + repr(len(trainingSet)))
    print('Test: ' + repr(len(testSet)))

    # generate predictions
    predictions = []
    k = 3
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(accuracy) + '%')

main()


