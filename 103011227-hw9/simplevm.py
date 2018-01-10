#103011227 CS18
class SimpleVM:
    _ReplacementPolicies = ['OPT', 'LRU', 'FIFO', 'SecondChance']
    def __init__(self, numPages, numFrames, replacementPolicy):
        self.numPages = numPages
        self.numFrames = numFrames
        if not replacementPolicy in SimpleVM._ReplacementPolicies:
            raise ValueError('Unknown replacement policy %s' % replacementPolichy)

        self.replacementPolicy = replacementPolicy
        self.pageTable = [None for i in range(numPages)]
        self.valid = ['i' for i in range(numPages)]

        self.frames = [None for i in range(numFrames)] # storage
        self.dirty = [False for i in range(numFrames)]

        # we prefill swapspace content with chars '0'...
        # we assume swap space is the size of virtual memory.
        # this is ok since we are dealing with just one process.
        # in practice, it should be larger to handle multiple processes.
        self.swapSpace = [chr(ord('0')+i) for i in range(numPages)]

        # pretty much all of them use a frameTable since the policies
        # work on frame age, frame index etc that then gets mapped to page.
        self.frameTable = [None for i in range(numFrames)]
        if self.replacementPolicy in ['LRU']:
            # use a "stack" (really more like a queue) to track age.
            self.stack = []
        if self.replacementPolicy in ['FIFO', 'SecondChance']:
            self.turn = 0
            # 'FIFO' policy is just round-robin, so just keep index.
            # similarly, SecondChance is roundRobin except it skips
            # invalid ones.
        if self.replacementPolicy == 'SecondChance':
            self.reference = [False for i in range(numFrames)]

        self.pageFaultCount=0
        self.pageInCount=0
        self.pageOutCount=0


    def getFreeFrame(self, pageNum):
        '''
            find a free frame if any and return its frameNum, or None if not.
            You could just go down linearly until finding one, and grab it,
            or you could queue up free pages and dequeue from it.
            The assumption is caller will use it immediately to fulfill a
            page fault.
            The pageNum is provided because we may want to optimize it
            in case of page buffering (slide 47 of week 9).
        '''
        for i in range(self.numFrames):
            if self.frames[i] is None:
                return i
        return None

    def pickVictim(self, future=None):
        '''
            finds a page whose frame is to be taken away.
        '''

        if self.replacementPolicy == 'OPT':
            # use future knowledge to pick victim
            if future is None:
                raise ValueError('cannot pick OPT without future')

            if future==[]:
                return 0
            else:
                t=[]
                for i in range(len(self.pageTable)):
                    if self.pageTable[i] != None:
                        t.append(i)

                victim=None
                val=0
                for i in t:
                    dis=0
                    if i not in future:
                        return i

                    for j in future:
                        if i == j:
                            if dis > val:
                                victim=i
                                val=dis
                            break
                        else:
                            dis=dis+1




                return victim









            # Your code here!!
            # find the page that won't be used for the longest time in future
            # find page that won't be used for longest time in future
            # Note if future is empty list, then any page is ok!
            # in any case, return the victim page's frame number.

        if self.replacementPolicy == 'LRU':
            e=self.stack[0]
            self.stack.pop(0)

            return  e
            # Your code here!!
            # pull the victim from the bottom of this "stack"
            # the assumption is if we have free frame in the first place,
            # we would not need to evict anybody.

        if self.replacementPolicy == 'FIFO':
            r=self.frameTable[self.turn]
            self.turn=(self.turn+1)%self.numFrames
            return  r

            # Your code here!!
            # pick victim according to FIFO order

        if self.replacementPolicy == 'SecondChance':
            #turn -> frame
            #self.referenc -> frame

            while True:
                if self.reference[self.turn]==False:
                    vic=self.frameTable[self.turn]
                    self.turn=(self.turn+1)%self.numFrames
                    return vic

                else:
                    self.reference[self.turn]=False
                    self.turn=(self.turn+1)%self.numFrames
            # Your code here!!
            # like FIFO, if found referenceBit==0 then use it; if not,
            # mark the first whose referencedBit==1 as 0, continue.

        # if we have not returned by then, it’s an unknown policy
        raise ValueError('unknown poliy %s' % self.replacementPolicy)

    def pageIn(self, frameNum, pageNum):

        self.pageInCount=self.pageInCount+1


        self.frames[frameNum]=self.swapSpace[pageNum]

        # Your code here!!
        # called to bring in a page from swap space to the frame.
        # pageNum is used to find location in swap space.
        # for simplicity, we use pageNum to index into swap space.
        # Assume frameNum is free, and thus no page is currently using it.
        # Update the page-to-frame table and frame-to-page table,
        self.pageTable[pageNum]=frameNum
        self.frameTable[frameNum]=pageNum

        # set valid bit for the page, and clear dirty bit for the frame.
        self.valid[pageNum]='v'
        self.dirty[frameNum]=False

        if self.replacementPolicy == 'SecondChance':
            self.reference[frameNum]=False
        # in case of SecondChance, also clear reference bit.

    def pageOut(self, frameNum):
        ele=self.frames[frameNum]
        self.pageTable[self.frameTable[frameNum]]=None
        self.dirty[frameNum]=False
        self.swapSpace[self.frameTable[frameNum]]=ele

        self.pageOutCount=self.pageOutCount+1

        # Your code here!!
        # this flushes a frame (for a given pageNum) to swap space.
        # Note that we only mark it as not-dirty, but it does not
        # change state of valid bit because that is someone else's decision
        # whether they want to reclaim the page or just flush it.
        # Similar to pageIn, we assume swap space uses the virtual address
        # as we have only one process.


    def getFrame(self, pageNum, future=None):
       # print(pageNum,future)
        p=None
        if self.pageTable[pageNum] != None:
            # self.swapSpace[pageNum] = self.frames[self.pageTable[pageNum]]

            return self.pageTable[pageNum]

        else:
            for i in range(len(self.frames)):
                if self.frames[i]==None:
                    self.frameTable[i]=pageNum
                    self.pageIn(i,pageNum)
                    self.pageFaultCount=self.pageFaultCount+1

                    return i
                # else

            vic = self.pickVictim(future)
            frame=self.pageTable[vic]
            self.pageOut(frame)
            self.valid[vic]='i'
            self.pageIn(frame, pageNum)

            self.frameTable[frame]=pageNum
            p=vic
            self.pageFaultCount=self.pageFaultCount+1

            return  self.pageTable[pageNum]





        # this is a utility that may be helpful, but not required.
        # - see if pageHit, if so, return valid frame # for read/write.
        # - if pageFault,
        #      - see if free frame available; if so, grab it;
        #      - but if no free frame, pick victim, page out first,
        #        fall thru to page-in
        #      - page-in and return the frame number
        # - bookkeeping: look up the page number whose frame is about to be reassigned
        #   - set its pageTable entry to None, clear that page's valid bit
        # finally, return the frame number for caller to use.


    def updateAccess(self, frameNum, write=False):
        # utility to update access (common to read/write) after
        # a page has been accessed.
        r=None
        if self.replacementPolicy == 'LRU':
            for i in range(len(self.stack)):
                if self.stack[i]==self.frameTable[frameNum]:
                    r=i
                    break

            if r != None :
                self.stack.pop(r)

            self.stack.append(self.frameTable[frameNum])

           # print(self.stack)


            # Your code here!!
            # find frame in stack; if found, pop it.
            # in either case, push back on stack.
            #
        if self.replacementPolicy == 'SecondChance':
            self.reference[frameNum]=True
            #mark the reference bit


        if write:  # for future use, supporting write access.
            self.dirty[frameNum] = True

    def readPage(self, pageNum, future=None):
        framenumber=self.getFrame(pageNum,future)
        data=self.swapSpace[pageNum]
        self.updateAccess(framenumber)


        self.pageOutCount=0

        return data

        # Your code here!!
        # get the frame number -- can call the getFrame() method for this.
        # use the frame number to get the data so we can return it.
        # do some bookkeeping by calling updateAccess

    def writePage(self, pageNum, data, future=None):

        framenumber = self.getFrame(pageNum, future)
        #print(framenumber)
        self.frames[framenumber]=data

        self.updateAccess(framenumber)

        return data

        # Your code here!!
        # analogous to the readPage, except
        # the frame is written to with data.
        # do bookkeeping with write=True


