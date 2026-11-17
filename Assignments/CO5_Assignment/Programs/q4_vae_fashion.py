"""Q4: Fashion-MNIST VAE latent 2 vs 16. Pass --demo ONLY for digits-proxy execution."""
from common import ROOT,load_images,seed_all,save_json,plot_grid,train_vae
import argparse,torch,numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from torch.nn import functional as F
ap=argparse.ArgumentParser();ap.add_argument('--demo',action='store_true');args=ap.parse_args()
seed_all();train,test,ytr,yte,source=load_images('demo' if args.demo else 'fashion',train_max=2500,test_max=700)
print('DATA SOURCE:',source);stats={'data_source':source,'n_train':len(train),'n_test':len(test),'models':{}}
for latent in [2,16]:
    model,losses=train_vae(train,latent,epochs=9,hidden=128);model.eval()
    with torch.no_grad():
        xin=torch.tensor(test[:10]);rec,mu,lv=model(xin)
        recall=model.dec(model.mu(model.enc(torch.tensor(test)))).numpy()
        mse=float(np.mean((recall-test)**2))
        generated=model.sample(250).numpy()
    torch.save({'state_dict':model.state_dict(),'latent':latent},ROOT/'Models'/f'q4_vae_latent_{latent}.pt')
    np.save(ROOT/'Outputs'/f'q4_vae_{latent}_samples.npy',generated)
    plot_grid(np.stack([v for pair in zip(test[:10],rec.numpy()) for v in pair]),ROOT/'Graphs'/f'q4_reconstruction_latent_{latent}.png',rows=4,cols=5,title=f'Q4 | VAE z={latent}, alternating ORIGINAL and RECONSTRUCTION | {source}')
    plot_grid(generated[:20],ROOT/'Graphs'/f'q4_generated_latent_{latent}.png',title=f'Q4 | 20 generated images, z={latent} | {source}')
    stats['models'][str(latent)]={'test_mse':mse,'last_train_loss_per_image':losses[-1],'train_losses':losses,'trainable_parameters':sum(p.numel() for p in model.parameters())}
    print('latent',latent,'mse',mse,'params',stats['models'][str(latent)]['trainable_parameters'])
    if latent==2:
        with torch.no_grad():
            h=model.enc(torch.tensor(test));z=model.mu(h).numpy()
        fig,ax=plt.subplots(figsize=(6.4,4.8));s=ax.scatter(z[:,0],z[:,1],c=yte,s=8,cmap='tab10',alpha=.8);fig.colorbar(s,ax=ax,label='Class index');ax.set(xlabel='Latent component 1',ylabel='Latent component 2',title=f'Q4 | 2D encoded test images | {source}')
        fig.tight_layout();fig.savefig(ROOT/'Graphs'/'q4_latent_space.png',dpi=160);plt.close(fig)
save_json('q4_results.json',stats)
