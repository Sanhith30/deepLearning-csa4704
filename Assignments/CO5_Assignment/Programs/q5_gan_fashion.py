"""Q5: Fashion-MNIST dense GAN, generating 20 images; --demo uses explicit digits proxy."""
from common import ROOT,load_images,seed_all,save_json,plot_grid,Gen,Disc
import argparse,torch,numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from torch import nn
ap=argparse.ArgumentParser();ap.add_argument('--demo',action='store_true');args=ap.parse_args()
seed_all(51);train,test,ytr,yte,source=load_images('demo' if args.demo else 'fashion',train_max=2500,test_max=700)
G=Gen();D=Disc();optg=torch.optim.Adam(G.parameters(),lr=.00025,betas=(.5,.999));optd=torch.optim.Adam(D.parameters(),lr=.00025,betas=(.5,.999));bce=nn.BCEWithLogitsLoss()
train_t=torch.tensor(train);history=[]
for epoch in range(24):
    ids=torch.randperm(len(train_t));dg=dd=0.;steps=0
    for ix in ids.split(128):
        real=train_t[ix];n=len(real)
        fake=G(torch.randn(n,32)).detach()
        dloss=bce(D(real),torch.ones(n))+bce(D(fake),torch.zeros(n));optd.zero_grad();dloss.backward();optd.step()
        fake=G(torch.randn(n,32));gloss=bce(D(fake),torch.ones(n));optg.zero_grad();gloss.backward();optg.step()
        dd+=dloss.item();dg+=gloss.item();steps+=1
    history.append(dict(epoch=epoch+1,generator_loss=dg/steps,discriminator_loss=dd/steps));print('epoch',epoch+1,'G',round(dg/steps,4),'D',round(dd/steps,4))
G.eval()
with torch.no_grad():samples=G(torch.randn(250,32)).numpy()
np.save(ROOT/'Outputs'/'q5_gan_samples.npy',samples)
torch.save(G.state_dict(),ROOT/'Models'/'q5_generator.pt')
torch.save(D.state_dict(),ROOT/'Models'/'q5_discriminator.pt')
plot_grid(samples[:20],ROOT/'Graphs'/'q5_gan_20_images.png',title=f'Q5 | 20 GAN samples | {source}')
vae=np.load(ROOT/'Outputs'/'q4_vae_2_samples.npy')
fig,ax=plt.subplots(4,10,figsize=(14,6))
for i in range(20):
    for r,im in [(i//10,vae[i]),(2+i//10,samples[i])]:ax[r,i%10].imshow(im.reshape(28,28),cmap='gray',vmin=0,vmax=1);ax[r,i%10].axis('off')
fig.suptitle(f'Q5 | Top 2 rows: VAE (z=2); bottom 2 rows: GAN | {source}');fig.tight_layout();fig.savefig(ROOT/'Graphs'/'q5_vae_vs_gan.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(6.5,4));ax.plot([x['epoch'] for x in history],[x['generator_loss'] for x in history],label='Generator');ax.plot([x['epoch'] for x in history],[x['discriminator_loss'] for x in history],label='Discriminator');ax.legend();ax.set(xlabel='Epoch',ylabel='BCE loss',title='Q5 | GAN training losses');fig.tight_layout();fig.savefig(ROOT/'Graphs'/'q5_losses.png',dpi=160);plt.close(fig)
save_json('q5_results.json',{'data_source':source,'epochs':24,'history':history,'G_parameters':sum(p.numel() for p in G.parameters()),'D_parameters':sum(p.numel() for p in D.parameters())})
