"""Small mmCIF atom-loop reader and proper SVD fit for the six frozen C01 files.
No model inference. Inputs are immutable; alternate-conformer policy is explicit.
"""
from pathlib import Path
import shlex, csv, json, hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BOLTZ='O95563_P0DKB6_Boltz-2_v2-1-1'
AF='AF-0000000204012512-model_v1'
REFS=['9GIX','9GIV','9GIW','9GIY']
NAMES=[BOLTZ]+REFS+[AF]
M73='fixed_union5_interface_CA_RMSD_A';M62='fixed_union4_interface_CA_RMSD_A';M198='full_198_two_chain_CA_RMSD_A'
def read_csv(path):
 with Path(path).open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write_csv(path,rows):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def atom_rows(path):
 # CIF whitespace separates fields; a source atom record can span lines.
 # The Boltz input contains comments inside the header and split model-number
 # tokens. Preserve the bytes and parse the token stream, without "repairing" it.
 lines=Path(path).read_text().splitlines(); cols=[];beg=None
 for i,s in enumerate(lines):
  if s.startswith('_atom_site.'):
   if not cols:beg=i
   cols.append(s.strip().split()[0].split('.',1)[1])
  elif cols and (not s.strip() or s.lstrip().startswith('#')):
   continue
  elif cols:
   beg=i;break
 assert cols and beg is not None
 pending=[]
 for s in lines[beg:]:
  s=s.strip()
  if not s:continue
  if s.startswith(('#','loop_','_')):break
  pending.extend(shlex.split(s,posix=True))
  while len(pending)>=len(cols):
   tok=pending[:len(cols)];pending=pending[len(cols):]
   yield dict(zip(cols,tok))
 if pending:raise ValueError('Truncated atom-loop record: '+str(path))
def read_structure(path,name):
 rev={'A':'MPC2','B':'MPC1L'} if name in (BOLTZ,AF) else {'A':'MPC1L','B':'MPC2'}
 out={p:{} for p in rev.values()}
 for a in atom_rows(path):
  p=rev.get(a['label_asym_id']);rid=a['label_seq_id']
  if p is None or a['group_PDB']!='ATOM' or not rid.isdigit():continue
  key=int(rid);atom=a['label_atom_id'];alt=a.get('label_alt_id','.')
  # Highest occupancy, then blank, then lexicographically first altloc.
  rank=(-float(a['occupancy']),'' if alt in ('.','?') else alt)
  a.update(xyz=np.array([float(a['Cartn_'+v]) for v in 'xyz']),rank=rank)
  old=out[p].setdefault(key,{})
  if atom not in old or rank<old[atom]['rank']:old[atom]=a
 return out
def load_all():return {n:read_structure(ROOT/'data/frozen/coordinates'/f'{n}.cif',n) for n in NAMES}
def mask_keys(masks,m):return [(p,r) for p in ('MPC1L','MPC2') for r in masks[str(m)][p]]
def chain_keys(masks,p):return [(p,r) for r in masks['198'][p]]
def xyz(data,name,keys):return np.array([data[name][p][r]['CA']['xyz'] for p,r in keys])
def fit(x,y):
 a=x.mean(0);b=y.mean(0);u,s,vt=np.linalg.svd((x-a).T@(y-b));d=np.eye(3);d[2,2]=1 if np.linalg.det(u@vt)>0 else -1
 R=u@d@vt;return R,b-a@R
def rms(x,y):return float(np.sqrt(np.mean(np.sum((x-y)**2,axis=1))))
def spec(masks):
 ans=[(M73,mask_keys(masks,73),mask_keys(masks,73)),(M62,mask_keys(masks,62),mask_keys(masks,62)),(M198,mask_keys(masks,198),mask_keys(masks,198))]
 for p,q in [('MPC1L','MPC2'),('MPC2','MPC1L')]:
  ans.extend([(p+'_independent_chain_CA_RMSD_A',chain_keys(masks,p),chain_keys(masks,p)),('fit_'+p+'_evaluate_'+q+'_CA_displacement_RMSD_A',chain_keys(masks,p),chain_keys(masks,q))])
 return ans
