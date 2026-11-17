"""Q3: RBM(64)->RBM(32)->Logistic Regression versus raw-pixel logistic regression."""
from common import ROOT,seed_all,save_json
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np,csv,time
D=load_digits();X=D.data/16;y=D.target
rows=[]
for seed in [11,29]:
    xtr,xt,ytr,yt=train_test_split(X,y,test_size=.25,random_state=seed,stratify=y)
    for n in [100,500,'all']:
        nn=len(ytr) if n=='all' else n
        a,b=train_test_split(np.arange(len(ytr)),train_size=nn,random_state=seed,stratify=ytr) if nn<len(ytr) else (np.arange(len(ytr)),None)
        for kind in ['baseline','DBN pipeline']:
            model=(LogisticRegression(max_iter=600,random_state=seed)) if kind=='baseline' else Pipeline([
                ('rbm1',BernoulliRBM(n_components=64,n_iter=5,batch_size=32,learning_rate=.035,random_state=seed)),
                ('rbm2',BernoulliRBM(n_components=32,n_iter=5,batch_size=32,learning_rate=.035,random_state=seed+1)),
                ('clf',LogisticRegression(max_iter=500,random_state=seed))])
            t=time.perf_counter();model.fit(xtr[a],ytr[a]);acc=accuracy_score(yt,model.predict(xt));dt=time.perf_counter()-t
            row=dict(seed=seed,labels=n,model=kind,accuracy=float(acc),train_seconds=dt);rows.append(row);print(row)
with open(ROOT/'Outputs'/'q3_accuracy.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
save_json('q3_results.json',rows)
fig,ax=plt.subplots(figsize=(7,4))
for model in ['baseline','DBN pipeline']:
    means=[np.mean([r['accuracy'] for r in rows if r['model']==model and str(r['labels'])==str(n)]) for n in [100,500,'all']]
    ax.plot([1,2,3],means,'o-',label=model,linewidth=2)
ax.set_xticks([1,2,3],['100','500','all']);ax.set_xlabel('Number of labeled training images');ax.set_ylabel('Test accuracy');ax.set_ylim(0,1);ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(ROOT/'Graphs'/'q3_accuracies.png',dpi=160);plt.close(fig)
