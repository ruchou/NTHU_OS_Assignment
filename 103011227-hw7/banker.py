# Bankers Algorithms is a resource allocation and deadlock
# avoidance algorithm developed by Edsger Dijkstra
# that tests for safety by simulating the allocation of
# predetermined maximum possible amounts of all resources
 
# utility functions 

def sumColumn(M, col):
   '''
       M is a row major matrix, and col is the column index.
       returns the scalar sum of the values in the column.
   '''
   return sum(list(map(lambda x: x[col], M)))
#  it is the same as
#   tot = 0
#   for row in M:
#     tot += row[col]
#   return tot

def IncrVec(A, B):
   '''
     vector A += B, assuming len(A) == len(B)
   '''
   for i in range(len(A)):
      A[i]=A[i]+B[i]
   # your code here

def DecrVec(A, B):
   '''
     vector A -= B, assuming len(A) == len(B)
   '''
   for i in range(len(A)):
      A[i]=A[i]-B[i]
   # your code here
 
def GtVec(A, B):
   '''
      vector greater-than.
      if one or more of A[i]>B[i], the whole thing is true
   '''
   for i in range(len(A)):
      if A[i] > B[i]:
         return  True
   return False


   # your code here

def LeVec(A, B):
   '''
     vector A[i] <= B[i] (less-than-or-equal-to).
     True if ALL pairs are true.
   '''
   for i in range(len(A)):
      if A[i]>B[i]:
         return False
   return True

   # your code here

class Banker:
   def __init__(self, alloc, max, totalRsrc):
      self.Allocation = alloc
      self.n = len(alloc) # number of processes
      self.TotalResources = totalRsrc
      self.m = len(totalRsrc)  # number of resources
      # the following line allows the deadlock detection algorithm
      # to be able to subclass without max (since it doesn't need it)
      if max is not None:
         self.Max = max
         self.Need =[ [self.Max[i][j]-self.Allocation[i][j] for j in range(self.m) ]  for i in range(self.n) ]
         #[n][m]
         # your code here to initialize the Need matrix.
              # Need[i][j] = Max[i][j] - Allocation[i][j] \

      self.Available = [self.TotalResources[i]-sumColumn(self.Allocation,i) for i in range(self.m)]

      # instances of resource type Rj available


      # your code here to compute Available vector.
      # hint: involves TotalResources and sumColumn() function,
      # a boolean flag to indicate whether in Safety() function you want to
      # print the traced output. by default False, but can be set to True.
      self.traceSafety = True
 
   def Safety(self):
      if self.traceSafety: print('Need=%s, Available=%s' % (self.Need, self.Available))
      # step 1
      Sequence = []  # use this list to save the safe sequence 
      Finish = [False for i in range(self.n)]
      Work = [self.Available[i] for i in range(self.m)]# your code to initialize Work vector
      # step 2
      for _ in range(self.n):
          for i in range(self.n):

              # follow the pseudocode on slide 37
              # may need to print
              #
              # compare Need[i] with Work.
              if Finish[i]==True:
                 if self.traceSafety:print("i=%d Finish[%d] True, skipping" %(i,i))
                 continue
                 #skip
              if self.traceSafety:
                 print('i=%d, (Need[%d]=%s) <= (' %(i,i,self.Need[i] ), end="")
                 print('(Work=%s)'%(Work), end="")

              if LeVec(self.Need[i],Work):
                 if self.traceSafety:
                    print(' True, append P%d'%(i),end="")
                 IncrVec(Work,self.Allocation[i])
                 Finish[i]=True
                 Sequence.append(i)
              else:
                 if self.traceSafety:
                    print(' False, P%d must wait'%(i),end="")

              if self.traceSafety: print()

              if all(Finish)==True:
                 return Sequence
      return  None
              # - hint: you may use LecVec(A, B) for A <= B:
              #
              # step 3
              # - update bookkeeping including Work, Finish, and add to sequence
              # - Hint: you may want to use IncrVec() for Work += Allocation
              # 
      # step 4. return the sequence if there is one, or None if not.
 
   def Request(self, i, rqst):  # slide 47

      '''
         called with the requesting process i and the resource vector
         for how many instances of each resource to request.
         the rqst is a vector of m length.
      '''
      # step 1
      # hint: use GtVec of LeVec to compare request vector rqst with Need[i]
      # raise an exception if over
      # step 2
      # in case of wait, simply return None
      # step 3
      # pretend to allocate requested resource:
      # save snapshot of Available, Allocation, and Need
      # update Available, Allocation, and Need
      # call Safety()
      # if a safe sequence exists, return it.
      # otherwise, restore saved snapshot and return None

      if LeVec(rqst,self.Need[i]):
         if LeVec(rqst,self.Available):
            tmp_avai = self.Available
            tmp_allo=self.Allocation
            tmp_need=self.Need
            self.Available = [self.Available[i] - rqst[i] for i in range(self.m)]
            self.Allocation[i]=[self.Allocation[i][j]+rqst[j] for j in range(self.m)]
            self.Need[i]=[self.Need[i][j]-rqst[j] for j in range(self.m) ]

            if self.Safety() != None:
               return rqst
            else:
               self.Available=tmp_avai
               self.Allocation=tmp_allo
               self.Need=tmp_need
               return None
            #Available[:] = Available[:] – Requesti[:];
            # Allocationi[:] = Allocationi[:] + Requesti[:];
            # Needi[:] = Needi[:] – Requesti[:];
         else:
            return None
            # Pi must wait, since resources are not available
      else:
         return 'error condition'




   def Release(self, i):
      '''
               need this function to release the resources allocated to process P_i
               after it has finished execution.
      '''
      IncrVec(self.Available,self.Allocation[i])
      self.Allocation[i]=[0]*self.m
      IncrVec(self.Need[i],self.Allocation[i])




         # hint: update Available, Allocation, and Need.
      # hint: you may want to call utility functions IncrVec
      # hint: but in which order? who goes first, last, or don't care?

 
