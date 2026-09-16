#!/usr/bin/env python3
"""Verify embedded source files are byte-for-byte current."""
from pathlib import Path
import argparse
import hashlib
import html as html_lib
import json
import re
import sys

p=argparse.ArgumentParser();p.add_argument("--source-root",type=Path,required=True);p.add_argument("--html",type=Path,default=Path("web/index.html"));p.add_argument("--report",type=Path,default=Path("qa/source-parity.json"));a=p.parse_args()
text=a.html.read_text(encoding="utf-8")
match=re.search(r'<script id="masterclass-data" type="application/json">(.*?)</script>',text,re.S)
if not match: raise SystemExit("embedded data payload not found")
payload=json.loads(html_lib.unescape(match.group(1)))
embedded=payload["files"]
checks=[]
for rel,record in embedded.items():
    candidate=a.source_root/rel
    actual=candidate.read_text(encoding="utf-8") if candidate.is_file() else None
    digest=hashlib.sha256(actual.encode()).hexdigest() if actual is not None else None
    checks.append({"path":rel,"exists":actual is not None,"contentMatch":actual==record["content"],"sha256Match":digest==record["sha256"],"sha256":digest})
failures=[c for c in checks if not(c["exists"] and c["contentMatch"] and c["sha256Match"])]
report={"embeddedFiles":len(checks),"missingDeclaredByBuild":payload["missing"],"failures":failures,"status":"PASS" if not failures and not payload["missing"] else "FAIL","checks":checks}
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({k:report[k] for k in ("embeddedFiles","missingDeclaredByBuild","failures","status")}))
sys.exit(0 if report["status"]=="PASS" else 1)
