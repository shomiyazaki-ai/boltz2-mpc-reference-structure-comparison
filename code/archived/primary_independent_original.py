import os,sys,json,csv,hashlib,itertools,platform,datetime,zipfile
from pathlib import Path
import gemmi,numpy as np,scipy
from scipy.spatial.transform import Rotation
R=Path(__file__).resolve().parent; inp=R/'input'; old=R/'previous/RESULTS'; out=R/'SESSION1';out.mkdir(exist_ok=True)
files=['O95563_P0DKB6_Boltz-2_v2-1-1','9GIX','9GIV','9GIW','9GIY']; roles={'MPC1L':list(range(22,106)),'MPC2':list(range(8,122))}; prev_masks=json.load(open(old/'masks.json'))
log=[]
def check(label,ok,detail=''):
 log.append(dict(check=label,status='PASS' if ok else 'FAIL',detail=str(detail))); print(label, 'PASS' if ok else 'FAIL', detail)
def hashfile(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
manifest=json.load(open(inp/'SHA256_MANIFEST.json'))
for it in manifest:check('input_sha256:'+it['path'],hashfile(inp/it['path'])==it['sha256'])
with zipfile.ZipFile('/mnt/data/C01_Minimum_Protocol_v1.0_FINAL_2026-10-31(1).zip') as z: protocol=z.read('C01_Minimum_Protocol_v1.0_FINAL_2026-10-31.md')
check('protocol_copies_equal',protocol==(inp/'00_PROTOCOL/C01_Minimum_Protocol_v1.0_FINAL_2026-10-31.md').read_bytes()==(R/'previous/PROTOCOL/C01_Minimum_Protocol_v1.0_FINAL_2026-10-31.md').read_bytes())
check('protocol_expected_hash',hashlib.sha256(protocol).hexdigest()=='87ba6cb500bdf4fc67803bec8cf2f655443367431945c7f7df359a1bff0381fa')
# Gemmi CIF independent parsing; select highest occupancy then lexical altloc.
data={}; cross=[]
for f in files:
 
 try:
  block=gemmi.cif.read_file(str(inp/'01_COORDINATES'/ (f+'.cif'))).sole_block()
 except RuntimeError as exc:
  # Original ModelCIF contains duplicate category tags outside atom_site; extract atom loop into in-memory CIF. Original input remains unchanged.
  source=(inp/'01_COORDINATES'/ (f+'.cif')).read_text()
  start=source.rfind('loop_',0,source.index('_atom_site.group_PDB'))
  end=source.index('\n#',source.index('\nATOM ',start))
  atomloop=source[start:end]+'\n#\n'
  block=gemmi.cif.read_string('data_atomloop\n'+atomloop).sole_block()
  check('prediction_cif_atom_loop_fallback',f==files[0] and 'duplicate tag' in str(exc),'in-memory only; original SHA256 unchanged')
 tab=block.find(['_atom_site.label_asym_id','_atom_site.label_seq_id','_atom_site.label_atom_id','_atom_site.label_comp_id','_atom_site.Cartn_x','_atom_site.Cartn_y','_atom_site.Cartn_z','_atom_site.occupancy','_atom_site.label_alt_id','_atom_site.type_symbol','_atom_site.auth_seq_id','_atom_site.group_PDB'])
 mapping={'A':'MPC2','B':'MPC1L'} if f==files[0] else {'A':'MPC1L','B':'MPC2'}
 dd={r:{} for r in roles}
 for row in tab:
  ch,rs,at,aa,x,y,z,occ,alt,element,auth,group=list(row)
  if ch not in mapping or not rs.isdigit() or group!='ATOM':continue
  r=mapping[ch];ix=int(rs);key=(ix,at); d=dd[r];entry={'xyz':np.array([float(x),float(y),float(z)]),'aa':aa,'occ':float(occ),'alt':alt,'element':element,'auth':auth,'chain':ch}
  if key not in d or (-entry['occ'],entry['alt'])<(-d[key]['occ'],d[key]['alt']): d[key]=entry
 data[f]=dd
 for role,ids in roles.items():
  for ix in ids:
   v=dd[role].get((ix,'CA'))
   cross.append({'structure':f,'protein':role,'aligned_residue':ix,'source_label_seq_id':ix,'source_label_asym_id':v['chain'] if v else '', 'source_auth_seq_id':v['auth'] if v else '', 'residue_name':v['aa'] if v else '', 'CA_present':int(v is not None),'selected_altloc':v['alt'] if v else ''})
check('198_CA_every_structure',all(v['CA_present'] for v in cross),f'{sum(x["CA_present"] for x in cross)}/990')
check('sequence_identity_all_198',all(len({data[f][r][(i,'CA')]['aa'] for f in files})==1 for r in roles for i in roles[r]))
# independent heavy contact reconstruction
masksets={}; contact_counts=[]
for cutoff,maskname in [(5.,'73'),(4.,'62')]:
 union=set(); shared=None
 for f in files[1:]:
  d=data[f]; pairs=set()
  for i in roles['MPC1L']:
   a=[v['xyz'] for (ix,at),v in d['MPC1L'].items() if ix==i and v['element'].upper() not in ('H','D')]
   for j in roles['MPC2']:
    b=[v['xyz'] for (ix,at),v in d['MPC2'].items() if ix==j and v['element'].upper() not in ('H','D')]
    if a and b and np.min(np.sum((np.asarray(a)[:,None,:]-np.asarray(b)[None,:,:])**2,axis=2))<cutoff**2:pairs.add((i,j))
  union |=pairs;shared=pairs if shared is None else shared & pairs;contact_counts.append(dict(cutoff=cutoff,structure=f,count=len(pairs)))
 masksets[maskname]={r:sorted({p[0 if r=='MPC1L' else 1] for p in union}) for r in roles}
 check(f'mask_{maskname}_matches_frozen',masksets[maskname]==prev_masks[maskname],str({r:len(masksets[maskname][r]) for r in roles}))
 check(f'contacts_{maskname}',len(union)==(107 if cutoff==5 else 69) and len(shared)==(37 if cutoff==5 else 13),f'union={len(union)},shared={len(shared)}')
masksets['198']=roles
# scipy Rotation.align_vectors yields active transform column, derive row rotation for X->Y
# covariance SVD not used in this script

def fit(X,Y):
 xc=X.mean(axis=0);yc=Y.mean(axis=0)
 rotation, angleerr=Rotation.align_vectors(Y-yc,X-xc)
 r=rotation.as_matrix().T; t=yc-xc@r
 return r,t

def rmsd(X,Y):return float(np.sqrt(np.mean(np.sum((X-Y)**2,axis=1))))
def positions(f,keys):return np.array([data[f][role][(i,'CA')]['xyz'] for role,i in keys])
def keys(mask):return [(r,i) for r in ('MPC1L','MPC2') for i in masksets[mask][r]]
rg=np.random.default_rng(20261031);sample=rg.normal(size=(73,3));rot=Rotation.from_euler('xyz',[22,35,-79],degrees=True).as_matrix().T; shifted=sample@rot+np.array([8.,-2.,4.]);r,t=fit(sample,shifted)
check('synthetic_rotation',rmsd(sample@r+t,shifted)<1e-10,rmsd(sample@r+t,shifted))
check('synthetic_identity',rmsd(sample@fit(sample,sample)[0]+fit(sample,sample)[1],sample)<1e-10)
perm=rg.permutation(73);r2,t2=fit(sample[perm],shifted[perm]);check('synthetic_order',rmsd(sample@r2+t2,shifted)<1e-10)
check('synthetic_proper_rotation',abs(np.linalg.det(r)-1)<1e-10)
check('negative_chain_swap',any(data[files[0]]['MPC1L'][(i,'CA')]['aa'] != data['9GIX']['MPC2'].get((i,'CA'),{}).get('aa') for i in roles['MPC1L']))
check('negative_residue_shift',any(data[files[0]]['MPC1L'][(i,'CA')]['aa']!=data['9GIX']['MPC1L'].get((i+1,'CA'),{}).get('aa') for i in roles['MPC1L']))
previous={ (r['source'],r['target'],r['metric']):float(r['RMSD_A']) for r in csv.DictReader(open(old/'all_10_comparisons_primary_and_controls.csv')) }
rows=[]; resids=[];transforms=[]
pairs=list(itertools.product(files[:1],files[1:]))+list(itertools.combinations(files[1:],2))
for a,b in pairs:
 for mask,metric in [('73','fixed_union5_interface_CA_RMSD_A'),('62','fixed_union4_interface_CA_RMSD_A'),('198','full_198_two_chain_CA_RMSD_A')]:
  kk=keys(mask);X=positions(a,kk);Y=positions(b,kk);rot,t=fit(X,Y);err=rmsd(X@rot+t,Y);ref=previous[(a,b,metric)]
  rows.append(dict(source=a,target=b,metric=metric,fit_mask=mask,n=len(kk),independent_A=err,previous_A=ref,abs_delta_A=abs(err-ref),pass_1e_5=abs(err-ref)<1e-5))
  transforms.append(dict(source=a,target=b,fit_mask=mask,rotation_json=json.dumps(rot.tolist()),translation_json=json.dumps(t.tolist()),det=float(np.linalg.det(rot))))
  if mask=='73':
   for (role,i),v in zip(kk,np.sum((X@rot+t-Y)**2,axis=1)):resids.append(dict(source=a,target=b,role=role,residue=i,squared_residual_A2=float(v)))
 for role in roles:
  other='MPC2' if role=='MPC1L' else 'MPC1L';kk=[(role,i) for i in roles[role]];kk2=[(other,i) for i in roles[other]]
  X=positions(a,kk);Y=positions(b,kk);rot,t=fit(X,Y)
  for metric,evals,n in [(role+'_independent_chain_CA_RMSD_A',rmsd(X@rot+t,Y),len(kk)),('fit_'+role+'_evaluate_'+other+'_CA_displacement_RMSD_A',rmsd(positions(a,kk2)@rot+t,positions(b,kk2)),len(kk2))]:
   ref=previous[(a,b,metric)];rows.append(dict(source=a,target=b,metric=metric,fit_mask=role+'_full',n=n,independent_A=evals,previous_A=ref,abs_delta_A=abs(evals-ref),pass_1e_5=abs(evals-ref)<1e-5))
  transforms.append(dict(source=a,target=b,fit_mask=role+'_full',rotation_json=json.dumps(rot.tolist()),translation_json=json.dumps(t.tolist()),det=float(np.linalg.det(rot))))
check('70_metric_comparisons',len(rows)==70 and all(v['pass_1e_5'] for v in rows),f'rows={len(rows)} max_delta={max(v["abs_delta_A"] for v in rows):.3e} Å')
prior_res={(v['source'],v['target'],v['role'],int(v['residue'])):float(v['squared_residual_A2']) for v in csv.DictReader(open(old/'primary_residue_squared_residuals.csv'))}
resdelta=[abs(v['squared_residual_A2']-prior_res[(v['source'],v['target'],v['role'],v['residue'])]) for v in resids]
check('730_residue_squared_residuals',len(resids)==730 and max(resdelta)<1e-5,f'max_abs_A2={max(resdelta):.3e}')
check('all_fit_determinants',all(abs(t['det']-1)<1e-10 for t in transforms))
prior_trans={(v['source'],v['target'],v['fit_mask']):v for v in csv.DictReader(open(old/'fit_transforms.csv'))}
tdelta=[]
for v in transforms:
 oldtr=prior_trans[(v['source'],v['target'],v['fit_mask'])];tdelta.append(max(np.max(abs(np.array(json.loads(v['rotation_json']))-np.array(json.loads(oldtr['rotation'])))),np.max(abs(np.array(json.loads(v['translation_json']))-np.array(json.loads(oldtr['translation']))))))
check('50_transforms_match',len(transforms)==50 and max(tdelta)<1e-5,f'max_component_delta={max(tdelta):.3e}')

def writecsv(filename,rows):
 with open(out/filename,'w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
for name,vals in [('independent_70_metrics.csv',rows),('independent_730_residue_residuals.csv',resids),('independent_50_transforms.csv',transforms),('atom_crosswalk.csv',cross),('qc_results.csv',log),('contact_counts.csv',contact_counts)]:writecsv(name,vals)
status='PASS' if all(v['status']=='PASS' for v in log) else 'FAIL'
environment={'sys_executable':sys.executable,'python_version':sys.version,'OS':platform.platform(),'numpy':np.__version__,'scipy':scipy.__version__,'gemmi':gemmi.__version__,'script_sha256':hashfile(__file__),'random_seed_synthetic_only':20261031,'real_analysis_seed':'none','algorithm':'SciPy Rotation.align_vectors (independent of prior SVD)','parser':'Gemmi CIF table (independent of prior Bio.PDB.MMCIF2Dict)','utc_completed':datetime.datetime.now(datetime.timezone.utc).isoformat()}
json.dump({'status':status,'environment':environment,'checks':log,'metrics':len(rows),'pairs':len(pairs),'max_metric_difference_A':max(v['abs_delta_A'] for v in rows),'max_residue_difference_A2':max(resdelta),'max_transform_component_difference':max(tdelta)},open(out/'audit_summary.json','w'),indent=2,ensure_ascii=False)
print('OVERALL',status)
if status!='PASS':sys.exit(2)
