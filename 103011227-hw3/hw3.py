import socket


def YieldBST(T):
   if T!=None:
       yield  from YieldBST(T[1])
       yield T[0]
       yield  from YieldBST(T[-1])


def MakeServerSocket(host='', port=8888, limit=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except socket.error as msg:
        print('bind fails: ' + str(msg[0]))
        import sys
        sys.exit(-1)
    s.listen(limit)
    return s

#create socket
#call bind listen accept
s = MakeServerSocket()

T = (17, (12, (6, None, None), (14, None, None)), (35, (32, None, None), (40, None, None)))
L = YieldBST(T)

#accept
conn, addr = s.accept()


for v in YieldBST(T):
    #recieve from client but discard
    conn.recv(1024)
    #send to client
    conn.sendall((str(v)+'\n').encode('utf-8'))



conn.close()