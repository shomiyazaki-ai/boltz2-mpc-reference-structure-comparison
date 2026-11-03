"""Generate all publication tables and the two-panel Figure 1 from canonical CSVs.
Every selected numeric cell retains its source filename, data-row and field.
"""
from cif_geometry import *
import argparse,re,platform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from collections import defaultdict
P=argparse.ArgumentParser();P.add_argument('--out-root',type=Path,default=ROOT);args=P.parse_args();O=args.out_root
for p in ['data/derived','figures','manuscript']:(O/p).mkdir(parents=True,exist_ok=True)
def table_read(n):
 path='data/results/'+n;return [dict(r,__path=path,__row=i+1) for i,r in enumerate(read_csv(ROOT/path))]
primary=table_read('primary_70_metrics.csv');af=table_read('AF_35_metrics.csv');allr=primary+af
m=json.loads((ROOT/'data/frozen/masks.json').read_text());tables={};numeric=[]
def label(s):return 'Boltz-2' if s==BOLTZ else 'AlphaFold' if s==AF else s
def v(row,field,precision=6):
 raw=row[field];value=format(float(raw),'.'+str(precision)+'f')
 return {'text':value,'source_path':row['__path'],'source_data_row':row['__row'],'source_field':field,'source_value':raw,'precision':precision}
def add(key,title,heads,rows,widths=None,note=''):
 cleaned=[]
 for ri,row in enumerate(rows):
  cells=[]
  for ci,x in enumerate(row):
   if isinstance(x,dict):
    numeric.append(dict(table_id=key,row_index=ri,column_index=ci,**x));cells.append(x['text'])
   else:cells.append(str(x))
  assert len(cells)==len(heads),(key,row)
  cleaned.append(cells)
 tables[key]={'title':title,'headers':heads,'rows':cleaned,'widths':widths,'note':note}
def get(src,tgt,metric):return next(r for r in allr if r['source']==src and r['target']==tgt and r['metric']==metric)
# Main tables.
structure_rows=[['Boltz-2',BOLTZ,'Not assigned','Protein-only fixed model','Primary A'],['9GIX','PDB 9GIX','Inward-open','Apo','Experimental reference'],['9GIV','PDB 9GIV','Outward-open','C7 (UK5099 derivative)','Experimental reference'],['9GIW','PDB 9GIW','Outward-open','Zaprinast','Experimental reference'],['9GIY','PDB 9GIY','Outward-open','Mitoglitazone','Experimental reference'],['AlphaFold',AF,'Not assigned','Protein-only fixed model','Exploratory B']]
add('T1','Structures and conditions',['Input','Source identifier','State','Condition','Role'],structure_rows,[.12,.29,.16,.24,.19],note='State labels describe experimental conditions from Sichrovsky et al. [1]. No state is assigned to either prediction by this table. Boltz-2 source: Atlas row 147, version 2.1.1. AlphaFold source: AFDB/NVIDIA entry v1, AF-Multimer 2.3.0 weights.')
principal=[]
for r in primary:
 if r['metric']==M73:principal.append(['Primary A' if r['source']==BOLTZ else 'Experimental control',label(r['source'])+' vs '+label(r['target']),v(r,'RMSD_A')])
for r in af:
 if r['metric']==M73 and r['target'] in REFS:principal.append(['Exploratory B',label(r['source'])+' vs '+label(r['target']),v(r,'RMSD_A')])
