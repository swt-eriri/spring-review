# 出题小工具：让各模块文件里的题目写得短一些
def Q(id, stem, options, answer, why, explain, lesson=None, adv=False, multi=None):
    """answer: 单个下标 或 下标列表；adv=True 表示进阶题（可跳过、模拟考不抽）"""
    ans = answer if isinstance(answer, list) else [answer]
    q = {'id': id, 'type': ('multi' if (multi if multi is not None else len(ans) > 1) else 'single'),
         'stem': ('【进阶，可跳过】' + stem) if adv else stem,
         'options': options, 'answer': ans, 'why': why, 'explain': explain,
         'tags': ['进阶'] if adv else (['basic'] if lesson is None else [])}
    if lesson is not None:
        q['lesson'] = lesson
    return q

def TF(id, stem, ok, why_true, why_false, explain, lesson=None):
    """判断题：ok=True 表示说法正确"""
    return Q(id, '判断：' + stem, ['正确', '错误'], 0 if ok else 1, [why_true, why_false], explain, lesson)
