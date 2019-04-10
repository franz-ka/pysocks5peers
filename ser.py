import threading
import socket
import datetime
import time
import sys
from byteutils import *

MAIN_TH_CLOCK=10
SER_TH_CLOCK=5
PEER_TH_CLOCK=5

PEER_ID_LEN=30
peerths = {}

HOST = '192.168.0.92'
PORT = 65432
#import random
#PORT = 65400 + random.randint(10,99)

class PeerThread(threading.Thread):
    def __init__(self, sock, add, peerid):
        threading.Thread.__init__(self, name="PeerThread peerid=" + str(peerid))
        self.sock = sock
        self.add = add
        self.peerid = peerid

        self.sock.settimeout(PEER_TH_CLOCK)
        self.start()

    def die(self):
        try:
            self.sock.shutdown(1)
            self.sock.close()
        except: pass
        peerths[self.peerid] = None

    def peersData(self):
        pdata = b''
        peerc = len(peerths) - 1#except himself
        if peerc < 1:
            pdata = b'00'
        else:
            #how many
            if peerc < 10:
                pdata = b'0' + intb(peerc)
            else:
                pdata = intb(peerc)
            #ids
            for peerid in peerths:
                if peerid != self.peerid:
                    pdata += peerid
        return pdata

    def run(self):
        print('PeerThread.run', threading.current_thread().name)
        # send peer data
        self.sock.sendall(self.peersData())
        while 1:
            r=b''
            try: r = self.sock.recv(50)
            except socket.timeout: continue
            except OSError: return self.die()
            if not r:
                print('Peer closed conn', self.add)
                return self.die()
            if r.find(b'getpeers')==0:
                self.sock.sendall(self.peersData())
                pass
            else:
                print(r)
                #self.sock.sendall(b'jojojo')
                time.sleep(5)


class ServerThread(threading.Thread):
    def __init__(self, host, port):
        global peerths
        threading.Thread.__init__(self, name="ServerThread")
        self.host = host
        self.port = port
        self.peerths = peerths
        self.S = None
        self.serstt = 0

    def die(self):
        print('Cerrando peer sockets')
        for peerid in peerths:
            if peerths[peerid]:
                try:
                    peerths[peerid].sock.shutdown(1)
                    peerths[peerid].sock.close()
                except: pass

    def run(self):
        print('ServerThread.run')
        self.S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.S.setblocking(1)
        self.S.settimeout(SER_TH_CLOCK)
        self.S.bind((self.host, self.port))
        self.S.listen()
        self.serstt = datetime.datetime.now()
        print('Listening on', (self.host, self.port))
        c, a = (0,0)
        while 1:
            print('Waiting new conn...')
            try: c, a = self.S.accept()
            except socket.timeout: continue
            except OSError: return self.die()
            r = c.recv( len(b'nuevo') + PEER_ID_LEN + 1)
            print('New conn', a, r)
            ### Para la primer conexion hay tres posibilidades
            # 1. b'nuevo' para registrarse, posterior send de peer_id >> peer_id valida ok, si no error
            # 2. peer_id para continuar sesion >> si existe ok, si no error
            # 3. ninguna de las anteriores >> error
            if b'nuevo' == r[:len(b'nuevo')]:
                peerid = r[len(b'nuevo'):]
                if len(peerid) != PEER_ID_LEN:
                    print('bad peer id', peerid[:PEER_ID_LEN])
                    c.close()
                else:
                    if peerid in self.peerths: print('Peer conocido')
                    else: print('Nuevo peer')
                    self.peerths[peerid] = PeerThread(c, a, peerid)
                    pass
            elif len(r) == PEER_ID_LEN :
                if r[:PEER_ID_LEN] in self.peerths:
                    peerid = r[:PEER_ID_LEN]
                    print('Peer conocido')
                    self.peerths[peerid] = PeerThread(c, a, peerid)
                    pass
                else:
                    print('peer not registered')
                    c.close()
            else:
                print('bad protocol')
                c.close()

## CTRL+C
import signal
import sys
def signal_handler(sig, frame):
    print('')
    if sth.S:
        print('Cerrando sockets')
        sth.S.shutdown(1)
        sth.S.close()
    sth.join()
    print('Chau')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

sth = ServerThread(HOST, PORT)
sth.start()
while 1:
    time.sleep(MAIN_TH_CLOCK)
    elaps = datetime.datetime.now() - sth.serstt if sth.serstt else 0
    connps = 0
    for p in peerths:
        if peerths[p]!=None: connps += 1
    print('on=',str(elaps)[:7],'port=',PORT,', ths=', threading.active_count()-1, ', kwnpeers=',len(peerths), ', connpeers=',connps)






'''print(time.time())
print("ID of process running main program: {}".format(os.getpid()))
print("Main thread name: {}".format(threading.main_thread().name))
print(threading.main_thread())
print(type(threading.main_thread()))
print(threading.main_thread().daemon)
print(threading.main_thread().ident)
print(threading.main_thread().is_alive)'''

'''print(a, threading.current_thread().name)'''

'''# https://stackoverflow.com/questions/19846332/python-threading-inside-a-class
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper'''

'''t1 = threading.Thread(target=f, args=(1.2,), name="Thread#1")'''