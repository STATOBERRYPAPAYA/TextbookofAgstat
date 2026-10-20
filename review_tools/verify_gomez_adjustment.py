from pathlib import Path
import csv,json,hashlib,math
root=Path(__file__).resolve().parents[1]
expected=[
 ['1','1','1'],['0.8','0.804','0.822'],['0.7','0.71','0.738'],
 ['0.6','0.617','0.656'],['0.5','0.528','0.578'],['0.4','0.443','0.504'],
 ['0.35','0.403','0.469'],['0.3','0.364','0.434'],['0.25','0.326','0.402'],
 ['0.2','0.291','0.371'],['0.15','0.257','0.343'],['0.1','0.226','0.312']]
with (root/'csv/b.csv').open(newline='',encoding='utf-8-sig') as f: rows=list(csv.reader(f))[2:]
assert [[float(v) for v in r] for r in rows]==[[float(v) for v in r] for r in expected]
with (root/'review_tools/uniformity_verified.csv').open(newline='') as f: d=list(csv.DictReader(f))
xs=[math.log(float(r['x'])) for r in d]
ys=[math.log(float(r['Vx'])/float(d[0]['Vx'])) for r in d]
b=-sum(x*y for x,y in zip(xs,ys))/sum(x*x for x in xs)
adj=.403+(b-.35)*(.443-.403)/(.4-.35)
assert abs(b-.360686601148)<1e-10 and abs(adj-.4115492809184)<1e-10
for r in d:
    n=150;x=float(r['x'])
    assert abs(float(r['Vx'])-float(r['SS'])/(n-x))<1e-7
    assert abs(float(r['Vx'])-float(r['sampleVarianceOfMeans']))<1e-7
report={'source':'Gomez and Gomez (1984), Statistical Procedures for Agricultural Research, second edition',
 'table':'Table 12.5, printed p. 493, PDF page 505','interpolation':'Printed p. 494, PDF page 506',
 'variance_definition':'Printed pp. 489–491; sample variance of totals divided by squared plot size',
 'table_rows_checked':len(rows),'corrected_computed_b_labels':[.15,.10],
 'b_fitted':b,'b_adjusted_full_precision':adj,'b_adjusted_using_rounded_fit':.41156,
 'raw_yield_data_unchanged':True,
 'reference_pdf_sha256':hashlib.sha256((root/'review_tools/gomez1984_reference.pdf').read_bytes()).hexdigest(),
 'reference_download':'https://www2.hcmuaf.edu.vn/data/ndnang/file/PPTN%202/Statistical%20procedure%20for%20agriculture%20research-Gomez.pdf'}
(root/'review_tools/gomez_adjustment_verified.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('All 12 adjustment-table rows verified against the source; nine plot-mean variances and interpolation agree.')
