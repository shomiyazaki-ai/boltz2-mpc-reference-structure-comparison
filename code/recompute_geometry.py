"""Recalculate all 105 fixed metrics, masks and contacts from original six CIFs."""
from cif_geometry import *
import argparse,itertools,platform,sys
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
S=load_all();m=json.loads((ROOT/'data/frozen/masks.json').read_text());checks=[]
def ck(name,v):
 checks.append({'check':name,'pass':bool(v)})
 if not v:raise AssertionError(name)
for k,n in [('73',73),('62',62),('198',198)]:ck('mask_count_'+k,len(mask_keys(m,k))==n)
for row in read_csv(ROOT/'data/frozen/crosswalk_6x198.csv'):
 a=S[row['structure']][row['protein']][int(row['residue'])]['CA']
 ck('crosswalk_'+row['structure']+'_'+row['protein']+row['residue'],a['label_comp_id']==row['aa3'] and a['label_asym_id']==row['chain'] and a['auth_seq_id']==row['auth_seq'])
for p in ['MPC1L','MPC2']:ck('subset_'+p,set(m['62'][p])<=set(m['73'][p])<=set(m['198'][p]))
# Fixed geometric controls before measuring the biological inputs.
x=np.array([[0.,1.,2.],[3.,4.,1.],[5.,2.,1.],[2.,3.,8.],[1.,7.,3.]])
r=np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]])
y=x@r+np.array([17.,-3.,8.]);rr,t=fit(x,y)
ck('known_rigid_transform',rms(x@rr+t,y)<1e-10);ck('proper_rotation',abs(np.linalg.det(rr)-1)<1e-10)
rr,t=fit(x[::-1],y[::-1]);ck('fit_order_invariance',rms(x@rr+t,y)<1e-10)
rr,t=fit(x,x);ck('identity',rms(x@rr+t,x)<1e-10)
ck('swapped_protein_negative_control',any(S[BOLTZ]['MPC1L'][i]['CA']['label_comp_id']!=S['9GIX']['MPC2'].get(i,{}).get('CA',{}).get('label_comp_id') for i in m['198']['MPC1L']))
ck('residue_shift_negative_control',any(S[BOLTZ]['MPC1L'][i]['CA']['label_comp_id']!=S['9GIX']['MPC1L'].get(i+1,{}).get('CA',{}).get('label_comp_id') for i in m['198']['MPC1L']))
rows=read_csv(ROOT/'data/results/primary_70_metrics.csv')+read_csv(ROOT/'data/results/AF_35_metrics.csv');defs={n:(f,e) for n,f,e in spec(m)};res=[]
for a in rows:
 f,e=defs[a['metric']];R,t=fit(xyz(S,a['source'],f),xyz(S,a['target'],f));v=rms(xyz(S,a['source'],e)@R+t,xyz(S,a['target'],e));d=abs(v-float(a['RMSD_A']))
 ck('metric_'+str(len(res)+1),d<=1e-5 and abs(np.linalg.det(R)-1)<1e-10)
 res.append(dict(source=a['source'],target=a['target'],metric=a['metric'],canonical_RMSD_A=a['RMSD_A'],recalculated_RMSD_A=v,abs_difference_A=d,det_rotation=np.linalg.det(R),pass_=True))
write_csv(out/'RMSD_105_recomputed.csv',res)
contacts=[];counts=[]
for cutoff,mask,total,common in [(5.,'73',107,37),(4.,'62',69,13)]:
 sets=[]
 for n in REFS:
  pairs=set()
  for i in m['198']['MPC1L']:
   aa=[a for a in S[n]['MPC1L'][i].values() if a['type_symbol'].upper() not in ('H','D')]
   for j in m['198']['MPC2']:
    bb=[a for a in S[n]['MPC2'][j].values() if a['type_symbol'].upper() not in ('H','D')]
    dd=np.sum((np.array([a['xyz'] for a in aa])[:,None,:]-np.array([b['xyz'] for b in bb])[None,:,:])**2,axis=2)
    ai,bi=np.unravel_index(dd.argmin(),dd.shape);dist=float(np.sqrt(dd[ai,bi]))
    if dist<cutoff:
     pairs.add((i,j));contacts.append({'threshold':int(cutoff),'structure':n,'mpc1l':i,'mpc2':j,'distance_A':dist,'mpc1l_atom':aa[ai]['label_atom_id'],'mpc2_atom':bb[bi]['label_atom_id']})
  sets.append(pairs);counts.append({'cutoff':cutoff,'structure':n,'count':len(pairs)})
 union=set.union(*sets);inter=set.intersection(*sets)
 ck('union_contact_pairs_'+mask,len(union)==total);ck('intersection_pairs_'+mask,len(inter)==common)
 ck('mask_residues_'+mask,{i for i,j in union}==set(m[mask]['MPC1L']) and {j for i,j in union}==set(m[mask]['MPC2']))
old=read_csv(ROOT/'data/results/contact_counts.csv');ck('per_reference_contact_counts',all(int(a['count'])==int(b['count']) and a['structure']==b['structure'] for a,b in zip(old,counts)))
oldc=read_csv(ROOT/'data/results/experimental_contacts.csv');key=lambda a:(int(float(a['threshold'])),a['structure'],int(a['mpc1l']),int(a['mpc2']))
a={key(r):r for r in oldc};b={key(r):r for r in contacts};ck('all_contact_identities',a.keys()==b.keys());delta=max(abs(float(a[k]['distance_A'])-float(b[k]['distance_A'])) for k in a);ck('all_contact_distances',delta<1e-8)
write_csv(out/'contacts_recomputed.csv',contacts);write_csv(out/'checks.csv',checks)
summary={'status':'PASS','metric_count':len(res),'max_abs_RMSD_difference_A':max(a['abs_difference_A'] for a in res),'contact_rows':len(contacts),'contact_max_distance_difference_A':delta,'checks':len(checks),'method':'proper SVD fit; separate from quaternion verifier','python':platform.python_version(),'numpy':np.__version__}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
