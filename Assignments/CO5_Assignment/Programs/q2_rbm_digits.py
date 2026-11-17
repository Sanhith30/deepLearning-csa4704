"""Q2: actual sklearn Digits RBM 16/64 hidden. Demonstrates training and Gibbs samples."""
from common import ROOT,seed_all,save_json
from sklearn.datasets import load_digits
from sklearn.neural_network import BernoulliRBM
import numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt,time
seed_all();ds=load_digits();X=ds.data.astype(np.float64)/16
rows=[]
for hidden in [16,64]:
    rbm=BernoulliRBM(n_components=hidden,learning_rate=.03,batch_size=32,n_iter=14,random_state=42,verbose=0)
    t=time.perf_counter();rbm.fit(X);dt=time.perf_counter()-t
    pseudo=float(rbm.score_samples(X).mean()); rows.append(dict(hidden_units=hidden,mean_pseudo_log_likelihood=pseudo,seconds=dt))
    np.save(ROOT/'Models'/f'q2_rbm_{hidden}_weights.npy',rbm.components_)
    fig,ax=plt.subplots(4, min(hidden//4,8),figsize=(min(hidden//4,8)*1.1,4.8))
    for i,a in enumerate(ax.flat):
        if i<hidden:a.imshow(rbm.components_[i].reshape(8,8),cmap='RdBu_r');a.axis('off')
        else:a.axis('off')
    fig.suptitle(f'Q2 | {hidden} RBM hidden-unit weights');fig.tight_layout();fig.savefig(ROOT/'Graphs'/f'q2_weights_{hidden}.png',dpi=160);plt.close(fig)
    originals=X[:8];recons=rbm.gibbs(originals)
    fig,axs=plt.subplots(2,8,figsize=(11,3.3))
    for j in range(8):
        axs[0,j].imshow(originals[j].reshape(8,8),cmap='gray');axs[1,j].imshow(recons[j].reshape(8,8),cmap='gray')
        for r in range(2):axs[r,j].axis('off')
    axs[0,0].set_title('Original');axs[1,0].set_title('Gibbs sample');fig.tight_layout();fig.savefig(ROOT/'Graphs'/f'q2_gibbs_{hidden}.png',dpi=160);plt.close(fig)
    print('hidden',hidden,'mean pseudo log likelihood',round(pseudo,4),'seconds',round(dt,3))
save_json('q2_results.json',rows)
