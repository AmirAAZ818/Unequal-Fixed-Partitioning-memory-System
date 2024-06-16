from MultiQ_sys import Multi_Queue_Sys
from SingleQ_sys import Single_Queue_Sys

from tqdm import tqdm
import matplotlib.pyplot as plt

plt.style.use('seaborn-darkgrid')

# Params (You Can Change)
max_p_amount: int = 1000
memory_size: int = 1024
quantum_time: int = 1  # do not change for now todo
sampling_step: int = 5

# For drawing the benchmarks
Response_Times = {'M_Sys_RR': [], 'S_Sys_RR': [], 'M_Sys_SRT': [], 'S_Sys_SRT': []}
Internal_Frags = {'M_Sys_RR': [], 'S_Sys_RR': [], 'M_Sys_SRT': [], 'S_Sys_SRT': []}
Utilization = {'M_Sys_RR': [], 'S_Sys_RR': [], 'M_Sys_SRT': [], 'S_Sys_SRT': []}
Pbatch_amount = [batch_num for batch_num in range(10, max_p_amount, sampling_step)]

for batch_num in tqdm(range(10, max_p_amount, sampling_step), desc='Processing', ncols=100):
    # Initializing the systems
    m_Sys_RR = Multi_Queue_Sys(memory_quantum_time=quantum_time, memory_size=memory_size, p_amount=batch_num,
                               show_log=False, scheduler='RR')

    s_Sys_RR = Single_Queue_Sys(memory_quantum_time=quantum_time, memory_size=memory_size, p_amount=batch_num,
                                show_log=False, scheduler='RR')

    m_Sys_SRT = Multi_Queue_Sys(memory_quantum_time=quantum_time, memory_size=memory_size, p_amount=batch_num,
                                show_log=False, scheduler='SRT')

    s_Sys_SRT = Single_Queue_Sys(memory_quantum_time=quantum_time, memory_size=memory_size, p_amount=batch_num,
                                 show_log=False, scheduler='SRT')

    # Running the systems
    m_Sys_RR.run_sys()
    s_Sys_RR.run_sys()
    m_Sys_SRT.run_sys()
    s_Sys_SRT.run_sys()

    # Saving results for drawing benchmarks
    m_sys_RR_benchs = m_Sys_RR.benchmark()
    s_sys_RR_benchs = s_Sys_RR.benchmark()
    m_sys_SRT_benchs = m_Sys_SRT.benchmark()
    s_sys_SRT_benchs = s_Sys_SRT.benchmark()

    Response_Times['M_Sys_RR'].append(m_sys_RR_benchs["avg rt"])
    Response_Times['S_Sys_RR'].append(s_sys_RR_benchs["avg rt"])
    Response_Times['M_Sys_SRT'].append(m_sys_SRT_benchs["avg rt"])
    Response_Times['S_Sys_SRT'].append(s_sys_SRT_benchs["avg rt"])

    Utilization['M_Sys_RR'].append(m_sys_RR_benchs["avg util"])
    Utilization['S_Sys_RR'].append(s_sys_RR_benchs["avg util"])
    Utilization['M_Sys_SRT'].append(m_sys_SRT_benchs["avg util"])
    Utilization['S_Sys_SRT'].append(s_sys_SRT_benchs["avg util"])

    Internal_Frags['M_Sys_RR'].append(m_sys_RR_benchs["avg if"])
    Internal_Frags['S_Sys_RR'].append(s_sys_RR_benchs["avg if"])
    Internal_Frags['M_Sys_SRT'].append(m_sys_SRT_benchs["avg if"])
    Internal_Frags['S_Sys_SRT'].append(s_sys_SRT_benchs["avg if"])

# Drawing the plots
fig, axs = plt.subplots(5, 3, figsize=(20, 13))

# Utilization Plots all
axs[0, 0].plot(Pbatch_amount, Utilization['M_Sys_RR'], label="Multi Queue System (RR)", color='b')
axs[0, 0].plot(Pbatch_amount, Utilization['S_Sys_RR'], label="Single Queue System (RR)", color='r')
axs[0, 0].plot(Pbatch_amount, Utilization['S_Sys_SRT'], label="Single Queue System (SRT)", color='green')
axs[0, 0].plot(Pbatch_amount, Utilization['M_Sys_SRT'], label="Multi Queue System (SRT)", color='orange')
axs[0, 0].set_title('Utilization Comparison')

# Response Time Plots all
axs[0, 1].plot(Pbatch_amount, Response_Times['M_Sys_RR'], label="Multi Queue System (RR)", color='b')
axs[0, 1].plot(Pbatch_amount, Response_Times['S_Sys_RR'], label="Single Queue System (RR)", color='r')
axs[0, 1].plot(Pbatch_amount, Response_Times['S_Sys_SRT'], label="Single Queue System (SRT)", color='green')
axs[0, 1].plot(Pbatch_amount, Response_Times['M_Sys_SRT'], label="Multi Queue System (SRT)", color='orange')
axs[0, 1].set_title('Response Time Comparison')
axs[0, 1].legend()

