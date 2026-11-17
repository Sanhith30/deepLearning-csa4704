"""Compile a complete editable assignment report from executed experiment artifacts."""
from common import ROOT
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path
import json,math,statistics,os,textwrap

D=Document();sec=D.sections[0];sec.page_height=Inches(11.69);sec.page_width=Inches(8.27);sec.top_margin=Inches(.78);sec.bottom_margin=Inches(.76);sec.left_margin=Inches(.86);sec.right_margin=Inches(.80);sec.header_distance=Inches(.38);sec.footer_distance=Inches(.38)
styles=D.styles
normal=styles['Normal'];normal.font.name='Times New Roman';normal.font.size=Pt(11.5);normal.font.color.rgb=RGBColor(25,25,25);normal.paragraph_format.space_after=Pt(6);normal.paragraph_format.line_spacing=1.13
for sty,size,bold in [('Title',20,True),('Heading 1',15,True),('Heading 2',12.5,True),('Heading 3',11.5,True)]:
 s=styles[sty];s.font.name='Times New Roman';s.font.size=Pt(size);s.font.bold=bold;s.font.color.rgb=RGBColor(0,0,0);s.paragraph_format.space_before=Pt(10);s.paragraph_format.space_after=Pt(5);s.paragraph_format.keep_with_next=True
if 'CodeListing' not in styles:
 s=styles.add_style('CodeListing',WD_STYLE_TYPE.PARAGRAPH);s.font.name='Consolas';s.font.size=Pt(7.0);s.paragraph_format.space_after=Pt(0);s.paragraph_format.line_spacing=1.0
if 'CaptionA' not in styles:
 s=styles.add_style('CaptionA',WD_STYLE_TYPE.PARAGRAPH);s.font.name='Times New Roman';s.font.size=Pt(9.4);s.font.italic=True;s.paragraph_format.space_before=Pt(2);s.paragraph_format.space_after=Pt(6)
# footer, header, border
header=sec.header.paragraphs[0];header.text='DEEP LEARNING  •  ASSIGNMENT 5 (CO5)  |  PAIR-WORK TECHNICAL REPORT';header.alignment=WD_ALIGN_PARAGRAPH.RIGHT
for run in header.runs:run.font.size=Pt(8);run.font.name='Times New Roman';run.font.color.rgb=RGBColor(75,75,75)
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
footer.add_run('Deep Learning — CO5  |  Page ').font.size=Pt(9)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
sectPr=sec._sectPr;pgb=OxmlElement('w:pgBorders');pgb.set(qn('w:offsetFrom'),'page')
for side in ('top','left','bottom','right'):
 e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'7');e.set(qn('w:space'),'15');e.set(qn('w:color'),'888888');pgb.append(e)
sectPr.append(pgb)

def p(t='',boldlead=None):
 a=D.add_paragraph();a.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
 if boldlead and t.startswith(boldlead):a.add_run(boldlead).bold=True;a.add_run(t[len(boldlead):])
 else:a.add_run(t)
 return a

def h(t,l=1):D.add_heading(t,l)
def b(t):
 a=D.add_paragraph(style='List Bullet');a.alignment=WD_ALIGN_PARAGRAPH.LEFT;a.add_run(t);return a

def eq(t):
 a=D.add_paragraph();a.alignment=WD_ALIGN_PARAGRAPH.CENTER;a.paragraph_format.space_before=Pt(5);a.paragraph_format.space_after=Pt(5)
 r=a.add_run(t);r.font.name='Cambria Math';r.font.size=Pt(11)

def table(headers,rows,width=None):
 t=D.add_table(rows=1,cols=len(headers));t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=True
 for i,key in enumerate(headers):
  c=t.rows[0].cells[i];c.text=str(key);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
  for rr in c.paragraphs[0].runs:rr.bold=True;rr.font.size=Pt(9)
  sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'ECEFF2');c._tc.get_or_add_tcPr().append(sh)
 for row in rows:
  cells=t.add_row().cells
  for i,val in enumerate(row):
   cells[i].text=str(val);cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   for cpar in cells[i].paragraphs:
    cpar.paragraph_format.space_after=Pt(2)
    for run in cpar.runs:run.font.size=Pt(8.7)
 # no split
 for row in t.rows:
  trpr=row._tr.get_or_add_trPr();tag=OxmlElement('w:cantSplit');trpr.append(tag)
 D.add_paragraph().paragraph_format.space_after=Pt(0)
 return t

