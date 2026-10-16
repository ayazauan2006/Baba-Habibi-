from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,urllib.request
BASE='https://baba-48-from-aya.groovydeer11.chatgpt.site/'
def get(item):
    p=Path(item['path'])
    if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']:return
    request=urllib.request.Request(BASE+item['path'],headers={'User-Agent':'Mozilla/5.0 (compatible; FamilyAlbum/1.0)'})
    data=urllib.request.urlopen(request,timeout=90).read()
    assert hashlib.sha256(data).hexdigest()==item['sha256'],f'Hash mismatch: {p}'
    p.parent.mkdir(parents=True,exist_ok=True)
    temporary=p.with_suffix(p.suffix+'.tmp');temporary.write_bytes(data);temporary.replace(p)
items=json.loads(Path('media-manifest.json').read_text())
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(get,items))
print(f'All {len(items)} family album and audio assets verified.')
