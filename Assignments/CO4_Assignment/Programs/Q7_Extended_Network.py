"""Q7: seven-variable examination Bayesian network, enumeration and simulation."""
import itertools
import numpy as np
import pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from _shared import ROOT,save_result

# Conditional probability tables are design hypotheses, NOT measured institutional frequencies.
# P -> U,G,W; U,G -> S; S -> C; S,W -> E
CPD_U={0:.02,1:.40}; CPD_G={0:.04,1:.30}; CPD_W={0:.03,1:.25}
CPD_S={(0,0):.05,(1,0):.80,(0,1):.35,(1,1):.95}
CPD_C={0:.05,1:.90}
CPD_E={(0,0):.01,(1,0):.75,(0,1):.55,(1,1):.95}

def sample(n,seed=177):
    rng=np.random.default_rng(seed)
    p=rng.random(n)<.1
    u=rng.random(n)<np.where(p,CPD_U[1],CPD_U[0])
    g=rng.random(n)<np.where(p,CPD_G[1],CPD_G[0])
    w=rng.random(n)<np.where(p,CPD_W[1],CPD_W[0])
    ps=np.select([u&g,u&~g,~u&g], [CPD_S[(1,1)],CPD_S[(1,0)],CPD_S[(0,1)]],default=CPD_S[(0,0)])
    s=rng.random(n)<ps
    c=rng.random(n)<np.where(s,CPD_C[1],CPD_C[0])
    pe=np.select([s&w,s&~w,~s&w],[CPD_E[(1,1)],CPD_E[(1,0)],CPD_E[(0,1)]],default=CPD_E[(0,0)])
    e=rng.random(n)<pe
    return dict(P=p,U=u,G=g,W=w,S=s,C=c,E=e)

def bern(x,prob):return prob if x else 1-prob

def enumerate_distribution():
    out=[]
    for P,U,G,W,S,C,E in itertools.product((0,1),repeat=7):
        prob=bern(P,.1)*bern(U,CPD_U[P])*bern(G,CPD_G[P])*bern(W,CPD_W[P])*bern(S,CPD_S[(U,G)])*bern(C,CPD_C[S])*bern(E,CPD_E[(S,W)])
        out.append(dict(P=P,U=U,G=G,W=W,S=S,C=C,E=E,prob=prob))
    return pd.DataFrame(out)

variables=['P','U','G','W','S','C','E']
G=nx.DiGraph([('P','U'),('P','G'),('P','W'),('U','S'),('G','S'),('S','C'),('S','E'),('W','E')])
pos={'P':(0,1.5),'U':(1.3,2.5),'G':(1.3,1.5),'W':(1.3,.2),'S':(3,2.1),'C':(4.5,2.8),'E':(4.5,.7)}
fig,ax=plt.subplots(figsize=(10,5))
nx.draw_networkx(G,pos,ax=ax,with_labels=True,node_size=1750,node_color='#e9eef6',edgecolors='#45536e',linewidths=1.5,arrowsize=20,font_size=12,font_weight='bold',min_source_margin=18,min_target_margin=18)
for name,p in pos.items(): ax.text(p[0],p[1]-.36,{'P':'Power cut','U':'UPS failure','G':'Generator failure','W':'Wi-Fi outage','S':'Server down','C':'Complaints','E':'Postponed'}[name],ha='center',va='top',fontsize=8)
ax.set_xlim(-.8,5.2);ax.set_ylim(-.6,3.5);ax.axis('off');ax.set_title('Q7: Extended seven-event Bayesian network');fig.tight_layout();fig.savefig(ROOT/'Diagrams'/'Q7_extended_network.png',dpi=220);plt.close(fig)

D=enumerate_distribution();D.to_csv(ROOT/'Outputs'/'Q7_exact_joint_128_states.csv',index=False)
exact_E=float(D.loc[D.E==1,'prob'].sum())
exact_E_given_P=float(D.loc[(D.E==1)&(D.P==1),'prob'].sum()/D.loc[D.P==1,'prob'].sum())
S=sample(10000,seed=2026)
p,e=S['P'],S['E']
emp_E=float(e.mean());emp_cond=float(e[p].mean())
pd.DataFrame({k:arr.astype(int) for k,arr in S.items()}).to_csv(ROOT/'Datasets'/'Q7_extended_10000_days.csv',index=False)
fig,ax=plt.subplots(figsize=(7,4.5))
keys=['P(E=1)','P(E=1 | P=1)']
xx=np.arange(2);width=.35
ax.bar(xx-width/2,[exact_E,exact_E_given_P],width,label='Exact enumeration')
ax.bar(xx+width/2,[emp_E,emp_cond],width,label='10,000 simulation days')
ax.set_xticks(xx,keys);ax.set(ylabel='Probability',ylim=(0,max(exact_E_given_P,emp_cond)*1.2),title='Q7: Postponement risk, overall and during power cuts')
ax.legend();ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q7_postponement_comparison.png',dpi=200);plt.close(fig)
cpds={'P':{'none':.10},'U':{str(k):v for k,v in CPD_U.items()},'G':{str(k):v for k,v in CPD_G.items()},'W':{str(k):v for k,v in CPD_W.items()},'S':{str(k):v for k,v in CPD_S.items()},'C':{str(k):v for k,v in CPD_C.items()},'E':{str(k):v for k,v in CPD_E.items()}}
save_result('Q7_results',{'full_joint_free_parameters':127,'graph_parameters':17,'probability_tables':cpds,'sum_exact_joint_probabilities':float(D.prob.sum()),'exact_P_E':exact_E,'exact_P_E_given_P':exact_E_given_P,'simulated_days':10000,'power_cuts_in_simulation':int(p.sum()),'postponed_days':int(e.sum()),'simulated_P_E':emp_E,'simulated_P_E_given_P':emp_cond,'conditional_risk_ratio':float(emp_cond/emp_E)})
