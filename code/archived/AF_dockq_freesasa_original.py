"""C01 AF Session D. Frozen inputs only; DockQ and FreeSASA 2.2.1 results require independent return audit."""
import csv,datetime,hashlib,json,math,platform,subprocess,sys,traceback
from pathlib import Path
from importlib.metadata import version,PackageNotFoundError
ROOT=Path(__file__).resolve().parent; IN=ROOT/'INPUT'; OUT=ROOT/'LOCAL_RESULTS';OUT.mkdir(exist_ok=True)
AF='AF-0000000204012512-model_v1'
refs=['9GIX','9GIV','9GIW','9GIY','O95563_P0DKB6_Boltz-2_v2-1-1']
OPT={'hetatm':False,'hydrogen':False,'skip-unknown':False,'halt-at-unknown':True}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(name,rows,fields=None):
 if not rows:return
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def subset(src,dst,chains,translate=False):
 count=0
 with src.open() as fin,dst.open('w') as out:
  for l in fin:
   if l.startswith('ATOM  ') and l[21] in chains:
    if translate:
     vals=[float(l[i:i+8])+123.0 for i in (30,38,46)];l=l[:30]+''.join(f'{x:8.3f}' for x in vals)+l[54:]
    out.write(l);count+=1
  out.write('END\n')
 return count

