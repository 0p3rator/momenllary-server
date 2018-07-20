from transforms3d.euler import quat2euler
from transforms3d.quaternions import quat2mat
from transforms3d.euler import mat2euler
import numpy as np
import time
import os

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

def generate_all_files(root):
    for item in os.listdir(root):
        item = os.path.join(root, item)
        if os.path.isfile(item):
            yield os.path.abspath(item)
        else:
            for item in generate_all_files(item):
                yield item

def find_allfiles(root):
    for item in generate_all_files(root):
        print(item)

def odd(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

def even(n):
    for i in range(n):
        if i % 2 != 0:
            yield i

def odd_even(n):
    #for i in odd(n):
    #    yield i
    #for i in even(n):
    #    yield i
    yield from odd(n)
    yield from even(n)
            
import asyncio
async def compute(x, y):
    print("Compute {x} + {y} ..".format(x=x, y=y))
    await asyncio.sleep(2.0)
    return x + y

async def print_sum(x, y):
    result = compute(x, y)
    print("I am here")
    await result
    print("{x} + {y} = {result}".format(x=x, y=y, result=result))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.close()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        print(1)
    loop.run_until_complete(print_sum(1, 2))
    loop.close()