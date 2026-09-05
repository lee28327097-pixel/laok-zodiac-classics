# -*- coding: utf-8 -*-
"""八字四本 波1 OCR：渊海子平(157) + 滴天髓今註(122) = 279 页。
引擎：RapidOCR (onnxruntime)，已证实兼容 Py3.13，支持繁体，CPU 跑。
输出：<work>/transcript/ocr_full/<书名>_p_NNN.txt + <书名>_all.txt 汇总。
断点续跑：已存在同页 txt 跳过。
"""
import fitz, numpy as np, os, time
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

BOOKS = [
    (r"E:/易经/周易2026/周易合集/易学/防和不断点/四柱八字命理/刻京台增补渊海子平大全.pdf", "渊海子平"),
    (r"E:/易经/周易2026/周易合集/易学/防和不断点/四柱八字命理/滴天髓 子平真詮 今註.pdf", "滴天髓今註"),
]
OUT = r"D:/国学命理库/3-Resources/命/八字四书/transcript/ocr_full"
os.makedirs(OUT, exist_ok=True)

print("加载 RapidOCR (繁体)...", flush=True)
t0 = time.time()
engine = RapidOCR()
print(f"  加载 {time.time()-t0:.0f}s", flush=True)

for path, name in BOOKS:
    if not os.path.exists(path):
        print("!! 找不到", path, flush=True)
        continue
    doc = fitz.open(path)
    n = doc.page_count
    print(f"=== {name} 共 {n} 页，开始转录 ===", flush=True)
    all_lines = []
    done = 0
    for i in range(n):
        out = os.path.join(OUT, f"{name}_p_{i+1:03d}.txt")
        if os.path.exists(out) and os.path.getsize(out) > 0:
            done += 1
            continue
        pg = doc[i]
        pix = pg.get_pixmap(dpi=150)
        arr = np.array(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
        result, elapse = engine(arr)
        lines = [text for box, text, score in result] if result else []
        txt = "\n".join(lines)
        with open(out, "w", encoding="utf-8") as f:
            f.write(txt)
        all_lines.append(txt)
        if (i + 1) % 20 == 0 or (i + 1) == n:
            print(f"  {name} 已处理 {i+1}/{n} 页", flush=True)
    # 汇总（含跳过已存在页）
    if not all_lines:
        for i in range(n):
            p = os.path.join(OUT, f"{name}_p_{i+1:03d}.txt")
            if os.path.exists(p):
                all_lines.append(open(p, encoding="utf-8").read())
    with open(os.path.join(OUT, f"{name}_all.txt"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_lines))
    print(f"=== {name} 完成 {n} 页（新增 {n-done}）===", flush=True)

print("全部完成", flush=True)
