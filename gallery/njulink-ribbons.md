---
title: 百分比堆叠连接带（NJU-LINK pastel）
kind: 数据图
purpose: [构成占比, 趋势变化]
data: 类别 × 阶段占比表，每列非负且合计 100%
loudness: 2
caveat: 连接带只是边际占比之间的视觉连接，不能解释为个体流向
low_quality: false
source: 本项目改绘（模拟数据）；上游 stacked-percent-bars-ribbons（MIT / qc）
code: ../scripts/gallery_examples.py
appreciated: true
edited: false
palettes:
  - "#57BDB5 #85B9E2 #B6A4D8"
render: python scripts/gallery_examples.py --output-dir figures/njulink
---

**评价**：类别色跨阶段一致；浅色带连接同类边界，柱内显示占比。

**部件来源**：结构改编自 stacked-percent-bars-ribbons，颜色与字体使用 NJU-LINK 默认 token，数据为新的模拟值。

**再现**：见 frontmatter 的 render 命令，输出 PNG/PDF/SVG。
