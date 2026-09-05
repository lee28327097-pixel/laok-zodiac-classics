import fitz
PDF = r"E:\易经\周易2026\周易合集\易学\防和不断点\四柱八字命理\滴天髓 子平真詮 今註.pdf"
doc = fitz.open(PDF)
print("TOTAL PAGES:", doc.page_count)
pages = [1,2,3,4,5,6,12,14,30,33,77,78,86,87,91,108,111,119]
for p in pages:
    idx = p-1
    txt = doc[idx].get_text().strip()
    print(f"\n===== PDF PAGE {p} (idx {idx}) | chars={len(txt)} =====")
    print(txt[:1500])
