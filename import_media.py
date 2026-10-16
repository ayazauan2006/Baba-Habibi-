from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,urllib.request
BASE="https://baba-48-from-aya.groovydeer11.chatgpt.site/"
def get(item):
    p=Path(item["path"])
    if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==item["sha256"]: return
    data=urllib.request.urlopen(BASE+item["path"],timeout=60).read()
    assert hashlib.sha256(data).hexdigest()==item["sha256"],p
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
with ThreadPoolExecutor(max_workers=6) as pool: list(pool.map(get,json.loads(Path("media-manifest.json").read_text())))
print("All 61 photographs, 3 videos and 3 posters verified.")
