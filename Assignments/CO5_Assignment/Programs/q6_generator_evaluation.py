"""Q6: classifier, 200 VAE and 200 GAN predictions, confidence, nearest-neighbor check."""
from common import ROOT,load_images,seed_all,save_json,plot_grid
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score,pairwise_distances
import argparse,numpy as np,joblib,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
ap=argparse.ArgumentParser();ap.add_argument('--demo',action='store_true');args=ap.parse_args()
seed_all(42);train,test,ytr,yte,source=load_images('demo' if args.demo else 'fashion',train_max=4000,test_max=1200)
clf=SGDClassifier(loss='log_loss',max_iter=180,tol=1e-4,random_state=42,alpha=.0001);clf.fit(train,ytr)
joblib.dump(clf,ROOT/'Models'/'q6_classifier.joblib');acc=float(accuracy_score(yte,clf.predict(test)))
vals={'data_source':source,'real_test_classifier_accuracy':acc,'full_RBM_weights':784*500,'conv_RBM_weights':16*5*5,'generators':{}}
fig,ax=plt.subplots(figsize=(8,4.3));width=.36
for i,(name,file) in enumerate([('VAE','q4_vae_2_samples.npy'),('GAN','q5_gan_samples.npy')]):
    gen=np.load(ROOT/'Outputs'/file)[:200];p=clf.predict_proba(gen);labels=np.argmax(p,axis=1);confidence=float(p.max(axis=1).mean());counts=np.bincount(labels,minlength=10)
    dist=pairwise_distances(gen[:10],train,metric='euclidean');nn_idx=dist.argmin(axis=1);nn_dist=dist.min(axis=1)
    vals['generators'][name]={'mean_confidence':confidence,'counts':counts.tolist(),'nearest_first_10_distances':nn_dist.tolist(),'nearest_indices':nn_idx.tolist()}
    print(name,'mean confidence',confidence,'class counts',counts.tolist(),'nearest Euclidean',np.round(nn_dist,3))
    ax.bar(np.arange(10)+i*width,counts,width,label=name)
    # 10 images and their nearest known real neighbor side by side
    fig2,axs=plt.subplots(2,10,figsize=(13,3.5))
    for j in range(10):
        axs[0,j].imshow(gen[j].reshape(28,28),cmap='gray');axs[1,j].imshow(train[nn_idx[j]].reshape(28,28),cmap='gray')
        for row in [0,1]:axs[row,j].axis('off')
    fig2.suptitle(f'Q6 | {name}: generated top vs nearest training bottom | {source}',fontsize=10);fig2.tight_layout();fig2.savefig(ROOT/'Graphs'/f'q6_nearest_{name.lower()}.png',dpi=150);plt.close(fig2)
ax.set(xticks=np.arange(10)+width/2,xticklabels=[str(i) for i in range(10)],xlabel='Predicted class',ylabel='Number of images',title='Q6 | Predicted class coverage (200 generated per model)');ax.legend();fig.tight_layout();fig.savefig(ROOT/'Graphs'/'q6_class_distribution.png',dpi=160);plt.close(fig)
print('classifier accuracy:',acc);save_json('q6_results.json',vals)
