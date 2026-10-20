"""Inventory table arithmetic candidates; flags require statistical review."""
from pathlib import Path
from html.parser import HTMLParser
import re, json, sys
root=Path(__file__).resolve().parents[1]
class Tables(HTMLParser):
    def __init__(self):
        super().__init__(); self.tables=[]; self.table=None; self.row=None; self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='table': self.table=[]
        elif tag=='tr' and self.table is not None: self.row=[]
        elif tag in ('th','td') and self.row is not None: self.cell=''
    def handle_data(self,data):
        if self.cell is not None: self.cell+=data
    def handle_endtag(self,tag):
        if tag in ('th','td') and self.cell is not None:
            self.row.append(self.cell.strip()); self.cell=None
        elif tag=='tr' and self.row is not None:
            self.table.append(self.row); self.row=None
        elif tag=='table' and self.table is not None:
            self.tables.append(self.table); self.table=None
def number(s):
    s=s.replace(',','').strip()
    return float(s) if re.fullmatch(r'-?\d+(?:\.\d+)?',s) else None
flags=[]; checks=0
for p in (root/(sys.argv[1] if len(sys.argv)>1 else 'docs')).glob('*.html'):
    parser=Tables(); parser.feed(p.read_text(encoding='utf-8'))
    for ti,rows in enumerate(parser.tables):
        for i,row in enumerate(rows):
            if not row or not re.fullmatch(r'(?:grand\s+)?total',row[0],re.I): continue
            for j in range(1,len(row)):
                displayed=number(row[j])
                vals=[number(r[j]) for r in rows[:i] if len(r)>j]
                vals=[x for x in vals if x is not None]
                if displayed is None or len(vals)<2: continue
                checks+=1
                tol=max(.015,.0006*len(vals))
                if abs(sum(vals)-displayed)>tol:
                    flags.append(dict(page=p.name,table=ti+1,column=j+1,displayed=displayed,sum=sum(vals),header=rows[0],values=vals))
out={'candidate_total_columns':checks,'flags':flags,'note':'ANOVA component subtotals and mixed-unit tables can legitimately trigger flags. Review before changing.'}
(root/'review_tools/table_arithmetic_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
