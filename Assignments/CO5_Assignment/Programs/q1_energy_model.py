"""Q1: Enumerate all states of a 2-visible/1-hidden RBM and conditional hidden probabilities."""
from common import ROOT,save_json
import itertools,math,csv

def table(w2):
    states=[]
    for v1,v2,h in itertools.product([0,1],repeat=3):
        E=-(.5*v1-.5*v2+v1*h+w2*v2*h)
        states.append(dict(v1=v1,v2=v2,h=h,energy=E,unnormalized=math.exp(-E)))
    Z=sum(r['unnormalized'] for r in states)
    for r in states:r['probability']=r['unnormalized']/Z
    return Z,states
result={}
for w2 in [1,-1]:
    Z,rows=table(w2);result[str(w2)]={'Z':Z,'most_likely':max(rows,key=lambda r:r['probability']),'states':rows}
    with open(ROOT/'Outputs'/f'q1_states_w2_{w2}.csv','w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    print(f'w2={w2}; Z={Z:.8f}; most likely={result[str(w2)]["most_likely"]}')
cond=[]
for v1,v2 in itertools.product([0,1],repeat=2):
    x=v1+v2;cond.append(dict(v1=v1,v2=v2,hidden_probability=1/(1+math.exp(-x))))
result['conditionals']=cond;save_json('q1_results.json',result)
for v in cond:print('P(h=1|v)=',v)
