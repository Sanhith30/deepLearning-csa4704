"""Q3: PCA vs ICA separation of sine and square wave source signals."""
import numpy as np
import pandas as pd
from scipy.signal import square
from scipy.optimize import linear_sum_assignment
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA, FastICA
from _shared import ROOT, save_result

fs=400.; t=np.arange(4000)/fs
sources=np.column_stack((np.sin(2*np.pi*1.1*t),square(2*np.pi*7.3*t)))
sources=(sources-sources.mean(axis=0))/sources.std(axis=0)
np.savetxt(ROOT/'Datasets'/'machine_sources.csv',np.column_stack([t,sources]),delimiter=',',header='time_s,sine_source,square_source',comments='')
matrices=[np.array([[1,.5],[.7,1.]]),np.array([[1.,.95],[.35,1.2]])]
rows=[]; cases=[]
def corr_table(est):
    return np.corrcoef(sources.T,est.T)[:2,2:]
def match(corr):
    r,c=linear_sum_assignment(-np.abs(corr))
    return float(np.mean(np.abs(corr[r,c]))),list(zip(r.tolist(),c.tolist()))
for i,A in enumerate(matrices,1):
    mix=sources@A.T
    pca=PCA(n_components=2).fit_transform(mix)
    ica=FastICA(n_components=2,whiten='unit-variance',random_state=2026,max_iter=2500,tol=1e-5).fit_transform(mix)
    pcorr=corr_table(pca);icorr=corr_table(ica)
    score_p,pi=match(pcorr);score_i,ii=match(icorr)
    cases.append({'matrix':A.tolist(),'PCA_corr':pcorr.tolist(),'ICA_corr':icorr.tolist(),'PCA_matching':pi,'ICA_matching':ii,'PCA_match_score':score_p,'ICA_match_score':score_i})
    for method,corr in [('PCA',pcorr),('ICA',icorr)]:
        for s in range(2):
            for r in range(2):
                rows.append({'mixing_case':i,'method':method,'original_source':['sine','square'][s],'recovered_component':r+1,'signed_correlation':float(corr[s,r]),'absolute_correlation':float(abs(corr[s,r]))})
    fig,axes=plt.subplots(4,2,figsize=(12,8),sharex=True)
    for c in range(2):
        for j,arr in enumerate((sources,mix,pca,ica)):
            axes[j,c].plot(t[:600],arr[:600,c],lw=.8)
            axes[j,c].set_ylabel(['Source','Mixture','PCA','ICA'][j]);axes[j,c].grid(alpha=.2)
        axes[0,c].set_title(f'Channel / component {c+1}')
        axes[-1,c].set_xlabel('Time (seconds)')
    fig.suptitle(f'Q3: Two-source signal separation; mixing matrix case {i}',y=1.01)
    fig.tight_layout();fig.savefig(ROOT/'Graphs'/f'Q3_signals_mix_{i}.png',dpi=180,bbox_inches='tight');plt.close(fig)
    np.savetxt(ROOT/'Datasets'/f'machine_mix_{i}.csv',np.column_stack([t,mix]),delimiter=',',header='time_s,mic1,mic2',comments='')
pd.DataFrame(rows).to_csv(ROOT/'Outputs'/'Q3_correlations.csv',index=False)
save_result('Q3_results',{'sampling_rate_hz':fs,'n_samples':len(t),'mixing_cases':cases,'sign_and_order_ambiguity':'ICA source order and sign are not identifiable; compare absolute correlations after assignment.'})
