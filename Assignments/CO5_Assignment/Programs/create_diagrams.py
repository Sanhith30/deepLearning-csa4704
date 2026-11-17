"""Generate clean, labelled architecture diagrams for Assignment 5."""
from common import ROOT
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Circle
NAVY='#14263d';BLUE='#eaf2fa';GREY='#f1f3f6';EDGE='#6e879e';WHITE='#ffffff'
def setup(title, size=(10,3.2)):
    fig,ax=plt.subplots(figsize=size);ax.set_xlim(0,10);ax.set_ylim(0,4);ax.axis('off');fig.patch.set_facecolor('white');ax.set_title(title,loc='left',fontsize=15,color=NAVY,fontweight='bold',pad=12);return fig,ax
def box(ax,x,y,w,h,label,fc=BLUE,sz=10):
    p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.04,rounding_size=0.13',facecolor=fc,edgecolor=EDGE,lw=1.35);ax.add_patch(p);ax.text(x+w/2,y+h/2,label,ha='center',va='center',color=NAVY,fontsize=sz,wrap=True,fontweight='medium')
def arrow(ax,x1,y1,x2,y2,txt=None):
    a=FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=14,lw=1.5,color=EDGE,connectionstyle='arc3');ax.add_patch(a)
    if txt:ax.text((x1+x2)/2,(y1+y2)/2+.1,txt,ha='center',va='bottom',fontsize=8,color=NAVY)
def save(fig,name):fig.tight_layout();fig.savefig(ROOT/'Diagrams'/name,dpi=180,bbox_inches='tight');plt.close(fig)
fig,ax=setup('Q1 | Restricted Boltzmann Machine: visible and hidden layers', (10,3.0))
for x,lab in [(2.2,'v1 | Dosa'),(7.4,'v2 | Coffee')]:box(ax,x,0.55,1.7,.7,lab)
box(ax,4.4,2.65,1.5,.7,'h | latent')
arrow(ax,3.1,1.26,4.8,2.62,'w1 = +1');arrow(ax,8.2,1.26,5.55,2.62,'w2 = +1');ax.text(1.5,1.75,'Visible biases: b1=+0.5, b2=−0.5    •    Hidden bias: c=0',fontsize=10,color=NAVY)
save(fig,'q1_rbm_graph.png')
fig,ax=setup('Q2 | One-step contrastive divergence', (10,3.0))
box(ax,.35,1.5,1.8,1,'Real digit\nvisible v0');box(ax,2.8,1.5,1.8,1,'Sample hidden\nh0 ~ P(h|v0)');box(ax,5.25,1.5,1.9,1,'Gibbs visible\nv1 ~ P(v|h0)');box(ax,7.8,1.5,1.85,1,'Negative phase\nmodel samples')
for x1,x2 in [(2.17,2.77),(4.63,5.22),(7.18,7.77)]:arrow(ax,x1,2,x2,2)
ax.text(.5,.6,'Positive phase: encourage observed patterns',fontsize=10,color=NAVY);ax.text(5.4,.6,'Negative phase: discourage model reconstructions',fontsize=10,color=NAVY)
save(fig,'q2_cd_workflow.png')
fig,ax=setup('Q3 | Deep belief network (DBN) vs deep Boltzmann machine (DBM)', (10,3.4))
box(ax,.2,.65,1.55,.7,'Visible v');box(ax,2.0,.65,1.55,.7,'Hidden h1');box(ax,3.8,.65,1.55,.7,'Hidden h2');
arrow(ax,1.78,1,1.97,1);arrow(ax,3.58,1,3.77,1)
ax.text(.3,1.75,'DBN: top layers learn feature hierarchy; upper RBM undirected',fontsize=9,color=NAVY)
box(ax,5.35,.65,1.35,.7,'Visible v',GREY);box(ax,7,.65,1.35,.7,'Hidden h1',GREY);box(ax,8.65,.65,1.15,.7,'Hidden h2',GREY)
for a,b in [(6.73,6.97),(8.38,8.62)]:
    arrow(ax,a,1.12,b,1.12);arrow(ax,b,.86,a,.86)
ax.text(5.7,1.75,'DBM: undirected links at every layer',fontsize=9,color=NAVY)
save(fig,'q3_dbn_vs_dbm.png')
fig,ax=setup('Q4 | Variational autoencoder architecture (dense)', (10,3.0))
for x,w,s in [(.3,1.55,'Input\n784 pixels'),(2.15,1.5,'Encoder\n128 ReLU'),(4.04,1.7,'μ, logσ²\nlatent 2 / 16'),(6.18,1.5,'Decoder\n128 ReLU'),(8.13,1.55,'Reconstruction\n784 sigmoid')]:box(ax,x,1.3,w,1,s)
for a,b in [(1.89,2.11),(3.69,4),(5.77,6.14),(7.72,8.09)]:arrow(ax,a,1.8,b,1.8)
ax.text(4.05,.65,'Sample z = μ + σ ε; ε ~ Normal(0, I)',fontsize=10,color=NAVY)
save(fig,'q4_vae_architecture.png')
fig,ax=setup('Q5 | Generative adversarial network', (10,3.0))
box(ax,.3,1.3,1.4,1,'Random noise\nz (32)');box(ax,2.2,1.3,1.8,1,'Generator G\n32→128→256→784');box(ax,4.55,1.3,1.45,1,'Fake image\n28×28');box(ax,7,1.3,1.65,1,'Discriminator D\n784→128→64→1');box(ax,8.95,1.3,.85,1,'Real /\nFake',GREY,8)
for a,b in [(1.73,2.17),(4.03,4.52),(6.04,6.97),(8.68,8.92)]:arrow(ax,a,1.8,b,1.8)
box(ax,4.55,2.75,1.4,.65,'Real images',GREY,9);arrow(ax,5.95,3.03,7.1,2.34)
ax.text(2.2,.65,'G learns to fool D; D learns to distinguish real and generated images',fontsize=10,color=NAVY)
save(fig,'q5_gan_architecture.png')
fig,ax=setup('Q7 | Category-specific generation and quality gates', (10,3.2))
for x,w,s in [(.2,1.8,'300 target-class\ntraining images'),(2.35,1.6,'Compact VAE\nlatent = 8'),(4.3,1.4,'Generate\n1,000 images'),(6.07,1.58,'Nearest-image\ncopy screening'),(8,1.8,'Classifier check\n+ review')]:box(ax,x,1.3,w,1,s)
for a,b in [(2.03,2.32),(3.98,4.27),(5.73,6.04),(7.68,7.97)]:arrow(ax,a,1.8,b,1.8)
ax.text(.25,.5,'Flagged images are reported; acceptance depends on both non-copying and class fidelity.',fontsize=10,color=NAVY)
save(fig,'q7_generation_workflow.png')