def fig(filename,caption,folder='Graphs',width=6.0):
 path=ROOT/folder/filename
 if not path.exists():return
 a=D.add_paragraph();a.alignment=WD_ALIGN_PARAGRAPH.CENTER;a.paragraph_format.space_after=Pt(0);a.paragraph_format.keep_with_next=True
 a.add_run().add_picture(str(path),width=Inches(width))
 c=D.add_paragraph(style='CaptionA');c.alignment=WD_ALIGN_PARAGRAPH.CENTER;c.add_run(caption)

def code(t):
 # list referenced programs with a readable excerpt
 a=D.add_paragraph();a.paragraph_format.space_after=Pt(1)
 r=a.add_run(t);r.font.name='Consolas';r.font.size=Pt(9)

def notes(*arr):
 for x in arr:b(x)

def newpage():D.add_page_break()
q1=json.loads((ROOT/'Outputs'/'q1_results.json').read_text());q2=json.loads((ROOT/'Outputs'/'q2_results.json').read_text());q3=json.loads((ROOT/'Outputs'/'q3_results.json').read_text());q4=json.loads((ROOT/'Outputs'/'q4_results.json').read_text());q5=json.loads((ROOT/'Outputs'/'q5_results.json').read_text());q6=json.loads((ROOT/'Outputs'/'q6_results.json').read_text());q7=json.loads((ROOT/'Outputs'/'q7_results.json').read_text())

# COVER
D.add_paragraph('DEEP LEARNING').alignment=WD_ALIGN_PARAGRAPH.CENTER
D.add_heading('ASSIGNMENT 5 — CO5',0).alignment=WD_ALIGN_PARAGRAPH.CENTER
D.add_heading('Energy-Based Models, Deep Belief Networks, VAEs and GANs',1).alignment=WD_ALIGN_PARAGRAPH.CENTER
D.add_paragraph('Pair-Work Submission • 2 Students per Group • 50 Marks • Duration: 1 Week').alignment=WD_ALIGN_PARAGRAPH.CENTER
D.add_paragraph('')
table(['Submission Information','Details'],[['Student A name / register no.','____________________________'],['Student B name / register no.','____________________________'],['Department / Institution','____________________________'],['Subject','Deep Learning'],['Assignment','Assignment 5 — CO5'],['Submission date','____________________________']])
D.add_paragraph('Reproducibility note').style='Heading 2'
p('Q1–Q3 were executed with the inputs and scikit-learn Digits dataset specified in the assignment. The required Fashion-MNIST images for Q4–Q7 were not accessible in the execution environment. The provided Q4–Q7 code supports official Fashion-MNIST input, but the enclosed measured outputs for those questions come from a clearly labelled upscaled Digits demonstration. They must not be represented as Fashion-MNIST results or proof of clothing-generation quality.')
p('All numerical experiment values below are produced by the supplied scripts. Collaborative proposals are illustrative technical drafts, not claims about which student personally developed them. The pair must verify individual authorship before submission.')
newpage()
h('Table of Contents',1)
for x in ['Introduction, objectives and dataset provenance','Q1 — Understanding an Energy-Based Model (6 marks)','Q2 — Training a Restricted Boltzmann Machine (7 marks)','Q3 — Deep Belief Networks with Few Labels (7 marks)','Q4 — Generating Images with a Variational Autoencoder (7 marks)','Q5 — Comparing a GAN with the VAE (6 marks)','Q6 — Generative Model Mini-Investigations (7 marks)','Q7 — New Product Category Design Challenge (10 marks)','Overall conclusions, limitations and references','Contribution record and individual verification','Appendix — Complete executable source listings']:
 b(x)
h('Introduction and objectives',1)
p('Energy-based models assign low energy to desirable or frequently occurring states, whereas latent-variable and adversarial models learn compressed representations or generate new examples. This assignment compares Restricted Boltzmann Machines (RBMs), deep belief networks (DBNs), variational autoencoders (VAEs), and generative adversarial networks (GANs), including the model-selection, evaluation and privacy implications of limited labelled data.')
notes('Compute the exact state probabilities for a small RBM and verify them programmatically.','Train RBMs with different numbers of hidden units and examine their learned filters.','Test DBN-style stacked RBM representations with scarce labels.','Implement VAE and GAN generation pipelines with quantitative and visual diagnostics.','Evaluate generator diversity, classifier confidence, and nearest-neighbour similarity.','Design and evaluate a small-data category-specific model, with explicit non-copying criteria.')
h('Dataset and experimental protocol',2)
table(['Questions','Required input','Executed evidence and qualification'],[['Q1','Given two-item order parameters','Exact eight-state enumeration'],['Q2–Q3','scikit-learn Digits; 1,797 images; 8×8','Executed on required dataset'],['Q4–Q7','Fashion-MNIST; 28×28 apparel images','Fashion-compatible programs supplied. Executed demonstration uses Digits resized to 28×28; NOT an apparel benchmark']])
p('Scripts use controlled seeds and save CSV/JSON, figures, and trained model files. Methods may yield different values on other hardware or library versions. The DBN experiment fits a specified Pipeline from the labelled subset; a separate unlabeled-pretraining protocol would be needed to establish the benefit of additional unlabeled images.')

