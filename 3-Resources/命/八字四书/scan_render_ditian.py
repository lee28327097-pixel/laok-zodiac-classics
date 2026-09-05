# -*- coding: utf-8 -*-
"""滴天髓今註 轻 L2：术语密度扫描 + render 关键页（PyMuPDF）"""
import os, re, glob

ROOT = r"D:\国学命理库\3-Resources\命\八字四书"
OCR = os.path.join(ROOT, "transcript", "ocr_full")
PAGES = os.path.join(ROOT, "pages", "滴天髓今註")
PDF = r"E:\易经\周易2026\周易合集\易学\防和不断点\四柱八字命理\滴天髓 子平真詮 今註.pdf"
os.makedirs(PAGES, exist_ok=True)

# 滴天髓核心术语（理气/旺衰派关键词）
TERMS = ["旺衰","日主","用神","通關","通关","顺逆","寒暖","寒熱","燥湿","天道","地道",
         "人道","知命","理氣","理气","配合","形象","方局","八格","體用","体用","精神",
         "月提","生時","生时","中和","源流","官殺","官杀","傷官","伤官","清氣","清气",
         "濁氣","浊气","真神","假神","剛柔","刚柔","隱顯","隐显","眾寡","众寡","震兌","震兑",
         "離坎","离坎","強弱","强弱","得令","得地","得勢","得势","生扶","克洩","克泄",
         "陽刃","阳刃","比劫","食神","財星","财星","印綬","印绶","格局","富貴","富贵"]

def count_terms(txt):
    c = 0
    for t in TERMS:
        c += txt.count(t)
    return c

# 扫描密度
files = sorted(glob.glob(os.path.join(OCR, "滴天髓今註_p_*.txt")))
density = []
for f in files:
    try:
        txt = open(f, encoding="utf-8", errors="ignore").read()
    except: 
        continue
    pg = re.search(r"p_(\d+)", os.path.basename(f))
    if not pg: continue
    density.append((int(pg.group(1)), count_terms(txt), len(txt)))

density.sort(key=lambda x: -x[1])
print("=== 滴天髓今註 术语密度 Top 15 ===")
for pg, c, n in density[:15]:
    print(f"  p_{pg:03d}  术语命中={c:3d}  字数={n}")

# 重点页：头6 + 术语Top12（去重，限量）
top_pgs = [d[0] for d in density[:12]]
key_pgs = sorted(set([1,2,3,4,5,6] + top_pgs))
print("\n=== 准备 render 重点页 ===")
print(" ", [f"p_{p:03d}" for p in key_pgs])

# render
import fitz
doc = fitz.open(PDF)
print(f"\nPDF 总页数: {doc.page_count}")
for p in key_pgs:
    if p > doc.page_count: 
        print(f"  跳过 p_{p} (超页)")
        continue
    page = doc[p-1]
    pix = page.get_pixmap(dpi=200)
    out = os.path.join(PAGES, f"滴天髓今註_p_{p:03d}.png")
    pix.save(out)
    print(f"  ✓ {out}  ({pix.width}x{pix.height})")
print("\nDONE")
