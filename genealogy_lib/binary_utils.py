import math

class Binary:

    def __init__(self, dec, binlen):
        self.dec = dec
        self.binlen = binlen
        self.binarr = convertDecimalToBinaryArray(dec, binlen)

    def getitem(self, i): return self.binarr[i]
    __getitem__ = getitem

    def length(self): return self.binlen
    __len__ = length

    def tostring(self):
        s = ""
        for b in self.binarr:
            s += convertBitToString(b)
        return s + "(" + str(self.dec) + ")"
    __str__ = tostring
    __repr__ = tostring

def convertBitToString(bit):
    return "1" if bit else "0"

def convertDecimalToBinaryArray(dec, binlen):
    binarr = [False for _ in range(binlen)]
    i_bin = binlen - 1
    while i_bin >= 0:
        i_dec = 2**i_bin
        if dec >= i_dec:
            dec -= i_dec
            binarr[binlen-1-i_bin] = True
        i_bin -= 1
    return binarr

def convertBinaryArrayToDecimal(binarr):
    dec = 0
    l = len(binarr)
    for i in range(len(binarr)): dec += binarr[l-1-i] * (2**i)
    return dec

def makeBinaryIterator(max_dec, binlen=False):
    binlen = binlen or math.ceil(math.log(max_dec,2))
    for i in range(max_dec):
        yield Binary(i, binlen)