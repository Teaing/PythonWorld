#!/usr/bin/env python
# -*- coding: utf_8 -*-


from itertools import groupby


def main():
    lst = [1, 2, 3, 5, 6, 7, 8, 11, 12, 13, 80, 90, 91, 99, 92]
    print convertData(lst)


def convertData(inputList):
    '''
    :param inputList:
    [1, 2, 3, 5, 6, 7, 8, 11, 12, 13, 80, 90, 91, 99, 92]
    [1, 2, 3, '5', '6', 7, 8, 11, 12, 13, 80, 90, 91, 99, 92]
    ['1', '2', '3', '5', '6', '7', '8', '11', '12', '13', '80', '90', '91', '99', '92']
    :return:
    1-3,5-8,11-13,80,90-92,99
    '''
    try:
        inputList = map(int, inputList)
    except:
        raise Exception('input data have string.')
    inputList.sort()
    # fun = lambda (i, v): v - i
    fun = lambda x: x[1] - x[0]
    outputList = []
    for k, g in groupby(enumerate(inputList), fun):
        tmpData = [v for i, v in g]
        if len(tmpData) == 1:
            outputList.append(str(tmpData[0]))
            continue
        outputList.append('-'.join([str(tmpData[0]), str(tmpData[-1])]))
    return ','.join(outputList)


if __name__ == '__main__':
    main()
