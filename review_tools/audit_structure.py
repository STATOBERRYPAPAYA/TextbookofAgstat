"""Static checks complement, but do not replace, a Quarto render."""
from pathlib import Path
import re, json, collections
ROOT=Path(__file__).resolve().parents[1]
files=list(ROOT.glob('*.qmd'))
labels=collections.defaultdict(list)
refs=[]
issues=[]
for path in files:
    text=path.read_text(encoding='utf-8')
    for pattern in [r'\{#([\w:.-]+)',r'^#\|\s*label:\s*[\'"]?([\w:.-]+)',r'^```\{r\s+([\w.-]+)\s*[,}]']:
        for m in re.finditer(pattern,text,re.M):
            labels[m[1]].append(f'{path.name}:{text[:m.start()].count(chr(10))+1}')
    for m in re.finditer(r'(?<![\w\\])@((?:fig|tbl|eq|sec|exm|exr|thm|def|lst)-[\w.-]*[\w-])', text):
        refs.append((m[1],f'{path.name}:{text[:m.start()].count(chr(10))+1}'))
    questions=re.search(r'### Fill in the blanks[^\n]*\n(.*?)(?=### )',text,re.S)
    key=re.search(r'### Answers to fill in the blanks[^\n]*\n(.*?)(?=### |\Z)',text,re.S)
    if questions:
        qnums=[int(x) for x in re.findall(r'^(\d+)\. ',questions[1],re.M)]
        knums=[int(x) for x in re.findall(r'`(\d+)\.`',key[1])] if key else []
        if qnums!=knums or qnums!=list(range(1,len(qnums)+1)):
            issues.append(f'Question/key numbering mismatch: {path.name}')
    fenced=False
    for i,line in enumerate(text.splitlines(),1):
        if line.startswith('```'): fenced=not fenced
        if not fenced and re.search(r'\$\$.*\$\$',line) and len(line)>180:
            issues.append(f'Wide display candidate ({len(line)} source characters): {path.name}:{i}')
result={'unresolved_explicit_references':[(x,loc) for x,loc in refs if x not in labels],
        'duplicate_labels':{k:v for k,v in labels.items() if len(v)>1},
        'structural_and_width_checks':issues,
        'note':'Wide equations are candidates only; PDF overflow requires the print build.'}
(ROOT/'review_tools'/'structure_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
