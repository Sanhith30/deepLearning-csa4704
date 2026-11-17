"""Shared paths, reproducibility, and Fashion-MNIST / explicit demonstration loading."""
from pathlib import Path
import os, json, gzip, struct, time, random
import numpy as np
from sklearn.datasets import load_digits
ROOT=Path(__file__).resolve().parent.parent
for sub in ['Programs','Datasets','Outputs','Graphs','Diagrams','Models']:(ROOT/sub).mkdir(exist_ok=True)

def seed_all(seed=42):
    random.seed(seed);np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed);torch.set_num_threads(2)
    except ImportError:pass

def save_json(name,d):
    (ROOT/'Outputs'/name).write_text(json.dumps(d,indent=2,default=lambda v: float(v) if isinstance(v,np.floating) else int(v) if isinstance(v,np.integer) else str(v)))

def load_images(mode='fashion',train_max=4000,test_max=1200,seed=42):
    """Return N x 784 float32 and class IDs. mode='demo' explicitly uses digits image interpolation.
    Fashion images must be provided as official IDX GZ archives in Datasets/fashion.
    """
    if mode=='demo':
        from sklearn.model_selection import train_test_split
        from scipy.ndimage import zoom
        ds=load_digits();x=ds.images.astype(np.float32)/16.;y=ds.target
        X=np.stack([zoom(a,(3.5,3.5),order=1) for a in x]).reshape(-1,784).clip(0,1)
        a,b,c,d=train_test_split(X,y,test_size=.25,random_state=seed,stratify=y)
        return a[:train_max],b[:test_max],c[:train_max],d[:test_max], 'DIGITS PROXY DEMONSTRATION (NOT Fashion-MNIST)'
    def read_idx(kind):
        data=ROOT/'Datasets'/'fashion'
        p=data/f'{kind}-images-idx3-ubyte.gz'; q=data/f'{kind}-labels-idx1-ubyte.gz'
        if not p.exists() or not q.exists():
            raise FileNotFoundError('Official Fashion-MNIST IDX files are unavailable. Download files listed in README into Datasets/fashion and rerun without --demo. Use --demo ONLY for distinctly labelled digits proxy tests.')
        with gzip.open(p,'rb') as f:
            head=f.read(16);magic,n,h,w=struct.unpack('>IIII',head)
            if magic != 2051 or (h,w)!=(28,28):raise ValueError('Invalid image IDX header')
            X=np.frombuffer(f.read(),dtype=np.uint8).reshape(n,784).astype(np.float32)/255.
        with gzip.open(q,'rb') as f:
            magic,n=struct.unpack('>II',f.read(8)); y=np.frombuffer(f.read(),dtype=np.uint8)
            if magic != 2049:raise ValueError('Invalid label IDX header')
        if len(X)!=len(y):raise ValueError('Inconsistent IDX lengths')
        return X,y
    x,y=read_idx('train'); a,b=read_idx('t10k')
    rng=np.random.default_rng(seed);ind=rng.permutation(len(y))[:train_max];ind2=rng.permutation(len(b))[:test_max]
    return x[ind],a[ind2],y[ind],b[ind2],'Fashion-MNIST official IDX images'

def plot_grid(images,path,rows=4,cols=5,title='',labels=None):
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(rows,cols,figsize=(cols*1.5,rows*1.6))
    for i,ai in enumerate(np.asarray(ax).flat):
        ai.axis('off')
        if i<len(images):
            ai.imshow(np.asarray(images[i]).reshape(28,28),cmap='gray',vmin=0,vmax=1)
            if labels is not None:ai.set_title(str(labels[i]),fontsize=8)
    fig.suptitle(title,fontsize=12);fig.tight_layout();fig.savefig(path,dpi=160,bbox_inches='tight');plt.close(fig)

# small torch models shared by programs 04..07
import torch
from torch import nn
class VAE(nn.Module):
    def __init__(self,z_dim=2,hidden=128):
        super().__init__();self.enc=nn.Sequential(nn.Linear(784,hidden),nn.ReLU());self.mu=nn.Linear(hidden,z_dim);self.logvar=nn.Linear(hidden,z_dim);self.dec=nn.Sequential(nn.Linear(z_dim,hidden),nn.ReLU(),nn.Linear(hidden,784),nn.Sigmoid());self.z_dim=z_dim
    def forward(self,x):
        h=self.enc(x);mu=self.mu(h);lv=self.logvar(h).clamp(-12,8);z=mu+torch.exp(.5*lv)*torch.randn_like(mu);return self.dec(z),mu,lv
    def sample(self,n):return self.dec(torch.randn(n,self.z_dim))
class Gen(nn.Module):
    def __init__(self,z_dim=32,hidden=128):
        super().__init__();self.net=nn.Sequential(nn.Linear(z_dim,hidden),nn.LeakyReLU(.2),nn.Linear(hidden,256),nn.LeakyReLU(.2),nn.Linear(256,784),nn.Sigmoid());self.z_dim=z_dim
    def forward(self,z):return self.net(z)
class Disc(nn.Module):
    def __init__(self,hidden=128):
        super().__init__();self.net=nn.Sequential(nn.Linear(784,hidden),nn.LeakyReLU(.2),nn.Linear(hidden,64),nn.LeakyReLU(.2),nn.Linear(64,1))
    def forward(self,x):return self.net(x).flatten()

def train_vae(x,z_dim=2,epochs=7,hidden=128,seed=42):
    seed_all(seed);m=VAE(z_dim,hidden);opt=torch.optim.Adam(m.parameters(),lr=.001)
    ar=torch.as_tensor(x,dtype=torch.float32);losses=[]
    for ep in range(epochs):
        ids=torch.randperm(len(ar));s=0
        for ix in ids.split(128):
            xb=ar[ix];rec,mu,lv=m(xb);loss=nn.functional.binary_cross_entropy(rec,xb,reduction='sum')/len(xb)+.25*(-.5*(1+lv-mu.square()-lv.exp()).sum())/len(xb)
            opt.zero_grad();loss.backward();opt.step();s+=loss.item()*len(xb)
        losses.append(s/len(ar))
    return m,losses