# Q1
h('Q1 — Understanding an Energy-Based Model (6 marks)',1)
p('Problem: a campus canteen uses a Restricted Boltzmann Machine with visible variables v₁ (dosa) and v₂ (coffee) and hidden variable h. The parameters are b₁=0.5, b₂=−0.5, c=0, w₁=1, w₂=1. Student A calculates energies and probabilities; Student B verifies and changes w₂. Both students explain the hidden unit.')
h('Shared work — model and all states',2)
eq('E(v,h) = −b₁v₁ − b₂v₂ − ch − w₁v₁h − w₂v₂h')
eq('P(v,h) = exp(−E(v,h)) / Z,      Z = Σᵥ,ₕ exp(−E(v,h))')
p('Lower energy produces a larger unnormalised score exp(−E); Z normalises these scores to sum to one across eight binary combinations. The graph is bipartite: visible units connect to the hidden unit, but not to one another.')
fig('q1_rbm_graph.png','Figure 1. Fully labelled RBM: two visible units and one hidden unit.','Diagrams',5.8)
h('Student A — hand computation and normalisation',2)
p('Substitute the given values to obtain E=−0.5v₁+0.5v₂−v₁h−v₂h. For example, E(1,1,1)=−0.5+0.5−1−1=−2 and exp(2)=7.389056. The complete enumeration is:')
rows=q1['1']['states'];table(['v₁','v₂','h','Energy E','exp(−E)','P(v,h)'],[[r['v1'],r['v2'],r['h'],f"{r['energy']:.2f}",f"{r['unnormalized']:.6f}",f"{r['probability']:.6f}"] for r in rows])
eq('Z = 18.77471837 ;     Σ P(v,h) = 1')
p('The most probable joint state is v₁=1, v₂=1, h=1, with probability 0.393564. It represents a customer ordering both dosa and coffee with the shared preference feature active. This is a joint-state comparison rather than a comparison of visible marginals alone.')
h('Student B — program verification and modified weight',2)
p('Script: Programs/q1_energy_model.py. Executed output: Z=18.77471837 with w₂=1. After setting w₂=−1, Z=10.96007116; the most probable state becomes (1,0,1), with probability 0.408911. A negative coffee–hidden weight makes simultaneous coffee and activation of h less favourable.')
h('Part B — hidden-unit probability (Student A calculation; Student B explanation)',2)
eq('P(h=1 | v) = sigmoid(c + w₁v₁ + w₂v₂)')
table(['v₁ (dosa)','v₂ (coffee)','Net input','P(h=1 | v)'],[[v['v1'],v['v2'],v['v1']+v['v2'],f"{v['hidden_probability']:.6f}"] for v in q1['conditionals']])
p('The hidden unit can be interpreted as a shared inclination toward purchasing these items; its activation rises when either or both is ordered. In a large RBM with 784 visible and 500 hidden binary units there are 2^(784+500)=2^1284 possible joint states. Direct enumeration of the partition function would be infeasible.')
p('Cross-verification: either student should be able to explain why the denominator Z is global and how changes to a single weight alter the entire distribution.')

