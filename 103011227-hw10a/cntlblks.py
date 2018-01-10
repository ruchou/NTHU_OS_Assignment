# control blocks
# including base class ControlBlock,
# subclass FCB (File Control Block),
# subclass DEntry (Directory Entry, aka directory control block)
import time

class ControlBlock:
    '''
        this is the base class for things in common between FCB and DEntry.
    '''
    def __init__(self, createTime=None, accessTime=None, modTime=None):
        if createTime is None:
            createTime = time.asctime()
        if accessTime is None:
            accessTime = createTime
        if modTime is None:
            modTime = createTime
        self.createTime = createTime
        self.accessTime = accessTime
        self.modTime = modTime

    def updateAccessTime(self):
        self.accessTime = time.asctime()

    def updateModTime(self):
        self.modTime = time.asctime()

class FCB(ControlBlock):
    '''
        FCB is the file control block.
        Note that there is the FCB on disk and in-memory FCB.
        The difference is in-memory one would have a count, but not on-disk.
        The name technically is not part of the FCB but kept by directory.
        it also does not know which directory it belongs to.
        
        The constructor should be called only by the file system,
        but not separately.  We add extra fields to simplify programming
        and tracing, but they are actually not part of actual FCBs.
    '''
    def __init__(self):
        ControlBlock.__init__(self)
        # self.name = name  # name is not stored in FCB
        # in the case of linked structure, FCB points to first block;
        # in unix FS, FCB points to an inode.
        self.index = [ ] # logical block to physical block mapping
        self.linkCount = 0 # num of directories with hard link to it
        # the count is for in-memory structure only
        self.openCount = 0
        ##### these are just useful for debugging.
        ### we assume the FS adds link to itself and number (ID) of this FCU
        ### as fields

    def nBlocks(self):
        return len(self.index)

    def incrOpenCount(self):
        self.openCount += 1

    def decrOpenCount(self):
        self.openCount -= 1

    def incrLinkCount(self):
        self.linkCount += 1

    def decrLinkCount(self):
        self.linkCount -= 1

    def nameInDir(self, d):
        '''find the name of this file in the given directory'''
        if self in d.content:
            return d.names[d.content.index(self)]
        return None


class DEntry(ControlBlock):
    def __init__(self, parent=None):
        '''
            a directory entry captures information for a directory.
            - list of both files (FCB) and directories (DEntry)
        '''
        ControlBlock.__init__(self)
        self.parent = parent
        self.content = []  # of FCBs and DEntry's
        self.names = [ ]


    def name(self):
        # find name in parent
        if self.parent is None:
            return ''
        return self.parent.names[self.parent.content.index(self)]

    def lookup(self, name):
        '''
            look up in the current directory for the name.
            It can be either a directory (DEntry) or a file (FCB).
            for simplicity, do linear search.
        '''
        # find the FCU or DEntry using name, or None if not found
        for i, n in enumerate(self.names):
            if n == name:
                return self.content[i]
        return None

    def addFile(self, fcb, name):
        '''
            add a file of given name. The file has already been created,
            so we just add to the directory.
        '''
        # @@@ Write this code
        if self.lookup(name) :
            raise  NameError('File already exist')
        else:
            self.content.append(fcb)
            self.names.append(name)
            fcb.incrLinkCount()
            fcb.updateModTime()


        # add a file to the directory under the given name.
        # * if the name is already in the directory, raise an exception.
        # * add the fcb to the content list,
        # * add the name to the names list.
        # * increment the linkCount of this fcb.
        # * update the last modified date of self.


    def rmFile(self, fcb):
        # @@@ Write this code
        fcb.decrLinkCount()

        tmp=None
        for i in  range(len(self.content)):
            if fcb== self.content[i]:
                tmp=i

        if tmp:
            del self.content[tmp]
            del self.names[tmp]




        # remove a file from the DEntry. this does not reclaim space.
        # * decrement the linkCount of the FCB corresponding to name.
        # * remove the name from the list and the FCB from the content.
        #   (hint: you can use the del operator in Python to delete 
        #    an element of a list)
        # * updates the last modified date of this directory

    def addDir(self, dEntry, name):
        # @@@ Write this code
        if self.lookup(name):
            raise  NameError('Directory already exist')
        else:
            self.content.append(dEntry)
            self.names.append(name)
            dEntry.parent=self
            dEntry.updateModTime()
            self.updateModTime()
        # it is similar to addFile except it is a directory, not a file.
        # the difference is a directory has a parent.
        # * if the name is already in the directory, raise an exception.
        # * add the dEntry to the directory content.
        # * add the name to the names list.
        # * set the parent of dEntry to this directory (self).
        # * update this directory last modification date.
        # it also needs to update the last modified date of self.


    def rmDir(self, d):
        # @@@ Write this code


        tmp = None
        for i in range(len(self.content)):
            if d == self.content[i]:
                tmp = i

        del self.content[tmp]
        del self.names[tmp]

        d.parent=None

        self.updateModTime()

        # remove a directory d from self. it does not reclaim space.
        # * find the position of d in this directory content,
        # * delete both d from content and name from names list.
        # * updates the last modified date of self.
        # * set the removed dEntry's parent to None.




def MakeDirFromTree(tree, root=None):
    '''
        utility function to make directory from tree
    '''
    if tree == ():
        return None
    if isinstance(tree, str):
        fcb = FCB()
        root.addFile(fcb, name=tree)
    elif tree[0][-1] == '/':
        if root is None:
            c = DEntry()
            root = c
        else:
            # c = root.makeDir(tree[0][:-1])
            name = tree[0][:-1]
            c = DEntry(root)
            root.addDir(c, name)

        if len(tree) > 1:
            for t in tree[1:]:
                MakeDirFromTree(t, c)
    return root

def MakeTreeFromDir(d):
    if d is None:
        return ()
    t = [d.name()+'/'] 
    for c in d.content:
        if isinstance(c, DEntry): 
            t.append(MakeTreeFromDir(c))
        elif isinstance(c, FCB):
            # just append the name
            t.append(c.nameInDir(d))
    return tuple(t)

if __name__ == '__main__':
    # a name that ends in a slash and is the initial item of a tuple => directory.
    # a name that is later in the tuple and does not end in a slash is a file.
    # when creating directory, we remove the slash.
    directoryTree = ( '/',  ('home/', ('u1/', 'hello.c'),
                                    ('u2/', 'world.h'), 'homefiles'),
                            ('bin/', 'ls'),
                            ('etc/', ))

    print('input directory tree=%s' % repr(directoryTree))
    root = MakeDirFromTree(directoryTree)
    print('tuple reconstructed from directory=%s' % repr(MakeTreeFromDir(root)))
    print('creation time for /home/u1/hello.c is %s' % \
            root.lookup('home').lookup('u1').lookup('hello.c').createTime)

