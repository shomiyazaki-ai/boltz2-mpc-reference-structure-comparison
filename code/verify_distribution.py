"""Read-only integrity/presentation checks for an extracted sealed candidate.
Writes checks to --out only; does not mutate canonical inputs or manifests.
"""
from pathlib import Path
import argparse,csv,json,re,hashlib,xml.etree.ElementTree as ET
from pypdf import PdfReader
import yaml
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);out=p.parse_args().out;out.mkdir(parents=True,exist_ok=True);checks=[]
def ck(name,value,detail=''):
 checks.append({'check':name,'pass':bool(value),'detail':str(detail)})
 if not value:raise AssertionError((name,detail))
def read(p):
 with (ROOT/p).open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Sealed SHA list excludes itself. New reproduction outputs are outside this declared set.
lines=(ROOT/'SHA256SUMS.txt').read_text().splitlines()
for i,s in enumerate(lines):
 digest,path=s.split('  ',1);f=ROOT/path;ck('sha_'+path,f.is_file() and sha(f)==digest)
manifest=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text());ck('candidate_scope',manifest['publication_status']=='LOCAL_CANDIDATE_NOT_PUBLISHED' and manifest['scope']=='C01 A+B only')
ck('no_fabricated_identifiers',manifest['zenodo_version_doi']=='10.5281/zenodo.23910491' and manifest['zenodo_doi_status']=='RESERVED_NOT_PUBLISHED' and manifest['github_release_commit'] is None and manifest['github_tag_status']=='not_created')
for row in manifest['files']:
 f=ROOT/row['path'];ck('manifest_'+row['path'],f.is_file() and f.stat().st_size==row['bytes'] and sha(f)==row['sha256'])
for r in read('provenance/SOURCE_MANIFEST.csv'):
 path=ROOT/r['public_path'];ck('selected_source_'+r['public_path'],path.is_file() and sha(path)==r['public_sha256'])
 if r['transformation']=='none; bytes preserved':ck('byte_identity_'+r['public_path'],r['source_sha256']==r['public_sha256'])
# Tables independently joined back to the recorded raw source cell.
tables=json.loads((ROOT/'data/derived/table_payload.json').read_text());cache={}
for r in read('data/derived/NUMERIC_PRESENTATION_MAP.csv'):
 path=r['source_path'];cache.setdefault(path,read(path));raw=cache[path][int(r['source_data_row'])-1][r['source_field']];display=format(float(raw),'.'+r['precision']+'f')
 ck('numeric_cell_'+r['table_id']+'_'+r['row_index']+'_'+r['column_index'],raw==r['source_value'] and display==r['text'] and tables[r['table_id']]['rows'][int(r['row_index'])][int(r['column_index'])]==display)
# Every generated table appears intact in editable manuscript source.
for key,t in tables.items():
 file='C01_AB_Technical_Note_v1.0.0.md' if key.startswith('T') else 'C01_AB_Supplementary_Information_v1.0.0.md';s=(ROOT/'manuscript'/file).read_text();m=re.search(r'<!-- TABLE '+key+r' START -->(.*?)<!-- TABLE '+key+r' END -->',s,re.S);ck('table_present_'+key,m is not None)
 block=[]
 for line in m.group(1).splitlines():
  if line.startswith('|'):
   rr=[c.strip() for c in line.strip('|').split('|')]
   if not all(re.fullmatch(':?-+:?',c) for c in rr):block.append(rr)
 ck('table_source_matches_'+key,block==[t['headers']]+t['rows'])
fig=read('data/derived/Figure_1_data.csv');ck('figure_14_rows',len(fig)==14)
for r in fig:
 raw=read(r['canonical_path'])[int(r['canonical_data_row'])-1];ck('figure_source_'+r['source']+r['target'],raw['source']==r['source'] and raw['target']==r['target'] and raw['RMSD_A']==r['RMSD_A'] and raw['metric']=='fixed_union5_interface_CA_RMSD_A')
