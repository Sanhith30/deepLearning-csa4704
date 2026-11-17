"""Shared deterministic utilities for Assignment 4; importable by individual experiments."""
from pathlib import Path
import json
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
for folder in ('Datasets','Outputs','Graphs','Diagrams','Logs'):
    (ROOT/folder).mkdir(exist_ok=True)

def save_result(name, values):
    p=ROOT/'Outputs'/f'{name}.json'
    p.write_text(json.dumps(values, indent=2, ensure_ascii=False, default=lambda x: x.item() if isinstance(x,np.generic) else x.tolist() if hasattr(x,'tolist') else str(x)),encoding='utf8')
    print(json.dumps(values,indent=2,ensure_ascii=False,default=lambda x: x.item() if isinstance(x,np.generic) else x.tolist() if hasattr(x,'tolist') else str(x)))

def bn_sample(n, seed=123):
    """Q5 graph P -> U -> S -> C. All outcomes boolean, shapes (n,)."""
    rng=np.random.default_rng(seed)
    p=rng.random(n)<0.10
    u=rng.random(n)<np.where(p,0.40,0.02)
    s=rng.random(n)<np.where(u,0.80,0.05)
    c=rng.random(n)<np.where(s,0.90,0.05)
    return {'P':p,'U':u,'S':s,'C':c}

def graph_exact():
    u=0.1*0.4+0.9*0.02
    s=u*0.8+(1-u)*0.05
    c=s*0.9+(1-s)*0.05
    s_given_p=0.4*0.8+0.6*0.05
    c_given_p=s_given_p*0.9+(1-s_given_p)*0.05
    return {'P_U':u,'P_S':s,'P_C':c,'P_C_given_P':c_given_p,'P_P_given_C':0.1*c_given_p/c}
