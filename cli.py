import socket
import socks # PySocks - https://github.com/Anorov/PySocks
import time
import random
import sys
from byteutils import *

if len(sys.argv) > 1:
    random.seed(int(sys.argv[1]))

PEER_ID_LEN=30
PEED= intb(random.randint(
    int( '1'+'0'*(PEER_ID_LEN-1) ),
    int( '9'*PEER_ID_LEN )
    ))
print('my id', PEED)
peerths = []
SER_HOST = '111.228.173.96'#ip publica del server
SER_PORT = 65432

## CTRL+C
import signal
import sys
def signal_handler(sig, frame):
    print('')
    if s:
        print('Cerrando socket')
        try:
            s.shutdown(1)
            s.close()
        except: pass
    print('Chau')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# to change tor circuit (must have ORPort and password set)
# (echo authenticate '"123"'; echo signal newnym; echo quit) | nc 127.0.0.1 9051
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
s = socks.socksocket()
s.settimeout(5)
s.connect((SER_HOST, SER_PORT))
s.sendall(b'nuevo'+PEED)
#s.sendall(b'3'*PEER_ID_LEN)
r = s.recv(1024)
if r:
    def recvPeers(r):
        peerths = []
        npeers = b2int(r[:2])
        if npeers:
            if len(r[2:]) < npeers * PEER_ID_LEN:
                print('peer ids short')
            else:
                trucpeers = []
                for _ in range(npeers):
                    pid = r[2 + PEER_ID_LEN * _:2 + PEER_ID_LEN * (_ + 1)]
                    peerths.append(pid)
                    trucpeers.append(b2str(pid[:4])+'...')
                print('peer pool', len(peerths), ', '.join(trucpeers))
        else:
            print('no peers')

    recvPeers(r)
    while 1:
        time.sleep(2)
        s.send(b'getpeers')
        r=s.recv(128)
        if not r:
            print('remote closed')
            break
        recvPeers(r)
else:
    print('remote closed')


'''import socks
socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
s = socks.socksocket() # Same API as socket.socket in the standard lib
#s.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
s.connect(("icanhazip.com", 80))
s.sendall(bytes("GET / HTTP/1.1",'utf-8'))
print('recv')
print(s.recv(32))'''