---
title: 上三角气泡矩阵（NJU-LINK 连续蓝色）
kind: 数据图
purpose: [相关关系, 模型解释]
data: 变量间对称非负强度矩阵，对角为零
loudness: 2
caveat: 仅适用于对称非负强度；有正负相关系数需改变色阶与编码
low_quality: false
source: 本项目改绘（模拟数据）；上游 bubble-matrix-upper（MIT / qc）
code: ../scripts/gallery_examples.py
appreciated: true
edited: false
palettes:
  - "#F3F7FB #85B9E2 #376995"
render: python scripts/gallery_examples.py --output-dir figures/njulink
---

**评价**：上三角放数据，下三角放面积/色阶图例；面积与强度成比例，零值不画点。

**部件来源**：结构改编自 bubble-matrix-upper，颜色与字体使用 NJU-LINK 默认 token，数据为新的模拟值。

**再现**：见 frontmatter 的 render 命令，输出 PNG/PDF/SVG。
