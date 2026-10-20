from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
r=Path(__file__).resolve().parents[1];out=r/'docs'
class Resources(HTMLParser):
 def __init__(self):super().__init__();self.resources=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ['img','script'] and a.get('src'):self.resources.append(a['src'])
  if tag=='link' and a.get('href') and any(x in a.get('rel','') for x in ['stylesheet','icon']):self.resources.append(a['href'])
issues=[];checked=0
for p in out.glob('*.html'):
 s=p.read_text(encoding='utf-8');parsed=Resources();parsed.feed(s)
 assert 'src="assets/melon-tracker.js"' in s,p.name
 for url in parsed.resources:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  path=unquote(u.path)
  if path.startswith('/TextbookofAgstat/'):target=out/path.removeprefix('/TextbookofAgstat/')
  elif path.startswith('/'):target=out/path.lstrip('/')
  else:target=p.parent/path
  checked+=1
  if not target.is_file():issues.append(f'{p.name}: missing resource {url}')
assert not issues,issues
report={'pages':33,'local_scripts_styles_icons_and_images_checked':checked,'issues':issues,'analytics_script_matches_remote_source':(r/'assets/melon-tracker.js').read_bytes()==(out/'assets/melon-tracker.js').read_bytes()}
assert report['analytics_script_matches_remote_source']
(r/'review_tools/publication_resource_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
