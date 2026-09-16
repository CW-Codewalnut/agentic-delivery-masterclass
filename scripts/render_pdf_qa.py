#!/usr/bin/env python3
"""Render every PDF page and a numbered contact sheet for visual QA."""
from pathlib import Path
import argparse
import json
import fitz
from PIL import Image, ImageDraw

p=argparse.ArgumentParser();p.add_argument("pdf",type=Path);p.add_argument("--out",type=Path,default=Path("qa/pdf-pages"));a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=True)
doc=fitz.open(a.pdf)
images=[]
for n,page in enumerate(doc):
    pix=page.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False)
    target=a.out/f"page-{n+1:02d}.png";pix.save(target);images.append(Image.open(target).convert("RGB"))
thumb_w=480;thumb_h=int(images[0].height*thumb_w/images[0].width);cols=2;rows=(len(images)+1)//2
sheet=Image.new("RGB",(cols*thumb_w,rows*(thumb_h+34)),"#071016");draw=ImageDraw.Draw(sheet)
for n,img in enumerate(images):
    x=(n%cols)*thumb_w;y=(n//cols)*(thumb_h+34);sheet.paste(img.resize((thumb_w,thumb_h)),(x,y));draw.text((x+12,y+thumb_h+8),f"{n+1:02d}",fill="#58d2df")
contact=a.out.parent/"pdf-contact-sheet.jpg";sheet.save(contact,quality=88)
report={"pdf":a.pdf.as_posix(),"pages":len(doc),"rendered":[(a.out/f"page-{n+1:02d}.png").as_posix() for n in range(len(doc))],"contactSheet":contact.as_posix(),"renderScale":1.4}
(a.out.parent/"pdf-render-report.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report))
