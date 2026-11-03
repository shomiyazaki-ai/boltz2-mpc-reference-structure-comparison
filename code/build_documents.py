"""Rebuild the two PDFs from editable Markdown and verified table metadata.
Requires ReportLab/Pillow and DejaVu TrueType fonts. No scientific computation.
"""
from pathlib import Path
import matplotlib
import re,argparse,json,html,os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,LongTable,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT,TA_CENTER
from reportlab.lib.colors import HexColor,white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--out-dir',type=Path,default=ROOT/'manuscript');p.add_argument('--font-dir',type=Path,default=Path(os.environ.get('C01_FONT_DIR',str(Path(matplotlib.get_data_path())/'fonts/ttf'))));args=p.parse_args();args.out_dir.mkdir(parents=True,exist_ok=True)
for name,file in [('C01','DejaVuSans.ttf'),('C01-Bold','DejaVuSans-Bold.ttf'),('C01-Italic','DejaVuSans-Oblique.ttf'),('C01-BoldItalic','DejaVuSans-BoldOblique.ttf')]:
 path=args.font_dir/file
 if not path.is_file():raise FileNotFoundError('Provide DejaVu fonts via --font-dir or C01_FONT_DIR: '+str(path))
 pdfmetrics.registerFont(TTFont(name,str(path)))
pdfmetrics.registerFontFamily('C01',normal='C01',bold='C01-Bold',italic='C01-Italic',boldItalic='C01-BoldItalic')
styles=getSampleStyleSheet();navy=HexColor('#173B5B');gray=HexColor('#53616D')
styles.add(ParagraphStyle('CBody',fontName='C01',fontSize=9.7,leading=14.0,spaceAfter=7.2,textColor=HexColor('#18232D'),allowWidows=0,allowOrphans=0))
styles.add(ParagraphStyle('CTitle',fontName='C01-Bold',fontSize=18.3,leading=24.1,spaceBefore=4,spaceAfter=16,textColor=navy,keepWithNext=True))
styles.add(ParagraphStyle('CH1',fontName='C01-Bold',fontSize=13.2,leading=17.3,spaceBefore=14,spaceAfter=8,textColor=navy,keepWithNext=True))
styles.add(ParagraphStyle('CH2',fontName='C01-Bold',fontSize=10.8,leading=14.3,spaceBefore=11,spaceAfter=6,textColor=navy,keepWithNext=True))
styles.add(ParagraphStyle('CCaption',fontName='C01',fontSize=8.25,leading=11.3,spaceAfter=8,spaceBefore=3,textColor=gray))
styles.add(ParagraphStyle('CTableTitle',fontName='C01-Bold',fontSize=9,leading=12.0,spaceBefore=9,spaceAfter=6,textColor=navy,keepWithNext=True))
styles.add(ParagraphStyle('CTable',fontName='C01',fontSize=7.7,leading=10.5,textColor=HexColor('#142B3D'),splitLongWords=True))
styles.add(ParagraphStyle('CTableHead',parent=styles['CTable'],fontName='C01-Bold',textColor=white,fontSize=7.4,leading=10.0))
styles.add(ParagraphStyle('CCode',fontName='C01',fontSize=8.2,leading=11.5,leftIndent=8,spaceAfter=7,textColor=navy))
styles.add(ParagraphStyle('CReference',parent=styles['CBody'],fontSize=8.4,leading=12,spaceAfter=7))
# SimpleDocTemplate's frame has 6-point left/right padding inside the margins.
width=A4[0]-88-12
payload=json.loads((ROOT/'data/derived/table_payload.json').read_text())
def inline(s):
 s=html.escape(s)
 s=re.sub(r'`([^`]+)`',r'<font color="#173B5B">\1</font>',s)
 s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<link href="\2" color="#235789">\1</link>',s)
 return s
class NumberCanvas(canvas.Canvas):
 def __init__(self,*a,**k):
  k['invariant']=1;super().__init__(*a,**k);self._states=[]
 def showPage(self):self._states.append(dict(self.__dict__));self._startPage()
 def save(self):
  total=len(self._states)
  for state in self._states:
   self.__dict__.update(state);self.setStrokeColor(HexColor('#CDD7E0'));self.setLineWidth(.5);self.line(44,35,A4[0]-44,35);self.setFont('C01',7.1);self.setFillColor(gray);self.drawString(44,23,'C01 A+B | v1.0.0 | Zenodo DOI 10.5281/zenodo.23910491 (reserved)');self.drawRightString(A4[0]-44,23,str(self._pageNumber)+' / '+str(total));super().showPage()
  super().save()
