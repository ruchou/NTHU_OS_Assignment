
class Task:
   weight=0
   def __init__(self, name, release, cpuBurst):
       self.name=name
       self.release=release
       self.cpuBurst=cpuBurst
       self.waitingTime=0
       self.remainTime=cpuBurst
       self.lastDispatchedTime=release
       self.completionTime=0
       self.clock=release
       self.fifo_prio=100


      # the task has a string name, release time and cpuBurst.
      # the constructor may also need to initialize other fields,
      # for statistics purpose.  Examples include
      # waiting time
      # remaining time
      # last dispatched time, and
      # completion time

   def __str__(self):
     return self.name

   def __repr__(self):
     # note: the field names here are just examples.
     # if you name them differently, please change them accordingly.
     return self.__class__.__name__ + '(%s, %d, %d)' % (repr(self.name), self.release, self.cpuBurst)

   _KNOWN_SCHEMES = ["FCFS", "SJF", "RR"]
   def setPriorityScheme(self, scheme="SJF"):
     """
        the scheme can be "FCFS", "SJF", "RR", etc
     """
     if not scheme in _KNOWN_SCHEMES:
        raise ValueError("unknown priority scheme %s: must be FCFS, SJF, RR")
     self.scheme = scheme

   def __str__(self):
     return self.name

   def decrRemaining(self):
       self.cpuBurst = self.cpuBurst - 1
     # call this method to decrement the remaining CPU burst time


   def remainingTime(self):
       return self.cpuBurst
     # return the remaining CPU burst time

   def done(self):
       if self.cpuBurst == 0:
           return  True
       else:
           return  False
     # returns a boolean for if this task has remaining work to do

   def setCompletionTime(self, time):
       self.completionTime=time
     # records the clock value when the task is completed

   def turnaroundTime(self):
       return  self.completionTime-self.release
      # returns the turnaround time of this atask, as on
      # week 7 lecture slide 10

   def incrWaitTime(self):
       self.waitingTime=self.waitingTime+1
      # increments the amount of waiting time

   def releaseTime(self):
       return self.release
     # returns the release time of ths task

   def __iter__(self):
      # this enables converting the task into a tuple() type so that
      # the priority queue can just cast it to tuple before comparison.
      # it depends on the policy
      if (self.scheme == 'FCFS'):
         t = (self.release,self.release )  # example, but you may want a secondary
           # priority for tie-breaker. if so, just add them to the tuple.
      elif (self.scheme == 'SJF'): # shortest job first
         t = (self.cpuBurst,self.release)# tuple that defines priority in terms of "job length"
             # or is it really job length?
      elif (self.scheme == 'RR'): # round robin
        t =(self.fifo_prio,self.lastDispatchedTime)# define round robin priority if you use a MinHeap;
             # or you could just use a FIFO.
      else:
         raise ValueError("Unknown scheme %s" % self.scheme)
      for i in t:
         yield i

