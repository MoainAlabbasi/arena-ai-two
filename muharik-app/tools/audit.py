#!/usr/bin/env python3
"""Check generated pages and curated part numbers against the extracted text.
This is a consistency check, not verification of diagnosis or part compatibility.
Run from muharik-app: python3 tools/audit.py
"""
import json, re
from pathlib import Path
root=Path(__file__).resolve().parent.parent
pages=json.loads((root/'data/pages.json').read_text(encoding='utf-8'))
parts=json.loads((root/'data/parts.json').read_text(encoding='utf-8'))
assert len(pages)==56
for i,p in enumerate(pages,1):
    assert p['number']==i
    assert (root/p['image']).is_file(),p['image']
    assert p['text'].strip(),i
for p in parts:
    page=pages[p['page']-1]
    assert p['number'].casefold() in page['text'].casefold(),(p['number'],p['page'])
print('OK: 56 pages, 56 images,',len(parts),'part numbers found on the cited pages.')
print('This check does NOT establish model compatibility or clinical/engineering accuracy.')
