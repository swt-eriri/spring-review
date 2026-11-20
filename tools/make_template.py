"""一次性脚本：把 Python 冲刺站（exam-review 仓库的 index.html）改造成 Spring 站的模板。
用法：python tools/make_template.py tools/python-site-index.html template.html
改造内容：数据换成占位符；学习路线、模拟卷结构、站名、存储键改为从数据读取；
去掉 Python 运行环境设置；代码高亮加 Java；「题号」改成「对应课程」。"""
import re, sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf8').read()

def sub(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f'期望出现 {count} 次，实际 {n} 次：{old[:60]!r}')
    s = s.replace(old, new)

def sub_re(pat, new):
    global s
    s2, n = re.subn(pat, lambda m: new, s, count=1, flags=re.S)
    if n != 1:
        sys.exit(f'没匹配到：{pat[:60]!r}')
    s = s2

# 数据
sub_re(r'window\.EXAM_DATA = .*?</script>', 'window.EXAM_DATA = /*__EXAM_DATA__*/;\n</script>')
sub_re(r'<title>[^<]*</title>', '<title>/*__TITLE__*/</title>')

# 学习路线、模拟卷结构从数据读取
sub_re(r'const STAGES = \[.*?\n\];', 'const STAGES = DATA.stages;')
sub_re(r'const BLUEPRINT = \[.*?\n\];', 'const BLUEPRINT = DATA.blueprint;')
sub("const KEY = 'exam-review-v1';", 'const KEY = DATA.storageKey;')
sub_re(r'const BRAND = `.*?`;', 'const BRAND = `<span class="brand-mark">${icon(\'logo\', 18)}</span><span class="brand-text"><b>${DATA.brand}</b><small>${DATA.brandSub}</small></span>`;')
sub("a.download = `考试冲刺进度-", "a.download = `${DATA.brand}进度-")

# 「题号」改成「对应课程」
sub('<span>题号 ${', '<span>课程 ${')
sub('desc: `考试题号 ${', 'desc: `对应课程 ${')

# 设置页：去掉盲写模式和 Python 运行环境（这个站没有代码题）
sub_re(r'\n    <div class="set-row"><div class="set-ic">\$\{icon\(\'code\', 18\)\}.*?现在加载</button></div>', '\n    <p class="muted">这个站全是选择题，没有需要设置的选项。</p>')
sub("  $('input', sec).onchange = e => { S.settings.blind = e.target.checked; save(); toast(e.target.checked ? '盲写模式已开启' : '盲写模式已关闭'); };\n", '')
sub("  $('[data-a=preload]', sec).onclick = () => Py.preload();\n", '')

# 代码高亮：加 Java
JAVA = r'''
const JAVA_KW = new Set('public private protected class interface extends implements static final void return new if else for while try catch finally throw throws this super null true false int long boolean double String import package'.split(' '));
function highlightJava(code) {
  const re = /(\/\/[^\n]*|\/\*[\s\S]*?\*\/)|("(?:[^"\\\n]|\\.)*")|(\b\d+(?:\.\d+)?[LlFfDd]?\b)|(@\w+)|([A-Za-z_$][\w$]*)|([^/"\w@$]+|.)/g;
  return code.replace(re, (m, c, s, n, ann, w) => {
    if (c) return `<span class="hl-c">${esc(c)}</span>`;
    if (s) return `<span class="hl-s">${esc(s)}</span>`;
    if (n) return `<span class="hl-n">${n}</span>`;
    if (ann) return `<span class="hl-d">${esc(ann)}</span>`;
    if (w) return JAVA_KW.has(w) ? `<span class="hl-k">${w}</span>` : /^[A-Z]/.test(w) ? `<span class="hl-b">${w}</span>` : w;
    return esc(m);
  });
}
'''
sub('function highlight(code, lang) {\n', JAVA + '\nfunction highlight(code, lang) {\n  if (lang === \'java\') return highlightJava(code);\n')

# 模拟考：卷面结构按 blueprint 统计，不再写死 Python 卷
sub("title: '按真实试卷结构，完整考一遍'", "title: '按估计的卷面结构，完整考一遍'")
sub('<div><b>20</b><span>单选</span></div><div><b>8</b><span>多选</span></div><div><b>2</b><span>简答</span></div><div><b>2</b><span>代码</span></div>',
    "${['single', 'multi'].map(t => `<div><b>${BLUEPRINT.filter(x => x.type === t).length}</b><span>${TYPE_NAME[t]}</span></div>`).join('')}")
sub('\n    <div><span><kbd>Ctrl</kbd> + <kbd>Enter</kbd></span><span>代码题运行测试</span></div>', '')

sub('<span class="muted">4 个阶段 · ${MODS.length}', '<span class="muted">${STAGES.length} 个阶段 · ${MODS.length}')

# 「全部学习站」入口
sys.path.insert(0, __import__('os').path.dirname(__file__))
from add_hub_link import add_hub_link
s = add_hub_link(s)

open(dst, 'w', encoding='utf8', newline='\n').write(s)
print('ok', len(s))
