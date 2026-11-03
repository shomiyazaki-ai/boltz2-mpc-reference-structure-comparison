"""Independent parser + Horn quaternion/eigen fit; does not import production core.
Computational verification only. No inference or new scientific endpoints.
"""
from pathlib import Path
import re,csv,json,math,argparse,platform
import numpy as np
from scipy.spatial.transform import Rotation
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);out=p.parse_args().out;out.mkdir(parents=True,exist_ok=True)
def read(path):
 with path.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
m=json.loads((ROOT/'data/frozen/masks.json').read_text());frozen=read(ROOT/'data/results/primary_70_metrics.csv')+read(ROOT/'data/results/AF_35_metrics.csv');structures={}
# Independently locate header and parse only CA records with a token regex.
for path in (ROOT/'data/frozen/coordinates').glob('*.cif'):
 lines=path.read_text().splitlines();head=[x.strip().split()[0] for x in lines if x.startswith('_atom_site.')];idx={s.split('.',1)[1]:i for i,s in enumerate(head)};atoms={}
 for line in lines:
  if not line.startswith('ATOM'):continue
  fields=[v[1:-1] if len(v)>1 and v[0]==v[-1] and v[0] in "\"'" else v for v in re.findall(r"'[^']*'|\"[^\"]*\"|\S+",line)]
  if len(fields)!=len(head) or fields[idx['label_atom_id']]!='CA':continue
  chain=fields[idx['label_asym_id']];seq=fields[idx['label_seq_id']]
  if chain not in ['A','B'] or not seq.isdigit():continue
  predicted=path.stem.startswith(('AF-','O95563'))
  protein=({'A':'MPC2','B':'MPC1L'} if predicted else {'A':'MPC1L','B':'MPC2'})[chain]
  k=(protein,int(seq));alt=fields[idx['label_alt_id']];rank=(-float(fields[idx['occupancy']]),'' if alt in ['.','?'] else alt)
  v=np.array([float(fields[idx['Cartn_'+q]]) for q in 'xyz'])
  if k not in atoms or rank<atoms[k][0]:atoms[k]=(rank,v)
 structures[path.stem]={k:v[1] for k,v in atoms.items()}
def coords(name,keys):return np.array([structures[name][k] for k in keys])
def keys(mask,protein=None):return [(p,i) for p in ([protein] if protein else ['MPC1L','MPC2']) for i in m[str(mask)][p]]
def qfit(x,y):
 a=x.mean(axis=0);b=y.mean(axis=0);H=(x-a).T@(y-b);xx,xy,xz=H[0];yx,yy,yz=H[1];zx,zy,zz=H[2]
 K=np.array([[xx+yy+zz,yz-zy,zx-xz,xy-yx],[yz-zy,xx-yy-zz,xy+yx,zx+xz],[zx-xz,xy+yx,-xx+yy-zz,yz+zy],[xy-yx,zx+xz,yz+zy,-xx-yy+zz]])
 _,Q=np.linalg.eigh(K);w,xq,yq,zq=Q[:,-1];R=Rotation.from_quat([xq,yq,zq,w]).as_matrix().T
 return R,b-a@R
checks=[];computed=[]
def ck(n,yes):
 checks.append({'check':n,'pass':bool(yes)})
 if not yes:raise AssertionError(n)
base=np.array([[0.,0.,0.],[2.,1.,0.],[1.,3.,2.],[-1.,-2.,4.]])
R0=Rotation.from_euler('xyz',[31,57,-43],degrees=True).as_matrix();target=base@R0+[4.,-3.,2.]
R,t=qfit(base,target);ck('quaternion_known_rigid_transform',np.max(abs(base@R+t-target))<1e-10);ck('quaternion_det',abs(np.linalg.det(R)-1)<1e-10)
for i,row in enumerate(frozen):
 metric=row['metric']
 if metric.startswith('fixed_union5'):f=e=keys(73)
 elif metric.startswith('fixed_union4'):f=e=keys(62)
 elif metric.startswith('full_198'):f=e=keys(198)
 elif metric.startswith('MPC1L_independent'):f=e=keys(198,'MPC1L')
 elif metric.startswith('MPC2_independent'):f=e=keys(198,'MPC2')
 elif metric.startswith('fit_MPC1L'):f=keys(198,'MPC1L');e=keys(198,'MPC2')
 elif metric.startswith('fit_MPC2'):f=keys(198,'MPC2');e=keys(198,'MPC1L')
 else:raise ValueError(metric)
 a,b=row['source'],row['target'];R,t=qfit(coords(a,f),coords(b,f));value=float(np.sqrt(np.mean(np.sum((coords(a,e)@R+t-coords(b,e))**2,axis=1))));delta=abs(value-float(row['RMSD_A']))
 ck('metric_'+str(i+1),delta<=1e-5 and abs(np.linalg.det(R)-1)<1e-10)
 # Fit an independently permuted list, evaluate with the original order.
 perm=np.random.default_rng(100+i).permutation(len(f));Rp,tp=qfit(coords(a,f)[perm],coords(b,f)[perm]);valuep=float(np.sqrt(np.mean(np.sum((coords(a,e)@Rp+tp-coords(b,e))**2,axis=1))))
 ck('permutation_'+str(i+1),abs(valuep-value)<1e-9)
 computed.append({'source':a,'target':b,'metric':metric,'canonical_RMSD_A':row['RMSD_A'],'quaternion_RMSD_A':value,'abs_difference_A':delta,'det_rotation':float(np.linalg.det(R)),'pass':True})
for n,rows in [('independent_105.csv',computed),('independent_checks.csv',checks)]:
 with (out/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
s={'status':'PASS','values':len(computed),'max_abs_difference_A':max(r['abs_difference_A'] for r in computed),'checks':len(checks),'method':'separate regex CA parser + Horn quaternion eigenproblem; no production module imported','python':platform.python_version(),'numpy':np.__version__}
(out/'independent_summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s))