# Q2
h('Q2 — Training a Restricted Boltzmann Machine (7 marks)',1)
p('Problem: use scikit-learn Digits images rescaled to [0,1], compare 16 and 64 hidden units with the same learning rate and iterations, inspect pseudo-likelihood, hidden weights, and Gibbs samples.')
h('Shared work — training methodology',2)
p('Each image is an 8×8 grayscale vector of 64 pixel intensities. BernoulliRBM was fitted with learning rate 0.03, batch size 32, 14 iterations, and random seed 42. The score_samples method returns pseudo-log-likelihood estimates rather than a normalized test log-likelihood.')
fig('q2_cd_workflow.png','Figure 2. Contrastive-divergence approximation using data and one-step reconstructions.','Diagrams',6.0)
h('Student A — measured comparison',2)
table(['Hidden units','Mean pseudo-log-likelihood','Training time (s)'],[[r['hidden_units'],f"{r['mean_pseudo_log_likelihood']:.4f}",f"{r['seconds']:.3f}"] for r in q2])
p('The 64-unit model achieved a less negative score (−27.4454 versus −28.1289), matching the stated expectation that additional capacity may help on this training setup. Because this is a stochastic pseudo-likelihood score on training images, it does not by itself prove generalisation.')
fig('q2_weights_16.png','Figure 3. RBM weight patterns learned by the 16 hidden units.',width=4.7)
fig('q2_weights_64.png','Figure 4. A selection of learned 8×8 weights for the 64-unit RBM.',width=5.3)
fig('q2_gibbs_64.png','Figure 5. Original Digits images (top) and one Gibbs step samples (bottom).',width=6.0)
h('Student B — contrastive divergence and interpretation',2)
p('The positive phase reinforces hidden activations associated with observed images; the negative phase reduces the probability of reconstructions generated under the model. A Gibbs step samples h conditional on an input v and then a new v conditional on h. Exact likelihood gradients require expectations under the entire model distribution, so contrastive divergence approximates the negative-phase expectation using short Gibbs chains. Filters encode recurring strokes and bright/dark digit substructures rather than complete digits. A wider RBM can specialise more filters but may overfit or add cost.')
p('Program and results: Programs/q2_rbm_digits.py; Outputs/q2_results.json; Graphs/q2_weights_16.png, q2_weights_64.png, q2_gibbs_16.png, q2_gibbs_64.png.')

# Q3
h('Q3 — Deep Belief Networks with Few Labels (7 marks)',1)
p('Problem: compare a two-RBM Pipeline (64→32) followed by logistic regression with raw-pixel logistic regression, for 100, 500 and all labelled images and two random seeds.')
h('Student A — concept and architecture',2)
p('Greedy layer-wise training fits the first RBM to pixels, transforms the data to hidden activation features, fits a second RBM to those activations, and trains the logistic classifier on the resulting representation. A conventional DBN uses an undirected top-layer RBM and top-down directed generative connections below it; a deep Boltzmann machine has undirected interactions between successive layers throughout. The scikit-learn Pipeline is a practical stacked-RBM feature extractor, not a full trained generative DBN.')
fig('q3_dbn_vs_dbm.png','Figure 6. Conceptual connection patterns for DBN-style hierarchical representation and a DBM.','Diagrams',6.1)
p('Unlabelled observations may support RBM representation learning before labels are used by a classifier. One might therefore expect a pretrained feature hierarchy to help most when labels are scarce. But this implementation fits each Pipeline on its labelled subset and did not include a separate unlabeled pool; it cannot test that particular benefit.')
h('Student B — two-seed experiment',2)
table(['Labels','Baseline test accuracy (seeds 11 / 29)','RBM Pipeline test accuracy (seeds 11 / 29)'],[
 [str(n), ' / '.join(f"{r['accuracy']:.3f}" for r in q3 if str(r['labels'])==str(n) and r['model']=='baseline'), ' / '.join(f"{r['accuracy']:.3f}" for r in q3 if str(r['labels'])==str(n) and r['model']=='DBN pipeline')] for n in [100,500,'all']])
fig('q3_accuracies.png','Figure 7. Mean accuracy over two seeds for the required three label budgets.',width=5.8)
p('Both models were trained with seeds 11 and 29. The raw-pixel baseline substantially outperformed the two-RBM feature extractor in these runs. A deeper model can discard information, have harder-to-tune representations, suffer from insufficient training, or add variance. More layers do not guarantee better classification. A stronger test would pretrain on the unlabeled training pool, tune iterations, and use separate validation data while keeping the test set untouched.')
p('Program and raw measurements: Programs/q3_dbn_labels.py, Outputs/q3_accuracy.csv. The training times for every run are recorded in the CSV. Joint conclusion: model selection should be validated empirically instead of assumed from depth.')

