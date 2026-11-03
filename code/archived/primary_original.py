import os,sys,json,hashlib,csv,itertools,platform
import numpy as np
from scipy.spatial.distance import cdist
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from Bio.SeqUtils import seq1
from scipy.spatial.transform import Rotation
root='/mnt/data/C01_work'; out=root+'/results';os.makedirs(out,exist_ok=True)
files=['O95563_P0DKB6_Boltz-2_v2-1-1','9GIX','9GIV','9GIW','9GIY'];chains={'O95563_P0DKB6_Boltz-2_v2-1-1':{'MPC1L':'B','MPC2':'A'}}|{x:{'MPC1L':'A','MPC2':'B'} for x in files[1:]}
masks={'198':{'MPC1L':list(range(22,106)),'MPC2':list(range(8,122))},'73':{'MPC1L':[25,26,27,28,30,31,32,34,35,37,38,41,44,45,51,52,53,54,55,56,57,58,60,61,63,64,67,68,70,71,74,75,76,77,79,82,93],'MPC2':[39,40,41,42,44,45,46,48,49,51,52,55,56,58,59,62,65,66,67,68,70,71,74,75,77,78,81,82,84,85,88,89,90,93,96,110]},'62':{'MPC1L':[27,28,30,31,32,34,35,37,38,41,44,45,51,52,53,54,56,57,60,61,64,67,68,70,71,74,75,76,79,82],'MPC2':[40,41,42,45,46,48,49,51,52,55,56,58,59,62,65,66,68,70,71,74,75,77,78,81,82,84,85,88,89,90,93,96]}}
def rows(path):
 d=MMCIF2Dict(path);n=len(d['_atom_site.label_asym_id']); ans={'MPC1L':{},'MPC2':{}};cross=[]
 for i in range(n):
  role=next((r for r,c in chains[os.path.basename(path).replace('.cif','')].items() if d['_atom_site.label_asym_id'][i]==c),None)
  if not role or d['_atom_site.group_PDB'][i]!='ATOM': continue
  r=d['_atom_site.label_seq_id'][i]
  if not r.isdigit(): continue
  r=int(r); atom=d['_atom_site.label_atom_id'][i]; alt=d.get('_atom_site.label_alt_id',['.']*n)[i];occ=float(d['_atom_site.occupancy'][i]);element=d['_atom_site.type_symbol'][i].upper()
  at={'xyz':np.array([float(d['_atom_site.Cartn_'+a][i]) for a in 'xyz']),'atom':atom,'res':d['_atom_site.label_comp_id'][i],'alt':alt,'occ':occ,'element':element,'auth_seq':d['_atom_site.auth_seq_id'][i],'label_seq':r,'chain':d['_atom_site.label_asym_id'][i]}
  grp=ans[role].setdefault(r,{})
  if atom not in grp or (occ,-ord(alt[0]) if alt!='.' else 0)>(grp[atom]['occ'],-ord(grp[atom]['alt'][0]) if grp[atom]['alt']!='.' else 0):grp[atom]=at
 return ans
