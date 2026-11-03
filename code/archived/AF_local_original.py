import zipfile,io,csv,json,hashlib,sys,platform,math
from pathlib import Path
import numpy as np
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from scipy.spatial.distance import cdist
from MDAnalysis.analysis.helix_analysis import helix_analysis
R=Path('/mnt/data');O=R/'C01_AF_SessionC_2026-11-01'; O.mkdir(exist_ok=True)
A='AF-0000000204012512-model_v1';B='O95563_P0DKB6_Boltz-2_v2-1-1'
af=zipfile.ZipFile(R/'AF-0000000204012512-model_v1.zip');h=zipfile.ZipFile(R/'C01_Research_Execution_Handoff_2026-10-31(1).zip'); ex=zipfile.ZipFile(R/'C01_Execution_Results_2026-10-31.zip')
inputs={A:af.read(A+'.cif')}; inputs.update({s:h.read('01_COORDINATES/'+s+'.cif') for s in [B,'9GIX','9GIV','9GIW','9GIY']})
manifest=list(csv.DictReader(open(R/'C01_AF_SessionA_2026-11-01/input_manifest.csv')))
for s,b in inputs.items():assert hashlib.sha256(b).hexdigest()==next(x['sha256'] for x in manifest if x['name']==s+'.cif'),s
assert hashlib.sha256((R/'C01_Addendum/C01_AF_Exploratory_Addendum_v1.0_FINAL.md').read_bytes()).hexdigest()=='8e7254dba2efd07a06b40b0f5dfc89a113f09352d8fb0b3cd02f79b4026fe62f'
S={}
for s,b in inputs.items():
 d=MMCIF2Dict(io.StringIO(b.decode()));n=len(d['_atom_site.label_atom_id']);alt=d.get('_atom_site.label_alt_id',['.']*n);rev={'A':'MPC2','B':'MPC1L'} if s in (A,B) else {'A':'MPC1L','B':'MPC2'};out={p:{} for p in ('MPC1L','MPC2')}
 for j in range(n):
  if d['_atom_site.group_PDB'][j]!='ATOM':continue
  p=rev.get(d['_atom_site.label_asym_id'][j]);i=d['_atom_site.label_seq_id'][j];atom=d['_atom_site.label_atom_id'][j]
  if not p or not i.isdigit():continue
  i=int(i);xyz=np.array([float(d['_atom_site.Cartn_'+v][j]) for v in 'xyz']);occ=float(d['_atom_site.occupancy'][j]);rank=(occ,alt[j]=='.',alt[j]=='A')
  entry={'xyz':xyz,'atom':atom,'res':d['_atom_site.label_comp_id'][j],'element':d['_atom_site.type_symbol'][j].upper(),'rank':rank}
  aa=out[p].setdefault(i,{})
  if atom not in aa or rank>aa[atom]['rank']:aa[atom]=entry
 S[s]=out