add('T2','Principal structural comparisons',['Comparison group','Source vs target','73-residue RMSD (Å)'],principal,[.28,.44,.28],note='All 14 comparisons use the same two-chain 73-Cα fit and evaluation set. Source/target direction identifies saved fits; the same-mask optimum RMSD is symmetric. These rows are not statistical replicates.')
rows=[]
for ref in REFS:rows.append([ref]+[v(get(BOLTZ,ref,q),'RMSD_A') for q in [M73,M62,M198]])
add('T3','Mask sensitivity of the fixed Boltz-2 structure',['Reference','73 residues (Å)','62 residues (Å)','198 residues (Å)'],rows,[.19,.27,.27,.27],note='Each column is fitted and evaluated on its own indicated Cα set. Thresholds defining the masks are strictly <5 Å and <4 Å; the 198-residue set is sequence-common coverage.')
cm=['MPC1L_independent_chain_CA_RMSD_A','MPC2_independent_chain_CA_RMSD_A','fit_MPC1L_evaluate_MPC2_CA_displacement_RMSD_A','fit_MPC2_evaluate_MPC1L_CA_displacement_RMSD_A']
add('T4','Chain-specific and cross-chain alignment: fixed Boltz-2',['Reference','Fit/evaluate MPC1L (Å)','Fit/evaluate MPC2 (Å)','Fit MPC1L; evaluate MPC2 (Å)','Fit MPC2; evaluate MPC1L (Å)'],[[ref]+[v(get(BOLTZ,ref,q),'RMSD_A') for q in cm] for ref in REFS],[.12,.20,.20,.24,.24],note='MPC1L: 84 Cα sites; MPC2: 114. Cross-chain evaluation applies the fitted transform without a second fit. It includes internal shape differences and relative arrangement; it is not a pure translation or a single rigid-body displacement.')
# SI 1-15 retain source, alignment, results, auxiliary geometry, quality.
add('S1','Structural source identities and data scope',['Input','Provider / version','Original CIF SHA-256 prefix','Role / source scope'],[[r[0],('Atlas / fixed dc55acabb3da' if r[0]=='Boltz-2' else 'AFDB/NVIDIA / v1' if r[0]=='AlphaFold' else 'wwPDB / frozen revision'),sha(ROOT/'data/frozen/coordinates'/((BOLTZ if r[0]=='Boltz-2' else AF if r[0]=='AlphaFold' else r[0])+'.cif'))[:16],r[4]] for r in structure_rows],[.12,.30,.29,.29],note='Full hashes and original archive-member identities are in provenance/SOURCE_MANIFEST.csv. Short hashes are visual keys only, not replacements for full hashes.')
add('S2','Protein identity and chain correspondence',['Input','Protein / UniProt','Source label chain; entity','Common label_seq positions','Source auth_seq positions'],[[label(n),p+' / '+('P0DKB6' if p=='MPC1L' else 'O95563'),('B; 2' if p=='MPC1L' else 'A; 1') if n==BOLTZ else ('B; 1' if p=='MPC1L' else 'A; 2') if n==AF else ('A; 1' if p=='MPC1L' else 'B; 2'),'22-105 (84)' if p=='MPC1L' else '8-121 (114)','Same numeric positions'] for n in [BOLTZ]+REFS+[AF] for p in ['MPC1L','MPC2']],[.14,.24,.20,.22,.20],note='Normalized auxiliary PDBs use A=MPC1L and B=MPC2 for all structures. Entity and label/auth namespaces remain separate. The full 1,188-row Cα crosswalk and primary observed-atom crosswalk are supplied as unchanged CSVs.')
add('S3','Frozen residue masks',['Mask','MPC1L aligned residue positions','MPC2 aligned residue positions'],[[str(k)+' residues',', '.join(map(str,m[str(k)]['MPC1L'])) if k!=198 else '22-105 inclusive (84)',', '.join(map(str,m[str(k)]['MPC2'])) if k!=198 else '8-121 inclusive (114)'] for k in [73,62,198]],[.13,.435,.435],note='Masks are unions of contacting residue identities from the four experimental structures, restricted to the common sequence region. The 73-residue mask comprises 37 MPC1L + 36 MPC2 sites; the 62-residue mask has 30 + 32 sites. No prediction defines or modifies either mask.')
cc=table_read('contact_counts.csv');rows=[]
for ref in REFS:rows.append([ref]+[v(next(r for r in cc if r['structure']==ref and float(r['cutoff'])==q),'count',0) for q in [5.,4.]])
add('S3a','Reference-specific contact-pair counts (separate from the mask union)',['Reference','Heavy-atom pair-of-residues <5 Å','Heavy-atom pair-of-residues <4 Å'],rows,[.18,.41,.41],note='Per-reference pairs are unique cross-chain residue pairs selected by their closest observed heavy atoms. Union/intersection counts over all references are 107/37 at <5 Å and 69/13 at <4 Å. These pair counts differ from residue-mask sizes.')
pairs=[]
for r in primary:
 if r['metric']==M73:pairs.append((r['source'],r['target']))
