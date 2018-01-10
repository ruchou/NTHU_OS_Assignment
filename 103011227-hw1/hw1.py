# hw1.py
# -*- coding: UTF-8 -*-
# Bill Chou 周延儒, 103011227
# comments

def PrintBST(T):
   if T==None:
       return
   else:
       PrintBST(T[1])
       print(T[0])
       PrintBST(T[-1])


## begin built-in test case follows your code in the same .py file
if __name__ == '__main__':
  T = (17, (12, (6, None, None), (14, None, None)), (35, (32, None, None), (40, None, None)))
  PrintBST(T)
