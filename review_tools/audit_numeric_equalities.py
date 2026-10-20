"""Conservative scan of closed numeric LaTeX equalities, for editorial review."""
from pathlib import Path
import re,ast,operator,json,math
root=Path(__file__).resolve().parents[1]
ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}
def calc(node):
    if isinstance(node,ast.Expression):return calc(node.body)
    if isinstance(node,ast.Constant) and isinstance(node.value,(int,float)):return node.value
    if isinstance(node,ast.BinOp) and type(node.op) in ops:return ops[type(node.op)](calc(node.left),calc(node.right))
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):return calc(node.operand)*(-1 if isinstance(node.op,ast.USub) else 1)
    raise ValueError()
def group(s,i):
    if s[i]!='{':raise ValueError()
    level=1;j=i+1
    while j<len(s) and level:
        if s[j]=='{':level+=1
        if s[j]=='}':level-=1
        j+=1
    if level:raise ValueError()
    return s[i+1:j-1],j
def convert(s):
    s=s.replace('−','-').replace('×','*').replace('÷','/')
    s=re.sub(r'\\(?:left|right|,|;|!|quad|qquad| )','',s)
    s=s.replace(r'\times','*').replace(r'\cdot','*')
    while re.search(r'\\(?:d?frac|sqrt)',s):
        m=re.search(r'\\(d?frac|sqrt)',s);i=m.end()
        a,j=group(s,i)
        if m[1]=='sqrt':new='(('+convert(a)+')**0.5)'
        else:
            b,j=group(s,j);new='(('+convert(a)+')/('+convert(b)+'))'
        s=s[:m.start()]+new+s[j:]
    s=s.replace('{','(').replace('}',')').replace('^','**')
    s=re.sub(r'(?<=[0-9)])\s*(?=\()', '*',s)
    s=re.sub(r'(?<=\))\s*(?=[0-9])','*',s)
    if re.search(r'[^0-9.\s()+*/-]',s):raise ValueError()
    return s
checked=[];flags=[]
for p in root.glob('*.qmd'):
    fence=chr(96)*3
    t=re.sub(r'(?ms)^'+fence+r'.*?^'+fence+r'[^\n]*','',p.read_text(encoding='utf-8'))
    for m in re.finditer(r'\${1,2}([^$]+)\${1,2}',t):
        s=m[1]
        if '\n' in s and len(s)>300:continue
        parts=re.split(r'=|\\approx',s)
        if len(parts)<2:continue
        for a,b in zip(parts,parts[1:]):
            try:
                av=calc(ast.parse(convert(a),mode='eval'));bv=calc(ast.parse(convert(b),mode='eval'))
                if not math.isfinite(av) or not math.isfinite(bv):continue
                if abs(av)>1e12 or abs(bv)>1e12:continue
            except (ValueError,SyntaxError,ZeroDivisionError,OverflowError,IndexError):continue
            item={'file':p.name,'expression':a+' = '+b,'left':av,'right':bv}
            checked.append(item)
            if abs(av-bv)>max(.015,.001*max(abs(av),abs(bv))):flags.append(item)
(root/'review_tools/numeric_equality_audit.json').write_text(json.dumps({'checked':len(checked),'flags':flags,'scope':'Closed numeric equalities only; not a verification of symbolic formulae or complete worked examples.'},indent=2),encoding='utf-8')
print(json.dumps({'checked':len(checked),'flags':flags},indent=2))
