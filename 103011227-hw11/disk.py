# disk scheduling algorithms
#103011227
import copy

class DiskScheduler:
    _POLICIES = ['FCFS', 'SSTF', 'SCAN', 'LOOK', 'C-SCAN', 'C-LOOK']

    def __init__(self, nCylinders):
        self.nCylinders = nCylinders

    def schedule(self, initPos, requestQueue, policy, direction):
        '''
            request is the list of cylinders to access
            policy is one of the strings in _POLICIES.
            direction is 'up' or 'down'
            returns the list for the order of cylinders to access.
        '''
        l=[]
        if policy == 'FCFS':
            for i in requestQueue:
                l.append(i)
            return  l
            # return the disk schedule for FCFS

        if policy == 'SSTF':
            Request_tmp = requestQueue[:]
            high = max(Request_tmp)
            x = high
            min_seek = abs(initPos - high)
            Request_tmp.sort()
            while len(Request_tmp) > 0:
                # find the shortest distance from the current position
                for request in Request_tmp:
                    seek = abs(initPos - request)
                    if (seek < min_seek):
                        min_seek = seek
                        x = request
                initPos = x
                l.append(x)
                Request_tmp.remove(x)
                min_seek = abs(initPos - high)
                x = high

            return  l

            # shortest seek time first
            # compute and return the schedule for the shortest seek time first
        if policy in ['SCAN', 'C-SCAN', 'LOOK', 'C-LOOK']:
            if policy =='SCAN':

                if direction=='down':
                    n = len(requestQueue)
                    Request_tmp = requestQueue[:]
                    Request_tmp.sort()
                    if initPos != 0 and initPos < min(Request_tmp):
                        Request_tmp.append(0)

                    p = len(Request_tmp)

                    i = initPos - 1
                    #Order.append(initPos)
                    while i > 0:
                        for j in range(0, p):
                            if (Request_tmp[j] == i):
                                l.append(i)
                        i -= 1

                    if (i==0 and len(requestQueue)>len(l)) or (0 in Request_tmp ):
                        l.append(i)

                    k = initPos + 1
                    while k < self.nCylinders:
                        for q in range(0, n):
                            if (Request_tmp[q] == k):
                                l.append(k)
                        k += 1

                else:
                    n = len(requestQueue)
                    Request_tmp = requestQueue[:]
                    Request_tmp.sort(reverse=True)
                    if initPos != self.nCylinders and initPos > max(Request_tmp):
                        Request_tmp.append(self.nCylinders)

                    p = len(Request_tmp)

                    i = initPos +1

                    while i < self.nCylinders:
                        for q in range(0, n):
                            if (Request_tmp[q] == i):
                                l.append(i)
                        i+=1

                    if (i==self.nCylinders and len(requestQueue)>len(l)) and (self.nCylinders-1 not in Request_tmp):
                        l.append(self.nCylinders-1)

                    i =initPos-1

                    while i >= 0:
                        for j in range(0, p):
                            if (Request_tmp[j] == i):
                                l.append(i)
                        i -= 1
                return l
            elif policy=='C-SCAN':
                if direction == 'down':
                    n = len(requestQueue)
                    Request_tmp = requestQueue[:]
                    Request_tmp.sort()
                    if initPos != 0 and initPos < min(Request_tmp):
                        Request_tmp.append(0)

                    p = len(Request_tmp)

                    i = initPos
                    while i >= 0:
                        if i==0:
                            l.append(i)
                        else:
                            for j in range(0, p):
                                if (Request_tmp[j] == i):
                                    l.append(i)
                        i -= 1

                    k =self.nCylinders-1

                    while k >initPos :
                        if k==self.nCylinders-1:
                            l.append(k)
                        else:
                            for q in range(0, n):
                                if (Request_tmp[q] == k):
                                    l.append(k)
                        k -= 1

                else:
                    n = len(requestQueue)
                    Request_tmp = requestQueue[:]
                    Request_tmp.sort(reverse=True)
                    if initPos != self.nCylinders and initPos > max(Request_tmp):
                        Request_tmp.append(self.nCylinders)

                    p = len(Request_tmp)

                    i = initPos

                    while i < self.nCylinders:
                        if i==(self.nCylinders-1):
                            l.append(i)
                        else:
                            for q in range(0, n):
                                if (Request_tmp[q] == i):
                                    l.append(i)
                        i += 1

                    i = 0

                    while i < initPos:
                        if i==0:
                            l.append(i)
                        else:
                            for j in range(0, p):
                                if (Request_tmp[j] == i):
                                    l.append(i)
                        i += 1
                return l

            elif policy=='LOOK':
                if direction == 'down':
                    n = len(requestQueue)
                    Request_tmp = requestQueue[:]
                    Request_tmp.sort()
                    if initPos != 0 and initPos < min(Request_tmp):
                        Request_tmp.append(0)

                    p = len(Request_tmp)

                    i = initPos - 1
                    # Order.append(initPos)
                    while i >= 0:
                        for j in range(0, p):
                            if (Request_tmp[j] == i):
                                l.append(i)
                        i -= 1

                    k = initPos + 1
                    while k < self.nCylinders:
                        for q in range(0, n):
                            if (Request_tmp[q] == k):
                                l.append(k)
                        k += 1

                else:
                    n = len(requestQueue)
                    Request_tmp = requestQueue[:]
                    Request_tmp.sort(reverse=True)
                    if initPos != self.nCylinders and initPos > max(Request_tmp):
                        Request_tmp.append(self.nCylinders)

                    p = len(Request_tmp)

                    i = initPos + 1

                    while i < self.nCylinders:
                        for q in range(0, n):
                            if (Request_tmp[q] == i):
                                l.append(i)
                        i += 1

                    i = initPos - 1

                    while i >= 0:
                        for j in range(0, p):
                            if (Request_tmp[j] == i):
                                l.append(i)
                        i -= 1
                return l
            elif  policy=='C-LOOK':
                if direction == 'down':
                    n = len(requestQueue)
                    Request_tmp = requestQueue[:]
                    Request_tmp.sort()
                    if initPos != 0 and initPos < min(Request_tmp):
                        Request_tmp.append(0)

                    p = len(Request_tmp)

                    i = initPos
                    while i >= min(Request_tmp):
                        if i==0:
                            l.append(i)
                        for j in range(0, p):
                            if (Request_tmp[j] == i):
                                l.append(i)
                        i -= 1

                    k =max(Request_tmp)

                    while k >initPos :
                        if k==len(requestQueue):
                            l.append(k)

                        for q in range(0, n):
                            if (Request_tmp[q] == k):
                                l.append(k)
                        k -= 1

                else:
                    n = len(requestQueue)
                    Request_tmp = requestQueue[:]
                    Request_tmp.sort(reverse=True)
                    if initPos != self.nCylinders and initPos > max(Request_tmp):
                        Request_tmp.append(self.nCylinders)

                    p = len(Request_tmp)

                    i = initPos

                    while i <=max(Request_tmp):

                        for q in range(0, n):
                            if (Request_tmp[q] == i):
                                l.append(i)
                        i += 1

                    i = min(Request_tmp)

                    while i < initPos:
                        for j in range(0, p):
                            if (Request_tmp[j] == i):
                                l.append(i)
                        i += 1
                return l

            return requestQueue


            # sequentially one direction to one end, 
            # then sequentially to the other `
            # decide on direction (up or down) based on initial request
            # compute and return the schedule accordingly

