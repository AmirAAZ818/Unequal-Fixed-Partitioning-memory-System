from Memory import Memory
from Utils import Queue, generate_process_batch, nearest_partition


class Single_Queue_Sys:

    def __init__(self, memory_quantum_time: int = 1, memory_size: int = 1024, p_amount: int = 20, show_log=False):
        self.q = Queue()
        self.pbatch = generate_process_batch(n=p_amount)
        self.memory = Memory(pbatch=self.pbatch, quantum_time=memory_quantum_time, size=memory_size)
        self.uti_log = []
        self.inter_frag_log = []
        self.slog = show_log
        self.current_time = 0
        self.pbatch_left = self.pbatch.copy()

    def init_q(self):
        for pID, process in self.pbatch.items():
            self.q.enqueue(pID)

    def update_q(self):

        found_pID = []
        for pID, process in self.pbatch_left.items():
            if process.PCB["Arrival Time"] == self.current_time:
                self.q.enqueue(pID)
                found_pID.append(pID)

        if len(found_pID) != 0:
            for pID in found_pID:
                _ = self.pbatch_left.pop(pID)

    def update_waiting_time(self):
        for i in range(self.q.size):
            pid = self.q[i]
            process = self.pbatch[pid]
            process.PCB['Waiting Time'] += self.memory.q_time
            # making sure their state is Waiting
            process.Waiting()

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

    def show_log(self, time):
        print(f"<><><><><><><><><><><><><><><> LOG <><><><><><><><><><><><><><><> TIME : {time}")
        print("<<<<<<<<<<<<< Process Batch >>>>>>>>>>>>>")
        for i in range(len(self.pbatch)):
            print(self.pbatch[i])

        print("<<<<<<<<<<<<< Remaining Process Batch >>>>>>>>>>>>>")
        for pid, process in self.pbatch_left.items():
            print(self.pbatch[pid])

        print(self.memory)
        print(self.q)

    def run_sys(self):
        # initializing the beginning state for queue
        # self.init_q()

        self.current_time = 0

        while (not self.q.isEmpty()) or (not self.memory.isEmpty()) or (len(self.pbatch_left) != 0):
            self.update_q()

            if self.slog:
                self.show_log(self.current_time)

            if not self.q.isEmpty():
                # Retrieving the entering process of the Queue
                e_process_pID = self.q.dequeue()
                e_process = self.pbatch[e_process_pID]

                # trying to enter the process to the memory
                np = nearest_partition(process=e_process)
                old_PID = self.memory.enter_memory(PID=e_process_pID, partition=np)
                if old_PID is not None:
                    self.q.enqueue(old_PID)

            # One Step of the Memory
            if not self.memory.isEmpty():
                self.memory.one_step()

            # Updating the pcb
            self.update_waiting_time()

            # Logging utilization and internal fragmentation of this step todo
            uti = self.memory.utilization()
            inter_frag = self.memory.internal_frag()
            self.log(utilization=uti, internal_fragmentation=inter_frag)

            # erasing the memory from the terminated processes
            self.memory.clean_memory()

            # adding the time to the r for logging
            self.current_time += self.memory.q_time

        if self.slog:
            print("||||||||| Final PCB of the Batch of Processes |||||||||")
            for i in range(len(self.pbatch)):
                print(self.pbatch[i])


# s1 = Single_Queue_Sys(p_amount=10, show_log=True)
# s1.run_sys()

# print(s1.show_log(s1.current_time))
# print(s1.pbatch_left)
#
#
# print("___________ START ___________")
# for i in range(20):
#     print(f"Time : {s1.current_time} ")
#     s1.update_q()
#     print("pbatch left______")
#     print(s1.pbatch_left)
#
#     print("Queue")
#     print(s1.q)
#     s1.current_time += 1