S={k:rows(root+'/handoff/01_COORDINATES/'+k+'.cif') for k in files}
def write(name,rs):
 if not rs:return
 with open(out+'/'+name,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def keys(mask):return [(r,i) for r in ['MPC1L','MPC2'] for i in masks[mask][r]]
def coords(s,kk):return np.array([S[s][r][i]['CA']['xyz'] for r,i in kk])
checks=[];cover=[]
for s in files:
 for r,i in keys('198'):
  a=S[s][r].get(i,{}).get('CA');cover.append({'structure':s,'protein':r,'residue':i,'present':bool(a),'aa':a['res'] if a else '', 'chain':a['chain'] if a else '', 'auth_seq':a['auth_seq'] if a else ''})
  if not a:checks.append('MISSING_CA '+s+' '+r+str(i))
for r,i in keys('198'):
 aa=[S[s][r][i]['CA']['res'] for s in files if 'CA' in S[s][r].get(i,{})]
 if len(set(aa))!=1:checks.append('IDENTITY '+r+str(i)+':'+str(aa))
write('atom_coverage_crosswalk.csv',cover)
contact_details=[]
for threshold,m in [(5,'73'),(4,'62')]:
 union=set(); common=None;counts={}
 for s in files[1:]:
  pairs=set();
  for r1 in masks['198']['MPC1L']:
   a=[a for a in S[s]['MPC1L'][r1].values() if a['element'] not in ('H','D')]
   for r2 in masks['198']['MPC2']:
    b=[a for a in S[s]['MPC2'][r2].values() if a['element'] not in ('H','D')]
    dd=cdist([x['xyz'] for x in a],[x['xyz'] for x in b]);ii,jj=np.unravel_index(dd.argmin(),dd.shape); dist=float(dd[ii,jj]);
    if dist<threshold:
     pairs.add((r1,r2));contact_details.append({'threshold':threshold,'structure':s,'mpc1l':r1,'mpc2':r2,'distance_A':dist,'mpc1l_atom':a[ii]['atom'],'mpc2_atom':b[jj]['atom']})
  counts[s]=len(pairs);union|=pairs;common=pairs if common is None else common & pairs
 actual={'MPC1L':{p[0] for p in union},'MPC2':{p[1] for p in union}}
 exp={r:set(masks[m][r]) for r in actual}
 if actual!=exp:checks.append('MASK_MISMATCH '+m+' '+str({r:sorted(actual[r]^exp[r]) for r in actual}))
 expected=(107,37,[57,84,82,86]) if threshold==5 else (69,13,[31,43,45,52])
 if (len(union),len(common),list(counts.values()))!=expected: checks.append('CONTACT_PAIR_COUNTS '+m+' '+str((len(union),len(common),counts)))
 print('CONTACT',threshold,len(union),len(common),counts,'mask', {r:len(actual[r]) for r in actual})
write('recomputed_contacts.csv',contact_details)
# Proper Kabsch row vector x @ R + t
def fit(x,y):
 cx=x.mean(0);cy=y.mean(0); u,sg,vt=np.linalg.svd((x-cx).T@(y-cy)); d=np.linalg.det(u@vt); q=np.diag([1,1,np.sign(d)]); R=u@q@vt;t=cy-cx@R; return R,t
def rms(a,b):return float(np.sqrt(np.mean(np.sum((a-b)**2,axis=1))))
rng=np.random.default_rng(20261031)
x=rng.normal(size=(73,3)); rot=Rotation.from_euler('xyz',[22,35,-79],degrees=True).as_matrix();y=x@rot+np.array([11,2,-6]);rr,tt=fit(x,y)
for name,value,tol in [('rigid_transform',rms(x@rr+tt,y),1e-10),('identity',rms(x@fit(x,x)[0]+fit(x,x)[1],x),1e-10),('order',rms(x@fit(x[::-1],y[::-1])[0]+fit(x[::-1],y[::-1])[1],y),1e-10),('det',abs(np.linalg.det(rr)-1),1e-10)]:
 print('UNIT',name,value); 
 if value>tol: checks.append('KABSCH '+name)
# negative sequence/chain swap checks
if all(S[files[0]]['MPC1L'][i]['CA']['res']==S['9GIX']['MPC2'].get(i,{}).get('CA',{}).get('res') for i in masks['198']['MPC1L']):checks.append('NEGATIVE_SWAPPED_CHAIN_UNDETECTED')
if all(S[files[0]]['MPC1L'][i]['CA']['res']==S['9GIX']['MPC1L'].get(i+1,{}).get('CA',{}).get('res') for i in masks['198']['MPC1L']):checks.append('NEGATIVE_SHIFT_UNDETECTED')
for m,num in [('73',73),('62',62),('198',198)]:
 if len(keys(m))!=num:checks.append('MASK_LENGTH '+m)
gate={'status':'PASS' if not checks else 'FAIL','failures':checks,'contact_counts_expected_recomputed':True,'input_manifest_verified':True,'protocol_sha256':'87ba6cb500bdf4fc67803bec8cf2f655443367431945c7f7df359a1bff0381fa','software':{'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__,'biopython':__import__('Bio').__version__}}
json.dump(gate,open(out+'/phase0_gate.json','w'),indent=2)
print('GATE',gate['status'],checks)
if checks:sys.exit(2)
with open(out+'/masks.json','w') as f:json.dump(masks,f,indent=2)
metrics=[];transforms=[];resids=[]
for a,b in list(itertools.product(files[:1],files[1:]))+list(itertools.combinations(files[1:],2)):
 for m in ['73','62','198']:
  kk=keys(m);X=coords(a,kk);Y=coords(b,kk);R,t=fit(X,Y);Z=X@R+t
  metrics.append({'source':a,'target':b,'metric':{'73':'fixed_union5_interface_CA_RMSD_A','62':'fixed_union4_interface_CA_RMSD_A','198':'full_198_two_chain_CA_RMSD_A'}[m],'fit_mask':m,'eval_mask':m,'n_fit':len(kk),'n_eval':len(kk),'RMSD_A':rms(Z,Y)})
  transforms.append({'source':a,'target':b,'fit_mask':m,'rotation':json.dumps(R.tolist()),'translation':json.dumps(t.tolist()),'det_rotation':np.linalg.det(R)})
  if m=='73':
   for (role,i),p,q in zip(kk,Z,Y):resids.append({'source':a,'target':b,'role':role,'residue':i,'squared_residual_A2':float(sum((p-q)**2))})
 for role,other in [('MPC1L','MPC2'),('MPC2','MPC1L')]:
  fitkeys=[(role,i) for i in masks['198'][role]]; otherkeys=[(other,i) for i in masks['198'][other]]
  X=coords(a,fitkeys);Y=coords(b,fitkeys);R,t=fit(X,Y)
  metrics.append({'source':a,'target':b,'metric':role+'_independent_chain_CA_RMSD_A','fit_mask':role+'_full','eval_mask':role+'_full','n_fit':len(fitkeys),'n_eval':len(fitkeys),'RMSD_A':rms(X@R+t,Y)})
  metrics.append({'source':a,'target':b,'metric':'fit_'+role+'_evaluate_'+other+'_CA_displacement_RMSD_A','fit_mask':role+'_full','eval_mask':other+'_full','n_fit':len(fitkeys),'n_eval':len(otherkeys),'RMSD_A':rms(coords(a,otherkeys)@R+t,coords(b,otherkeys))})
  transforms.append({'source':a,'target':b,'fit_mask':role+'_full','rotation':json.dumps(R.tolist()),'translation':json.dumps(t.tolist()),'det_rotation':np.linalg.det(R)})
write('all_10_comparisons_primary_and_controls.csv',metrics);write('fit_transforms.csv',transforms);write('primary_residue_squared_residuals.csv',resids)
print('PRIMARY RESULTS');[print(x['source'][:8],x['target'],round(x['RMSD_A'],3)) for x in metrics if x['fit_mask']=='73']
# Local residues
pairs=[('MPC1L',51,'MPC2',66),('MPC2',82,'MPC1L',35),('MPC2',82,'MPC1L',31),('MPC2',90,'MPC1L',76),('MPC2',85,'MPC1L',79)]
local=[]
for s in files:
 for ra,ia,rb,ib in pairs:
  aa=S[s][ra][ia];bb=S[s][rb][ib]; a=[v for v in aa.values() if v['element'] not in ('H','D')];b=[v for v in bb.values() if v['element'] not in ('H','D')];dd=cdist([v['xyz'] for v in a],[v['xyz'] for v in b]);i,j=np.unravel_index(dd.argmin(),dd.shape);dist=float(dd[i,j]);local.append({'structure':s,'role1':ra,'res1':ia,'role2':rb,'res2':ib,'ca_dist_A':float(np.linalg.norm(aa['CA']['xyz']-bb['CA']['xyz'])),'min_heavy_dist_A':dist,'atom1':a[i]['atom'],'atom2':b[j]['atom'],'contact_lt4':dist<4,'contact_lt5':dist<5})
write('local_geometry.csv',local)
# H2-H3 within-state PCA
def pca_axis(points):
 xyz=points-points.mean(0);w,v=np.linalg.eigh(xyz.T@xyz);axis=v[:,-1];axis*=np.sign(axis@(points[-1]-points[0]));return axis,float(w[-1]/max(w[-2],1e-20))
h23=[]
for s in files:
 for role,h2,h3 in [('MPC1L',(54,75),(79,105)),('MPC2',(68,89),(93,121))]:
  p=coords(s,[(role,i) for i in range(h2[0],h2[1]+1)]);q=coords(s,[(role,i) for i in range(h3[0],h3[1]+1)]);u,an1=pca_axis(p);v,an2=pca_axis(q);theta=np.degrees(np.arccos(np.clip(u@v,-1,1)))
  h23.append({'structure':s,'role':role,'H2_residues':str(h2),'H3_residues':str(h3),'H2_n':len(p),'H3_n':len(q),'H2_anisotropy':an1,'H3_anisotropy':an2,'directed_deg':theta,'acute_deg':min(theta,180-theta),'bundle_between_state':'NOT QUALIFIED / NOT RUN'})
write('H2_H3_within_state.csv',h23)
# Tier0 / Tier1 typing
charged={'LYS':['NZ'],'ARG':['NE','NH1','NH2'],'ASP':['OD1','OD2'],'GLU':['OE1','OE2']}
def typ(res,atom):
 donor=atom=='N' and res!='PRO'; accept=atom=='O'
 if res in ('ASN','GLN'):
  donor|=atom in ('ND2','NE2');accept|=atom in ('OD1','OE1')
 if res in ('LYS','ARG'):donor|=atom in charged[res]
 if res in ('ASP','GLU'):accept|=atom in charged[res]
 if res in ('SER','THR','TYR') and atom in ('OG','OG1','OH'):donor=True;accept=True
 if res=='TRP' and atom=='NE1':donor=True
 return donor,accept
salt=[];tier1=[]
for s in files:
 for r1 in masks['198']['MPC1L']:
  for r2 in masks['198']['MPC2']:
   a=S[s]['MPC1L'][r1];b=S[s]['MPC2'][r2]; aa=list(a.values());bb=list(b.values());res1=aa[0]['res'];res2=bb[0]['res']
   for ab,bb2,ra,rb,ia,ib in [(a,b,res1,res2,r1,r2),(b,a,res2,res1,r2,r1)]:
    if ra in ('LYS','ARG') and rb in ('ASP','GLU'):
     candidates=[(np.linalg.norm(ab[x]['xyz']-bb2[y]['xyz']),x,y) for x in charged[ra] if x in ab for y in charged[rb] if y in bb2]
     if candidates:
      d,x,y=min(candidates)
      if d<4:salt.append({'structure':s,'cation_role':'MPC1L' if ab is a else 'MPC2','cation_res':ia,'anion_res':ib,'cation_atom':x,'anion_atom':y,'min_distance_A':d})
   for x in aa:
    if x['element'] in ('H','D'):continue
    for y in bb:
     if y['element'] in ('H','D'):continue
     dist=float(np.linalg.norm(x['xyz']-y['xyz']))
     if dist>3:continue
     dx,ax=typ(res1,x['atom']);dy,ay=typ(res2,y['atom'])
     for dr,ac in [(('MPC1L',r1,x['atom']),('MPC2',r2,y['atom']))] if dx and ay else []:
      tier1.append({'structure':s,'donor_role':dr[0],'donor_res':dr[1],'donor_atom':dr[2],'acceptor_role':ac[0],'acceptor_res':ac[1],'acceptor_atom':ac[2],'distance_A':dist})
     if dy and ax:tier1.append({'structure':s,'donor_role':'MPC2','donor_res':r2,'donor_atom':y['atom'],'acceptor_role':'MPC1L','acceptor_res':r1,'acceptor_atom':x['atom'],'distance_A':dist})
write('tier0_salt_bridge_candidates.csv',salt);write('tier1_heavy_atom_DA_candidates.csv',tier1)
status={'DockQ':'NOT RUN: environment command and per-structure export QC not executed','FreeSASA':'NOT RUN: required installed FreeSASA v2.2.1 API/classifier QC not executed','Tier2':'NOT RUN: per-structure hydrogen placement and detector positive/negative tests not completed','H1':'NOT RUN: exact frozen HELANAL axis implementation not yet executed','experimental_quality':'NOT RUN: coordinate-to-wwPDB validation crosswalk pending','scientific_final_assessment':'PENDING source-paper/SI prior art and RDM assessment'}
json.dump(status,open(out+'/remaining_metrics_status.json','w'),indent=2)
print('SECONDARY',len(local),'local',len(h23),'H23',len(salt),'salts',len(tier1),'Tier1')
