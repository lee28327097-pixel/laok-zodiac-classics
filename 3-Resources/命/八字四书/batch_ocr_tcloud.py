#!/usr/bin/env python3
# 批量调用腾讯云通用文字识别（高精度版）重 OCR 滴天髓今註 18 张关键页
# 依赖: tencentcloud-sdk-python（须先 pip install）
# 环境变量: TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY
import os, base64, glob, io, sys
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import models, ocr_client

PNG_DIR = r"D:\国学命理库\3-Resources\命\八字四书\pages\滴天髓今註"
OUT_DIR = r"D:\国学命理库\3-Resources\命\八字四书\transcript\ocr_tcloud"
os.makedirs(OUT_DIR, exist_ok=True)

sid = os.environ.get("TENCENTCLOUD_SECRET_ID")
skey = os.environ.get("TENCENTCLOUD_SECRET_KEY")
if not sid or not skey:
    print("错误: 请先设置 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
    sys.exit(1)

cred = credential.Credential(sid, skey)
http = HttpProfile(); http.endpoint = "ocr.tencentcloudapi.com"
cpf = ClientProfile(); cpf.httpProfile = http; cpf.request_client = "Skills"
client = ocr_client.OcrClient(cred, "ap-guangzhou", cpf)

MAX_BYTES = 9 * 1024 * 1024

def get_b64(path):
    raw = open(path, "rb").read()
    if len(raw) <= MAX_BYTES:
        return base64.b64encode(raw).decode("utf-8"), "png"
    # 超限则用 PyMuPDF 重渲低 DPI 转 JPEG
    import fitz
    doc = fitz.open(path)
    pix = doc[0].get_pixmap(dpi=120)
    buf = pix.tobytes("jpeg")
    return base64.b64encode(buf).decode("utf-8"), "jpeg(compressed)"

results = {}
files = sorted(glob.glob(os.path.join(PNG_DIR, "滴天髓今註_p_*.png")))
print(f"共 {len(files)} 页待 OCR")
for png in files:
    name = os.path.basename(png)
    pg = name.replace("滴天髓今註_p_", "").replace(".png", "")
    try:
        b64, tag = get_b64(png)
        req = models.GeneralAccurateOCRRequest()
        req.ImageBase64 = b64
        resp = client.GeneralAccurateOCR(req)
        text = "\n".join(t.DetectedText or "" for t in (resp.TextDetections or []))
        results[pg] = text
        with open(os.path.join(OUT_DIR, f"滴天髓今註_p_{pg}.txt"), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[OK] p_{pg} ({tag}): {len(text)} 字")
    except Exception as e:
        print(f"[FAIL] p_{pg}: {e}")

with open(os.path.join(OUT_DIR, "滴天髓今註_all.txt"), "w", encoding="utf-8") as f:
    for pg in sorted(results, key=lambda x: int(x)):
        f.write(f"\n===== p_{pg} =====\n" + results[pg])
print(f"DONE 成功 {len(results)}/{len(files)} 页 -> {OUT_DIR}")
