"""Replay deterministic geometry and inspect saved engine outputs.
DockQ/FreeSASA/OpenMM engines are NOT invoked by this program.
"""
from cif_geometry import *
import argparse,itertools,re,math
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);out=p.parse_args().out;out.mkdir(parents=True,exist_ok=True)
S=load_all();results=[]
def check(name,delta,tol):
 yes=float(delta)<=tol;results.append({'check':name,'absolute_difference':float(delta),'tolerance':tol,'pass':yes})
 if not yes:raise AssertionError((name,delta,tol))
def angle(u,v):return float(np.degrees(np.arccos(np.clip(np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v),-1,1))))
def ca(name,p,start,end):return np.array([S[name][p][i]['CA']['xyz'] for i in range(start,end+1)])
# H1 local axis is the normal to adjacent second-difference vectors of four CAs.
# Mathematical reimplementation; no MDAnalysis package source is bundled here.
# Reference implementation: MDAnalysis 2.9.0 helix_analysis, local_axes definition.
for r in read_csv(ROOT/'data/results/H1_angles_stability_6.csv'):
 n,p=r['structure'],r['role'];lo,hi,hinge=[int(r[k]) for k in ('window_start','window_end','hinge')];xyz=ca(n,p,lo,hi)
 axes=[]
 for j in range(len(xyz)-3):
  q=xyz[j:j+4];u=(q[1]-q[0])-(q[2]-q[1]);v=(q[2]-q[1])-(q[3]-q[2]);axis=np.cross(u,v);axis/=np.linalg.norm(axis)
  if np.dot(axis,xyz[-1]-xyz[0])<0:axis=-axis
  axes.append(axis)
 starts=list(range(lo,hi-2));left=np.array([a for a,s in zip(axes,starts) if s<=hinge-4]);right=np.array([a for a,s in zip(axes,starts) if s>=hinge+1]);full=angle(left.mean(0),right.mean(0))
 sens=max(abs(angle(l.mean(0),q.mean(0))-full) for l in [left,left[1:],left[:-1]] for q in [right,right[1:],right[:-1]] if len(l)>=2 and len(q)>=2)
 check('H1_'+n+'_'+p,abs(full-float(r['bend_angle_deg'])),1e-8);check('H1_sensitivity_'+n+'_'+p,abs(sens-float(r['max_end_axis_perturbation_deg'])),1e-8)
 check('H1_flag_'+n+'_'+p,int((sens>5)!=(r['flag']=='H1_NUMERIC_SENSITIVITY_GT5')),0)
for r in read_csv(ROOT/'data/results/H2_H3_within_state_6.csv'):
 axes=[]
 for col in ['H2','H3']:
  lo,hi=[int(i) for i in re.findall(r'\d+',r[col+'_residues'])];q=ca(r['structure'],r['role'],lo,hi);d=q-q.mean(0);w,v=np.linalg.eigh(d.T@d);ax=v[:,-1]
  if np.dot(ax,q[-1]-q[0])<0:ax=-ax
  axes.append(ax);an=float(w[-1]/w[-2]);check('H23_anisotropy_'+r['structure']+r['role']+col,abs(an-float(r[col+'_anisotropy'])),1e-8)
 val=angle(*axes);check('H23_directed_'+r['structure']+r['role'],abs(val-float(r['directed_deg'])),1e-8);check('H23_acute_'+r['structure']+r['role'],abs(min(val,180-val)-float(r['acute_deg'])),1e-8)
for r in read_csv(ROOT/'data/results/local_geometry_6.csv'):
 a=S[r['structure']][r['role1']][int(r['res1'])];b=S[r['structure']][r['role2']][int(r['res2'])]
 ca_d=np.linalg.norm(a['CA']['xyz']-b['CA']['xyz']);d=min(np.linalg.norm(x['xyz']-y['xyz']) for x in a.values() for y in b.values() if x['type_symbol'] not in ['H','D'] and y['type_symbol'] not in ['H','D'])
 check('local_CA_'+str(len(results)),abs(ca_d-float(r['ca_dist_A'])),1e-8);check('local_heavy_'+str(len(results)),abs(d-float(r['min_heavy_dist_A'])),1e-8)
