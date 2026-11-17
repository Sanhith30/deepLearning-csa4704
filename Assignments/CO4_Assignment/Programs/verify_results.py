"""Regression checks for every executed experiment in Assignment 4."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from docx import Document
from _shared import ROOT
read=lambda q: json.loads((ROOT/'Outputs'/f'Q{q}_results.json').read_text())
q={i:read(i) for i in range(1,8)}
assert q[1]['samples']==178 and q[1]['features']==13
assert q[1]['component_count_for_90_percent']==8 and q[1]['retained_at_k90']>=.9
assert all(a['mse']>b['mse'] for a,b in zip(q[1]['reconstructions'],q[1]['reconstructions'][1:]))
assert q[2]['both_noisy_features_highest']
assert len(q[2]['fa_noise_variance'])==13
assert len(q[3]['mixing_cases'])==2
assert all(v['ICA_match_score']>v['PCA_match_score'] for v in q[3]['mixing_cases'])
assert q[4]['atoms']==36 and q[4]['samples']==1797
assert all(a['avg_nonzero_coefficients']>b['avg_nonzero_coefficients'] and a['mse_per_pixel']<b['mse_per_pixel'] for a,b in zip(q[4]['rows'],q[4]['rows'][1:]))
assert q[5]['full_joint_free_parameters']==15 and q[5]['model_parameters']==7
assert abs(q[5]['joint_all_events']-.0288)<1e-12
assert len(q[5]['sample_results'])==3
assert q[6]['SFA']['corr_extracted_original']>.99
assert abs(q[6]['sampling_exact']['P_C']-.129475)<1e-12
assert abs(q[6]['sampling_exact']['P_P_given_C']-.2683915813863681)<1e-9
assert q[7]['full_joint_free_parameters']==127 and q[7]['graph_parameters']==17
assert abs(q[7]['sum_exact_joint_probabilities']-1)<1e-12
assert q[7]['exact_P_E_given_P']>q[7]['exact_P_E']
assert len(pd.read_csv(ROOT/'Outputs'/'Q7_exact_joint_128_states.csv'))==128
for i in range(1,8):
    assert (ROOT/'Logs'/['','Q1_PCA_PPCA','Q2_Factor_Analysis','Q3_ICA','Q4_Sparse_Coding','Q5_Bayesian_Network','Q6_SFA_And_Sampling','Q7_Extended_Network'][i]).with_suffix('.log').exists()
d=Document(ROOT/'Final_Assignment_4.docx')
assert len(d.inline_shapes)>=14 and len(d.tables)>=18
assert all(f'Q{i} –' in '\n'.join(p.text for p in d.paragraphs) for i in range(1,8))
print('PASS: seven experiments, numerical consistency, 128-state enumeration, all logs, document sections, tables and diagrams.')
