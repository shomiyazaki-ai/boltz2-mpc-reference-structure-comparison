"""C01 Session2 local DockQ/FreeSASA runner: only operates on QC-exported PDB files."""
import argparse,csv,hashlib,json,platform,subprocess,sys,datetime,traceback
from pathlib import Path

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rows_to_csv(path,rows):
 if not rows:return
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

def subp(cmd, path):
 try:
  proc=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
  path.write_text('CMD '+repr(cmd)+'\nEXIT '+str(proc.returncode)+'\nSTDOUT\n'+proc.stdout+'\nSTDERR\n'+proc.stderr,encoding='utf-8')
  return proc.returncode
 except Exception as e:
  path.write_text('CMD '+repr(cmd)+'\nEXCEPTION '+repr(e)+'\n',encoding='utf-8');return -1

def select_chains(src,dest,chains,translate=False):
 n=0
 with src.open() as fin,dest.open('w') as out:
  for line in fin:
   if line.startswith('ATOM  ') and line[21] in chains:
    if translate:
     vals=[float(line[i:i+8])+123.0 for i in (30,38,46)]
     line=line[:30]+''.join(f'{x:8.3f}' for x in vals)+line[54:]
    out.write(line);n+=1
  out.write('END\n')
 return n

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,default=Path(__file__).parent/'SESSION2');ap.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'LOCAL_RESULTS');args=ap.parse_args()
 inp=args.input_dir.resolve();out=args.output_dir.resolve();out.mkdir(exist_ok=True,parents=True)
 names=['O95563_P0DKB6_Boltz-2_v2-1-1','9GIX','9GIV','9GIW','9GIY'];files={n:inp/(n+'_normalized_AB.pdb') for n in names}
 if any(not p.is_file() for p in files.values()):raise RuntimeError('Missing normalized input PDB')
 inventory={x['structure']:0 for x in csv.DictReader((inp/'atom_inventory.csv').open())}
 for r in csv.DictReader((inp/'atom_inventory.csv').open()): inventory[r['structure']]+=int(r['atoms'])
 inputhash={n:digest(files[n]) for n in names};counts={}
 for n,p in files.items():
  k=sum(line.startswith('ATOM  ') for line in p.open());counts[n]=k
  if k!=inventory[n]:raise RuntimeError(f'{n} unexpected atoms {k} != {inventory[n]}')
 env={'run_id':'C01-S2-LOCAL-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python_executable':sys.executable,'python_version':sys.version,'os':platform.platform(),'script_sha256':digest(__file__),'input_sha256':inputhash,'atom_counts':counts,'dockq_status':'NOT RUN','freesasa_status':'NOT RUN'}
 try:
  import importlib.metadata as metadata
  env['DockQ_version']=metadata.version('DockQ');env['freesasa_version']=metadata.version('freesasa')
 except Exception as e:env['version_error']=repr(e)
 dockrows=[]
 # Prepared inputs contain A=MPC1L, B=MPC2 in BOTH model/native. Hence AB:AB, not original AB:BA.
 pairs=[(names[0],n) for n in names[1:]]+[(names[i],names[j]) for i in range(1,5) for j in range(i+1,5)]
 if env.get('DockQ_version')=='2.1.3':
  rc_ok=True
  for model,native in pairs:
   log=out/f'DockQ_{model}_vs_{native}.txt'
   cmd=['DockQ',str(files[model]),str(files[native]),'--mapping','AB:AB']
   rc=subp(cmd,log);dockrows.append({'model':model,'native':native,'mapping':'AB:AB','exit_code':rc,'log':log.name,'status':'COMPLETED_RAW' if rc==0 else 'FAIL'})
   if rc:rc_ok=False
  env['dockq_status']='RAW COMPLETE; MANUAL METRIC/QC REVIEW REQUIRED' if rc_ok else 'PARTIAL FAILURE: REVIEW LOGS'
 else:env['dockq_status']='NOT RUN: DockQ exact version 2.1.3 required'
 rows_to_csv(out/'dockq_run_status.csv',dockrows)
 try:
  import freesasa
  if env.get('freesasa_version')!='2.2.1':raise RuntimeError('Requires exact FreeSASA v2.2.1')
  fsrows=[];tmp=out/'temporary_single_chain_pdb';tmp.mkdir(exist_ok=True)
  pars=freesasa.Parameters({'algorithm':freesasa.LeeRichards,'n-slices':20,'probe-radius':1.4})
  for name in names:
   f=files[name];parts={};ncount={}
   for tag,chains in [('A','A'),('B','B'),('AB','AB'),('AB_translated','AB')]:
    p=tmp/(name+'_'+tag+'.pdb');ncount[tag]=select_chains(f,p,chains,tag=='AB_translated')
    st=freesasa.Structure(str(p),options={'hetatm':False,'skip-unknown':False,'halt-at-unknown':True})
    if st.nAtoms()!=ncount[tag]:raise RuntimeError(f'{name} {tag} FreeSASA atom count {st.nAtoms()} != {ncount[tag]}')
    parts[tag]=freesasa.calc(st,pars).totalArea()
   diff=parts['A']+parts['B']-parts['AB'];shift=abs(parts['AB']-parts['AB_translated'])
   status='PASS' if diff>=-0.01 and shift<0.1 else 'FAIL'
   fsrows.append({'structure':name,'SASA_A_A2':parts['A'],'SASA_B_A2':parts['B'],'SASA_AB_A2':parts['AB'],'delta_SASA_A2':diff,'BSA_half_A2':diff/2,'translation_diff_A2':shift,'atoms_A':ncount['A'],'atoms_B':ncount['B'],'atoms_AB':ncount['AB'],'status':status})
  rows_to_csv(out/'freesasa_results.csv',fsrows)
  env['freesasa_status']='COMPLETED; REVIEW REQUIRED' if all(x['status']=='PASS' for x in fsrows) else 'QC FAIL'
 except Exception as e:
  (out/'freesasa_error.txt').write_text(traceback.format_exc(),encoding='utf-8')
  env['freesasa_status']='NOT RUN/FAILED: '+repr(e)
 (out/'execution_record.json').write_text(json.dumps(env,indent=2,ensure_ascii=False),encoding='utf-8')
 print(json.dumps(env,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
