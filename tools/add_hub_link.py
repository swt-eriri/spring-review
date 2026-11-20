"""给学习站加「全部学习站」入口（侧栏最后一项 + 手机顶栏图标），指向导航站。
Spring 站由 make_template.py 调用；Python 站（exam-review 仓库只有生成好的 index.html）直接对文件运行：
    python tools/add_hub_link.py path/to/index.html"""
import sys

HUB_URL = 'https://swt-eriri.github.io/study/'

def add_hub_link(s):
    if HUB_URL in s:
        return s   # 已经加过
    nav_old = "  { href: '#/settings', icon: 'settings', name: '设置', match: /^#\\/settings/ },\n];"
    nav_new = ("  { href: '#/settings', icon: 'settings', name: '设置', match: /^#\\/settings/ },\n"
               f"  {{ href: '{HUB_URL}', icon: 'layers', name: '全部学习站', match: /^$/, hub: true }},\n];")
    tab_old = "NAV.filter(n => n.href !== '#/settings')"
    tab_new = "NAV.filter(n => n.href !== '#/settings' && !n.hub)"
    top_old = "<a class=\"icon-btn\" href=\"#/settings\" aria-label=\"设置\">"
    top_new = f"<a class=\"icon-btn\" href=\"{HUB_URL}\" aria-label=\"全部学习站\">${{icon('layers', 20)}}</a>" + top_old
    for old, new in ((nav_old, nav_new), (tab_old, tab_new), (top_old, top_new)):
        if s.count(old) != 1:
            sys.exit(f'找不到要改的位置（或不唯一）：{old[:50]!r}')
        s = s.replace(old, new)
    return s

if __name__ == '__main__':
    p = sys.argv[1]
    s = open(p, encoding='utf8').read()
    open(p, 'w', encoding='utf8', newline='\n').write(add_hub_link(s))
    print('ok')
