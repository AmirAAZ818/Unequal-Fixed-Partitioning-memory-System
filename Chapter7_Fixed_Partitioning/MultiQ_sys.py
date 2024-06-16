import math

from Memory import Memory
from Utils import Queue, generate_process_batch, nearest_partition


class Multi_Queue_Sys:

    def __init__(self, memory_quantum_time: int = 1, memory_size: int = 1024, p_amount: int = 20,
                 show_log: bool = False):
        self.pbatch = generate_process_batch(n=p_amount)
        self.memory = Memory(pbatch=self.pbatch, quantum_time=memory_quantum_time, size=memory_size)
        self.qs = {2 ** i: Queue() for i in range(math.ceil(math.log2(memory_size)))}
        self.pbatch_left = self.pbatch.copy()
        self.current_time = 0

        self.uti_log = []
        self.inter_frag_log = []
        self.slog = show_log

    def update_waiting_time(self):
        for part, q in self.qs.items():
            for i in range(q.size):
                pid = q[i]
                process = self.pbatch[pid]
                process.PCB['Waiting Time'] += self.memory.q_time
                # making sure their state is Waiting
                process.Waiting()

    def show_log(self, time):
        print(f"<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><> TIME : {time}")
        for i in range(len(self.pbatch)):
            print(self.pbatch[i])
        print(self.memory)
        for part, q in self.qs.items():
            print(f">>>>> Q of partition {part} <<<<<")
            print(q)

    def init_q(self):
        for pID, process in self.pbatch.items():
            part_size = nearest_partition(process)
            self.qs[part_size].enqueue(pID)

    def update_q(self):
        """
        This method is used to enter processes that have arrived at the system to the queue.

        It updates the self.q property
        """

        found_pID = []
        for pID, process in self.pbatch_left.items():
            if process.PCB["Arrival Time"] == self.current_time:
                part_size = nearest_partition(process)
                self.qs[part_size].enqueue(pID)

                found_pID.append(pID)

        if len(found_pID) != 0:
            for pID in found_pID:
                _ = self.pbatch_left.pop(pID)

    def run_sys(self):
        self.current_time = 0

        empty_Qs = False
        while (not empty_Qs) or (not self.memory.isEmpty()) or (len(self.pbatch_left) != 0):
            self.update_q()

            if self.slog:
                self.show_log(self.current_time)

            # Entering Processes of all the Qs to the memory
            for part, q in self.qs.items():

                if not q.isEmpty():
                    # Picking the Process from the Q based on the scheduler
                    e_process_pID = q.dequeue()

                    # Passing the process to the memory
                    old_PID = self.memory.enter_memory(PID=e_process_pID, partition=part)
                    if old_PID is not None:
                        q.enqueue(old_PID)

            # One Step of the Memory
            if not self.memory.isEmpty():
                self.memory.one_step()

            # Updating the PCBs
            self.update_waiting_time()

            # Logging utilization and internal fragmentation of this step
            uti = self.memory.utilization()
            inter_frag = self.memory.internal_frag()
            self.log(utilization=uti, internal_fragmentation=inter_frag)

            # erasing the memory from the terminated processes
            self.memory.clean_memory()

            # adding the time to the r for logging
            self.current_time += self.memory.q_time

            flag = True
            for part, q in self.qs.items():
                if not q.isEmpty():
                    flag = False
                    break

            if flag:
                empty_Qs = True

        if self.slog:
            print("||||||||| Final PCB of the Batch of Processes |||||||||")
            for i in range(len(self.pbatch)):
                print(self.pbatch[i])

    def log(self, utilization, internal_fragmentation):
        self.uti_log.append(utilization)
        self.inter_frag_log.append(internal_fragmentation)

    def benchmark(self):
        """
        This method Computes the Benchmarks and returns them
        :return: A dictionary with keys: avg rt, avg if, avg util
        """
        assert len(self.uti_log) == len(self.inter_frag_log), " Logs length are not the same "
        benchmarks = {'avg rt': 0, 'avg if': 0, 'avg util': 0}

        # AVG Response Time Calculation
        avg_rt = 0
        for pid, process in self.pbatch.items():
            avg_rt += process.PCB['Service Time'] + process.PCB['Waiting Time']

        benchmarks["avg rt"] = avg_rt / len(self.pbatch)

        # AVG Internal Fragmentation
        # print(self.inter_frag_log)
        benchmarks["avg if"] = sum(self.inter_frag_log) / len(self.inter_frag_log)

        # AVG Utilization
        benchmarks["avg util"] = sum(self.uti_log) / len(self.uti_log)

        return benchmarks