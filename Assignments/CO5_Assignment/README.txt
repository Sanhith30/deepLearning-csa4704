DEEP LEARNING ASSIGNMENT 5 (CO5) — PROJECT

1) Python 3.10+, pip install -r requirements.txt
2) Run from project/Programs:
   python q1_energy_model.py
   python q2_rbm_digits.py
   python q3_dbn_labels.py
   python q4_vae_fashion.py
   python q5_gan_fashion.py
   python q6_generator_evaluation.py
   python q7_category_generator.py

DEPENDENCY / DATA LIMITATION:
Official Fashion-MNIST files were not available in the execution container.
For actual assignment Fashion-MNIST results, download original four IDX gzip files
from https://github.com/zalandoresearch/fashion-mnist/tree/master/data/fashion
and put them under Datasets/fashion/:
  train-images-idx3-ubyte.gz
  train-labels-idx1-ubyte.gz
  t10k-images-idx3-ubyte.gz
  t10k-labels-idx1-ubyte.gz
Programs q4..q7 require these files by default (do not use --demo for assignment results).

The bundled Q4..Q7 execution outputs were generated with explicit --demo,
which substitutes an upscaled sklearn DIGITS dataset to verify execution.
They are NOT Fashion-MNIST experiment results or evidence of clothing quality.
In Q7, the demonstration numerals were augmented to obtain 300 input samples,
which does NOT satisfy the 300 distinct Fashion-MNIST Bag images requirement.

To reproduce the non-Fashion demonstration scripts:
   python q4_vae_fashion.py --demo
   python q5_gan_fashion.py --demo
   python q6_generator_evaluation.py --demo
   python q7_category_generator.py --demo

Q1-Q3 use actual scikit-learn Digits dataset as required.
Q3's Pipeline greedily fits each RBM using the labeled training subset and does
not exploit an additional unlabeled pool; this limitation is noted in the report.
All timings and measurements depend on CPU, software versions, and random seeds.
The Student A/Student B design records and contribution table should be confirmed
and revised by the actual pair before submitting.