def pdb_atoms(path):
 a={}
 for line in path.read_text().splitlines():
  if line[:6].strip() not in ['ATOM','HETATM']:continue
  key=(line[21],int(line[22:26]),line[12:16].strip());a[key]={'res':line[17:20].strip(),'xyz':np.array([float(line[i:i+8]) for i in [30,38,46]]),'element':line[76:78].strip()}
 return a
# Interactions were screened on ALL observed atoms of normalized two-chain PDBs,
# not just the 198-residue CA mask. Match IDs exactly; allow float32 reader rounding.
def typed(res,a):
 donor=(a=='N' and res!='PRO');accept=a=='O'
 donor|=(res=='ASN' and a=='ND2') or (res=='GLN' and a=='NE2') or (res=='LYS' and a=='NZ') or (res=='ARG' and a in ['NE','NH1','NH2']) or (res=='TRP' and a=='NE1')
 accept|=(res=='ASN' and a=='OD1') or (res=='GLN' and a=='OE1') or (res=='ASP' and a in ['OD1','OD2']) or (res=='GLU' and a in ['OE1','OE2'])
 if (res,a) in [('SER','OG'),('THR','OG1'),('TYR','OH')]:donor=accept=True
 return donor,accept
counts=[]
for name in NAMES:
 short='AF' if name==AF else 'Boltz' if name==BOLTZ else name;atoms=pdb_atoms(ROOT/'data/frozen/normalized'/f'{name}_normalized_AB.pdb');left=[(k,v) for k,v in atoms.items() if k[0]=='A' and v['element'] not in ['H','D']];right=[(k,v) for k,v in atoms.items() if k[0]=='B' and v['element'] not in ['H','D']];salt={};tier1={}
 for k,a in left:
  for l,b in right:
   d=float(np.linalg.norm(a['xyz']-b['xyz']))
   if d>4.:continue
   for (dk,da),(ak,aa) in [((k,a),(l,b)),((l,b),(k,a))]:
    if (da['res']=='LYS' and dk[2]=='NZ' or da['res']=='ARG' and dk[2] in ['NE','NH1','NH2']) and (aa['res']=='ASP' and ak[2] in ['OD1','OD2'] or aa['res']=='GLU' and ak[2] in ['OE1','OE2']) and d<4.:
     pair=(dk[0],dk[1],ak[0],ak[1]);rec=(dk+ak,d)
     if pair not in salt or d<salt[pair][1]:salt[pair]=rec
    if d<=3. and typed(da['res'],dk[2])[0] and typed(aa['res'],ak[2])[1]:tier1[dk+ak]=d
 saved0=read_csv(ROOT/'data/results'/('tier0_AF.csv' if name==AF else 'tier0_primary.csv'));saved0=[r for r in saved0 if r['structure']==short]
 saved1=read_csv(ROOT/'data/results'/('tier1_AF.csv' if name==AF else 'tier1_primary.csv'));saved1=[r for r in saved1 if r['structure']==short]
 s0={(r['cation_chain'],int(r['cation_res']),r['cation_atom'],r['anion_chain'],int(r['anion_res']),r['anion_atom']):float(r['distance_A']) for r in saved0}
 s1={(r['donor_chain'],int(r['donor_res']),r['donor_atom'],r['acceptor_chain'],int(r['acceptor_res']),r['acceptor_atom']):float(r['distance_A']) for r in saved1}
 r0=dict(salt.values());check('Tier0_id_'+short,int(s0.keys()!=r0.keys()),0);check('Tier1_id_'+short,int(s1.keys()!=tier1.keys()),0)
 for kind,x,y in [('Tier0',s0,r0),('Tier1',s1,tier1)]:
  for key in x:check(kind+'_distance_'+short+str(key),abs(x[key]-y[key]),2e-5)
 counts.append({'structure':short,'tier0_candidates':len(s0),'tier1_atom_pairs':len(s1),'normalization':'A=MPC1L; B=MPC2; all observed atoms'})
