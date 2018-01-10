#

import bisect

class MemAlloc:

   _POLICIES = ('FirstFit', 'BestFit', 'WorstFit')

   def __init__(self, totalMemSize, policy = 'BestFit'):
      if not policy in MemAlloc._POLICIES:
         raise ValueError('policy must be in %s' % MemAlloc._POLICIES)
      self.allocation = { } # map pointer to (size)
      self.holes = [(0, totalMemSize)] # sorting by pointer
      # your code here
      self.policy=policy
      self.totalMemsize=totalMemSize
   # insert your own utility methods as needed

   def malloc(self, reqSize):
      '''return the starting address of the block of memory, or None'''
      # your code here
      if self.policy=='FirstFit':
         # first free block size >= n
         for i in self.holes:
            hole_add,hole_size=i
            if hole_size>=reqSize:
               self.holes.remove(i)
               if hole_size - reqSize > 0:
                  self.holes.append((hole_add+reqSize,hole_size-reqSize))


               #allocation
               self.allocation[hole_add]=reqSize
               self.holes.sort()

               return hole_add
            pass

         pass
      elif self.policy=='BestFit':
         #find best  free block and the smallest difference between blocksize- request >=0
         diff=self.totalMemsize
         best_hold=None
         for i in self.holes:
            hole_add, hole_size = i
            if hole_size>=reqSize:
               if hole_size-reqSize<diff:
                  diff=hole_size-reqSize
                  best_hold=i

         #find the best
         if best_hold:
            hole_add,hole_size=best_hold
            self.holes.remove(best_hold)
            if hole_size-reqSize>0:
               self.holes.append((hole_add + reqSize, hole_size - reqSize))


            # allocation
            self.allocation[hole_add] = reqSize
            self.holes.sort()

            return hole_add
      else:
         #locate largest available free portion （size – n）largest >=0
         # find best  free block and the smallest difference between blocksize- request >=0
         diff = -self.totalMemsize
         best_hold = None
         for i in self.holes:
            hole_add, hole_size = i
            if hole_size >= reqSize:
               if hole_size - reqSize >diff:
                  diff = hole_size - reqSize
                  best_hold = i
         # find the best
         if best_hold:
            hole_add, hole_size = best_hold
            self.holes.remove(best_hold)
            if hole_size - reqSize > 0:
               self.holes.append((hole_add + reqSize, hole_size - reqSize))

            # allocation
            self.allocation[hole_add] = reqSize

            self.holes.sort()
            return hole_add
         pass

      return None


   def free(self, pointer):
      '''free the previously allocated memory starting at pointer'''
      # your code here
      target_node=self.allocation[pointer]
      #get the desired free node
      if target_node==None:return

      target_add=pointer
      target_size=target_node

      if target_add==0 and target_size ==self.totalMemsize:
         self.holes.remove(target_node)
         self.holes.append((0,self.totalMemsize))

         self.allocation.clear()
         pass
      else:
         next_hole=None
         pre_hole=None

         for i in self.holes:
            hole_add,hold_size=i
            if target_add+target_size == hole_add:
               next_hole=i
            if target_add== hole_add+hold_size:
               pre_hole=i

         if pre_hole and next_hole:
            #merge the three
            pre_add,pre_size=pre_hole
            next_add,next_size=next_hole
            self.holes.remove(pre_hole)
            self.holes.remove(next_hole)
            self.holes.append((pre_add,pre_size+self.allocation[pointer]+next_size))

            del  self.allocation[pointer]


            pass
         elif pre_hole and not next_hole:

            pre_add, pre_size = pre_hole
            self.holes.remove(pre_hole)
            self.holes.append((pre_add, pre_size + self.allocation[pointer]))
            del self.allocation[pointer]

            pass
         elif  not pre_hole and next_hole:

            next_add, next_size = next_hole
            self.holes.remove(next_hole)
            self.holes.append( (pointer, self.allocation[pointer] + next_size) )
            del self.allocation[pointer]

            pass
         else:
            self.holes.append((pointer,self.allocation[pointer]))
            del self.allocation[pointer]

            pass





      self.holes.sort()



   def __str__(self):
      return repr(self.allocation)


def runTestScript(requests):
   ff = MemAlloc(20, 'FirstFit')
   bf = MemAlloc(20, 'BestFit')
   wf = MemAlloc(20, 'WorstFit')
   ffSym = {}
   bfSym = {}
   wfSym = {}
   for name, size in requests:
      if size is None:
         # do a free() call
         ff.free(ffSym[name]); del(ffSym[name])
         bf.free(bfSym[name]); del(bfSym[name])
         wf.free(wfSym[name]); del(wfSym[name])
         print('free(%s)' % name)
      else: 
         # do an malloc() call
         ffSym[name] = ff.malloc(size)
         bfSym[name] = bf.malloc(size)
         wfSym[name] = wf.malloc(size)
         print('%s=malloc(%d):' % (name, size))
      print(' FirstFit symbols=%s holes=%s allocation=%s' % (ffSym, ff.holes, ff.allocation))
      print(' BestFit symbols=%s holes=%s allocation=%s' % (bfSym, bf.holes, bf.allocation))
      print(' WorstFit symbols=%s holes=%s allocation=%s' % (wfSym, wf.holes, wf.allocation))

if __name__ == '__main__':

   requests = [('a', 10), ('b', 1), ('c', 4), ('c', None), ('a', None),
               ('d', 9),  # worst fit and first fit would use (0, 10), but best fit would use (11, 9)
               ('e', 10), # worst fit and first fit wold fail, but best fit would succeed with (0, 10)
    ]
   runTestScript(requests)

   print('------------------------')

   requests = [('a', 3), ('b', 6), ('c', 2), ('d', 5), # malloc
               ('a', None), ('c', None), # free
               ('e', 2),  # best fit (9, 2), first fit (0, 2), worst fit (16, 2)
               ('b', None), # free: best fit merges (0,3) and (3,6) => (0,9)
                   # first fit merges (3,6), (9,2) => (3, 8)
                   # worst fit merges (0,3), (3,6), (9,2) => (0,11)
               ('f', 11)   # both best fit and first fit fail, but worst fit succeeds
    ]
   runTestScript(requests)


   print('My test Case---------------')
   print('---------------------------')

   requests = [('a', 2), ('b', 1), ('c', 9), ('d', 1),('e',7),  # malloc
               ('a', None),('c',None),('e',None),
               ('f',2),
               ('g', 4),
               ('h', 4),
               ('i', 6),

               ]
   runTestScript(requests)