add('S4','All ten Primary/control comparisons: mask fits',['Source vs target','73 residues (Å)','62 residues (Å)','198 residues (Å)'],[[label(a)+' vs '+label(b)]+[v(get(a,b,q),'RMSD_A') for q in [M73,M62,M198]] for a,b in pairs],[.34,.22,.22,.22],note='Thirty of the 70 Primary/control RMSD values. Each same-mask value uses its own optimal proper rotation.')
add('S5','All ten Primary/control comparisons: chain fits',['Source vs target','MPC1L own fit (Å)','MPC2 own fit (Å)','Fit MPC1L; eval MPC2 (Å)','Fit MPC2; eval MPC1L (Å)'],[[label(a)+' vs '+label(b)]+[v(get(a,b,q),'RMSD_A') for q in cm] for a,b in pairs],[.25,.17,.17,.205,.205],note='The remaining 40 Primary/control RMSD values. Direction follows the source/target fields of primary_70_metrics.csv; cross-chain evaluation remains directional.')
rows=[]
for ref in REFS+[BOLTZ]:
 rows.append([label(ref)]+[v(get(AF,ref,q),'RMSD_A') for q in [M73,M62,M198]])
add('S6a','Exploratory AF comparisons: all mask fits',['AF vs target','73 residues (Å)','62 residues (Å)','198 residues (Å)'],rows,[.28,.24,.24,.24],note='Part of Table S6: all 15 mask-fit values. AF-9GIX 62-residue value is the canonical corrected 3.898180 Å.')
add('S6b','Exploratory AF comparisons: all chain fits',['AF vs target','MPC1L own fit (Å)','MPC2 own fit (Å)','Fit MPC1L; eval MPC2 (Å)','Fit MPC2; eval MPC1L (Å)'],[[label(ref)]+[v(get(AF,ref,q),'RMSD_A') for q in cm] for ref in REFS+[BOLTZ]],[.24,.18,.18,.20,.20],note='Part of Table S6: all 20 chain-fit values. Together S6a/S6b show all 35 AF RMSD values. AF-Boltz is a fixed-coordinate contrast, with Boltz as operational target.')
dock=table_read('dockq_primary.csv');da=table_read('dockq_AF.csv');rows=[]
for r in dock:rows.append([label(r['model'])+' vs '+label(r['native'])]+[v(r,k,3) for k in ['DockQ','iRMSD','LRMSD','fnat']])
for r in da:rows.append(['AlphaFold vs '+label(r['reference'])]+[v(r,k,3) for k in ['dockq','irmsd','lrmsd','fnat']])
add('S7','DockQ directional saved-engine outputs',['Model vs native','DockQ','Standard iRMSD (Å)','LRMSD (Å)','Fnat'],rows,[.34,.14,.19,.18,.15],note='DockQ 2.1.3. These iRMSDs are DockQ definitions, not the frozen 73-Cα endpoint. All normalized files use identity mapping AB:AB. Full canonical CSVs also retain fnonnat, F1, clashes or run status; all 15 stdout numerical excerpts are supplied. Engine not rerun for this production.')
sasa=table_read('freesasa_primary.csv');safa=table_read('freesasa_AF.csv');rows=[]
for r in sasa:rows.append([label(r['structure'])]+[v(r,k,3) for k in ['SASA_A_A2','SASA_B_A2','SASA_AB_A2','delta_SASA_A2','BSA_half_A2']]+[r['atoms_AB']])
for r in safa:rows.append(['AlphaFold']+[v(r,k,3) for k in ['SASA_MPC1L_A2','SASA_MPC2_A2','SASA_complex_A2','delta_SASA_A2','BSA_half_A2']]+[r['n_atoms_complex']])
add('S8','FreeSASA areas and observed heavy-atom coverage',['Structure','MPC1L SASA (Å²)','MPC2 SASA (Å²)','Complex SASA (Å²)','ΔSASA (Å²)','Half-BSA (Å²)','Atoms'],rows,[.14,.15,.15,.17,.15,.15,.09],note='Lee-Richards; 1.4 Å probe; 20 slices; ProtOr radii. Within each structure the same atom policy is used for isolated chains and complex. Cross-structure heavy-atom coverage differs; no energy or affinity interpretation follows. Primary columns A/B here refer to normalized chains A=MPC1L/B=MPC2. Engine not rerun for this production.')
h=table_read('H1_angles_stability_6.csv');add('S9','H1 local-axis proxy and endpoint sensitivity',['Structure','Protein','Bend (°)','Max endpoint change (°)','Left / right axes','Flag'],[[label(r['structure']),r['role'],v(r,'bend_angle_deg',3),v(r,'max_end_axis_perturbation_deg',3),r['n_left']+' / '+r['n_right'],'>5° sensitivity' if r['flag']=='H1_NUMERIC_SENSITIVITY_GT5' else 'No >5° flag'] for r in h],[.14,.14,.15,.21,.16,.20],note='MPC1L window 26-48, hinge 33; MPC2 40-61, hinge 53. Left starts ≤hinge-4; right starts ≥hinge+1. Mean resultant lengths and every local axis remain in the unchanged CSVs. The 9GIX MPC2 flag is retained, not relabeled PASS.')
h23=table_read('H2_H3_within_state_6.csv');add('S10','H2/H3 within-structure axis angles',['Structure','Protein','Directed angle (°)','Acute angle (°)','H2 anisotropy','H3 anisotropy'],[[label(r['structure']),r['role'],v(r,'directed_deg',3),v(r,'acute_deg',3),v(r,'H2_anisotropy',3),v(r,'H3_anisotropy',3)] for r in h23],[.15,.13,.19,.19,.17,.17],note='MPC1L H2 54-75 and H3 79-105; MPC2 H2 68-89 and H3 93-121. Anisotropy is the largest/second-largest centered-Cα scatter eigenvalue ratio. Directed axes face N to C; acute angle is min(θ,180-θ). Between-state rigid bundle rotation is NOT QUALIFIED / NOT RUN for all structures.')
local=table_read('local_geometry_6.csv');add('S11','All 30 predefined local residue-pair geometries',['Structure','Residue pair','Cα distance (Å)','Minimum heavy distance (Å)','Closest observed atoms','<4 / <5 Å'],[[label(r['structure']),r['role1']+' '+r['res1']+' - '+r['role2']+' '+r['res2'],v(r,'ca_dist_A',3),v(r,'min_heavy_dist_A',3),r['atom1']+' - '+r['atom2'],r['contact_lt4']+' / '+r['contact_lt5']] for r in local],[.13,.27,.14,.18,.16,.12],note='Distances use original CIF heavy atoms, not hydrogenated copies. E51-K66 minimum observed distance need not use charged side-chain atoms; the Tier0 functional-atom criterion is distinct. Closest atom names and exact distances are preserved in local_geometry_6.csv.')
t0=table_read('tier0_primary.csv')+table_read('tier0_AF.csv');add('S12','All Tier0 functional-atom salt-bridge candidates',['Structure','Cation residue / atom','Anion residue / atom','Distance (Å)'],[[r['structure'],('MPC1L' if r['cation_chain']=='A' else 'MPC2')+' '+r['cation_resname']+r['cation_res']+' '+r['cation_atom'],('MPC1L' if r['anion_chain']=='A' else 'MPC2')+' '+r['anion_resname']+r['anion_res']+' '+r['anion_atom'],v(r,'distance_A',6)] for r in t0],[.14,.33,.33,.20],note='Four observed structure/pair instances, two different residue-pair types. Successful Tier0 screens found zero qualifying functional-atom pairs in Boltz, AlphaFold and 9GIX under the fixed definition; this is not a thermodynamic absence statement.')
t1=table_read('tier1_primary.csv')+table_read('tier1_AF.csv');add('S13','All Tier1 donor/acceptor heavy-atom proximity candidates',['Structure','Donor residue / atom','Acceptor residue / atom','D-A (Å)'],[[r['structure'],('MPC1L' if r['donor_chain']=='A' else 'MPC2')+' '+r['donor_resname']+r['donor_res']+' '+r['donor_atom'],('MPC1L' if r['acceptor_chain']=='A' else 'MPC2')+' '+r['acceptor_resname']+r['acceptor_res']+' '+r['acceptor_atom'],v(r,'distance_A',6)] for r in t1],[.13,.34,.34,.19],note='All 21 atom-level candidates, representing eight different residue-pair types across structures. Criterion D-A ≤3.0 Å on all observed normalized protein atoms; no hydrogens or D-H-A angle is evaluated in Tier1. These are not demonstrated hydrogen bonds.')
t2=table_read('tier2_primary.csv')+table_read('tier2_AF.csv');add('S14a','All accepted Tier2 atom triplets',['Structure','Donor / hydrogen','Acceptor','D-A (Å)','D-H-A (°)'],[[r['structure'],('MPC1L' if r['donor_chain']=='A' else 'MPC2')+' '+r['donor_resname']+r['donor_res']+' '+r['donor_atom']+' / '+r['hydrogen'],('MPC1L' if r['acceptor_chain']=='A' else 'MPC2')+' '+r['acceptor_resname']+r['acceptor_res']+' '+r['acceptor_atom'],v(r,'da_distance_A',6),v(r,'dha_angle_deg',3)] for r in t2],[.12,.32,.27,.14,.15],note='All five atom triplets and all three residue-pair types. These counts are conditional on accepted historical protonation/hydrogen placement. No new OpenMM calculation was performed for this production.')
q=json.loads((ROOT/'verification/historical/tier2_primary_qc.json').read_text())+json.loads((ROOT/'verification/historical/tier2_AF_qc.json').read_text());fail=json.loads((ROOT/'verification/historical/tier2_failed_displacements.json').read_text())['records'];fd={r['structure']:r for r in fail}
add('S14b','Tier2 structure status and preservation gate',['Structure','Screen status','Accepted triplets','Max original-heavy displacement (Å)'],[[r['structure'],r['status'],str(r['tier2_triplet_count']) if r['status']=='PASS' else 'NOT RUN',format(r['hydrogenation_heavy_max_shift_A'],'.9g') if r['status']=='PASS' else format(fd[r['structure']]['post_h_max_A'],'.9g')+' (diagnostic)'] for r in q],[.15,.22,.22,.41],note='Gate: original-heavy displacement ≤1e-5 Å. 9GIX/9GIW/9GIY exceeded the gate; their H-bond screens remain NOT RUN. Diagnostic displacement values do not restore screening eligibility. Counts are not zero for these rows.')
quality=table_read('residue_validation_with_model_B.csv');wanted={('MPC1L','45'),('MPC1L','51'),('MPC1L','54'),('MPC1L','56'),('MPC2','59'),('MPC2','66'),('MPC2','68'),('MPC2','90')};qr=[r for r in quality if (r['protein'],r['resnum']) in wanted]
add('S15','Local experimental quality for interaction and coverage examples',['PDB','Protein / residue','Q-score','Residue map inclusion','Mean source B (Å²)','Rotamer code'],[[r['pdb'],r['protein']+' '+r['resname']+r['resnum'],v(r,'q_score',3),v(r,'residue_inclusion',4),v(r,'original_cif_mean_B_A2',3),r['rotamer_outlier'] or 'not listed'] for r in qr],[.10,.24,.12,.20,.20,.14],note='32 selected residue/structure rows supporting the local interpretation; the full 308-row residue-quality CSV and 25-row local-pair quality crosswalk are supplied. Raw wwPDB PDF/XML reports are linked, not redistributed. B is a source coordinate displacement/refinement field for experiment; prediction B-like confidence fields are not treated as experimental B factors.')
# Machine-readable table data and all direct numeric source-cell links.
(O/'data/derived/table_payload.json').write_text(json.dumps(tables,indent=2,ensure_ascii=False)+'\n')
write_csv(O/'data/derived/NUMERIC_PRESENTATION_MAP.csv',numeric)
figdata=[{'group':r['Comparison group'] if 'Comparison group' in r else '',} for r in []]
figdata=[]
for r in allr:
 if r['metric']==M73 and not (r['source']==AF and r['target']==BOLTZ):figdata.append({'source':r['source'],'target':r['target'],'RMSD_A':r['RMSD_A'],'canonical_path':r['__path'],'canonical_data_row':r['__row']})
