"""Q6: linear SFA using whitening and difference covariance; ancestral/rejection sampling."""
import numpy as np
import pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from _shared import ROOT, save_result, bn_sample, graph_exact

n=3000; dt=.005;t=np.arange(n)*dt
slow=np.sin(2*np.pi*.22*t);fast=np.sin(2*np.pi*9*t)
source=np.column_stack([slow,fast])
A=np.array([[1.,.8],[.6,-1.]])
X=source@A.T
Xc=X-X.mean(axis=0)
# Whiten using symmetric eigen-decomposition of covariance.
cov=np.cov(Xc,rowvar=False);eigval,eigvec=np.linalg.eigh(cov)
whitener=eigvec@np.diag(1/np.sqrt(eigval))@eigvec.T
Xw=Xc@whitener
DX=np.diff(Xw,axis=0)
diff_cov=DX.T@DX/len(DX)
dval,dvec=np.linalg.eigh(diff_cov)
slow_extracted=Xw@dvec[:,0]
slow_extracted=(slow_extracted-slow_extracted.mean())/slow_extracted.std()
slow_ref=(slow-slow.mean())/slow.std()
if np.corrcoef(slow_ref,slow_extracted)[0,1]<0: slow_extracted=-slow_extracted
slowness=lambda x: float(np.mean(np.diff(x)**2))
correlation=float(np.corrcoef(slow_ref,slow_extracted)[0,1])
pd.DataFrame({'time_s':t,'slow_source':slow_ref,'fast_source':fast,'channel1':X[:,0],'channel2':X[:,1],'sfa_extracted':slow_extracted}).to_csv(ROOT/'Datasets'/'Q6_wearable_signals.csv',index=False)
fig,axes=plt.subplots(3,1,figsize=(10,7),sharex=True)
axes[0].plot(t,X[:,0],label='Channel 1',lw=.7);axes[0].plot(t,X[:,1],label='Channel 2',lw=.7,alpha=.7);axes[0].set_ylabel('Mixed channels');axes[0].legend()
axes[1].plot(t,slow_ref,label='Original slow signal',color='black');axes[1].set_ylabel('Slow source');axes[1].legend()
axes[2].plot(t,slow_extracted,label='SFA extracted slow feature');axes[2].set_ylabel('Extracted feature');axes[2].set_xlabel('Time (seconds)');axes[2].legend()
for ax in axes: ax.grid(alpha=.2)
fig.suptitle('Q6: Linear Slow Feature Analysis of mixed wearable signals');fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q6_sfa_extraction.png',dpi=200);plt.close(fig)
exact=graph_exact();rows=[]
for m in (100,1000,10000):
    sam=bn_sample(m,seed=2400+m); p=sam['P'];c=sam['C']
    kept=int(c.sum());rej=int(m-kept)
    rows.append({'samples':m,'estimated_P_C':float(c.mean()),'absolute_error_P_C':float(abs(c.mean()-exact['P_C'])),'accepted_C_events':kept,'rejected_events':rej,'estimated_P_P_given_C':float(p[c].mean()) if kept else None})
pd.DataFrame(rows).to_csv(ROOT/'Outputs'/'Q6_sampling_results.csv',index=False)
save_result('Q6_results',{'SFA':{'mixing_matrix':A.tolist(),'slowness_slow_source':slowness(slow_ref),'slowness_fast_source':slowness(fast),'slowness_extracted':slowness(slow_extracted),'corr_extracted_original':correlation,'smallest_difference_eigenvalue':float(dval[0])},'sampling_exact':exact,'sampling_results':rows})
