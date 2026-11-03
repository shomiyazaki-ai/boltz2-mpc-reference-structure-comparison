"""C01 Tier2 fixed protocol v1.0. Execute only in qualified local OpenMM 8.2 + PDBFixer 1.12.0 environment.
Read-only originals; no minimization; all outputs under local_results. Fail closed per structure.
"""
import json,csv,hashlib,sys,platform,traceback,math
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1]
IN=BASE/'input/s2/SESSION2'; OUT=BASE/'local_results';OUT.mkdir(exist_ok=True)
NAMES={'AF':'AF-0000000204012512-model_v1'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def angle(d,h,a):
 v=np.asarray(d)-np.asarray(h);w=np.asarray(a)-np.asarray(h)
 return float(np.degrees(np.arccos(np.clip(np.dot(v,w)/(np.linalg.norm(v)*np.linalg.norm(w)),-1,1))))
def positive(d,h,a):return np.linalg.norm(np.asarray(d)-np.asarray(a))<=3.0 and angle(d,h,a)>=150.0
# Independent positive / negative / boundary tests must run before any C01 structure
D=(0.,0.,0.);H=(1.,0.,0.)
assert positive(D,H,(2.8,0.,0.))
assert positive(D,H,(3.,0.,0.))
assert not positive(D,H,(3.001,0.,0.))
assert not positive(D,H,(1.,1.,0.))
assert not positive(D,H,(2.,1.5,0.))
print('Synthetic Tier2 HB distance/angle tests PASS')
import openmm
from openmm import unit, NonbondedForce
from openmm.app import PDBFile, Modeller, ForceField, NoCutoff
from pdbfixer import PDBFixer
if not openmm.version.version.startswith('8.2'):raise RuntimeError('OpenMM MUST be 8.2')
# pdbfixer version metadata can differ by installation. Capture install distribution version.
from importlib.metadata import version
pv=version('pdbfixer')
if not pv.startswith('1.12'):raise RuntimeError('PDBFixer MUST be 1.12.0, got '+pv)
ff=ForceField('amber14-all.xml')
records=[];triplets=[];inputs=[]
def map_heavy(t,p):
 result={}
 for atom in t.atoms():
  if atom.element is not None and atom.element.symbol=='H':continue
  key=(atom.residue.chain.id,atom.residue.id,atom.residue.name,atom.name)
  if key in result:raise ValueError('duplicate heavy atom identity '+str(key))
  result[key]=np.array(p[atom.index].value_in_unit(unit.angstrom),dtype=float)
 return result
for label,base in NAMES.items():
 path=IN/(base+'_normalized_AB.pdb'); record={'structure':label,'input':path.name,'input_sha256':sha(path),'status':'NOT RUN'}
 try:
  fix=PDBFixer(filename=str(path)); pre=map_heavy(fix.topology,fix.positions)
  fix.findMissingResidues();record['detected_missing_residues']=str(dict(fix.missingResidues));fix.missingResidues={}
  fix.findNonstandardResidues()
  if fix.nonstandardResidues:raise ValueError('nonstandard residue replacement forbidden')
  fix.findMissingAtoms()
  missing=[(r.chain.id,r.id,r.name,[a.name for a in atoms]) for r,atoms in fix.missingAtoms.items()]
  terminal_missing=[(r.chain.id,r.id,r.name,list(atoms)) for r,atoms in fix.missingTerminals.items()]
  missing += terminal_missing
  record['missing_atoms_and_terminals']=missing
  if any(set(x[3])!={'OXT'} for x in missing):raise ValueError('missing atom not OXT; reject completion')
  # Validate OXT additions at actual chain endpoints
  terminal={(c.id, list(c.residues())[-1].id) for c in fix.topology.chains()}
  if any((x[0],x[1]) not in terminal for x in missing):raise ValueError('OXT not at chain endpoint')
  fix.addMissingAtoms()
  repaired=map_heavy(fix.topology,fix.positions)
  added=set(repaired)-set(pre)
  if added!={(x[0],x[1],x[2],'OXT') for x in missing}:raise ValueError('added unexpected heavy atoms')
  if set(pre)-set(repaired):raise ValueError('lost original heavy atoms')
  repair_shift=max(np.linalg.norm(pre[k]-repaired[k]) for k in pre)
  if repair_shift>1e-5:raise ValueError('repair moved original heavy atoms')
  mod=Modeller(fix.topology,fix.positions)
  variants=['HIE' if r.name=='HIS' else None for r in mod.topology.residues()]
  mod.addHydrogens(ff,pH=7.0,variants=variants)
  after=map_heavy(mod.topology,mod.positions)
  if set(after)!=set(repaired):raise ValueError('hydrogenation changed heavy keys')
  shift=max(np.linalg.norm(pre[k]-after[k]) for k in pre)
  if shift>1e-5:raise ValueError('hydrogenation moved original heavy atoms >1e-5A')
  system=ff.createSystem(mod.topology,nonbondedMethod=NoCutoff)
  nb=next(x for x in system.getForces() if isinstance(x,NonbondedForce))
  net=sum(float(nb.getParticleParameters(a.index)[0].value_in_unit(unit.elementary_charge)) for a in mod.topology.atoms())
  hcount=sum(a.element is not None and a.element.symbol=='H' for a in mod.topology.atoms())
  if hcount<=0:raise ValueError('no hydrogens added')
  # record charged residues per force field, not inference about true protonation
  residuecharges={}
  for res in mod.topology.residues():
   val=sum(float(nb.getParticleParameters(a.index)[0].value_in_unit(unit.elementary_charge)) for a in res.atoms())
   residuecharges[(res.chain.id,res.id,res.name)]=val
  record.update(repair_heavy_max_shift_A=float(repair_shift),added_heavy_atoms=[list(x) for x in sorted(added)],original_heavy_count=len(pre),hydrogenation_heavy_max_shift_A=float(shift),hydrogen_count=int(hcount),net_charge_e=float(net),forcefield_particles=system.getNumParticles(),charge_by_residue_type={name:[round(v,4) for (ch,rid,rname),v in residuecharges.items() if rname==name] for name in ('ASP','GLU','LYS','ARG','HIS')})
  # Bonded donor hydrogen; PDB topology bonds include hydrogens after Modeller
  bonded={}
  for a,b in mod.topology.bonds():bonded.setdefault(a.index,[]).append(b);bonded.setdefault(b.index,[]).append(a)
  # fixed protocol acceptor chemical typing; His/terminus OXT excluded
  def acceptor(a):
   name=a.name;res=a.residue.name
   return name=='O' or (res=='ASN' and name=='OD1') or (res=='GLN' and name=='OE1') or (res in ('ASP','GLU') and name in ('OD1','OD2','OE1','OE2')) or (res=='SER' and name=='OG') or (res=='THR' and name=='OG1') or (res=='TYR' and name=='OH')
  atoms=list(mod.topology.atoms());xyz=np.asarray(mod.positions.value_in_unit(unit.angstrom))
  # KDTree accelerator, never changes actual threshold
  from scipy.spatial import cKDTree
  acc=[a for a in atoms if a.element.symbol!='H' and a.name!='OXT' and a.residue.name!='HIS' and acceptor(a)]
  tree=cKDTree([xyz[a.index] for a in acc]) if acc else None
  curr=[]
  for donor in atoms:
   if donor.element.symbol not in ('N','O') or donor.residue.name=='HIS' or donor.name=='OXT':continue
   hydro=[a for a in bonded.get(donor.index,[]) if a.element.symbol=='H']
   if not hydro:continue
   if tree is None:continue
   for j in tree.query_ball_point(xyz[donor.index],r=3.0000001):
    ac=acc[j]
    if ac.residue.chain.id==donor.residue.chain.id:continue
    d=float(np.linalg.norm(xyz[donor.index]-xyz[ac.index]));
    if d>3.0:continue
    for ha in hydro:
     deg=angle(xyz[donor.index],xyz[ha.index],xyz[ac.index])
     if deg<150.:continue
     curr.append({'structure':label,'donor_chain':donor.residue.chain.id,'donor_res':donor.residue.id,'donor_resname':donor.residue.name,'donor_atom':donor.name,'hydrogen':ha.name,'acceptor_chain':ac.residue.chain.id,'acceptor_res':ac.residue.id,'acceptor_resname':ac.residue.name,'acceptor_atom':ac.name,'da_distance_A':d,'dha_angle_deg':deg})
  outp=OUT/(label+'_hydrogenated_DERIVED.pdb')
  with outp.open('w') as f:PDBFile.writeFile(mod.topology,mod.positions,f,keepIds=True)
  record.update(status='PASS',tier2_triplet_count=len(curr),tier2_unique_residue_pairs=len({(r['donor_chain'],r['donor_res'],r['acceptor_chain'],r['acceptor_res']) for r in curr}),derived_sha256=sha(outp))
  triplets.extend(curr)
 except Exception as e:
  record.update(status='NOT RUN',reason=str(e),traceback=traceback.format_exc(limit=3))
 records.append(record);print(label,record['status'],record.get('reason',''),record.get('tier2_triplet_count'))
(OUT/'tier2_structure_qc.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
fields=['structure','donor_chain','donor_res','donor_resname','donor_atom','hydrogen','acceptor_chain','acceptor_res','acceptor_resname','acceptor_atom','da_distance_A','dha_angle_deg']
with (OUT/'tier2_triplets.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(triplets)
manifest={'python':sys.executable,'python_version':sys.version,'os':platform.platform(),'openmm':openmm.version.version,'pdbfixer':pv,'code_sha256':sha(Path(__file__)),'synthetic_tests':'PASS','structures_pass':sum(r['status']=='PASS' for r in records),'structures_not_run':sum(r['status']!='PASS' for r in records),'note':'derived hydrogenated coordinates for exploratory only; never feed to Primary/DockQ/FreeSASA'}
(OUT/'tier2_execution.json').write_text(json.dumps(manifest,indent=2))
if any(r['status']!='PASS' for r in records):sys.exit(2)
