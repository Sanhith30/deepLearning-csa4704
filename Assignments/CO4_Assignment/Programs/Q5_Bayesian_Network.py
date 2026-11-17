"""Q5: four-variable Bayesian network exact and empirical evaluation."""
import numpy as np
import pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from _shared import ROOT, save_result, bn_sample, graph_exact

G=nx.DiGraph([('P','U'),('U','S'),('S','C')]); pos={v:(i,0) for i,v in enumerate('PUSC')}
fig,ax=plt.subplots(figsize=(8,2.7))
nx.draw_networkx(G,pos=pos,ax=ax,node_color='#e9eef6',edgecolors='#45536e',node_size=2000,font_size=14,font_weight='bold',arrowsize=23,arrows=True)
ax.set_title('Q5: Examination portal Bayesian network');ax.axis('off');fig.tight_layout();fig.savefig(ROOT/'Diagrams'/'Q5_network.png',dpi=220);plt.close(fig)
rows=[]
for n in (100,1000,10000):
    sample=bn_sample(n,seed=130+n)
    p,u,s,c=(sample[k] for k in 'PUSC')
    rows.append({'n':n,'n_power_cuts':int(p.sum()),'n_server_down':int(s.sum()),'P_U_given_P':float(u[p].mean()) if p.any() else None,'P_C_given_S':float(c[s].mean()) if s.any() else None,'absolute_error_U_given_P':float(abs(u[p].mean()-.4)) if p.any() else None,'absolute_error_C_given_S':float(abs(c[s].mean()-.9)) if s.any() else None})
    if n==1000: pd.DataFrame({k:sample[k].astype(int) for k in 'PUSC'}).to_csv(ROOT/'Datasets'/'Q5_1000_exam_days.csv',index=False)
pd.DataFrame(rows).to_csv(ROOT/'Outputs'/'Q5_empirical_probabilities.csv',index=False)
q_joint=.1*.4*.8*.9
save_result('Q5_results',{'model_parameters':7,'full_joint_free_parameters':15,'joint_all_events':q_joint,'reference_conditional_probabilities':{'P_U_given_P':.4,'P_C_given_S':.9},'sample_results':rows,'exact_marginals':graph_exact()})
