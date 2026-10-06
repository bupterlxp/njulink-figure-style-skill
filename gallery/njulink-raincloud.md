---
title: 雨云图（NJU-LINK pastel，中位数圆标）
kind: 数据图
purpose: [分布, 组间比较]
data: 少量模型各有多个逐样本得分；需要组内原始观测
loudness: 2
caveat: 小样本或恒定值不适合 KDE；圆标是中位数，云宽不等于样本数
low_quality: false
source: 本项目改绘（模拟数据）；上游 raincloud-median-badges（MIT / qc）
code: ../scripts/gallery_examples.py
appreciated: true
edited: false
palettes:
  - "#57BDB5 #85B9E2 #B6A4D8 #E5A1AF"
render: python scripts/gallery_examples.py --output-dir figures/njulink
---

**评价**：左侧散点与右侧半小提琴保留分布细节，中位数圆标突出位置；无阴影。

**部件来源**：结构改编自 raincloud-median-badges，颜色与字体使用 NJU-LINK 默认 token，数据为新的模拟值。

**再现**：见 frontmatter 的 render 命令，输出 PNG/PDF/SVG。