svg=(ROOT/'figures/Figure_1.svg').read_text();ET.fromstring(svg)
for r in fig:ck('svg_bar_label_'+r['source']+r['target'],format(float(r['RMSD_A']),'.3f') in svg)
ck('main_Table2_14_rows',len(tables['T2']['rows'])==14)
ck('all_primary_S4_S5',len(tables['S4']['rows'])==10 and len(tables['S5']['rows'])==10)
ck('all_AF_S6',len(tables['S6a']['rows'])==5 and len(tables['S6b']['rows'])==5)
# Semantic exception/count checks independent of the authoring narrative.
primary=read('data/results/primary_70_metrics.csv');af=read('data/results/AF_35_metrics.csv');ck('canonical_counts',len(primary)==70 and len(af)==35)
ck('AF_erratum_exact',af[1]['target']=='9GIX' and af[1]['RMSD_A']=='3.8981798013974487')
h1=read('data/results/H1_angles_stability_6.csv');flag=[r for r in h1 if r['flag']=='H1_NUMERIC_SENSITIVITY_GT5'];ck('H1_flag_retained',len(flag)==1 and flag[0]['structure']=='9GIX' and flag[0]['role']=='MPC2' and float(flag[0]['max_end_axis_perturbation_deg'])>5)
ck('old_H1_FAIL',all(r['flag_gt_5deg']=='True' for r in read('verification/historical/H1_short_window_PCA_FAIL.csv')))
ck('H23_between_NOT_RUN',all(r['bundle_between_state']=='NOT QUALIFIED / NOT RUN' for r in read('data/results/H2_H3_within_state_6.csv')))
t1=read('data/results/tier1_primary.csv')+read('data/results/tier1_AF.csv');tp={tuple(sorted([(r['donor_chain'],int(r['donor_res'])),(r['acceptor_chain'],int(r['acceptor_res']))])) for r in t1};ck('Tier1_21_rows_8_types',len(t1)==21 and len(tp)==8)
t2=read('data/results/tier2_primary.csv')+read('data/results/tier2_AF.csv');tp={tuple(sorted([(r['donor_chain'],int(r['donor_res'])),(r['acceptor_chain'],int(r['acceptor_res']))])) for r in t2};ck('Tier2_5_rows_3_types',len(t2)==5 and len(tp)==3)
q=json.loads((ROOT/'verification/historical/tier2_primary_qc.json').read_text());ck('three_Tier2_NOT_RUN',{r['structure'] for r in q if r['status']=='NOT RUN'}=={'9GIX','9GIW','9GIY'})
ck('all_quality_rows',len(read('data/results/residue_validation_with_model_B.csv'))==308 and len(tables['S15']['rows'])==32)
# Check full text of both PDFs and every exact displayed numeric table value.
pdftext={};pdfpages={}
for stem in ['C01_AB_Technical_Note_v1.0.0','C01_AB_Supplementary_Information_v1.0.0']:
 reader=PdfReader(ROOT/'manuscript'/f'{stem}.pdf');texts=[p.extract_text() or '' for p in reader.pages];ck('pdf_readable_'+stem,len(texts)>0 and all(len(s)>100 for s in texts));text='\n'.join(texts);ck('no_replacement_glyph_'+stem,'\ufffd' not in text and '\x00' not in text);pdftext[stem]=text;pdfpages[stem]=len(texts)
for r in read('data/derived/NUMERIC_PRESENTATION_MAP.csv'):
 stem='C01_AB_Technical_Note_v1.0.0' if r['table_id'].startswith('T') else 'C01_AB_Supplementary_Information_v1.0.0';ck('pdf_numeric_'+r['table_id']+'_'+r['row_index']+'_'+r['column_index'],r['text'] in pdftext[stem])
readme=(ROOT/'README.md').read_text()
for ref,b,afval in [('9GIX','3.853976','4.045460'),('9GIV','0.964115','1.794373'),('9GIW','1.217374','1.966428'),('9GIY','1.077057','1.837599')]:
 ck('README_at_glance_'+ref,any(ref in line and b in line and afval in line for line in readme.splitlines()))
links=re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',readme)
for link in links:
 if re.match('https?://|mailto:',link):continue
 path=link.split('#',1)[0];ck('README_link_'+path,(ROOT/path).exists())
ck('no_future_repository_url','https://github.com/shomiyazaki-ai/boltz2-mpc-reference-structure-comparison' not in readme)
# All claim-map file references resolve; numeric row descriptions are retained as selectors.
for r in read('provenance/CLAIM_EVIDENCE_MAP.csv'):
 for key in ['canonical_evidence','verification_evidence','source_or_protocol']:
  for s in r[key].split(';'):
   s=s.strip();ck('claim_path_'+r['claim_id']+'_'+s,(ROOT/s).exists())
ck('CFF_parse',yaml.safe_load((ROOT/'CITATION.cff').read_text())['cff-version']=='1.2.0')
ck('rights_files',all((ROOT/p).is_file() for p in ['provenance/RIGHTS_MANIFEST.csv','provenance/LICENSE_SCOPE.md','provenance/licenses/Atlas_MIT.txt','provenance/THIRD_PARTY_NOTICES.md']))
ck('no_thirdparty_PDF',(set(p.name for p in (ROOT/'manuscript').glob('*.pdf'))=={'C01_AB_Technical_Note_v1.0.0.pdf','C01_AB_Supplementary_Information_v1.0.0.pdf'}) and len(list(ROOT.rglob('*.pdf')))==2)
with (out/'distribution_checks.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
s={'status':'PASS','checks':len(checks),'declared_SHA_files':len(lines),'canonical_metrics':105,'direct_numeric_cells':len(read('data/derived/NUMERIC_PRESENTATION_MAP.csv')),'figure_rows':len(fig),'relative_README_links_checked':sum(not re.match('https?://|mailto:',s) for s in links),'claim_rows':len(read('provenance/CLAIM_EVIDENCE_MAP.csv')),'PDF_pages':pdfpages,'visual_inspection':'separate rendered-page review; not certified by this script','author_declarations_and_licenses':'author approved 2026-11-03; DOI 10.5281/zenodo.23910491 reserved but unpublished; GitHub tag/commit pending'}
(out/'distribution_summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s))
