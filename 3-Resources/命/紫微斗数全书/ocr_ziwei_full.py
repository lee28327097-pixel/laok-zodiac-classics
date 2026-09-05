# ocr_ziwei_full.py — 紫微斗数全书 全 265 页 L1 粗转录 (RapidOCR / onnxruntime, 支持繁体)
# 用法: venv python ocr_ziwei_full.py
# 特性: 每页独立存 p_NNN.txt (可断点续跑, 已存在则跳过); 汇总 ocr_all.txt
import fitz, numpy as np, os, time
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

SRC = r"E:/易经/周易2026/周易合集/易学/防和不断点/紫微斗数/紫微斗数全书-.pdf"
OUT_DIR = r"D:/国学命理库/3-Resources/命/紫微斗数全书/transcript/ocr_full"
os.makedirs(OUT_DIR, exist_ok=True)
MASTER = os.path.join(OUT_DIR, "ocr_all.txt")

print("启动 RapidOCR (繁体 ch_tra)...", flush=True)
engine = RapidOCR()

doc = fitz.open(SRC)
n = doc.page_count
print(f"总页数 {n}，开始逐页转录 (断点续跑, 已存在跳过)...", flush=True)

t0 = time.time()
done = 0
skipped = 0
with open(MASTER, "w", encoding="utf-8") as mf:
    mf.write(f"# 紫微斗数全书 — RapidOCR 全本粗转录 (L1)\n# 生成: {time.strftime('%Y-%m-%d %H:%M')}\n# 说明: 准确率约七成, 夹注/古字有错(如凶↔卤 諸↔諾 賦↔毒), 关键页以 L2 视觉精读校正\n\n")
    for i in range(n):
        out_path = os.path.join(OUT_DIR, f"p_{i+1:03d}.txt")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            skipped += 1
            done += 1
            continue
        pg = doc[i]
        pix = pg.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        arr = np.array(img)
        try:
            result, _ = engine(arr)
            lines = [text for (box, text, score) in result] if result else []
            text = "\n".join(lines)
        except Exception as e:
            text = f"[OCR_ERR p{i+1}: {e}]"
        with open(out_path, "w", encoding="utf-8") as pf:
            pf.write(text)
        mf.write(f"\n\n===== 第 {i+1} 页 =====\n{text}")
        done += 1
        if done % 10 == 0:
            print(f"  [{done}/{n}] 已用 {time.time()-t0:.0f}s (跳过 {skipped})", flush=True)
print(f"完成！共 {done} 页 (跳过已存在 {skipped} 页)，总时 {time.time()-t0:.0f}s。输出: {MASTER}", flush=True)
