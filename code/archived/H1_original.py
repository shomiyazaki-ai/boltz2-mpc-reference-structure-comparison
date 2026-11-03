exec(open('/mnt/data/C01_work/run.py').read().split('checks=[]')[0])
from MDAnalysis.analysis.helix_analysis import helix_analysis
out='/mnt/data/C01_work/results'; vals=[];axes=[]
def normal(v):return v/np.linalg.norm(v)
for s in files:
 for role,(lo,hi),hinge in [('MPC1L',(26,48),33),('MPC2',(40,61),53)]:
  xyz=coords(s,[(role,i) for i in range(lo,hi+1)]); loc=helix_analysis(xyz)['local_axes'];starts=np.arange(lo,hi-2)
  direction=xyz[-1]-xyz[0]; oriented=np.array([normal(a)*np.sign(a@direction) for a in loc]);left=oriented[starts<=hinge-4];right=oriented[starts>=hinge+1]
  def angle(l,r):return float(np.degrees(np.arccos(np.clip(normal(l.mean(axis=0))@normal(r.mean(axis=0)),-1,1))))
  full=angle(left,right)
  cases=[angle(l,r) for l in (left,left[1:],left[:-1]) for r in (right,right[1:],right[:-1]) if len(l)>=2 and len(r)>=2]
  maximum=max(abs(t-full) for t in cases)
  vals.append({'structure':s,'role':role,'window_start':lo,'window_end':hi,'hinge':hinge,'n_left':len(left),'n_right':len(right),'bend_angle_deg':full,'max_end_axis_perturbation_deg':maximum,'flag':'H1_NUMERIC_SENSITIVITY_GT5' if maximum>5 else 'NO_GT5_FLAG','left_mean_resultant_length':np.linalg.norm(left.mean(axis=0)),'right_mean_resultant_length':np.linalg.norm(right.mean(axis=0))})
  for idx,a in zip(starts,oriented):axes.append({'structure':s,'role':role,'start_residue':idx,'axis_x':a[0],'axis_y':a[1],'axis_z':a[2],'zone':'left' if idx<=hinge-4 else 'right' if idx>=hinge+1 else 'excluded_hinge_adjacent'})
write('H1_HELANAL_angles_stability.csv',vals);write('H1_HELANAL_local_axes.csv',axes)
print([(v['structure'][:5],v['role'],round(v['bend_angle_deg'],3),round(v['max_end_axis_perturbation_deg'],3)) for v in vals])
