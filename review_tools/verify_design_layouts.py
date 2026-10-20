from pathlib import Path
import xml.etree.ElementTree as ET
import csv,json,collections
root=Path(__file__).resolve().parents[1]
folder=root/'images/singlefactor'
def letters(name):
    return [''.join(e.itertext()).strip() for e in ET.parse(folder/name).iter()
            if e.tag.endswith('text') and ''.join(e.itertext()).strip() in list('ABCDEF')]
def matrix(xs,n): return [xs[i:i+n] for i in range(0,len(xs),n)]
def latin(rows):
    n=len(rows);target=set('ABCDEF'[:n])
    assert all(set(r)==target for r in rows)
    assert all(set(c)==target for c in zip(*rows))
base=matrix(letters('lsdlayout.svg'),6)
row=matrix(letters('lsdlayout1.svg'),6)
col=matrix(letters('lsd_layout2.svg'),6)
for rows in (base,row,col): latin(rows)
assert row==[base[i-1] for i in [1,3,5,2,6,4]]
assert col==[[r[i-1] for i in [3,1,2,5,6,4]] for r in row]
crd=letters('layoutcrd.svg')
assert collections.Counter(crd)==dict.fromkeys('ABCD',5)
with (root/'csv/crd_sequence.csv').open(newline='',encoding='utf-8-sig') as f:
    seq=list(csv.reader(f))
assert crd==seq[0][1:]+seq[2][1:]
# RCBD PNG read visually: each column is a block.
rcbd=[list(s) for s in ['BADC','CADB','ACBD','BCDA','BACD']]
assert all(set(b)==set('ABCD') for b in rcbd)
# Corrected introductory diagram: four treatments once in every block.
blocks=[['T1','T3','T4','T2'],['T3','T4','T2','T1'],
        ['T2','T4','T3','T1'],['T2','T3','T4','T1'],['T3','T2','T4','T1']]
assert all(set(b)=={'T1','T2','T3','T4'} for b in blocks)
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="550" viewBox="0 0 1050 550" role="img" aria-labelledby="title desc">',
       '<title id="title">Four treatments randomized within five complete blocks</title>',
       '<desc id="desc">Each vertical block contains treatments T1, T2, T3 and T4 exactly once. Blocks are perpendicular to the left-to-right fertility gradient.</desc>',
       '<rect width="1050" height="550" fill="white"/>',
       '<g font-family="Times New Roman,serif" text-anchor="middle" font-size="28" font-weight="bold">']
colors=['#e2efda','#c5e0b4','#a9d18e','#548235','#375623']
for c,block in enumerate(blocks):
    x=95+c*182
    parts.append(f'<text x="{x+91}" y="47">Block {c+1}</text>')
    parts.append(f'<path d="M{x+91} 58v45" stroke="#4472c4" stroke-width="2"/>')
    parts.append(f'<path d="M{x+85} 94l6 12 6-12z" fill="#4472c4"/>')
    for r,tr in enumerate(block):
        y=119+r*95
        parts.append(f'<rect x="{x}" y="{y}" width="182" height="95" fill="{colors[c]}" stroke="#111" stroke-width="4"/>')
        parts.append(f'<text x="{x+91}" y="{y+57}" fill="{"white" if c>2 else "#111"}">{tr}</text>')
parts.append('</g></svg>')
(root/'images/design/field2-corrected.svg').write_text('\n'.join(parts),encoding='utf-8')
report={'latin_squares':3,'row_permutation':[1,3,5,2,6,4],
        'column_permutation':[3,1,2,5,6,4],
        'crd_sequence_matches_layout':True,'crd_treatment_counts':dict(collections.Counter(crd)),
        'rcbd_layout_blocks':rcbd,'introductory_blocks_corrected':blocks,
        'scope':'Checks allocation restrictions and agreement with figures; a realised layout cannot prove the random process used to generate it.'}
(root/'review_tools/design_layout_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Three Latin squares, row/column permutations, CRD sequence and both RCBD layouts verified.')
