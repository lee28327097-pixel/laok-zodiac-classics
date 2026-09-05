import fitz, os

SRC = r"E:/易经/周易2026/周易合集/易学/防和不断点/四柱八字命理/刻京台增补渊海子平大全.pdf"
BASE = r"D:/国学命理库/3-Resources/命/八字四书"
OCR = os.path.join(BASE, "transcript/ocr_full")
PAGES = os.path.join(BASE, "pages/渊海子平")
os.makedirs(PAGES, exist_ok=True)

doc = fitz.open(SRC)
n = doc.page_count
print("总页数:", n)

# 术语词表（命理学核心词，用于密度扫描）
terms = ["用神","日主","格局","喜忌","纳音","神煞","大運","流年","六親","父母","妻","兄弟","姊妹","子孫",
         "五行","旺衰","天干","地支","合化","沖","刑","空亡","祿","馬","貴人","財","官","食","傷","比","劫",
         "甲乙丙丁戊己庚辛壬癸","子丑寅卯辰巳午未申酉戌亥","十干","十二支","起例","安命","身宮","起運","交運",
         "用神","日主","格","喜","忌","煞","祿","馬"]

score = {}
for i in range(n):
    fn = os.path.join(OCR, f"渊海子平_p_{i+1:03d}.txt")
    if not os.path.exists(fn):
        continue
    t = open(fn, encoding="utf-8", errors="ignore").read()
    c = sum(t.count(x) for x in terms)
    score[i] = c

top = sorted(score.items(), key=lambda x: -x[1])[:20]
print("\n术语密度 Top 20 页:")
for i, c in top:
    print(f"  p_{i+1:03d}  术语命中 {c}")

# render 集合：头6页 + 每20页抽样 + top 重点
render_set = set(list(range(0, 6))
                 + [i for i in range(19, n, 20)]
                 + [i for i, _ in top[:10]])
print(f"\n将 render {len(render_set)} 页 ...")
for i in sorted(render_set):
    if i >= n:
        continue
    pix = doc[i].get_pixmap(dpi=200)
    pix.save(os.path.join(PAGES, f"渊海子平_p_{i+1:03d}.png"))
print("render done ->", PAGES)
