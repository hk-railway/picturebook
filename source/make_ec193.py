from pathlib import Path
import re
import shutil

base = Path(r"C:/Users/Hiro/81.GitHub/picturebook/source")

type_dir = base / "type"
type2_dir = base / "type2"

src_photo = type_dir / "EC193.html"
ref_type2 = type2_dir / "typeEC255.html"
new_type2 = type2_dir / "typeEC193.html"

# --------------------------------------------------
# (1) typeEC193.html を作成
# --------------------------------------------------

# コピー作成
shutil.copyfile(ref_type2, new_type2)

# EC193.html 読み込み
photo_html = src_photo.read_text(encoding="utf-8")

# typeEC193.html 読み込み
new_html = new_type2.read_text(encoding="utf-8")

# --------------------------------------------------
# 写真部分を抽出
# （imgタグを取得）
# --------------------------------------------------
img_tags = re.findall(r'<img[^>]+>', photo_html, flags=re.IGNORECASE)

# --------------------------------------------------
# 説明文を抽出
# （tableのtdなどを簡易取得）
# 必要に応じて調整してください
# --------------------------------------------------
text_blocks = re.findall(r'<td[^>]*>(.*?)</td>', photo_html, flags=re.DOTALL | re.IGNORECASE)
text_blocks = [re.sub(r'<.*?>', '', t).strip() for t in text_blocks]

# --------------------------------------------------
# typeEC193.html 側の img を差し替え
# --------------------------------------------------
new_html = re.sub(
    r'<img[^>]+>',
    img_tags[0] if img_tags else '',
    new_html,
    count=1,
    flags=re.IGNORECASE
)

# --------------------------------------------------
# 説明文の差し替え
# --------------------------------------------------
# 必要に応じて対象部分を調整
for i, text in enumerate(text_blocks[:4]):
    new_html = re.sub(
        rf'(<td[^>]*class="col{i+1}"[^>]*>)(.*?)(</td>)',
        rf'\1{text}\3',
        new_html,
        count=1,
        flags=re.DOTALL | re.IGNORECASE
    )

# --------------------------------------------------
# 5カラム目を空欄にする
# --------------------------------------------------
new_html = re.sub(
    r'(<td[^>]*class="col5"[^>]*>)(.*?)(</td>)',
    r'\1\3',
    new_html,
    count=1,
    flags=re.DOTALL | re.IGNORECASE
)

# 保存
new_type2.write_text(new_html, encoding="utf-8")

print("typeEC193.html を作成しました")

# --------------------------------------------------
# (2) EC193.html に「詳細」リンク追加
# --------------------------------------------------

photo_html = src_photo.read_text(encoding="utf-8")

link_html = '<a href="../type2/typeEC193.html">詳細</a>'

# body直後などに追加
if link_html not in photo_html:
    photo_html = re.sub(
        r'(<body[^>]*>)',
        rf'\1\n<div>{link_html}</div>',
        photo_html,
        count=1,
        flags=re.IGNORECASE
    )

src_photo.write_text(photo_html, encoding="utf-8")

print("EC193.html に詳細リンクを追加しました")