def render(src,out):
 lines=src.read_text().splitlines();story=[];i=0;is_si='Supplementary' in src.name;intable=False;tableid=None
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line=='<!-- PAGEBREAK -->':story.append(PageBreak());i+=1;continue
  if line.startswith('<!-- TABLE '):
   if line.endswith(' START -->'):tableid=line.split()[2]
   elif line.endswith(' END -->'):tableid=None
   i+=1;continue
  if line.startswith('<!--'):i+=1;continue
  if line.startswith('# '):story.append(Paragraph(inline(line[2:]),styles['CTitle']));i+=1;continue
  if line.startswith('## '):story.append(Paragraph(inline(line[3:]),styles['CH1']));i+=1;continue
  if line.startswith('### '):story.append(Paragraph(inline(line[4:]),styles['CH2']));i+=1;continue
  if line.startswith('!['):
   match=re.match(r'!\[.*?\]\((.*?)\)',line);path=(src.parent/match.group(1)).resolve();img=Image(str(path));draw_width=min(width,490);scale=draw_width/img.imageWidth;img.drawWidth=draw_width;img.drawHeight=img.imageHeight*scale;img.hAlign='CENTER'
   j=i+1
   while j<len(lines) and not lines[j].strip():j+=1
   if j<len(lines) and lines[j].strip().startswith('**Figure '):
    story.append(KeepTogether([img,Spacer(1,6),Paragraph(inline(lines[j].strip()),styles['CCaption'])]));i=j+1
   else:story.append(img);story.append(Spacer(1,6));i+=1
   continue
  if line.startswith('|'):
   block=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    row=[s.strip() for s in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',s) for s in row):block.append(row)
    i+=1
   widths=payload.get(tableid,{}).get('widths');n=len(block[0]);cw=[x*width for x in widths] if widths else [width/n]*n
   cells=[[Paragraph(inline(c),styles['CTableHead' if ri==0 else 'CTable']) for c in row] for ri,row in enumerate(block)]
   note=payload.get(tableid,{}).get('note','')
   if note:
    cells.append([Paragraph(inline(note),styles['CCaption'])]+['']*(n-1))
   tab=LongTable(cells,colWidths=cw,repeatRows=1,hAlign='LEFT',splitByRow=True)
   tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5),('LINEBELOW',(0,0),(-1,0),.6,navy),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F1F5F8')]),('LINEBELOW',(0,1),(-1,-1),.25,HexColor('#DAE2E9'))]))
   if note:
    last=len(cells)-1
    tab.setStyle(TableStyle([('SPAN',(0,last),(n-1,last)),('BACKGROUND',(0,last),(n-1,last),white),('LEFTPADDING',(0,last),(n-1,last),0),('RIGHTPADDING',(0,last),(n-1,last),0),('LINEBELOW',(0,last),(n-1,last),0,white),('NOSPLIT',(0,last-1),(n-1,last))]))
    # Skip the same italic note in the editable Markdown; it is already
    # attached to the table's final row to prevent an orphan note.
    j=i
    while j<len(lines) and not lines[j].strip():j+=1
    if j<len(lines) and lines[j].strip()=='*'+note+'*':i=j+1
   story.append(tab);story.append(Spacer(1,4));continue
  # Paragraph including explicit Markdown hard line-breaks in author blocks.
  buff=[lines[i]];i+=1
  while i<len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(('#','|','![','<!--','- ')):
   buff.append(lines[i]);i+=1
  if line.startswith('- '):buff[0]='• '+buff[0][2:]
  text=''
  for j,s in enumerate(buff):
   text+=inline(s.strip())
   if j<len(buff)-1:text+=('<br/>' if s.endswith('  ') else ' ')
  style=styles['CBody']
  if line.startswith('**Table '):style=styles['CTableTitle']
  elif line.startswith('**Figure '):style=styles['CCaption']
  elif tableid and line.startswith('*'):style=styles['CCaption']
  elif re.match(r'^\[\d+\]',line):style=styles['CReference']
  story.append(Paragraph(text,style))
 doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=43,bottomMargin=48,title=('Supplementary Information: ' if is_si else '')+'Experimental-Reference Sensitivity of a Fixed Boltz-2 MPC1L–MPC2 Complex Prediction, with an Exploratory AlphaFold Structural Comparison',author='Sho Miyazaki',subject='C01 A+B Technical Note v1.0.0, reserved Zenodo DOI 10.5281/zenodo.23910491; unpublished',creator='C01 reproducible ReportLab builder')
 doc.build(story,canvasmaker=NumberCanvas)
for name in ['C01_AB_Technical_Note_v1.0.0','C01_AB_Supplementary_Information_v1.0.0']:
 src=ROOT/'manuscript'/f'{name}.md';dest=args.out_dir/f'{name}.pdf';render(src,dest);print(str(dest))
