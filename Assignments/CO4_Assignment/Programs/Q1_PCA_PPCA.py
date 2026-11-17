"""Q1: PCA and probabilistic PCA theory; executable PCA Wine benchmark."""
import numpy as np
import pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from _shared import ROOT, save_result

wine=load_wine()
raw=wine.data
names=list(wine.feature_names)
X=StandardScaler().fit_transform(raw)
np.savetxt(ROOT/'Datasets'/'wine_standardized.csv',X,delimiter=',',header=','.join(names),comments='')
pca=PCA().fit(X)
expl=pca.explained_variance_ratio_
cum=expl.cumsum()
k90=int(np.searchsorted(cum,.9)+1)
rows=[]
for k in (2,4,6,8):
    model=PCA(n_components=k).fit(X)
    X_hat=model.inverse_transform(model.transform(X))
    mse=float(np.mean((X-X_hat)**2))
    rows.append({'components':k,'variance_retained':float(expl[:k].sum()),'mse':mse,'rmse':float(np.sqrt(mse))})
pd.DataFrame(rows).to_csv(ROOT/'Outputs'/'Q1_reconstruction.csv',index=False)
pd.DataFrame({'component':np.arange(1,14),'explained_ratio':expl,'cumulative_ratio':cum}).to_csv(ROOT/'Outputs'/'Q1_variance.csv',index=False)

fig,ax=plt.subplots(figsize=(8,4.5))
ax.bar(range(1,14),expl,alpha=.55,label='Per-component variance')
ax.plot(range(1,14),cum,'o-',label='Cumulative variance')
ax.axhline(.9,ls='--',label='90% target',color='gray')
ax.axvline(k90,ls=':',color='black',label=f'{k90} components')
ax.set(xlabel='Number of principal components',ylabel='Fraction of total variance',title='Q1: Wine PCA explained variance'); ax.set_xticks(range(1,14)); ax.legend(); ax.grid(alpha=.25)
fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q1_explained_variance.png',dpi=200);plt.close(fig)

fig,ax=plt.subplots(figsize=(7.5,5))
scores=pca.transform(X)
for cls in np.unique(wine.target):
    mask=wine.target==cls
    ax.scatter(scores[mask,0],scores[mask,1],s=27,alpha=.78,label=f'Wine class {cls}')
ax.set(xlabel='PC1 score',ylabel='PC2 score',title='Q1: Wine projected onto first two PCs')
ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q1_wine_pc_scatter.png',dpi=200);plt.close(fig)

fig,ax=plt.subplots(figsize=(7,4.3))
ax.plot([r['components'] for r in rows],[r['mse'] for r in rows],'o-',lw=2)
ax.set(xlabel='Retained PCA components',ylabel='Mean squared reconstruction error (standardised units)',title='Q1: Reconstruction error');ax.set_xticks([2,4,6,8]);ax.grid(alpha=.25)
fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q1_reconstruction_error.png',dpi=200);plt.close(fig)

save_result('Q1_results',{'dataset':'sklearn Wine','samples':len(X),'features':len(names),'component_count_for_90_percent':k90,'retained_at_k90':float(cum[k90-1]),'variance_ratio':expl.tolist(),'reconstructions':rows,'class_counts':np.bincount(wine.target).tolist()})