# Check accepted historical Tier2 snapshots, without regenerating hydrogens.
for r in read_csv(ROOT/'data/results/tier2_primary.csv')+read_csv(ROOT/'data/results/tier2_AF.csv'):
 n=r['structure'];a=pdb_atoms(ROOT/'data/frozen/hydrogenated'/f'{n}_hydrogenated_DERIVED.pdb');dk=(r['donor_chain'],int(r['donor_res']),r['donor_atom']);hk=(r['donor_chain'],int(r['donor_res']),r['hydrogen']);ak=(r['acceptor_chain'],int(r['acceptor_res']),r['acceptor_atom']);D,H,A=[a[k]['xyz'] for k in [dk,hk,ak]];d=float(np.linalg.norm(D-A));v=angle(D-H,A-H)
 check('Tier2_saved_DA_'+n+str(dk),abs(d-float(r['da_distance_A'])),0.002);check('Tier2_saved_angle_'+n+str(dk),abs(v-float(r['dha_angle_deg'])),0.15)
# Saved FreeSASA arithmetic (not a rerun of Lee-Richards surface calculation).
for n in ['freesasa_primary.csv','freesasa_AF.csv']:
 for r in read_csv(ROOT/'data/results'/n):
  k=['SASA_A_A2','SASA_B_A2','SASA_AB_A2','delta_SASA_A2'] if n.startswith('freesasa_primary') else ['SASA_MPC1L_A2','SASA_MPC2_A2','SASA_complex_A2','delta_SASA_A2']
  a,b,c,d=[float(r[i]) for i in k];check('SASA_arithmetic_'+r['structure'],abs(a+b-c-d),1e-8);check('BSA_half_'+r['structure'],abs(d/2-float(r['BSA_half_A2'])),1e-8)
# Compare all parsed DockQ scalars to archived numerical stdout excerpts.
for fname in ['dockq_primary.csv','dockq_AF.csv']:
 for r in read_csv(ROOT/'data/results'/fname):
  model=AF if fname.endswith('_AF.csv') else r['model'];target=r['reference'] if fname.endswith('_AF.csv') else r['native'];stem='DockQ_AF_vs_'+target+'.txt' if model==AF else 'DockQ_'+model+'_vs_'+target+'.txt';s=(ROOT/'verification/historical/dockq'/stem).read_text()
  for f,k in [('DockQ','dockq' if model==AF else 'DockQ'),('iRMSD','irmsd' if model==AF else 'iRMSD'),('LRMSD','lrmsd' if model==AF else 'LRMSD'),('fnat','fnat')]:
   v=float(re.search(r'^\s*'+f+r':\s*([0-9.]+)',s,re.M).group(1));check('DockQ_stdout_'+stem+f,abs(v-float(r[k])),0)
write_csv(out/'auxiliary_checks.csv',results);write_csv(out/'interaction_replay_counts.csv',counts)
s={'status':'PASS','checks':len(results),'recomputed':['H1 local-axis proxies and flags','H2/H3 within-structure proxies','30 local residue pairs','Tier0/1 all-observed normalized atom screens'],'saved_output_checks':['Tier2 five triplets against rounded saved hydrogenated coordinates','FreeSASA arithmetic only','15 DockQ scalar/stdout consistency'],'not_rerun':['DockQ engine','FreeSASA engine','OpenMM/PDBFixer hydrogen placement','cryo-EM map refinement'],'Tier2_NOT_RUN':['9GIX','9GIW','9GIY']}
(out/'auxiliary_summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s))
