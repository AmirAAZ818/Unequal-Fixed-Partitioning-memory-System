from MultiQ_sys import Multi_Queue_Sys
from SingleQ_sys import Single_Queue_Sys

m_Sys_RR = Single_Queue_Sys(memory_size=1024, p_amount=20,
                            show_log=True, scheduler='SRT')

m_Sys_RR.run_sys()