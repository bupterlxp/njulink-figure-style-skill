# NJU-LINK Figure Style

这是一个 Codex skill，用于按公开 NJU-LINK / Jiaming Wang 论文中可观察到的视觉语法，重画或新建科研图表。它把白底、低饱和 pastel、圆角模块、细箭头、编号阶段、radar、heatmap 和统计面板整理成可复现的 Matplotlib 工具链。

## 覆盖范围

语料快照为 2026-10-06，基于 Jiaming Wang 个人主页列出的 9 篇论文，以及 NJU-LINK 的公开项目仓库交叉核验。详细来源和证据边界见 [`references/paper-corpus.md`](references/paper-corpus.md)；抽象后的布局、颜色、线型和字体规则见 [`references/figure-grammar.md`](references/figure-grammar.md)。

这里描述的是共同作者论文语料的可观察视觉语法，不把图表归因成某位作者的个人签名，也不分发原论文图片、数据、文字或项目 logo。

## 使用

把本目录放入 Codex 的 skills 目录后，可用 `$njulink-figure-style` 调用。绘图脚本只依赖 NumPy 和 Matplotlib：

```bash
PYTHONPATH=scripts python scripts/demo.py --output-dir ./demo-output
```

`demo.py` 使用合成数据生成 PNG 与 PDF，作为工具链 smoke test。新图可从 `scripts/njulink_style.py` 导入 `apply_style`、`draw_pipeline`、`radar`、`pastel_bars`、`heatmap` 和 `save_figure`。

## 目录

- `SKILL.md`：触发条件、四种工作模式和复核清单。
- `references/`：论文语料索引与视觉 grammar。
- `scripts/njulink_style.py`：可复用绘图原语。
- `scripts/demo.py`：合成数据示例。
- `assets/`：Matplotlib 风格文件和 palette JSON。

复刻参考图时，保留布局和信息层级的抽象规律，使用用户拥有的数据或合成数据，并在图注中记录来源。

