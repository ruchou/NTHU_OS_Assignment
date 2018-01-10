from fifo import FIFO
from minheap import MinHeap
from task import Task
from npsched import NPScheduler

class PScheduler(NPScheduler):
   # this means it can inherit 
   # __init__(), addTask(), dispatch(), releaseTasks()
   # clockGen(), getSchedule(), and other methods

   def preempt(self):
      self.readyQueue.put(self.running)
      self.running=None
      self.running = self.readyQueue.get()
      self.running.lastDispatchedTime = self.clock
      if self.readyQueue.head():
         self.running.fifo_prio=self.readyQueue.head().fifo_prio+1



      # this is the new method to add to put the running task
      # back into ready queue, plus any bookkeeping if necessary.

   def schedule(self):
      self.releaseTasks() # same as before

      if self.checkTaskCompletion() == False:
         if self.readyQueue.head():
            run=tuple(self.running)
            head=tuple(self.readyQueue.head())
            if  run >= head:
               self.running.fifo_prio=self.clock+1
               self.preempt()
               pass

         if self.running :
               self.running.fifo_prio=self.running.fifo_prio+1
         self.ganttChart.put(self.running)

         for i in self.readyQueue:
            i.incrWaitTime()



      else:
         self.running = self.readyQueue.head()
         self.dispatch(self.readyQueue.head())

         if self.running and self.readyQueue.head() :
            self.running.fifo_prio=self.readyQueue.head().fifo_prio+self.readyQueue.__len__()+1




         # still have operation to do.
         # see if running task or next ready task has higher priority
         # hint: compare by first typecasting the tasks to tuple() first
         #   and compare them as tuples.  The tuples are defined in
         #   the __iter__() method of the Task class based on policy.
         # if next ready is not higher priority, redispatch current task.
         # otherwise,
         # - swap out current running (by calling preempt method)
      # task completed or swapped out
      # pick next task from ready queue to dispatch, if one exists.
   # inherit 
   # - clockGen(self):
   # - getSchedule(self):
   # - getThroughput(self):
   # - getWaitTime(self):
   # - getTurnaroundTime(self):







def testPScheduler(tasks, policy):
   # the tuples are release time, cpuBurst, taskName
   nClocks = 20
   scheduler = PScheduler(nClocks, policy)
 
   for t in tasks:
      scheduler.addTask(t)

   for clock in scheduler.clockGen():
      pass

   # the following are for part 2.5
   thruput = scheduler.getThroughput()
   waittime = scheduler.getWaitTime()
   turnaround = scheduler.getTurnaroundTime()

   print('preemptive %s: %s' % (policy, scheduler.getSchedule()))

   # the following is for testing part 2.5
   print('  thruput = %s = %.2f, warittimes = %s = %.2f, turnaroundtime = %s = %.2f'\
       % (thruput, thruput[0]/thruput[1],
          waittime, waittime[0]/waittime[1],
          turnaround, turnaround[0]/turnaround[1]))

if __name__ == '__main__':
   tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
   print('tasks = %s' % tasks)
   for policy in ['SJF', 'FCFS', 'RR']:
      tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
      testPScheduler(tasks, policy)
