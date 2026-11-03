import os, io, csv, json, zipfile, hashlib, math, platform, sys
from pathlib import Path
import numpy as np
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from scipy.linalg import orthogonal_procrustes
ROOT=Path('/mnt/data'); O=ROOT/'C01_AF_SessionB_2026-11-01';O.mkdir(exist_ok=True)
A=ROOT/'C01_AF_SessionA_2026-11-01'; h=zipfile.ZipFile(ROOT/'C01_Research_Execution_Handoff_2026-10-31(1).zip');af=zipfile.ZipFile(ROOT/'AF-0000000204012512-model_v1.zip');ex=zipfile.ZipFile(ROOT/'C01_Execution_Results_2026-10-31.zip')
masks=json.loads((A/'masks_frozen.json').read_text()); names=['AF-0000000204012512-model_v1','O95563_P0DKB6_Boltz-2_v2-1-1','9GIX','9GIV','9GIW','9GIY']; data={}; manifest=list(csv.DictReader(open(A/'input_manifest.csv')))
for name in names:
 b=af.read(name+'.cif') if name.startswith('AF-') else h.read('01_COORDINATES/'+name+'.cif'); want=next(x['sha256'] for x in manifest if x['name']==name+'.cif');assert hashlib.sha256(b).hexdigest()==want
 d=MMCIF2Dict(io.StringIO(b.decode('utf8'))); rev={'A':'MPC2','B':'MPC1L'} if name.startswith(('AF-','O95563')) else {'A':'MPC1L','B':'MPC2'}
 atoms={};n=len(d['_atom_site.label_atom_id']); alt=d.get('_atom_site.label_alt_id',['.']*n)
 for i in range(n):
  if d['_atom_site.group_PDB'][i]!='ATOM' or d['_atom_site.label_atom_id'][i]!='CA':continue
  c=rev.get(d['_atom_site.label_asym_id'][i]);rid=d['_atom_site.label_seq_id'][i]
  if c and rid.isdigit():
   k=(c,int(rid));occ=float(d['_atom_site.occupancy'][i]);rank=(occ,alt[i]=='.',alt[i]=='A')
   if k not in atoms or rank>atoms[k][1]:atoms[k]=(np.array([float(d['_atom_site.Cartn_'+a][i]) for a in 'xyz']),rank)
 data[name]={k:v[0] for k,v in atoms.items()}
for name in names:
 for prot in ('MPC1L','MPC2'):
  assert all((prot,r) in data[name] for r in masks['198'][prot])
def keys(m):return [(p,r) for p in ('MPC1L','MPC2') for r in masks[m][p]]
def chain(p):return [(p,r) for r in masks['198'][p]]
def xyz(name,kk):return np.array([data[name][k] for k in kk])
def fit(X,Y):
 x=X.mean(0);y=Y.mean(0);u,s,vt=np.linalg.svd((X-x).T@(Y-y));sign=np.linalg.det(u@vt);D=np.diag([1,1,1 if sign>=0 else -1]);R=u@D@vt;t=y-x@R;return R,t
# alternative independently-coded fit based on SVD of opposite covariance (column convention)
def independent_fit(X,Y):
 a=X.mean(axis=0);b=Y.mean(axis=0); H=(Y-b).T@(X-a); U,s,Vh=np.linalg.svd(H);D=np.eye(3);D[-1,-1]=np.sign(np.linalg.det(U@Vh));Q=U@D@Vh; R=Q.T;t=b-a@R;return R,t
spec=[('fixed_union5_interface_CA_RMSD_A',keys('73'),keys('73')),
 ('fixed_union4_interface_CA_RMSD_A',keys('62'),keys('62')),
 ('full_198_two_chain_CA_RMSD_A',keys('198'),keys('198')),
 ('MPC1L_independent_chain_CA_RMSD_A',chain('MPC1L'),chain('MPC1L')),
 ('fit_MPC1L_evaluate_MPC2_CA_displacement_RMSD_A',chain('MPC1L'),chain('MPC2')),
 ('MPC2_independent_chain_CA_RMSD_A',chain('MPC2'),chain('MPC2')),
 ('fit_MPC2_evaluate_MPC1L_CA_displacement_RMSD_A',chain('MPC2'),chain('MPC1L'))]