if __name__ == '__main__':
    def TestRead(numPages, numFrames, refString, policy):
        # ['OPT', 'LRU', 'FIFO', 'SecondChance']
        print('-------------- policy (read): %s-------------- ' % policy)
        vm = SimpleVM(numPages, numFrames, policy)
        for i, pageNum in enumerate(refString):
            nextIndex = i+1
            if nextIndex >= len(refString):
                future = []
            else:
                future = refString[nextIndex:]
            r = vm.readPage(pageNum, future)
            print('readPage(%d)=%s, pageTable=%s, valid=%s, frames=%s' %\
                (pageNum, repr(r), vm.pageTable, ''.join(vm.valid), vm.frames))
        print('   page faults = %d, page ins = %d, page outs = %d' % (vm.pageFaultCount, vm.pageInCount, vm.pageOutCount))

    def TestWrite(numPages, numFrames, refString, wrData, policy):
        print('-------------- policy (write): %s-------------- ' % policy)
        vm = SimpleVM(numPages, numFrames, policy)
        for i, testData in enumerate(map(lambda x,y:(x,y), refString, wrData)):
            pageNum, data = testData
            nextIndex = i+1
            if nextIndex >= len(refString):
                future = []
            else:
                future = refString[nextIndex:]
            vm.writePage(pageNum, data, future)
            print('writePage(%d, %s), frames=%s, swapSpace=%s' %\
                (pageNum, repr(data), vm.frames, vm.swapSpace))
        print('   page faults = %d, page ins = %d, page outs = %d' % (vm.pageFaultCount, vm.pageInCount, vm.pageOutCount))

    # define the script, or
    numPages = 8
    numFrames = 3
    refString = [7,0,1,2,0,3,0,4,2,3,0,3,0,3,2,1,2,0,1,7,0,1]
    wrData = [chr(ord('A')+i) for i in range(len(refString))]
    for policy in SimpleVM._ReplacementPolicies:
        TestRead(numPages, numFrames, refString, policy)
        TestWrite(numPages, numFrames, refString, wrData, policy)