# Q4
h('Q4 — Generating Images with a Variational Autoencoder (7 marks)',1)
p('Problem: use Fashion-MNIST with a dense VAE, compare latent sizes 2 and 16, reconstruct 10 inputs, generate 20 outputs, and visualise the two-dimensional latent space. The following executed results are Digits-proxy demonstrations, not Fashion-MNIST experiments.')
h('Student B — VAE concept and loss',2)
fig('q4_vae_architecture.png','Figure 8. Dense VAE architecture: encoder, reparameterised latent variables and decoder.','Diagrams',6.1)
eq('L = E[−log pθ(x|z)] + β KL(qφ(z|x) || p(z))')
eq('z = μ + σ ⊙ ε ;       ε ~ N(0,I)')
p('The reconstruction term measures how well decoded pixels match the input; the KL divergence keeps the approximate posterior near the unit Gaussian prior, enabling generation by drawing fresh latent points. The reparameterisation trick moves randomness into ε, allowing gradients to flow through μ and σ. Here a BCE reconstruction objective and 0.25-weighted KL term were used in training, with dense 784→128→latent→128→784 layers. The user-proposed 256-unit example is optional, not mandatory.')
h('Student A — executed reconstruction and generation demonstration',2)
table(['Latent units','Trainable parameters','Demonstration test pixel MSE','Final train objective / image'],[[l,q4['models'][str(l)]['trainable_parameters'],f"{q4['models'][str(l)]['test_mse']:.5f}",f"{q4['models'][str(l)]['last_train_loss_per_image']:.2f}"] for l in [2,16]])
fig('q4_reconstruction_latent_2.png','Figure 9. Ten alternating originals and reconstructions from the 2D-latent VAE — Digits demonstration.',width=5.5)
fig('q4_generated_latent_2.png','Figure 10. Twenty images sampled from the 2D VAE prior — Digits demonstration.',width=5.3)
fig('q4_latent_space.png','Figure 11. Encoded test images in two latent dimensions, coloured by digit class — not clothing classes.',width=5.5)
fig('q4_reconstruction_latent_16.png','Figure 12. Reconstruction comparison for the 16D latent model — Digits demonstration.',width=5.3)
p('The 16D model reduced demonstration MSE from 0.03842 to 0.02644, so it preserved more input detail. The 2D model is simpler to visualise and sample. A platform that prioritises reconstruction fidelity would select 16 latent units subject to validation of generation quality, diversity and resources on real Fashion-MNIST.')
p('Program: Programs/q4_vae_fashion.py. Its default expects official Fashion-MNIST IDX archives; the supplied executed run used --demo. Model files, generated arrays, and the latent plot are included.')

# Q5
h('Q5 — Comparing a GAN with the VAE (6 marks)',1)
p('Problem: train a small dense GAN on Fashion-MNIST, draw its architecture and training losses, compare 20 GAN and 20 VAE images, and assess sharpness, variety and mode collapse. Executed results below are a Digits demonstration only.')
h('Student A — adversarial design and mode collapse',2)
fig('q5_gan_architecture.png','Figure 13. Dense GAN: random-noise generator and binary real/fake discriminator.','Diagrams',6.0)
eq('min_G max_D   Eₓ log D(x) + E_z log(1 − D(G(z)))')
p('The generator transforms random vectors into candidate images without directly receiving individual real images as its own training input. The discriminator receives real images and generated images and learns to distinguish them. The generator receives gradients through the discriminator: it is rewarded for fooling D. Mode collapse occurs when many different latent inputs map to very similar outputs, reducing class coverage and variety even when individual images appear plausible.')
h('Student B — measurements and image-based comparison',2)
p(f"The dense GAN was trained for {q5['epochs']} epochs. Generator and discriminator parameter counts were {q5['G_parameters']:,} and {q5['D_parameters']:,}, respectively. The final mean losses were generator={q5['history'][-1]['generator_loss']:.4f} and discriminator={q5['history'][-1]['discriminator_loss']:.4f}. Adversarial losses are not calibrated image-quality metrics.")
fig('q5_losses.png','Figure 14. Generator and discriminator BCE losses over training.',width=5.6)
fig('q5_vae_vs_gan.png','Figure 15. Two rows of VAE samples and two rows of GAN samples — Digits demonstration.',width=6.1)
p('A pronounced class-coverage failure was measured in Q6: all 200 GAN demonstration images were predicted as the same digit class. This is strong evidence of poor diversity under this classifier and setup, consistent with mode collapse. It is not evidence about Fashion-MNIST sharpness. VAE images also had limited class diversity and were often blurry. Image comparisons alone cannot establish which model is better.')
p('Program: Programs/q5_gan_fashion.py; Graphs/q5_losses.png, q5_vae_vs_gan.png; Models/q5_generator.pt and q5_discriminator.pt.')

