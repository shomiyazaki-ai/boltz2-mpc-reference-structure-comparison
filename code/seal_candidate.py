"""Seal local candidate files only; no git/network/deposit operations.
No file hashes itself; no archive or containing commit hash is inserted here.
"""
from pathlib import Path
import json,hashlib,argparse
P=argparse.ArgumentParser();P.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);r=P.parse_args().root.resolve()
def eligible(p):return p.is_file() and p.name not in ['RELEASE_MANIFEST.json','SHA256SUMS.txt'] and not any(s in ['__pycache__','.git','reproduction','.venv'] for s in p.relative_to(r).parts) and p.suffix!='.pyc'
files=[]
for p in sorted(r.rglob('*')):
 if eligible(p):files.append({'path':p.relative_to(r).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
m={'schema_version':'1.0','title':'Experimental-Reference Sensitivity of a Fixed Boltz-2 MPC1L–MPC2 Complex Prediction, with an Exploratory AlphaFold Structural Comparison','document_type':'Technical Note','version':'1.0.0','candidate_date_JST':'2026-11-03','publication_status':'LOCAL_CANDIDATE_NOT_PUBLISHED','scope':'C01 A+B only','github_repository_name':'boltz2-mpc-reference-structure-comparison','intended_github_tag':'v1.0.0','github_tag_status':'not_created','github_release_commit':None,'zenodo_version_doi':'10.5281/zenodo.23910491','zenodo_doi_status':'RESERVED_NOT_PUBLISHED','author_license_approval':'approved 2026-11-03 for future release; no public release yet; source-specific upstream terms retained','packaging_equivalence':'GitHub candidate ZIP and Zenodo reproducibility ZIP contain the same sealed root payload; PDFs intentionally inside for standalone README links','excluded_from_this_file_list':['RELEASE_MANIFEST.json','SHA256SUMS.txt','all containing archive bytes','containing git commit SHA','reproduction outputs and bytecode'],'external_receipt_rule':'Actual future release commit/tag/DOI and outer archive hashes must be recorded outside their containing immutable payload; see provenance/PUBLICATION_PROCEDURE.md','files':files}
p=r/'RELEASE_MANIFEST.json';p.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
items=files+[{'path':'RELEASE_MANIFEST.json','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}];items.sort(key=lambda x:x['path']);(r/'SHA256SUMS.txt').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in items))
print(json.dumps({'payload_files':len(files),'checksum_entries':len(items),'self_hashing':False}))