write_csv(O/'data/derived/Figure_1_data.csv',figdata)
def markdown_table(k):
 t=tables[k];heads=t['headers'];out=['<!-- TABLE '+k+' START -->','**Table '+k[1:] if k.startswith('T') else '**Table '+k]
 name=('Table '+k[1:]) if k.startswith('T') else ('Table '+k)
 out=['<!-- TABLE '+k+' START -->','**'+name+'. '+t['title']+'**','','| '+' | '.join(heads)+' |','| '+' | '.join(['---']*len(heads))+' |']
 out+=['| '+' | '.join(row)+' |' for row in t['rows']]
 if t['note']:out+=['','*'+t['note']+'*']
 out+=['<!-- TABLE '+k+' END -->'];return '\n'.join(out)
(O/'manuscript/generated_tables.md').write_text('\n\n'.join(markdown_table(k) for k in tables)+'\n')
# If an editable manuscript exists, refresh only its tagged generated table block.
for f in ['C01_AB_Technical_Note_v1.0.0.md','C01_AB_Supplementary_Information_v1.0.0.md']:
 p=O/'manuscript'/f
 if p.exists():
  s=p.read_text()
  for k in tables:s=re.sub(r'<!-- TABLE '+k+r' START -->.*?<!-- TABLE '+k+r' END -->',lambda _:markdown_table(k),s,flags=re.S)
  p.write_text(s)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelsize':10,'svg.fonttype':'none','pdf.fonttype':42,'svg.hashsalt':'C01_AB_v1.0.0'})