# Q6
h('Q6 — Generative Model Mini-Investigations (7 marks)',1)
h('Student A — classifier-based generator evaluation',2)
p('Problem: train a classifier on real Fashion-MNIST, classify 200 images from each model, show class distributions and mean confidence, and examine the nearest real neighbours for ten generated images. Executed demonstration is on Digits and cannot substantiate Fashion-MNIST quality.')
table(['Evaluation item','VAE proxy demo','GAN proxy demo'],[
['200-image class distribution',str(q6['generators']['VAE']['counts']),str(q6['generators']['GAN']['counts'])],
['Average maximum class confidence',f"{q6['generators']['VAE']['mean_confidence']:.4f}",f"{q6['generators']['GAN']['mean_confidence']:.4f}"],
['Nearest-image mean distance (first 10)',f"{statistics.mean(q6['generators']['VAE']['nearest_first_10_distances']):.3f}",f"{statistics.mean(q6['generators']['GAN']['nearest_first_10_distances']):.3f}"]])
p(f"A stochastic-gradient logistic classifier achieved test accuracy {q6['real_test_classifier_accuracy']:.4f} on real Digits test examples. Generated-image prediction confidence is not the same as human realism or image fidelity; classifier biases can assign high confidence to poor, off-distribution generations. Assess category coverage, nearest-real similarity, visual fidelity, and external validation together.")
fig('q6_class_distribution.png','Figure 16. Predicted class counts for 200 VAE and 200 GAN outputs — Digits proxy.',width=5.9)
fig('q6_nearest_vae.png','Figure 17. Ten generated VAE images (top) and their closest training images (bottom).',width=6.0)
fig('q6_nearest_gan.png','Figure 18. Ten generated GAN images (top) and their closest training images (bottom).',width=6.0)
p('A good unconditional generator should cover all classes in approximately the diversity of the real training distribution when appropriate, not concentrate on one class. Memorisation requires explicit nearest-neighbour screening because visually diverse outputs can still reproduce individual training images. Euclidean distance in pixel space is a crude first check; perceptual features and manual review should supplement it.')
h('Student B — convolutional and structured Boltzmann machines',2)
eq('Fully connected RBM: 784 × 500 = 392,000 connection weights')
eq('Convolutional RBM: 16 × 5 × 5 = 400 shared filter weights')
p('Including biases would alter the total numbers, but the question asks for weights. Reusing the same 5×5 filter across an image detects a local pattern regardless of position, allowing strong parameter efficiency. A structured-output Boltzmann model assigns an energy to combinations of poster labels and can learn that certain label pairs are common or rare. Independent binary classifiers omit such label–label interactions and may produce implausible combinations. Counterpoint: rare but legitimate combinations should not be mechanically excluded. Student A should also be able to explain weight sharing; Student B should be able to justify class diversity.')
p('Program and results: Programs/q6_generator_evaluation.py; Outputs/q6_results.json; Models/q6_classifier.joblib.')

