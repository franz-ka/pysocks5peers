def strb(str):
    return bytes(str,'utf-8')
def intb(i):
    return strb(str(i))
def b2str(bs):
    return bs.decode('utf-8')
def b2int(bs):
    return int(b2str(bs))