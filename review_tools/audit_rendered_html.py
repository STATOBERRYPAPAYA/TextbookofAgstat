from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'review_tools/final_rendered')
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.links=[];self.images=[];self.duplicates=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:self.duplicates.append(a['id'])
            self.ids.add(a['id'])
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='img' and a.get('src'):self.images.append(a['src'])
pages={}
for p in ROOT.glob('*.qmd'):
    html=OUT/(p.stem+'.html')
    if html.exists():
        parser=Page();parser.feed(html.read_text(encoding='utf-8'));pages[html.resolve()]=parser
issues=[];checked=0
for p,parsed in pages.items():
    for link in parsed.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        if not u.path:target=p
        elif u.path.startswith('/'):target=(OUT/unquote(u.path.lstrip('/'))).resolve()
        else:target=(p.parent/unquote(u.path)).resolve()
        checked+=1
        if not target.exists():issues.append(f'{p.name}: missing local link {link}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            issues.append(f'{p.name}: missing rendered anchor {link}')
    for src in parsed.images:
        u=urlsplit(src)
        if u.scheme or u.netloc:continue
        target=(OUT/u.path.lstrip('/')).resolve() if u.path.startswith('/') else (p.parent/unquote(u.path)).resolve()
        if not target.exists():issues.append(f'{p.name}: missing image {src}')
    for i in parsed.duplicates:issues.append(f'{p.name}: duplicate HTML id {i}')
result={'pages':len(pages),'local_links_checked':checked,'issues':issues}
(ROOT/'review_tools'/'rendered_html_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