# Q7
h('Q7 — Generate Images for a New Product Category (10 marks)',1)
p('Problem: only 300 target-category Fashion-MNIST images (for example, Bags) are available. Build a model, generate 1,000 diverse images, screen for near-copies, evaluate category recognition, and report the final engineering decision. The following proposals are example design drafts rather than records of actual independent student work.')
h('Stage 1 — illustrative independent proposals',2)
table(['Design consideration','Illustrative Student A proposal','Illustrative Student B proposal'],[
['Model','Small VAE: stable optimisation and a latent distribution','Small GAN: potentially sharper samples; careful regularisation'],
['Use of 300 images','Compact hidden layer, train/validation holdout, light augmentation','Pretrain generative features, low-capacity discriminator, early stop'],
['Copy check','Nearest training-image pixel distance; inspect the lowest tail','Embedding-based similarity plus manual inspection and class score'],
['Risks','Blurry outputs; may miss fine details','GAN instability and memorisation on tiny data']])
p('The actual pair should retain their true initial independent proposals and record authorship. The table above is a technically useful illustration, not verified collaboration evidence.')
h('Stage 2 — comparison and selection logic',2)
p('Both designs recognise the limited training set, need for regularisation, and importance of duplicate screening. The VAE offers stable training and smoother latent sampling; the GAN may produce sharper outputs but is susceptible to collapse and copy risk. The demonstrator adopts a compact VAE to prioritise reproducibility and tractable parameter counts, although this does not imply that it meets Fashion-MNIST quality requirements.')
h('Stage 3 — joint final architecture and pseudocode',2)
fig('q7_generation_workflow.png','Figure 19. Target-class generation, image-similarity screening, and classifier validation.','Diagrams',6.1)
p('Proposed model: 784→64 encoder; μ and logσ² each of size 8; 8→64→784 sigmoid decoder. Train on 300 class-specific 28×28 grayscale images using reconstruction BCE plus 0.25 KL regularisation. Split target-class examples into training/holdout sets for a production protocol; this demonstration uses all 300 for fitting and therefore does not provide an unbiased target-class generation assessment.')
code('1. Load 300 distinct target-class Fashion-MNIST training images (e.g., Bag=8).')
code('2. Train compact VAE: z_dim=8; hidden=64; Adam learning rate=0.001.')
code('3. Sample 1,000 latent vectors; decode images in [0,1].')
code('4. Compute minimum image distance from each output to 300 training inputs.')
code('5. Flag output if min distance falls below the data-derived threshold.')
code('6. Evaluate 1,000 images with the independently trained classifier.')
code('7. Report flagged images, class recognition, diversity and limitations.')
h('Stage 4 — Student A analytical validation',2)
eq('Encoder: (784×64+64) + 2×(64×8+8) = 51,280')
eq('Decoder: (8×64+64) + (64×784+784) = 51,536')
eq('Total: 51,280 + 51,536 = 102,816 trainable parameters')
p('This is a relatively small dense generative model, but still large compared with a 300-image training set, so memorisation, blurry reconstructions, and limited coverage remain risks. The demonstration defines its nearest-neighbour threshold as the 2nd percentile of the nearest-other-training-image Euclidean distances among the training images. This is an explicit screening rule with a reproducible calibration, not a guarantee of privacy or perceptual uniqueness.')
h('Stage 4 — Student B experimental validation (Digits-proxy run)',2)
table(['Measured item','Value'],[['Data source',q7['data_source']],['Input images',f"{q7['category_train_count']} (includes augmented digits; not 300 distinct bags)"],['Parameters',f"{q7['parameters']:,}"],['Generated and screened images',f"{q7['generated_count']:,}"],['Copy-threshold',f"{q7['copy_threshold']:.4f}"],['Images flagged under threshold',q7['flagged_near_copies']],['Unflagged images',q7['unflagged_count']],['Classified as intended numeral 8',f"{q7['recognized_as_target']} / {q7['generated_count']}"],['Recognition rate',f"{100*q7['target_recognition_rate']:.1f}%"],['Mean target-class probability',f"{q7['mean_target_confidence']:.4g}"]])
fig('q7_20_generated.png','Figure 20. Category-8 demonstration output samples; these are not Bag images.',width=5.5)
fig('q7_copy_distances.png','Figure 21. Minimum pixel-space distances to training images with threshold line.',width=5.6)
p('Experimental interpretation: none of the 1,000 proxy images was classified as the intended numeral 8, despite all passing this lenient pixel-distance screen. Thus the demonstrator failed the category-fidelity criterion. The absence of flagged near-copies here must NOT be interpreted as successful realism, privacy, or diversity. In the proxy, fewer than 300 distinct source digit-eight images existed, so images were augmented to create 300 training inputs. This does not satisfy the original 300 distinct Fashion-MNIST Bag examples requirement.')
h('Stage 5 — cross-defence',2)
p('Student A should be able to point to the measured class-recognition failure and explain that the model cannot be recommended for deployment. Student B should derive the 102,816 trainable parameters from the dense layers and explain why limited observations raise capacity/overfitting concerns. Both should distinguish the copy-screen threshold from the class-identity threshold.')
h('Stage 6 — joint evaluation and conditional recommendation',2)
p('The architecture is inexpensive and straightforward to train; however, the executed proxy validation failed the stated category-fidelity requirement. A production decision therefore requires a fresh run on 300 genuine Bag training images, a separate held-out Bag test set, assessment of visual realism and variety, and stricter privacy checks with perceptual embeddings. Potential improvements include stronger conditioning, balanced KL weight, image-space augmentation, more training, data filtering and expert review. Synthetic outputs should not replace real images for safety-critical decisions, unbiased evaluation, or preservation of rare patterns without evidence of representativeness.')
p('Before selecting any generative model, inspect dataset size, image complexity, need for controllability, realism/diversity targets, allowable inference cost, training stability, privacy risk, and the measurable acceptance criteria.')

