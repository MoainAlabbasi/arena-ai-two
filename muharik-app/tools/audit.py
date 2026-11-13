#!/usr/bin/env python3
"""Check generated content and source references, not engineering suitability."""
import json, re
from pathlib import Path
root=Path(__file__).resolve().parent.parent
def load(name): return json.loads((root/'data'/name).read_text(encoding='utf-8'))
pages,parts,components,terms=map(load,['pages.json','parts.json','components.json','terms.json'])
assert len(pages)==56
for i,p in enumerate(pages,1):
    assert p['number']==i
    assert (root/p['image']).is_file(),p['image']
    assert p['text'].strip(),i
for p in parts:
    assert p['number'].casefold() in pages[p['page']-1]['text'].casefold(),(p['number'],p['page'])
clean=lambda s: re.sub(r'[^a-z0-9]+','',s.lower())
for group in (components,terms):
    for row in group:
        assert clean(row['english']) in clean(pages[row['page']-1]['text']),(row['english'],row['page'])
assert len(components)==53 and len(terms)==41
print(f'OK: {len(pages)} pages; {len(parts)} part numbers; {len(components)} diagram labels; {len(terms)} technical terms.')
print('English source phrases found on cited pages. This does not validate translations, compatibility, or repairs.')