def main():
 exp=json.loads((ROOT/'expected_inputs.json').read_text());record={'run_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.executable,'python_version':sys.version,'os':platform.platform(),'script_sha256':sha(Path(__file__)),'status':'STARTED','dockq':'NOT_RUN','freesasa':'NOT_RUN','radius_qc':'NOT_RUN','checks':[]}
 def check(label,status,detail=''):
  record['checks'].append({'check':label,'status':'PASS' if status else 'FAIL','detail':str(detail)})
 try:
  files={n:IN/(n+'_normalized_AB.pdb') for n in [AF]+refs}
  for n,p in files.items():
   expected=exp['inputs'][p.name]
   assert p.is_file(),p
   assert sha(p)==expected['sha256'],f'Input SHA mismatch: {p}'
   atoms=[l for l in p.read_text().splitlines() if l.startswith('ATOM  ')]
   assert len(atoms)==expected['atoms'],f'Atom count mismatch {n}'
   assert all(l[21] in 'AB' and l[76:78].strip() in ('C','N','O','S') for l in atoms)
   check('input '+n,True,f'{len(atoms)} atoms, SHA256 verified')
  aflines=[l for l in files[AF].read_text().splitlines() if l.startswith('ATOM  ')]
  assert sum(l[21]=='A' for l in aflines)==1062 and sum(l[21]=='B' for l in aflines)==1008
  assert len({(l[21],int(l[22:26])) for l in aflines if l[12:16].strip()=='CA'})==263
  check('AF chain mapping and CA coverage',True,'A MPC1L 1062 atoms, B MPC2 1008 atoms, 263 CA')
 except Exception:
  record['status']='INPUT_QC_FAIL';record['error']=traceback.format_exc();(OUT/'execution_record.json').write_text(json.dumps(record,indent=2));print(record['error']);return 2
 versions={}
 for name in ['DockQ','freesasa']:
  try:versions[name]=version(name)
  except PackageNotFoundError:versions[name]='NOT_INSTALLED'
 record['versions']=versions
 # DockQ: fail closed on wrong version and preserve all raw logs
 dq=[]
 if versions['DockQ']=='2.1.3':
  for native in refs:
   cmd=['DockQ',str(files[AF]),str(files[native]),'--mapping','AB:AB']
   log=OUT/f'DockQ_AF_vs_{native}.txt'
   try:
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=240)
    log.write_text('COMMAND: '+repr(cmd)+'\nEXIT: '+str(p.returncode)+'\nSTDOUT\n'+p.stdout+'\nSTDERR\n'+p.stderr,encoding='utf-8')
    dq.append({'model':AF,'reference':native,'mapping':'AB:AB','exit_code':p.returncode,'log':log.name,'status':'RAW_COMPLETE_REVIEW_REQUIRED' if p.returncode==0 else 'FAIL'})
   except Exception as e:
    log.write_text('COMMAND: '+repr(cmd)+'\nEXCEPTION '+repr(e),encoding='utf-8');dq.append({'model':AF,'reference':native,'mapping':'AB:AB','exit_code':-1,'log':log.name,'status':'FAIL'})
  table('dockq_run_status.csv',dq)
  record['dockq']='RAW_COMPLETE_REVIEW_REQUIRED' if len(dq)==5 and all(r['exit_code']==0 for r in dq) else 'PARTIAL_FAIL'
 else:record['dockq']='NOT_RUN_WRONG_VERSION'
 # FreeSASA exact settings + all-atom ProtOr cross-check. Do not call BSA PASS unless radius QC passes.
 if versions['freesasa']=='2.2.1':
  try:
   import freesasa
   cls=freesasa.Classifier.getStandardClassifier('protor')
   par=freesasa.Parameters({'algorithm':freesasa.LeeRichards,'n-slices':20,'probe-radius':1.4})
   structure=freesasa.Structure(str(files[AF]),options=OPT)
   explicit=freesasa.Structure(str(files[AF]),classifier=cls,options=OPT)
   assert structure.nAtoms()==explicit.nAtoms()==2070,'atom retention failure'
   rad=[];bad=0
   for i in range(2070):
    name=structure.atomName(i).strip();res=structure.residueName(i).strip();rid=structure.residueNumber(i).strip();chain=structure.chainLabel(i).strip()
    typ=cls.classify(res,name);r=float(cls.radius(res,name));actual=float(structure.radius(i));rexp=float(explicit.radius(i))
    ok=typ!='Unknown' and math.isfinite(r) and r>0 and actual>0 and abs(r-actual)<1e-8 and abs(r-rexp)<1e-8
    bad+=not ok;rad.append({'index':i,'chain':chain,'residue_number':rid,'residue_name':res,'atom_name':name,'protor_class':typ,'protor_radius_A':r,'default_radius_A':actual,'explicit_radius_A':rexp,'pass':ok})
   table('AF_protor_radius_per_atom.csv',rad)
   assert bad==0,f'Radius QC failure {bad} atoms'
   a=freesasa.calc(structure,par).totalArea();a2=freesasa.calc(explicit,par).totalArea()
   assert abs(a-a2)<1e-5,'Default vs ProtOr SASA mismatch'
   temp=OUT/'temporary_pdb';temp.mkdir(exist_ok=True)
   areas={};counts={}
   for tag,chains,tr in [('A','A',False),('B','B',False),('AB','AB',False),('AB_translated','AB',True)]:
    dest=temp/f'{AF}_{tag}.pdb';counts[tag]=subset(files[AF],dest,chains,tr)
    st=freesasa.Structure(str(dest),options=OPT)
    assert st.nAtoms()==counts[tag],f'{tag} atom loss'
    areas[tag]=freesasa.calc(st,par).totalArea()
   assert abs(areas['AB']-a)<1e-5,'Complex re-export mismatch'
   delta=areas['A']+areas['B']-areas['AB'];shift=abs(areas['AB']-areas['AB_translated'])
   passed=delta>=-0.01 and shift<0.1
   table('AF_freesasa_results.csv',[{'structure':AF,'SASA_MPC1L_A2':areas['A'],'SASA_MPC2_A2':areas['B'],'SASA_complex_A2':areas['AB'],'delta_SASA_A2':delta,'BSA_half_A2':delta/2,'translation_difference_A2':shift,'n_atoms_MPC1L':counts['A'],'n_atoms_MPC2':counts['B'],'n_atoms_complex':counts['AB'],'radius_bad_count':bad,'explicit_vs_default_difference_A2':abs(a-a2),'status':'PASS' if passed else 'FAIL'}])
   record['radius_qc']='PASS_2070_ATOMS';record['freesasa']='COMPLETED_REVIEW_REQUIRED' if passed else 'QC_FAIL'
  except Exception:
   record['freesasa']='FAIL';record['radius_qc']='FAIL_OR_INCOMPLETE';(OUT/'freesasa_error.txt').write_text(traceback.format_exc(),encoding='utf-8')
 else:record['freesasa']='NOT_RUN_WRONG_VERSION'
 record['status']='RAW_COMPLETE_AUDIT_PENDING' if record['dockq']=='RAW_COMPLETE_REVIEW_REQUIRED' and record['freesasa']=='COMPLETED_REVIEW_REQUIRED' and record['radius_qc']=='PASS_2070_ATOMS' else 'INCOMPLETE_REVIEW_REQUIRED'
 (OUT/'execution_record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
 table('input_qc.csv',record['checks'])
 print(json.dumps({'status':record['status'],'versions':versions,'dockq':record['dockq'],'freesasa':record['freesasa'],'radius_qc':record['radius_qc']},ensure_ascii=False,indent=2))
 return 0 if record['status']=='RAW_COMPLETE_AUDIT_PENDING' else 1
if __name__=='__main__':sys.exit(main())