roster=[(names[0],x) for x in names[2:]]+[(names[0],names[1])]
results=[];trans=[];residuals=[];qc=[]
for src,tgt in roster:
 for metric,fk,ek in spec:
  X,Y=xyz(src,fk),xyz(tgt,fk);R,t=fit(X,Y);R2,t2=independent_fit(X,Y); xx,yy=xyz(src,ek),xyz(tgt,ek);rr=np.linalg.norm(xx@R+t-yy,axis=1);val=float(np.sqrt(np.mean(rr**2)));val2=float(np.sqrt(np.mean(np.sum((xx@R2+t2-yy)**2,axis=1))))
  perm=np.random.default_rng(20261101).permutation(len(fk));Rp,tp=fit(X[perm],Y[perm]);valp=float(np.sqrt(np.mean(np.sum((xx@Rp+tp-yy)**2,axis=1))))
  row={'source':src,'target':tgt,'metric':metric,'n_fit':len(fk),'n_eval':len(ek),'RMSD_A':val,'independent_RMSD_A':val2,'delta_independent_A':abs(val-val2),'delta_permuted_A':abs(val-valp),'detR':float(np.linalg.det(R)),'status':'PASS' if abs(val-val2)<1e-9 and abs(val-valp)<1e-9 and abs(np.linalg.det(R)-1)<1e-9 else 'FAIL'}
  results.append(row);qc.append({'source':src,'target':tgt,'metric':metric,'test':'independent_fit_and_permutation_and_proper_rotation','status':row['status'],'value':str((row['delta_independent_A'],row['delta_permuted_A'],row['detR']))})
  trans.append({'source':src,'target':tgt,'metric':metric,'R':R.tolist(),'t_A':t.tolist(),'fit_residual_rmsd_A':float(np.sqrt(np.mean(np.sum((X@R+t-Y)**2,axis=1)))),'n_fit':len(fk),'n_eval':len(ek)})
  for (prot,rid),d in zip(ek,rr):residuals.append({'source':src,'target':tgt,'metric':metric,'protein':prot,'residue':rid,'residual_A':float(d)})
# parent replay independent via previously verified Session A and new fit
old=list(csv.DictReader(io.StringIO(ex.read('RESULTS/all_10_comparisons_primary_and_controls.csv').decode())));checks=[]
for row in old:
 f,e=row['fit_mask'],row['eval_mask'];fk=keys(f) if f in masks else chain(f.replace('_full',''));ek=keys(e) if e in masks else chain(e.replace('_full',''))
 R,t=independent_fit(xyz(row['source'],fk),xyz(row['target'],fk));X=xyz(row['source'],ek);Y=xyz(row['target'],ek);v=float(np.sqrt(np.mean(np.sum((X@R+t-Y)**2,axis=1))))
 checks.append({'source':row['source'],'target':row['target'],'metric':row['metric'],'original':float(row['RMSD_A']),'recalculated':v,'difference_A':abs(v-float(row['RMSD_A'])),'pass':abs(v-float(row['RMSD_A']))<1e-8})
assert all(r['status']=='PASS' for r in results)
assert all(r['pass'] for r in checks)
with open(O/'primary_5_comparisons_35_metrics.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=results[0]);w.writeheader();w.writerows(results)
with open(O/'per_residue_residuals.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=residuals[0]);w.writeheader();w.writerows(residuals)
with open(O/'numeric_qc_35.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=qc[0]);w.writeheader();w.writerows(qc)
with open(O/'parent_70_replay.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=checks[0]);w.writeheader();w.writerows(checks)
(O/'fit_transforms.json').write_text(json.dumps(trans,indent=2))
manifest2={'input_manifest':manifest,'addendum_sha256':hashlib.sha256((ROOT/'C01_Addendum/C01_AF_Exploratory_Addendum_v1.0_FINAL.md').read_bytes()).hexdigest(),'session_A_gate':json.loads((A/'execution_record.json').read_text())['gate'],'python':sys.version,'numpy':np.__version__,'scipy':__import__('scipy').__version__,'biopython':__import__('Bio').__version__,'result_count':len(results),'residual_records':len(residuals),'max_independent_difference_A':max(r['delta_independent_A'] for r in results),'max_parent_replay_difference_A':max(r['difference_A'] for r in checks),'status':'PASS','new_pairs':roster}
(O/'execution_record.json').write_text(json.dumps(manifest2,indent=2,ensure_ascii=False))
print('COMPLETED',len(results),len(residuals),'max independent',manifest2['max_independent_difference_A']);
for r in results:
 if r['metric']=='fixed_union5_interface_CA_RMSD_A':print(r['target'],r['RMSD_A'])
