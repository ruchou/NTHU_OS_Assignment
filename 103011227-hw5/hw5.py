import threading


def MakeParkingLot(N):
    global sem  # semaphore for the parking lot
    global spots # list for the spots
    global spotsSync  # for synchronizing access to spots
    spots = [None for i in range(N)]
    #  your code to initialize sem and spotsSync
    sem=threading.BoundedSemaphore(N) #integer by default


    #############################
    # for lock the list
    # Choose An RLock, and it can be acquired multiple times, by the same thread.
    # It needs to be released the same number of times in order to be "unlocked".
    spotsSync=threading.RLock()
    #We don not use Class, and that is  sugar syntax

def MakeCars(C):
     #your code here to spawn threads
     # don’t forget to return the list
     Threads=[] #a list of theads
     for i in range(C):
         Threads.append(threading.Thread(target=Park, args=(i,))) #each thread contains a function Park()
     return  Threads


def Park(car):
    global sem, spots, spotsSync
    # 2.3.1 [5 points]  ############################
    # if spot available, grab it; otherwise wait until available.
    #  Hint: don’t use if/else statement!  this is just one line.
    sem.acquire()
    # 2.3.2  [10 points] ###########################################
    # after confirming one parking spot, modify the spots (Python list or your choice
    # of list-like data structure to put this car into the spot.  The following is an example
    # of what it can do, but you may have a different way of grabbing parking spots.
    # Do you need to protect access to the following block of code? If so,
    # add code to protect it; if not, explain why not.
    loc=None
    spotsSync.acquire()
    for i in range(len(spots)):
        if spots[i] is None:
            spots[i] = car
            loc=i
            break
    spotsSync.release()

    #print(threading.currentThread().getName() + 'get lock')
    snapshot = spots[:]  # make a copy for printing
    # now let us print out the current occupancy
    print("Car %d got spot: %s" % (car, snapshot))
    # leave the car on the lot for some (real) time!
    import time
    import random
    st = random.randrange(1,10)
    time.sleep(st)
    # now ready to exit the parking lot.  What do we need to
         # 2.3.3 [5 points] #################################
         # (1) give the spot back to the pool (hint: semaphore operation)
         # 2.3.4 [10 points] ################################
         # (2) update the spots data structure by replacing the spot
         #    that current car occupies with the value None; protect code if needed
    sem.release()
    spots[loc]=None


    myCopySpots = spots[:]  # make a copy for printing
         # (3) print out the status of the spots
    print("Car %d left after %d sec, %s" % (car, st, myCopySpots))

if __name__ == '__main__':
    MakeParkingLot(5)
    cars = MakeCars(15)
    for i in range(15):
        cars[i].start()

