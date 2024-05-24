from Process import Process
import math


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
    :param self:
    :param process:
    :return:
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