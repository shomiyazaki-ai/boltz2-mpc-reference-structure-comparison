import csv, json, hashlib, platform, sys, math
from pathlib import Path
from Bio.PDB import PDBParser
import numpy as np
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parents[1]; IN=ROOT/'input/s2/SESSION2'; OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
NAMES={'Boltz':'O95563_P0DKB6_Boltz-2_v2-1-1','9GIX':'9GIX','9GIV':'9GIV','9GIW':'9GIW','9GIY':'9GIY'}
CATIONS={'LYS':('NZ',),'ARG':('NE','NH1','NH2')}; ANIONS={'ASP':('OD1','OD2'),'GLU':('OE1','OE2')}
def roles(res, name):
 r=res
 donor=name=='N' and r!='PRO'; accept=name=='O'
 if r=='ASN':donor|=name=='ND2';accept|=name=='OD1'
 if r=='GLN':donor|=name=='NE2';accept|=name=='OE1'
 if r in CATIONS:donor|=name in CATIONS[r]
 if r in ANIONS:accept|=name in ANIONS[r]
 if r=='SER' and name=='OG' or r=='THR' and name=='OG1' or r=='TYR' and name=='OH':donor=accept=True
 if r=='TRP' and name=='NE1':donor=True
 return donor,accept
# independent synthetic controls (expected by construction)
assert roles('PRO','N')==(False,False)
assert roles('GLU','OE1')==(False,True)
assert roles('TRP','NE1')==(True,False)
assert roles('SER','OG')==(True,True)
assert roles('ALA','N')==(True,False)
assert math.dist((0,0,0),(4,0,0))==4.0 and not math.dist((0,0,0),(4,0,0))<4
assert math.dist((0,0,0),(3,0,0))<=3 and not math.dist((0,0,0),(3.001,0,0))<=3
headers0=['structure','cation_chain','cation_res','cation_resname','cation_atom','anion_chain','anion_res','anion_resname','anion_atom','distance_A','source']
headers1=['structure','donor_chain','donor_res','donor_resname','donor_atom','acceptor_chain','acceptor_res','acceptor_resname','acceptor_atom','distance_A','source']
salts=[]; hbs=[]; summary=[]; exclusions=[]; provenance=[]
for label,base in NAMES.items():
 p=IN/(base+'_normalized_AB.pdb'); data=p.read_bytes(); digest=hashlib.sha256(data).hexdigest()
 structure=PDBParser(QUIET=True).get_structure('s',str(p)); model=next(structure.get_models())
 chains={c.id:c for c in model}; assert set(chains)=={'A','B'},(label,list(chains))
 atoms={}
 for chain in ('A','B'):
  arr=[]
  for residue in chains[chain]:
   if residue.id[0]!=' ': continue
   for atom in residue:
    if atom.element.upper() in ('H','D'):continue
    key=(chain,residue.id[1],residue.resname,atom.name)
    arr.append({'chain':chain,'resid':residue.id[1],'res':residue.resname,'atom':atom.name,'coord':np.asarray(atom.coord,dtype=float),'element':atom.element.upper(),'occupancy':atom.occupancy,'altloc':atom.altloc})
  atoms[chain]=arr
 A,B=atoms['A'],atoms['B']; assert A and B
 tree=cKDTree(np.array([a['coord'] for a in B])); candidate=tree.query_ball_point(np.array([a['coord'] for a in A]),r=4.000001)
 local0={}; local1={}
 for i,js in enumerate(candidate):
  x=A[i]
  for j in js:
   y=B[j]; d=float(np.linalg.norm(x['coord']-y['coord']))
   if d<4:
    for c,a in [(x,y),(y,x)]:
     if c['res'] in CATIONS and c['atom'] in CATIONS[c['res']] and a['res'] in ANIONS and a['atom'] in ANIONS[a['res']]:
      key=(c['chain'],c['resid'],a['chain'],a['resid']); record=dict(zip(headers0,[label,c['chain'],c['resid'],c['res'],c['atom'],a['chain'],a['resid'],a['res'],a['atom'],d,'original normalized PDB']))
      if key not in local0 or d<local0[key]['distance_A']:local0[key]=record
   if d<=3.0:
    dx,ax=roles(x['res'],x['atom']);dy,ay=roles(y['res'],y['atom'])
    for donor,accept,eligible in [(x,y,dx and ay),(y,x,dy and ax)]:
     if not eligible:continue
     key=(donor['chain'],donor['resid'],donor['atom'],accept['chain'],accept['resid'],accept['atom'])
     record=dict(zip(headers1,[label,donor['chain'],donor['resid'],donor['res'],donor['atom'],accept['chain'],accept['resid'],accept['res'],accept['atom'],d,'original normalized PDB']))
     if key in local1:raise AssertionError('duplicate oriented site '+str(key))
     local1[key]=record
 salts.extend(local0.values());hbs.extend(local1.values())
 pairs1={(r['donor_chain'],r['donor_res'],r['acceptor_chain'],r['acceptor_res']) if r['donor_chain']=='A' else (r['acceptor_chain'],r['acceptor_res'],r['donor_chain'],r['donor_res']) for r in local1.values()}
 summary.append({'structure':label,'pdb_sha256':digest,'heavy_A':len(A),'heavy_B':len(B),'heavy_total':len(A)+len(B),'tier0_residue_pairs':len(local0),'tier1_oriented_atom_pairs':len(local1),'tier1_unique_residue_pairs':len(pairs1),'tier2':'NOT RUN: OpenMM 8.2/PDBFixer 1.12 unavailable in this environment'})
 provenance.append({'name':p.name,'sha256':digest})
 print(label,'atoms',len(A)+len(B),'Tier0',len(local0),'Tier1',len(local1),'unique',len(pairs1))
def save(file,rows,fields):
 with (OUT/file).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(sorted(rows,key=lambda r:tuple(str(v) for v in r.values())))
save('tier0_all_observed.csv',salts,headers0);save('tier1_all_observed.csv',hbs,headers1);save('tier01_summary.csv',summary,list(summary[0]));
manifest={'timestamp_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'python':sys.version,'python_path':sys.executable,'biopython':__import__('Bio').__version__,'scipy':__import__('scipy').__version__,'platform':platform.platform(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'inputs':provenance,'tests':'synthetic boundaries and donor/acceptor typing PASS','scope':'all observed heavy atoms in two-chain normalized PDBs; not just common 198 residues','status':'PASS'}
(OUT/'tier01_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