def totalSeeks(initPos, queue):
    lastPos = initPos
    totalMoves = 0
    for p in queue:
        totalMoves += abs(p - lastPos)
        lastPos = p
    return totalMoves



if __name__  == '__main__':
    def TestPolicy(scheduler, initHeadPos, requestQueue, policy, direction):
        s = scheduler.schedule(initHeadPos, requestQueue, policy, direction)
        t = totalSeeks(initHeadPos, s)
        print('policy %s %s (%d): %s' % (policy, direction, t, s))

    scheduler = DiskScheduler(200)
    requestQueue = [98, 183, 37, 122, 14, 124, 65, 67]
    initHeadPos = 53
    for policy in DiskScheduler._POLICIES:
        if policy[:2] == 'C-' or policy[-4:] in ['SCAN', 'LOOK']:
            TestPolicy(scheduler, initHeadPos, requestQueue, policy, 'up')
            TestPolicy(scheduler, initHeadPos, requestQueue, policy, 'down')
        else:
            TestPolicy(scheduler, initHeadPos, requestQueue, policy, '')

    print('more tests on SCAN and C-SCAN')
    rQs = [[98, 37, 0, 122, 14], [98, 37, 199, 122, 14], [98, 0, 37, 199, 14]]
    for q in rQs:
        print('Q=%s' % q)
        for policy in ['SCAN', 'C-SCAN']:
            for direction in ['up', 'down']:
                TestPolicy(scheduler, initHeadPos, q, policy, direction)
