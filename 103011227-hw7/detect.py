# Deadlock Detection, similar to Banker's

from banker import Banker, sumColumn, IncrVec, DecrVec, GtVec ,LeVec

class DeadlockDetector(Banker):
   def __init__(self, alloc, totalRsrc):
      Banker.__init__(self, alloc, None, totalRsrc)

   def detect(self, Request):
      '''detect deadlock with the request matrix'''
      # 1(a) initialize Work = a copy of Available
      # 1(b) Finish[i] = (Allocation[i] == [0, ...0])
      # optionally, you can keep a Sequence list
      #work m finish n
      self.work=[self.Available[i] for i in range(self.m)]
      self.finish=[self.Allocation[i]==0 for i in range(self.n)]
      seq=list()

      print(self.finish)

      for _ in range(self.n):
          for i in range(self.n):
             if self.finish[i]==True:
                if all(self.finish)==True:
                   return seq
                print('i=%d, Finish[%d] is True, skipping' %(i,i))
                continue

             print('i=%d, '%i,end='')
             print('(Request[%d]=%s) <= (Work=%s)' % (i,Request[i],self.work),end='')
             if LeVec(Request[i],self.work):
                IncrVec(self.work,self.Allocation[i])
                self.finish[i]=True
                print(' True, append P%d (+Allocation[%d]=%s)=> Work=%s, Finish=%s' %(i,i,self.Allocation[i],self.work,self.finish))
                seq.append(i)
             elif all(self.finish)==True:
                return seq
             else:
                print(' False, P%d must wait' %i)



              # Step 2: similar to safety algorithm
              #   if there is an i such that (Finish[i] == False)
              #   and Request_i <= Work, (hint: LeVec() or GtVec()) then
              #   Step 3: 
              #     Work += Allocation[i] # hint IncrVec()
              #     Finish[i] = True
              #        continue Step 2
      # Step 4: either done iterating or (no such i exists)
      #    Finish vector indicates deadlocked processes.
      #    if all True then no deadlock.

 
if __name__ == '__main__':
   Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1], [0, 0, 2]]
   Request    = [[0, 0, 0], [2, 0, 2], [0, 0, 0], [1, 0, 0], [0, 0, 2]]
   Available  = [0, 0, 0]
   TotalResources = [7, 2, 6]
   d = DeadlockDetector(Allocation, TotalResources)
   s = d.detect(Request)
   if s is not None:
      print('sequence = %s' % s)
   else:
      print('deadlock')

   #testcase2
   Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1], [0, 0, 2]]
   Request = [[0, 0, 0], [2, 0, 2], [0, 0, 1], [1, 0, 0], [0, 0, 2]]
   Available = [0, 0, 0]
   TotalResources = [7, 2, 6]
   d = DeadlockDetector(Allocation, TotalResources)
   s = d.detect(Request)
   if s is not None:
      print('sequence = %s' % s)
   else:
      print('deadlock')
 
