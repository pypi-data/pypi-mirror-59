# -*- coding: utf-8 -*-
#!/usr/bin/env python

import struct

class Serialize:
    def __init__(self):
        self.fso = None
    pass

    def writefile(self,filepath=''):
        if self.fso == None:
            self.fso = open(filepath,'wb')
        return self.fso

    def readfile(self,filepath=''):
        if self.fso == None:
            self.fso = open(filepath,'rb')
        return self.fso

    def close(self):
        if self.fso != None:
            self.fso.close()
            self.fso = None

    def out(self,val,mode=''):
        if self.fso == None:
            return

        if mode == '':
            mode = val.__class__.__name__


        if mode == 'str':
            for x in val:
                a = struct.pack('s',x)
                self.fso.write(a)
            a = struct.pack('s', '\0')
            self.fso.write(a)
        elif mode == 'uint':
            a = struct.pack('I', val)
            self.fso.write(a)
        elif mode == 'int':
            a = struct.pack('i', val)
            self.fso.write(a)
        elif mode == 'char':
            a = struct.pack('b', val)
            self.fso.write(a)
        elif mode == 'long':
            a = struct.pack('l', val)
            self.fso.write(a)
        elif mode == 'float':
            a = struct.pack('f', val)
            self.fso.write(a)

    def input(self,mode):
        if self.fso == None:
            return

        if mode == 'str':
            val = ''
            data = self.fso.read(1)
            while(data[0]!='\0'):
                val += str(data[0])
                data = self.fso.read(1)
            return val


        elif mode == 'uint':
            val = self.fso.read(4)
            a = struct.unpack('I', val)[0]
            return a
        elif mode == 'int':
            val = self.fso.read(4)
            a = struct.unpack('i', val)[0]
            return a
        elif mode == 'char':
            val = self.fso.read(1)
            a = struct.unpack('b', val)[0]
            return a
        elif mode == 'long':
            val = self.fso.read(4)
            a = struct.unpack('l', val)[0]
            return a
        elif mode == 'float':
            val = self.fso.read(4)
            a = struct.unpack('f', val)[0]
            return a
        pass



if __name__ == '__main__':
    ss = Serialize()
    ss.writefile('bin_test.bin')
    ss.out('abcdefg')
    ss.out('|','str')
    ss.out(1)
    ss.out(2)
    ss.out(3,'char')
    ss.out(4,'long')
    ss.out(5.22)
    ss.close()


    ss.readfile('bin_test.bin')
    print ss.input('str')
    print ss.input('str')
    print ss.input('uint')
    print ss.input('int')
    print ss.input('char')
    print ss.input('long')
    print ss.input('float')
    ss.close()