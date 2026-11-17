"""Q2: Factor Analysis on Wine data with known perturbations to two features."""
import numpy as np
import pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, FactorAnalysis
from _shared import ROOT, save_result

wine=load_wine(); names=list(wine.feature_names)
X=StandardScaler().fit_transform(wine.data)
noisy_cols=[0,9] # alcohol and color_intensity, fixed for reproducibility
rng=np.random.default_rng(2026)
X_corrupt=X.copy()
noise_std=4.0
X_corrupt[:,noisy_cols]+=rng.normal(0,noise_std,size=(len(X),2))
np.savetxt(ROOT/'Datasets'/'wine_noisy_sensors.csv',X_corrupt,delimiter=',',header=','.join(names),comments='')
pca=PCA(n_components=2,random_state=2026).fit(X_corrupt)
fa=FactorAnalysis(n_components=2,random_state=2026,max_iter=2500,tol=1e-4).fit(X_corrupt)
# The signs of PCA/FA components are arbitrary; comparisons focus on absolute values.
rows=[{'feature':name,'added_noise_variance':16.0 if j in noisy_cols else 0.0,'FA_noise_variance':float(fa.noise_variance_[j]),'PCA_first_loading':float(pca.components_[0,j]),'FA_first_loading':float(fa.components_[0,j]),'noisy':j in noisy_cols} for j,name in enumerate(names)]
pd.DataFrame(rows).to_csv(ROOT/'Outputs'/'Q2_feature_comparison.csv',index=False)
fig,ax=plt.subplots(figsize=(9,5))
y=np.arange(len(names))
ax.barh(y,[r['FA_noise_variance'] for r in rows],label='FA estimated unique variance')
ax.set_yticks(y,names,fontsize=8);ax.invert_yaxis();ax.set(xlabel='Estimated feature-specific noise variance',title='Q2: Factor Analysis noise variance by sensor')
for i in noisy_cols: ax.get_yticklabels()[i].set_fontweight('bold')
ax.grid(axis='x',alpha=.25);fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q2_noise_variances.png',dpi=210);plt.close(fig)
fig,ax=plt.subplots(figsize=(7,4))
labels=[names[j] for j in noisy_cols];xx=np.arange(2); width=.35
ax.bar(xx-width/2,[abs(pca.components_[0,j]) for j in noisy_cols],width,label='|PCA PC1 loading|')
ax.bar(xx+width/2,[abs(fa.components_[0,j]) for j in noisy_cols],width,label='|FA factor 1 loading|')
ax.set_xticks(xx,labels);ax.set(ylabel='Absolute component loading',title='Q2: Loadings on noisy features')
ax.legend();ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q2_loading_comparison.png',dpi=200);plt.close(fig)
ranked=np.argsort(fa.noise_variance_)[::-1]
save_result('Q2_results',{'noisy_features':[names[j] for j in noisy_cols],'added_noise_std':noise_std,'added_noise_variance':noise_std**2,'fa_noise_variance':{names[j]:float(fa.noise_variance_[j]) for j in range(len(names))},'two_highest_noise_features':[names[j] for j in ranked[:2]],'both_noisy_features_highest':set(ranked[:2])==set(noisy_cols),'noisy_loadings':[rows[j] for j in noisy_cols]})
