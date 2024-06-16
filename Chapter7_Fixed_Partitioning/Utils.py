from Process import Process
import math
from queue import PriorityQueue


def generate_process_batch(n=20):
    """
    This method is for making a batch of processes.
    :param n: Number of Processes in the batch
    :return: A dict containing {PID: process object} key value pairs.
    """
    process_batch = dict()

    for i in range(n):
        process = Process()
        process_batch[process.PCB['PID']] = process

    return process_batch


def nearest_partition(process: Process):
    """
    This method finds the nearest partition size for the process.
    :param process: A process object
    :return: the nearest partition size for the process
    """
    i = math.ceil(math.log2(process.PCB['Size']))
    np = 2 ** i

    return np


class Queue:

    def __init__(self):
        self.Q = []

    def enqueue(self, item):
        self.Q.append(item)

    def dequeue(self):
        assert not self.isEmpty(), "Dequeue Operation: Queue is Empty"

        return self.Q.pop(0)

    def top(self):
        return self.Q[0]

    def isEmpty(self):
        return len(self.Q) == 0

    @property
    def size(self):
        return len(self.Q)

    def __getitem__(self, index):
        return self.Q[index]

    def __str__(self):
        res = '<<<<<Process Q is as Follow>>>>>\n' + str(self.Q)
        return res


class PQ:
    def __init__(self, pbatch: dict):
        self.Q = PriorityQueue()
        self.pbatch = pbatch

    def enqueue(self, item: int):
        process = self.pbatch[item]
        self.Q.put((process.remaining(), item))

    def dequeue(self):
        return self.Q.get()[1]

    @property
    def size(self):
        return self.Q.qsize()

    def isEmpty(self):
        return self.Q.empty()

    def __getitem__(self, index):
        return self.Q.queue[index][1]

    def __str__(self):
        res = '<<<<<Process Q is as Follow>>>>>\n' + str(self.Q.queue)
        return res


# pbatch = generate_process_batch(10)
# p1 = PQ(pbatch=pbatch)
#
# for pid, _ in pbatch.items():
#     p1.enqueue(pid)
#
# print('here i am')
# for i in range(10):
#     print(p1.Q.queue[i])
#
# print(p1.Q.queue)
# print(p1.size)
# for i in range(10):
#     print(p1.dequeue())
# print(p1.size)
