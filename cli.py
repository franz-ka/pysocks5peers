import socket
# PySocks - https://github.com/Anorov/PySocks
import socks
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
peerths = []
SER_HOST = '121.228.179.96'#ip publica del server
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
s.connect((SER_HOST, SER_PORT))
s.sendall(b'nuevo'+PEED)
#s.sendall(b'3'*PEER_ID_LEN)
s.settimeout(5)
r = s.recv(1024)
print(r)
if r:
    npeers = b2int(r[:2])
    if npeers:
        if len(r[2:]) < npeers*PEER_ID_LEN:
            print('peer ids short')
        else:
            for _ in range(npeers):
                peerths.append(r[2+PEER_ID_LEN*_:2+PEER_ID_LEN*(_+1)])
            print('peers shared', len(peerths))
    else:
        print('no peers')

    while 1:
        s.send(b'jijij')
        s.send(intb(random.randint(111,999)))
        r=s.recv(128)
        print(r)
        if not r:
            break
        time.sleep(2)
        s.send(b'getpeers')
        time.sleep(2)
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