# Internal Fragmentation Plots all
axs[0, 2].plot(Pbatch_amount, Internal_Frags['M_Sys_RR'], label="Multi Queue System (RR)", color='b')
axs[0, 2].plot(Pbatch_amount, Internal_Frags['S_Sys_RR'], label="Single Queue System (RR)", color='r')
axs[0, 2].plot(Pbatch_amount, Internal_Frags['S_Sys_SRT'], label="Single Queue System (SRT)", color='green')
axs[0, 2].plot(Pbatch_amount, Internal_Frags['M_Sys_SRT'], label="Multi Queue System (SRT)", color='orange')
axs[0, 2].set_title('Internal Fragmentation Comparison')

# _______________ SRT Plots _______________

# Utilization
axs[1, 0].plot(Pbatch_amount, Utilization['S_Sys_SRT'], label="Single Queue System (SRT)", color='green')
axs[1, 0].plot(Pbatch_amount, Utilization['M_Sys_SRT'], label="Multi Queue System (SRT)", color='orange')

# Response Time
axs[1, 1].plot(Pbatch_amount, Response_Times['S_Sys_SRT'], label="Single Queue System (SRT)", color='green')
axs[1, 1].plot(Pbatch_amount, Response_Times['M_Sys_SRT'], label="Multi Queue System (SRT)", color='orange')
axs[1, 1].legend()

# Internal Fragmentation
axs[1, 2].plot(Pbatch_amount, Internal_Frags['S_Sys_SRT'], label="Single Queue System (SRT)", color='green')
axs[1, 2].plot(Pbatch_amount, Internal_Frags['M_Sys_SRT'], label="Multi Queue System (SRT)", color='orange')

# _______________ RR Plots _______________

# Utilization
axs[2, 0].plot(Pbatch_amount, Utilization['M_Sys_RR'], label="Multi Queue System (RR)", color='b')
axs[2, 0].plot(Pbatch_amount, Utilization['S_Sys_RR'], label="Single Queue System (RR)", color='r')

# Response Time
axs[2, 1].plot(Pbatch_amount, Response_Times['M_Sys_RR'], label="Multi Queue System (RR)", color='b')
axs[2, 1].plot(Pbatch_amount, Response_Times['S_Sys_RR'], label="Single Queue System (RR)", color='r')
axs[2, 1].legend()

# Internal Fragmentation
axs[2, 2].plot(Pbatch_amount, Internal_Frags['M_Sys_RR'], label="Multi Queue System (RR)", color='b')
axs[2, 2].plot(Pbatch_amount, Internal_Frags['S_Sys_RR'], label="Single Queue System (RR)", color='r')

# _______________ Single Sys RR & SRT Plots _______________

# Utilization
axs[3, 0].plot(Pbatch_amount, Utilization['S_Sys_SRT'], label="Single Queue System (SRT)", color='green')
axs[3, 0].plot(Pbatch_amount, Utilization['S_Sys_RR'], label="Single Queue System (RR)", color='r')

# Response Time
axs[3, 1].plot(Pbatch_amount, Response_Times['S_Sys_SRT'], label="Single Queue System (SRT)", color='green')
axs[3, 1].plot(Pbatch_amount, Response_Times['S_Sys_RR'], label="Single Queue System (RR)", color='r')
axs[3, 1].legend()

# Internal Fragmentation
axs[3, 2].plot(Pbatch_amount, Internal_Frags['S_Sys_RR'], label="Single Queue System (RR)", color='r')
axs[3, 2].plot(Pbatch_amount, Internal_Frags['S_Sys_SRT'], label="Single Queue System (SRT)", color='green')

# _______________ Multi Sys RR & SRT Plots _______________

# Utilization
axs[4, 0].plot(Pbatch_amount, Utilization['M_Sys_RR'], label="Multi Queue System (RR)", color='b')
axs[4, 0].plot(Pbatch_amount, Utilization['M_Sys_SRT'], label="Multi Queue System (SRT)", color='orange')

# Response Time
axs[4, 1].plot(Pbatch_amount, Response_Times['M_Sys_RR'], label="Multi Queue System (RR)", color='b')
axs[4, 1].plot(Pbatch_amount, Response_Times['M_Sys_SRT'], label="Multi Queue System (SRT)", color='orange')
axs[4, 1].legend()

# Internal Fragmentation
axs[4, 2].plot(Pbatch_amount, Internal_Frags['M_Sys_SRT'], label="Multi Queue System (SRT)", color='orange')
axs[4, 2].plot(Pbatch_amount, Internal_Frags['M_Sys_RR'], label="Multi Queue System (RR)", color='b')

plt.tight_layout()
fig.savefig('Plots/Plots.png', dpi=500)
plt.show()
