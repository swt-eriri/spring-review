"""把 content/ 里的讲解和题目装进 template.html，生成 index.html。
用法：python build.py          生成
      python build.py --check  只检查题目数据，不生成"""
import importlib, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'content'))
site = importlib.import_module('site_conf')

errors = []
def err(msg): errors.append(msg)

mods, sheets = [], []
for mid in site.MODULE_ORDER:
    c = importlib.import_module(mid)
    m = c.MODULE
    if m['id'] != mid: err(f'{mid}: 模块 id 写成了 {m["id"]}')
    mods.append(m)
    sheets.append(c.CHEATSHEET.strip())

ids = set()
for m in mods:
    nl = len(m['lessons'])
    for li, l in enumerate(m['lessons']):
        if not l['cards']: err(f'{m["id"]} 第 {li} 节没有内容')
        if not any(q.get('lesson') == li for q in m['questions']): err(f'{m["id"]} 第 {li} 节没有随堂练习')
    for q in m['questions']:
        q['m'] = m['id']
        q.setdefault('tags', [])
        where = q.get('id', '?')
        if where in ids: err(f'题目 id 重复：{where}')
        ids.add(where)
        if q['type'] not in ('single', 'multi'): err(f'{where}: 题型只能是 single / multi')
        n = len(q['options'])
        if len(q['why']) != n: err(f'{where}: why 有 {len(q["why"])} 条，选项有 {n} 个')
        if not q['answer'] or any(not 0 <= a < n for a in q['answer']): err(f'{where}: 答案下标越界')
        if len(set(q['answer'])) != len(q['answer']): err(f'{where}: 答案重复')
        if q['type'] == 'single' and len(q['answer']) != 1: err(f'{where}: 单选题答案必须只有 1 个')
        if q['type'] == 'multi' and len(q['answer']) < 2: err(f'{where}: 多选题答案至少 2 个')
        if 'lesson' in q and not 0 <= q['lesson'] < nl: err(f'{where}: lesson 下标越界')
        if not q.get('explain'): err(f'{where}: 缺少 explain')

pool = [q for m in mods for q in m['questions'] if 'lesson' not in q]
for t in ('single', 'multi'):
    need = sum(1 for s in site.BLUEPRINT if s['type'] == t)
    have = sum(1 for q in pool if q['type'] == t)
    if have < need: err(f'模拟卷要 {need} 道{t}，刷题单只有 {have} 道')
from collections import Counter
for (mid, t), n in Counter((s['m'], s['type']) for s in site.BLUEPRINT).items():
    have = sum(1 for m in mods if m['id'] == mid for q in m['questions'] if q['type'] == t and 'basic' in q['tags'])
    if have < n: err(f'模拟卷要从 {mid} 抽 {n} 道 {t} 主线题，只有 {have} 道')
known = {m['id'] for m in mods}
for st in site.STAGES:
    for mid in st['mods']:
        if mid not in known: err(f'学习路线引用了不存在的模块 {mid}')

if errors:
    print('检查没通过：'); [print(' -', e) for e in errors]; sys.exit(1)
nq = sum(len(m['questions']) for m in mods)
print(f'检查通过：{len(mods)} 个模块，{sum(len(m["lessons"]) for m in mods)} 节讲解，{nq} 道题（刷题单 {len(pool)} 道）')
if '--check' in sys.argv: sys.exit(0)

# 中文标点紧挨 ** 时 Markdown 不认加粗（如「编程。**按」），统一换成 <strong>；代码块和行内代码不动
import re
_BOLD = re.compile(r'\*\*([^*\n`]+?)\*\*')
def fix_bold(text):
    parts = re.split(r'(```[\s\S]*?```|`[^`\n]*`)', text)
    return ''.join(p if p.startswith('`') else _BOLD.sub(r'<strong>\1</strong>', p) for p in parts)
for m in mods:
    for l in m['lessons']:
        l['cards'] = [fix_bold(c) for c in l['cards']]
    for q in m['questions']:
        q['stem'], q['explain'] = fix_bold(q['stem']), fix_bold(q['explain'])
        q['options'] = [fix_bold(o) for o in q['options']]
        q['why'] = [fix_bold(w) for w in q['why']]
sheets = [fix_bold(t) for t in sheets]

data = {
    'modules': mods, 'cheatsheet': '\n\n'.join(sheets), 'harness': '',
    'stages': site.STAGES, 'blueprint': site.BLUEPRINT,
    'brand': site.BRAND, 'brandSub': site.BRAND_SUB, 'storageKey': site.STORAGE_KEY,
}
tpl = (ROOT / 'template.html').read_text(encoding='utf8')
js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
out = tpl.replace('/*__EXAM_DATA__*/', js, 1).replace('/*__TITLE__*/', site.TITLE, 1)
with open(ROOT / 'index.html', 'w', encoding='utf8', newline='\n') as f:
    f.write(out)
print('已生成 index.html')
