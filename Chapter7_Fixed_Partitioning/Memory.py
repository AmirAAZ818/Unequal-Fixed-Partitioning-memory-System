import math


class Memory:

    def __init__(self, pbatch: dict, quantum_time: int = 1, size: int = 1024):
        """
        :param pbatch: dict containing {PID, process obj}
        """
        self.size = size
        self.q_time = quantum_time
        self.memory_partitioning = {2 ** i: None for i in
                                    range(math.ceil(math.log2(self.size)))}  # (partition_size, PID)

        self.process_batch = pbatch

    def enter_memory(self, PID: int, partition: int):
        assert partition in self.memory_partitioning.keys(), f"Partition size {partition} needed for the process does not exist in the memory! "

        old_pId = None
        if self.memory_partitioning[partition] is None:
            self.memory_partitioning[partition] = PID
        else:
            old_pId = self.memory_partitioning[partition]
            self.memory_partitioning[partition] = PID

        # Updating the status of the process
        self.process_batch[PID].in_Memory()
        return old_pId

    def one_step(self):
        for part_size, PID in self.memory_partitioning.items():
            if PID is not None:
                # obtaining the process and its pcb
                process = self.process_batch[PID]
                pcb = process.PCB

                # Using the memory
                pcb['Service Time'] += self.q_time

                # If this process ended its work with the memory, terminate it
                _isdone = process.isDone()

    def clean_memory(self):
        for part_size, PID in self.memory_partitioning.items():
            if PID is not None:
                process = self.process_batch[PID]

                if process.isDone():
                    self.memory_partitioning[part_size] = None

    def utilization(self):
        """
        This method computes the utilization of the memory with the present processes in the memory.
        :return: Memory utilization
        """
        used_memory = 0
        for part_size, PID in self.memory_partitioning.items():
            if PID is not None:
                # obtaining the process and its pcb
                process = self.process_batch[PID]
                pcb = process.PCB
                used_memory += pcb['Size']

        return round(used_memory / self.size, 2)

    def internal_frag(self):
        """
        This method computes the internal fragmentation of the memory with the present processes in the memory.
        :return: An int representing internal fragmentation.
        """
        inter_frag = 0
        for part_size, PID in self.memory_partitioning.items():
            if PID is not None:
                # obtaining the process and its pcb
                process = self.process_batch[PID]
                pcb = process.PCB

                # Computing the internal fragmentation
                inter_frag += part_size - pcb['Size']

        return inter_frag

    def isEmpty(self):
        for par, pid in self.memory_partitioning.items():
            if pid is not None:
                return False

        return True

    def __str__(self):
        res = '__________________ Memory Report __________________\n\n' \
              f'Internal Frag : {self.internal_frag()}\n' \
              f'Utilization : {self.utilization() * 100}%\n'

        for par, pid in self.memory_partitioning.items():
            res += f"{par} \t\t\t\t | {pid}\n"

        return res