def coordinates(s,p,start,end):return np.array([S[s][p][i]['CA']['xyz'] for i in range(start,end+1)])
def write(name,rows):
 with open(O/name,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
pairs=[('MPC1L',51,'MPC2',66),('MPC2',82,'MPC1L',35),('MPC2',82,'MPC1L',31),('MPC2',90,'MPC1L',76),('MPC2',85,'MPC1L',79)]
local=[]
for s in inputs:
 for pa,ia,pb,ib in pairs:
  aa=S[s][pa][ia];bb=S[s][pb][ib];x=[v for v in aa.values() if v['element'] not in ('H','D')];y=[v for v in bb.values() if v['element'] not in ('H','D')]
  dist=cdist([z['xyz'] for z in x],[z['xyz'] for z in y]);a,b=np.unravel_index(dist.argmin(),dist.shape);dd=float(dist[a,b]);ca=float(np.linalg.norm(aa['CA']['xyz']-bb['CA']['xyz']))
  local.append({'structure':s,'role1':pa,'res1':ia,'role2':pb,'res2':ib,'ca_dist_A':ca,'min_heavy_dist_A':dd,'atom1':x[a]['atom'],'atom2':y[b]['atom'],'contact_lt4':dd<4,'contact_lt5':dd<5})
write('local_geometry_6.csv',local)
# H1 exact original algorithm
h1=[];axes=[]
def normal(v):return v/np.linalg.norm(v)
for s in inputs:
 for p,(lo,hi),hinge in [('MPC1L',(26,48),33),('MPC2',(40,61),53)]:
  xyz=coordinates(s,p,lo,hi);loc=helix_analysis(xyz)['local_axes'];starts=np.arange(lo,hi-2);direction=xyz[-1]-xyz[0];oriented=np.array([normal(a)*np.sign(a@direction) for a in loc]);left=oriented[starts<=hinge-4];right=oriented[starts>=hinge+1]
  def angle(l,r):return float(np.degrees(np.arccos(np.clip(normal(l.mean(axis=0))@normal(r.mean(axis=0)),-1,1))))
  full=angle(left,right);cases=[angle(l,r) for l in (left,left[1:],left[:-1]) for r in (right,right[1:],right[:-1]) if len(l)>=2 and len(r)>=2];maximum=max(abs(t-full) for t in cases)
  h1.append({'structure':s,'role':p,'window_start':lo,'window_end':hi,'hinge':hinge,'n_left':len(left),'n_right':len(right),'bend_angle_deg':full,'max_end_axis_perturbation_deg':maximum,'flag':'H1_NUMERIC_SENSITIVITY_GT5' if maximum>5 else 'NO_GT5_FLAG','left_mean_resultant_length':float(np.linalg.norm(left.mean(axis=0))),'right_mean_resultant_length':float(np.linalg.norm(right.mean(axis=0)))})
  for idx,ax in zip(starts,oriented):axes.append({'structure':s,'role':p,'start_residue':int(idx),'axis_x':float(ax[0]),'axis_y':float(ax[1]),'axis_z':float(ax[2]),'zone':'left' if idx<=hinge-4 else 'right' if idx>=hinge+1 else 'excluded_hinge_adjacent'})
write('H1_angles_stability_6.csv',h1);write('H1_local_axes_6.csv',axes)
def pca_axis(points):
 xyz=points-points.mean(0);w,v=np.linalg.eigh(xyz.T@xyz);axis=v[:,-1];axis*=np.sign(axis@(points[-1]-points[0]));return axis,float(w[-1]/max(w[-2],1e-20))
h23=[]
for s in inputs:
 for p,h2,h3 in [('MPC1L',(54,75),(79,105)),('MPC2',(68,89),(93,121))]:
  x=coordinates(s,p,*h2);y=coordinates(s,p,*h3);u,an1=pca_axis(x);v,an2=pca_axis(y);theta=float(np.degrees(np.arccos(np.clip(u@v,-1,1))))
  h23.append({'structure':s,'role':p,'H2_residues':str(h2),'H3_residues':str(h3),'H2_n':len(x),'H3_n':len(y),'H2_anisotropy':an1,'H3_anisotropy':an2,'directed_deg':theta,'acute_deg':min(theta,180-theta),'bundle_between_state':'NOT QUALIFIED / NOT RUN'})
write('H2_H3_within_state_6.csv',h23)
# Reproduce pre-AF reference results to numerical tolerance
checks=[]
for file,rows,key,fields in [('RESULTS/local_geometry.csv',local,('structure','role1','res1','role2','res2'),('ca_dist_A','min_heavy_dist_A')),('RESULTS/H1_HELANAL_angles_stability.csv',h1,('structure','role'),('bend_angle_deg','max_end_axis_perturbation_deg')),('RESULTS/H2_H3_within_state.csv',h23,('structure','role'),('acute_deg','H2_anisotropy','H3_anisotropy'))]:
 old=list(csv.DictReader(io.StringIO(ex.read(file).decode())));orig={tuple(str(x[c]) for c in key):x for x in old};new={tuple(str(x[c]) for c in key):x for x in rows if x['structure']!=A};assert orig.keys()==new.keys(),file
 for k in orig:
  for field in fields:
   delta=abs(float(orig[k][field])-float(new[k][field]));checks.append({'file':file,'key':str(k),'metric':field,'abs_delta':delta,'pass':delta<1e-8})
assert all(x['pass'] for x in checks)
write('replay_existing_local_QC.csv',checks)
# Independent validation of AF nearest pair using direct brute force distances
assert len([x for x in local if x['structure']==A])==5 and len([x for x in h1 if x['structure']==A])==2 and len([x for x in h23 if x['structure']==A])==2
checks2=[]
for x in local:
 if x['structure']!=A:continue
 aa=S[A][x['role1']][x['res1']];bb=S[A][x['role2']][x['res2']];ds=sorted((float(np.linalg.norm(v['xyz']-w['xyz'])),v['atom'],w['atom']) for v in aa.values() for w in bb.values() if v['element'] not in ('H','D') and w['element'] not in ('H','D'))
 checks2.append({'pair':f"{x['role1']}{x['res1']}-{x['role2']}{x['res2']}",'distance_difference_A':abs(ds[0][0]-x['min_heavy_dist_A']),'atom_agreement':ds[0][1:]==(x['atom1'],x['atom2']),'pass':abs(ds[0][0]-x['min_heavy_dist_A'])<1e-10 and ds[0][1:]==(x['atom1'],x['atom2'])})
write('AF_pair_bruteforce_QC.csv',checks2)
manifest2={'status':'PASS','scope':'Session C only','input_hashes':{s:hashlib.sha256(b).hexdigest() for s,b in inputs.items()},'parent_reference_checks':len(checks),'parent_max_difference':max(x['abs_delta'] for x in checks),'AF_pair_bruteforce_checks':len(checks2),'H1_algorithm':'original CODE/h1.py MDAnalysis helix_analysis','H23_algorithm':'original CODE/run.py PCA eigenvectors','local_algorithm':'original CODE/run.py all observed heavy atoms','software':{'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__,'MDAnalysis':__import__('MDAnalysis').__version__,'biopython':__import__('Bio').__version__},'later_sessions':'NOT RUN'}
(O/'execution_record.json').write_text(json.dumps(manifest2,indent=2))
print('Local AF:')
for r in local:
 if r['structure']==A:print(r)
print('H1 AF:',[x for x in h1 if x['structure']==A]);print('H23 AF:',[x for x in h23 if x['structure']==A]);print('QC',len(checks),manifest2['parent_max_difference'])
