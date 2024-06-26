import random
import itertools

random.seed(4)


class Process:
    """
    A class for creating objects that represent a process.
    """

    # A variable for implementing auto increment for the id of each process.
    ID_Counter = itertools.count()

    def __init__(self):
        """
        This Method Creates a process with random size and memory allocation time.

        For comparison, we will use a fixed seed number for the random generator.
        :return: A process object.
        """

        self.PCB = {"PID": next(Process.ID_Counter),
                    "Size": random.randint(1, 512),
                    "Request Memory Time": random.randint(1, 5),  # For now request time is static todo
                    "Service Time": 0,
                    "Waiting Time": 0,
                    "Arrival Time": random.randint(0, 10),  # For now the arrival time is static todo
                    "Status": 'Init'  # The value for Status can only be Terminated - Waiting In Memory
                    }

    def isDone(self):
        if self.PCB['Service Time'] >= self.PCB['Request Memory Time']:
            self.PCB['Status'] = 'Terminated'
            return True
        else:
            return False

    def isWaiting(self):
        if self.PCB['Status'] == 'Waiting':
            return True
        else:
            return False

    def isInMemory(self):
        if self.PCB['Status'] == 'In Memory':
            return True
        else:
            return False

    def Waiting(self):
        self.PCB['Status'] = 'Waiting'

    def in_Memory(self):
        self.PCB['Status'] = 'In Memory'

    def remaining(self):
        return self.PCB['Request Memory Time'] - self.PCB['Service Time']

    def __str__(self):
        return str(self.PCB)