######################## 
def TestUtility():
   print('Testing Utility Functions:')
   # test vector. A, B, C, compare.  Here A + B = C, and A > B.
   L = [[[1, 2, 1], [1, 0, 2], [2, 2, 3], True],
        [[1, 2, 3], [2, 2, 4], [3, 4, 7], False],
        [[2, 3, 3], [2, 3, 3], [4, 6, 6], False]]

   for T in L:
      # make a copy
      A, B, C, compare = T[0][:], T[1][:], T[2][:], T[3]
      print('A = %s, B = %s, ' % (A, B))
      IncrVec(A, B)
      print('A += B is %s, expect %s' % (A, C))
      DecrVec(A, B)
      print('A -= B is %s, expect %s' % (A, T[0]))
      print('A > B is %s, expect %s; A <= B is %s, expect %s' % (GtVec(A, B), compare, LeVec(A, B), not compare))

def TestConstructor():
   Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
   Max        = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
   Available=[3, 3, 2],
   Need=[[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
   TotalResources = [10, 5, 7]
   b = Banker(Allocation, Max, TotalResources)
   # check Available and Need are computed properly
   print("b.Available=%s, expect %s" % (b.Available, Available))
   print("b.Need=%s, expect %s" % (b.Need, Need))

def TestSafety():
   Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
   Max        = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
   TotalResources = [10, 5, 7]
   b = Banker(Allocation, Max, TotalResources)
   b.traceSafety = True
   s = b.Safety()
   b.traceSafety = False
   print('s is %s' % s)
   return b, s

def TestRequests(banker, sequence):
   n = 5
   m = 3
   requestVector = [[0, 2, 0], [1, 0, 2], [3, 0, 0], [0, 1, 1], [3, 3, 0]]
   if sequence is None:
      print('impossible to safely satisfy request vector')
   else:
      print('Found safe sequence %s' % sequence)
      # follow the sequence
      for j in range(n):
         i = sequence[j]
         print('P%d allocated %s, requesting %s, ' % (i, banker.Allocation[i], requestVector[i]))
         if banker.Request(i, requestVector[i]) is None:
            print('err: following sequence %s but cannot fulfil P%d request %s' % (s, i, requestVector[i]))
         banker.Release(i)
         print(" P%d releasing, available=%s" % (i, banker.Available))


if __name__ == '__main__':
   TestUtility()
   TestConstructor()
   banker, sequence = TestSafety()
   TestRequests(banker, sequence)
