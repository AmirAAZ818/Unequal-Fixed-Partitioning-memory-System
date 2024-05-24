from MultiQ_sys import Multi_Queue_Sys
from SingleQ_sys import Single_Queue_Sys

from tqdm import tqdm
import matplotlib.pyplot as plt

plt.style.use('seaborn-darkgrid')

# Params (You Can Change)
max_p_amount: int = 1000
memory_size: int = 1024
quantum_time: int = 1
sampling_step: int = 5

# For drawing the benchmarks
Response_Times = {'M_Sys': [], 'S_Sys': []}
Internal_Frags = {'M_Sys': [], 'S_Sys': []}
Utilization = {'M_Sys': [], 'S_Sys': []}
Pbatch_amount = [batch_num for batch_num in range(10, max_p_amount, sampling_step)]

for batch_num in tqdm(range(10, max_p_amount, sampling_step), desc='Processing', ncols=100):
    # Initializing the systems
    m_Sys = Multi_Queue_Sys(memory_quantum_time=quantum_time, memory_size=memory_size, p_amount=batch_num,
                            show_log=False)
    s_Sys = Single_Queue_Sys(memory_quantum_time=quantum_time, memory_size=memory_size, p_amount=batch_num,
                             show_log=False)

    # Running the systems
    m_Sys.run_sys()
    s_Sys.run_sys()

    # Saving results for drawing benchmarks
    m_sys_benchs = m_Sys.benchmark()
    s_sys_benchs = s_Sys.benchmark()

    Response_Times['M_Sys'].append(m_sys_benchs["avg rt"])
    Response_Times['S_Sys'].append(s_sys_benchs["avg rt"])

    Utilization['M_Sys'].append(m_sys_benchs["avg util"])
    Utilization['S_Sys'].append(s_sys_benchs["avg util"])

    Internal_Frags['M_Sys'].append(m_sys_benchs["avg if"])
    Internal_Frags['S_Sys'].append(s_sys_benchs["avg if"])

# Drawing the plots
fig, axs = plt.subplots(1, 3, figsize=(15, 3))

# Utilization Plot
axs[0].plot(Pbatch_amount, Utilization['M_Sys'], label="Multi Queue System", color='b')
axs[0].plot(Pbatch_amount, Utilization['S_Sys'], label="Single Queue System", color='r')
axs[0].set_title('Utilization Comparison')
axs[0].legend()

# Response Time Plot
axs[1].plot(Pbatch_amount, Response_Times['M_Sys'], label="Multi Queue System", color='b')
axs[1].plot(Pbatch_amount, Response_Times['S_Sys'], label="Single Queue System", color='r')
axs[1].set_title('Response Time Comparison')
axs[1].legend()

# Internal Fragmentation Plot
axs[2].plot(Pbatch_amount, Internal_Frags['M_Sys'], label="Multi Queue System", color='b')
axs[2].plot(Pbatch_amount, Internal_Frags['S_Sys'], label="Single Queue System", color='r')
axs[2].set_title('Internal Fragmentation Comparison')
axs[2].legend()

plt.tight_layout()
plt.show()