fig,ax=plt.subplots(2,1,figsize=(7.2,7.4),gridspec_kw={'hspace':.52});colors=['#235789','#B66A24'];x=np.arange(4);width=.34
for j,(name,short) in enumerate([(BOLTZ,'Fixed Boltz-2 (Primary)'),(AF,'Fixed AlphaFold (Exploratory)')]):
 vals=[float(get(name,ref,M73)['RMSD_A']) for ref in REFS];bars=ax[0].bar(x+(j-.5)*width,vals,width,label=short,color=colors[j],edgecolor='white',linewidth=.4)
 ax[0].bar_label(bars,labels=[f'{y:.3f}' for y in vals],padding=3,fontsize=8.5)
ax[0].set_xticks(x,REFS);ax[0].legend(frameon=False,fontsize=9,loc='upper right');ax[0].set_title('A  Fixed predictions against four experimental references',loc='left',fontsize=11,fontweight='bold',pad=12)
exp=[r for r in primary if r['metric']==M73 and r['source']!=BOLTZ];xx=np.arange(6);vals=[float(r['RMSD_A']) for r in exp];bars=ax[1].bar(xx,vals,color=['#59677A']*3+['#8DABC5']*3,width=.64)
ax[1].bar_label(bars,labels=[f'{y:.3f}' for y in vals],padding=3,fontsize=9);ax[1].set_xticks(xx,[r['source']+'–'+r['target'] for r in exp],rotation=25,ha='right',fontsize=9);ax[1].set_title('B  All six experimental-reference comparisons',loc='left',fontsize=11,fontweight='bold',pad=12)
for a in ax:
 a.set_ylim(0,4.65);a.set_ylabel('73-residue interface Cα RMSD (Å)');a.yaxis.set_major_locator(MultipleLocator(1));a.set_axisbelow(True);a.grid(axis='y',color='#D8DEE5',linewidth=.6,alpha=.75)
fig.subplots_adjust(left=.12,right=.98,top=.94,bottom=.10)
fig.savefig(O/'figures/Figure_1.png',dpi=300,facecolor='white');fig.savefig(O/'figures/Figure_1.svg',facecolor='white',metadata={'Date':'2026-11-03'});plt.close(fig)
print(json.dumps({'tables':len(tables),'numeric_cells_traced':len(numeric),'figure_rows':len(figdata),'figure_panels':2,'standalone_figure_pdf':False,'reason':'ReportLab embeds the 300-dpi PNG; SVG provides vector reuse. A separate Figure PDF would duplicate the same artifact without a typesetting dependency.'}))
