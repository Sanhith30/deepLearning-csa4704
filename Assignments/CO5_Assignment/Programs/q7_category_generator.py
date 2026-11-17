"""Q7: train compact VAE on 300 category images, screen generated samples and score them.
For the required experiment provide Fashion-MNIST IDX files, choose category 8 (Bag).
--demo uses an explicitly disclosed augmented digits category; NOT a completed Fashion experiment.
"""
from common import ROOT,load_images,seed_all,save_json,plot_grid,train_vae
from sklearn.metrics import pairwise_distances
import argparse,numpy as np,torch,joblib,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
ap=argparse.ArgumentParser();ap.add_argument('--demo',action='store_true');args=ap.parse_args()
seed_all(73);train,test,yt,ytest,source=load_images('demo' if args.demo else 'fashion',train_max=7000,test_max=800,seed=73)
# Fashion class 8 = Bag; in digits proxy class 8 is numeral eight, not a bag.
target=8;category=train[yt==target]
if len(category)>=300:category=category[:300]
else:
    if not args.demo:raise ValueError('Fewer than 300 distinct target category training images')
    from scipy.ndimage import shift
    print('DEMO WARNING: augmenting digit images to 300; not distinct Fashion-MNIST Bag photographs')
    rng=np.random.default_rng(73);aug=[]
    for j in range(300):
        a=category[j%len(category)].reshape(28,28)
        if j>=len(category):a=shift(a,shift=(rng.uniform(-1,1),rng.uniform(-1,1)),order=1,mode='constant',cval=0)
        aug.append(a.reshape(-1))
    category=np.stack(aug).astype(np.float32)
# compact VAE architecture: 784 -> 64 -> mu & logvar (8) -> 64 -> 784
model,losses=train_vae(category,8,epochs=25,hidden=64,seed=73);model.eval()
params=sum(p.numel() for p in model.parameters());print('model trainable params',params)
with torch.no_grad():
    candidates=model.sample(1200).numpy()
# Near-copy threshold: 2% quantile of distances between distinct training images.
real_dist=pairwise_distances(category,metric='euclidean')
np.fill_diagonal(real_dist,np.inf)
threshold=float(np.quantile(real_dist.min(axis=1),.02))
nearest=pairwise_distances(candidates,category,metric='euclidean').min(axis=1)
flag=nearest<threshold
# exactly 1000 generated candidates are screened; count flagged among these 1000
screened=candidates[:1000];flag1000=flag[:1000];accepted=screened[~flag1000]
# Keep all screened images for reproducibility, including flags; do not claim all passed
np.save(ROOT/'Outputs'/'q7_1000_generated.npy',screened);np.save(ROOT/'Outputs'/'q7_copy_flags.npy',flag1000)
plot_grid(screened[:20],ROOT/'Graphs'/'q7_20_generated.png',title=f'Q7 | 20 generated category {target} images | {source}')
plt.figure(figsize=(6.2,3.6));plt.hist(nearest[:1000],bins=35);plt.axvline(threshold,color='red',ls='--',label=f'Copy-screen threshold={threshold:.3f}');plt.xlabel('Minimum Euclidean distance to training image');plt.ylabel('Generated image count');plt.title('Q7 | Copy-screen distance distribution');plt.legend();plt.tight_layout();plt.savefig(ROOT/'Graphs'/'q7_copy_distances.png',dpi=160);plt.close()
clf=joblib.load(ROOT/'Models'/'q6_classifier.joblib');pred=clf.predict(screened);recognized=int(np.sum(pred==target));conf=float(clf.predict_proba(screened)[:,target].mean())
res={'data_source':source,'target_class':target,'category_train_count':len(category),'parameters':params,'generated_count':1000,'flagged_near_copies':int(flag1000.sum()),'unflagged_count':int((~flag1000).sum()),'recognized_as_target':recognized,'target_recognition_rate':recognized/1000,'mean_target_confidence':conf,'copy_threshold':threshold,'min_distance_mean':float(nearest[:1000].mean()),'train_loss_start':losses[0],'train_loss_end':losses[-1]}
torch.save({'state_dict':model.state_dict(),'latent':8,'hidden':64},ROOT/'Models'/'q7_category_vae.pt')
save_json('q7_results.json',res);print(res)
