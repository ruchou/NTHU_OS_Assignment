
# hw2.py
# -*- coding: UTF-8 -*-
# Bill Chou 周延儒, 103011227
# comments

def YieldBST(T):
   if T!=None:
       yield  from YieldBST(T[1])
       yield T[0]
       yield  from YieldBST(T[-1])



if __name__ == '__main__':
    L = []
    T = (17, (12, (6, None, None), (14, None, None)), (35, (32, None, None), (40, None, None)))

    for v in YieldBST(T):
        L.append(v)
    print(L)  # print list
