# Spring 全家桶考试冲刺站

课程：极客时间《玩转 Spring 全家桶》（丁雪丰，123 讲）。素材是 GPT 根据网页摘要整理的逐讲要点
（`C:\Users\80681\Documents\Codex\2026-11-20\x-a\outputs\Spring全家桶-逐讲要点与学习笔记.md`）。

## 已定的事（2026-11-20）

- 考试题型未知，按**全选择题**准备（单选 + 多选，含「读代码判断结果」的选择题）。
- 以**课程版本**（Spring 5 / Boot 2 时代）为准；新版本的变化只作旁注。
- 用户**没有 Java 基础**：每个模块开头补读懂代码所需的最少 Java。
- 不排每日计划，用户自己安排时间。
- 新开一个站（新仓库），以后用户做导航页汇总各学习站。

## 内容来源标注

GPT 素材只有概括。默认值、常量、回滚规则这类细节是按 Spring 5 官方行为补充的，讲解里标了「补充」。

## 构建

    python build.py          # 检查题目并生成 index.html
    python build.py --check  # 只检查

- `content/site_conf.py`：站名、学习路线分组、模拟卷结构、存储键
- `content/<模块>.py`：讲解（lessons）、题目（questions）、速查（CHEATSHEET）
- `template.html`：由 `tools/make_template.py` 从 Python 冲刺站改造生成，平时不用动
- 进度存在浏览器 localStorage，键名 `spring-review-v2`。它和 Python 站在同一个域名下，所以键名必须不同。

## 进度

- [x] 样品第一版：按「讲透机制」深度做，用户反馈太难、看不懂（2026-11-20）
- [x] 样品第二版：改为「认得出」深度——一句话、对号入座、默认值、易混对、必背的坑；不补 Java，只在规则需要时教认关键词；推理题标「进阶，可跳过」，模拟考只抽主线题（tags 含 basic）。3 节讲解，33 道题
- [x] 用户确认第二版后（2026-11-20），铺开全部 20 个模块：52 节讲解，423 道题（主线题 + 进阶题 + 随堂练习）；模拟卷 43 单选 + 10 多选，只抽主线题
- [x] build.py 会把加粗统一换成 <strong>（中文标点紧挨 ** 时 Markdown 不认加粗）
- [ ] 用户试用全部内容
- [x] 已发布（2026-11-20）：仓库 swt-eriri/spring-review，网址 https://swt-eriri.github.io/spring-review/
- [x] 导航站：仓库 swt-eriri/study，网址 https://swt-eriri.github.io/study/（源码副本在上一级 study 文件夹）；两个学习站侧栏都有「全部学习站」入口（tools/add_hub_link.py，Python 站直接对它的 index.html 运行）

## 以后更新怎么发布

改完 content 后运行 python build.py，把整个文件夹提交推送到 swt-eriri/spring-review 的 main 分支，GitHub Pages 会自动更新。
