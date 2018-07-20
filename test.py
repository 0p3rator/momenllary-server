from transforms3d.euler import quat2euler
from transforms3d.quaternions import quat2mat
from transforms3d.euler import mat2euler
import numpy as np
import time

def consumer():
    r = ''
    while True:
        # print('I am waiting')
        n = yield r
        print('n::::::::', n)
        print('r::::::::', r)
        if not n:
            print('I will return')
            return
        print('[Consumer] consumer {number}'.format(number=n))
        r = '200 OK'

def producer(c):
    c.send(None)
    n = 0
    time.sleep(1)
    while n < 5:
        r = c.send(n)
        n = n + 1
        print('[Producer] producing {number}'.format(number=n))
        r = c.send(n)
        print('[Producer] Consumer return: %s' % r)
    # c.close()

class yrange(object):
    def __init__(self, n):
        self.i = 0
        self.n = n
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()
    

if __name__ == '__main__':
    y = yrange(3)
    print(y.next())
    print(y.next())
    print(y.next())
    print(y.next())