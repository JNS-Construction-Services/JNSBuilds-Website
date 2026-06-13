from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BAD_ROOT = './styles.css" />`n  <link rel="stylesheet" href="./CSS/site-shared.css" />'
GOOD_ROOT = './styles.css" />\n  <link rel="stylesheet" href="./CSS/site-shared.css" />'
BAD_SVC = '../styles.css" />`n  <link rel="stylesheet" href="../CSS/site-shared.css" />'
GOOD_SVC = '../styles.css" />\n  <link rel="stylesheet" href="../CSS/site-shared.css" />'

for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    updated = text.replace(BAD_ROOT, GOOD_ROOT).replace(BAD_SVC, GOOD_SVC)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        print(f"fixed {path.relative_to(ROOT)}")
