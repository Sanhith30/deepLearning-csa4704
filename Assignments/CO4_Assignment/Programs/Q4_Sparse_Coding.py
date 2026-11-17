"""Q4: Mini-batch learned dictionary (36 atoms) and three L1 penalties for digits."""
import numpy as np
import pandas as pd
import time
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import MiniBatchDictionaryLearning, sparse_encode
from _shared import ROOT, save_result

digits=load_digits()
X=digits.data.astype(float)    # original pixel intensities in [0, 16]
mean=X.mean(axis=0); Xc=X-mean
start=time.perf_counter()
learner=MiniBatchDictionaryLearning(n_components=36,alpha=1.0,max_iter=65,batch_size=180,random_state=2026,transform_algorithm='lasso_cd',transform_alpha=1.0,n_jobs=1)
learner.fit(Xc)
learn_seconds=time.perf_counter()-start
D=learner.components_
np.save(ROOT/'Datasets'/'Q4_dictionary_atoms.npy',D)
np.save(ROOT/'Datasets'/'Q4_digits_mean.npy',mean)
np.save(ROOT/'Datasets'/'Q4_digits_labels.npy',digits.target)
rows=[]; pictures=[]
for lam in (.1,1.,5.):
    tic=time.perf_counter()
    coef=sparse_encode(Xc,D,algorithm='lasso_cd',alpha=lam,max_iter=1300,n_jobs=1)
    recon=coef@D+mean
    nnz=float((np.abs(coef)>1e-5).sum(axis=1).mean())
    mse=float(np.mean((X-recon)**2))
    rows.append({'lambda':lam,'avg_nonzero_coefficients':nnz,'sparsity_percent':float(100*(1-nnz/36)),'mse_per_pixel':mse,'rmse_per_pixel':float(np.sqrt(mse)),'encoding_seconds':time.perf_counter()-tic})
    pictures.append(recon[:8])
    np.savez_compressed(ROOT/'Datasets'/f'Q4_codes_lambda_{str(lam).replace(".","_")}.npz',codes=coef)
pd.DataFrame(rows).to_csv(ROOT/'Outputs'/'Q4_lambda_tradeoff.csv',index=False)
fig,axes=plt.subplots(6,6,figsize=(8.5,8.5))
for i,ax in enumerate(axes.flat):
    atom=D[i].reshape(8,8)
    ax.imshow(atom,cmap='gray',vmin=-np.max(np.abs(D)),vmax=np.max(np.abs(D)))
    ax.axis('off');ax.set_title(f'Atom {i+1}',fontsize=7)
fig.suptitle('Q4: 36 learned sparse-code dictionary atoms',fontsize=13);fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q4_dictionary_atoms.png',dpi=180);plt.close(fig)
fig,axes=plt.subplots(4,8,figsize=(12,6))
for r,items in enumerate([X[:8],*pictures]):
    for j,ax in enumerate(axes[r]):
        ax.imshow(items[j].reshape(8,8),cmap='gray',vmin=0,vmax=16)
        ax.axis('off')
        if j==0: ax.set_ylabel(['Original','lambda=0.1','lambda=1','lambda=5'][r],fontsize=9)
fig.suptitle('Q4: Original digits and sparse reconstructions',fontsize=13);fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q4_digit_reconstructions.png',dpi=200);plt.close(fig)
fig,ax=plt.subplots(figsize=(7.2,4.5))
ax.plot([r['lambda'] for r in rows],[r['avg_nonzero_coefficients'] for r in rows],'o-',label='Avg nonzero codes')
ax.set_xscale('log');ax.set(xlabel='L1 penalty lambda',ylabel='Nonzero coefficients per image',title='Q4: Sparsity versus regularisation')
ax.grid(alpha=.25);ax2=ax.twinx();ax2.plot([r['lambda'] for r in rows],[r['mse_per_pixel'] for r in rows],'s--',color='gray',label='MSE per pixel');ax2.set_ylabel('Reconstruction mean squared error')
fig.tight_layout();fig.savefig(ROOT/'Graphs'/'Q4_sparsity_tradeoff.png',dpi=200);plt.close(fig)
save_result('Q4_results',{'dataset':'sklearn digits','samples':len(X),'pixels_per_image':64,'atoms':36,'dictionary_training_seconds':learn_seconds,'rows':rows,'dictionary_shape':list(D.shape)})