# Conclusions / refs / contribution
h('Overall results and conclusions',1)
notes('Q1 exact RBM enumeration verified Z=18.77471837; the most likely state switches when w₂ changes sign.','Q2 the 64-unit RBM had the better recorded pseudo-log-likelihood under matched hyperparameters.','Q3 the raw-pixel logistic baseline strongly outperformed this stacked-RBM feature Pipeline across two seeds.','Q4 the demonstration latent=16 VAE reconstructed Digits more accurately than latent=2; this is not a Fashion-MNIST result.','Q5–Q6 the Digits-proxy GAN had complete single-class concentration under the evaluation classifier, a warning about mode collapse.','Q7 the Digits-proxy model screened 1,000 outputs but achieved 0% correct-target recognition; its quality target was not met.')
p('The key conclusion is that a generative model requires more than a compelling architecture or high-looking confidence score: it needs reproducible data handling, held-out evaluation, diversity measurement, near-copy detection and evidence that generated examples belong to the intended distribution. None of the Q4–Q7 Digits demonstration results can stand in for the required Fashion-MNIST experiments.')
h('References and reproducibility',2)
for txt in ['1. Scikit-learn API: BernoulliRBM, load_digits, Pipeline, LogisticRegression, SGDClassifier and pairwise_distances. https://scikit-learn.org/stable/','2. Fashion-MNIST dataset repository and official four gzip IDX downloads: https://github.com/zalandoresearch/fashion-mnist','3. Kingma, D. P., and Welling, M. (2014). Auto-Encoding Variational Bayes. ICLR.','4. Goodfellow, I., et al. (2014). Generative Adversarial Nets. NeurIPS.','5. Hinton, G. (2002). Training Products of Experts by Minimizing Contrastive Divergence. Neural Computation.']:
 p(txt)
p('Run commands, package versions, data-download requirements, graphs and JSON measurement files are in README.txt and requirements.txt. To obtain Fashion-MNIST evidence, download official IDX gzip files, then run Programs/q4_vae_fashion.py, q5_gan_fashion.py, q6_generator_evaluation.py and q7_category_generator.py without --demo in that order.')
h('Contribution Record — to be verified by both students',1)
p('The assignment requires truthful individual evidence. The following describes the designated primary responsibilities, not a factual assertion that either student performed them. Both students should verify and sign the final record after completing the work together.')
table(['Q','Student A — designated primary responsibility','Student B — designated primary responsibility','Joint work'],[
 ['Q1','Energy/probability hand calculation','Code verification; w₂ change','Model and parameter interpretation'],
 ['Q2','RBM comparison, filters, reconstructions','Positive/negative phases and CD','Digit modelling and pattern analysis'],
 ['Q3','DBN/DBM models and explanation','Two-seed classifier comparison','Evaluate depth and label availability'],
 ['Q4','VAE generation and reconstruction experiment','VAE equations, KL, reparameterisation','Latent-size decision'],
 ['Q5','GAN architecture and mode collapse','Loss curves and image-quality evidence','Generator comparison'],
 ['Q6','Classifier and nearest-neighbour evaluation','Conv RBM and structured label modelling','Cross-verification'],
 ['Q7','Analytical size and threshold','Implementation and experimental validation','Initial designs, final selection, review']])
h('Individual verification — preparation questions',2)
notes('What exactly does the RBM normalising constant represent?','Why is the RBM pseudo-likelihood not an exact data likelihood?','What differs between a DBN and a fully undirected DBM?','Why does removing the VAE KL term hurt prior sampling?','What evidence would distinguish GAN mode collapse from a classifier defect?','Why do 400 convolutional filter weights replace 392,000 fully connected connections in the stated example?','How can a generator pass a nearest-pixel check while failing the class-quality criterion?')

# Source appendix
newpage();h('Appendix — Complete executable source listings',1)
p('The actual source files in Programs/ are authoritative, including shared common.py and create_diagrams.py. The following listings reproduce every principal experiment. Code files remain separately downloadable and runnable, since copying from a word processor may modify some spacing or typography.')
for name in ['q1_energy_model.py','q2_rbm_digits.py','q3_dbn_labels.py','q4_vae_fashion.py','q5_gan_fashion.py','q6_generator_evaluation.py','q7_category_generator.py','common.py']:
 h(name,2)
 src=(ROOT/'Programs'/name).read_text().splitlines()
 for line in src:
  # avoid excessively long monospaced source lines: let Word wrap automatically
  a=D.add_paragraph(style='CodeListing');a.alignment=WD_ALIGN_PARAGRAPH.LEFT
  r=a.add_run(line if line else ' ');r.font.name='Consolas';r.font.size=Pt(6.7)

path=ROOT/'Final_Assignment_5.docx';D.save(path)
print('WROTE',path,path.stat().st_size)
