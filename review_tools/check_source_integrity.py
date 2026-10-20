from pathlib import Path
import re,subprocess,json
ROOT=Path(__file__).resolve().parents[1]
report={'chapters':[],'issues':[],'code_changes':[]}
bib=(ROOT/'book.bib').read_text(encoding='utf-8')
bibkeys=set(re.findall(r'@\w+\s*\{\s*([^,\s]+)',bib))
for p in sorted(ROOT.glob('*.qmd')):
    t=p.read_text(encoding='utf-8')
    old=subprocess.run(['git','show',f'HEAD:{p.name}'],cwd=ROOT,capture_output=True).stdout.decode('utf-8').replace('\r\n','\n')
    fence=chr(96)*3
    pattern=r'(?ms)^'+fence+r'.*?^'+fence+r'[^\n]*'
    before=re.findall(pattern,old);after=re.findall(pattern,t)
    if before!=after:report['code_changes'].append(p.name)
    if any(ord(c)<32 and c not in '\n\r\t' for c in t):report['issues'].append(f'Control character in {p.name}')
    body=re.sub(pattern,'',t)
    stack=[]
    for i,l in enumerate(body.splitlines(),1):
        if re.match(r'^:{3,}\s+\{',l):stack.append(i)
        elif re.match(r'^:{3,}\s*$',l):
            if stack:stack.pop()
            else:report['issues'].append(f'Unmatched div closing in {p.name}, stripped line {i}')
    if stack:report['issues'].append(f'Unclosed div in {p.name}, stripped lines {stack}')
    for key in re.findall(r'(?<!\w)@([A-Za-z][\w.-]*)',body):
        key=key.rstrip('.')
        if not re.match(r'(fig|tbl|eq|sec|exm|exr|thm|def|lst)-',key) and key not in bibkeys:
            report['issues'].append(f'Missing bibliography key {key} in {p.name}')
    q=re.search(r'### Fill in the blanks[^\n]*\n(.*?)(?=### )',t,re.S)
    a=re.search(r'### Answers to fill in the blanks[^\n]*\n(.*?)(?=### |\Z)',t,re.S)
    n=len(re.findall(r'^\d+\. ',q[1],re.M)) if q else 0
    ka=len(re.findall(r'\x60\d+\.\x60',a[1])) if a else 0
    if n!=ka:report['issues'].append(f'Question/key count mismatch {p.name}: {n}/{ka}')
    nums=re.search(r'### Numerical and conceptual questions[^\n]*\n(.*?)(?=### )',t,re.S)
    sols=re.search(r'### Solutions to numerical and conceptual questions[^\n]*\n(.*?)(?=::: \{\.callout|\Z)',t,re.S)
    qnums=re.findall(r'^(\d+)\. ',nums[1],re.M) if nums else []
    snums=re.findall(r'^(\d+)\.\s+',sols[1],re.M) if sols else []
    if qnums!=snums:report['issues'].append(f'Numerical question/solution numbering mismatch {p.name}: {qnums}/{snums}')
    if n:report['chapters'].append({'file':p.name,'conceptual_blanks':n,'numerical_questions':len(qnums)})
report['total_conceptual_questions']=sum(x['conceptual_blanks'] for x in report['chapters'])
(ROOT/'review_tools'/'source_integrity.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='chapters'},indent=2))
print(f'{len(report["chapters"])} chapters have matching conceptual question sections.')
