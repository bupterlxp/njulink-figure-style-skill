---
name: njulink-figure-style
description: "Use when creating or revising research figures in the observable NJU-LINK/Jiaming Wang visual grammar: pastel modular diagrams, evidence-first charts, radar/sunburst/heatmap panels, typography, spacing, and reproducible Matplotlib code. Apply it as a visual-system study from public papers, not as a claim of personal authorship or a copy of source artwork."
metadata:
  short-description: "NJU-LINK 科研图表语法与可复现绘图实践工具包"
---

# NJU-LINK Figure Style

这个技能把公开论文中可观察、可复用的视觉规则整理成绘图系统。目标是高保真复刻版式、色彩、线型、信息层级和图表结构，让新图看起来属于同一套研究视觉语法；它不复制原论文的图片、图标、数据或文字，也不把合作者共同完成的图表归因给某一个作者。

## 何时使用

当用户要做以下事情时触发：

- 按 NJU-LINK 论文风格重画流程图、框架图、radar、sunburst、heatmap、bar chart、qualitative panel 或 benchmark figure；
- 从 Jiaming Wang / NJU-LINK 的公开论文或项目页提炼图表风格；
- 审查现有科研图是否符合该视觉语法，并给出可执行的修改或 Matplotlib 代码；
- 把一张参考图拆成布局、视觉 token、组件和可复现脚本。

纯粹的海报、品牌宣传图、网页 UI 或与科研图无关的插画不应触发本技能。

## 证据边界与来源

本技能基于 [references/paper-corpus.md](references/paper-corpus.md) 中的公开主页、arXiv、项目页和 NJU-LINK GitHub 仓库快照。论文往往由多人共同完成，因此将结果称为“Jiaming Wang/NJU-LINK corpus 的可观察视觉语法”，而不是未经作者确认的个人签名风格。若用户要求“所有论文”，先检查该语料的更新时间和来源，再说明是否是主页精选集、NJU-LINK 组织仓库集，还是某个时间范围内的可核验全集。

不要把原论文 PDF、原始 figure、受版权保护的图标、数据或 logo 放进生成仓库。引用来源和复刻说明写入文档；新图使用同等功能的抽象图标、合成数据或用户拥有的素材。

## 标准工作流

### 1. 确定图的任务

先把图的任务写成一句话：展示流程、解释机制、比较模型、分解错误、描述数据分布，还是呈现定性案例。每张主图只保留一个阅读终点；需要同时表达“流程 + 结果”时，拆成编号子图并共享视觉 token。

### 2. 选择图形骨架

从 [references/figure-grammar.md](references/figure-grammar.md) 选择最接近的骨架：

- **模块化流程**：左到右 3–6 个阶段，圆角卡片、编号圆点、细箭头和少量图标；
- **数据/评测总览**：中心主题 + 环形/旭日/玫瑰分解，旁接 2–5 个小统计图；
- **多模型比较**：radar 或分组 bar，少量半透明填充，图例置于底部；
- **机制/错误分析**：sunburst + heatmap + 小型分布图，使用同一类别色；
- **定性案例**：图像/视频帧外加彩色边框、虚线分组和短标签，显式区分输入、输出、预期和评分。

不要从默认 Matplotlib 图开始堆装饰。先画白底网格、面板边界和信息流，再放数据和图标。

## 具体调用例子

把用户请求先归入下面最接近的形状，再决定代码和交付物：

| 用户请求 | 主骨架 | 应交付的关键内容 |
|---|---|---|
| “把数据清洗、检索、推理、审核画成一张方法总览图” | 模块化流程 | 3–6 张圆角卡片、编号徽章、左到右箭头、每卡一个动作 |
| “比较三个模型在召回、鲁棒性、成本和覆盖率上的差异” | Radar / 分组 bar | 统一量纲、同一类别颜色、底部图例、避免超过 5–6 条重叠曲线 |
| “分析不同阶段和错误类型的失败率” | Heatmap + 小统计图 | 连续色阶、格内数值、缺失值与低值区分、图注写清方向和单位 |

例如，用户说“用 NJU-LINK 风格重画我的 agent pipeline”，应先追问或从上下文确定阶段名称、输入/输出和主结论，然后调用 `draw_pipeline`；用户说“只想看模型比较”，不要额外堆流程卡片。代码级参考见 [`README.md`](README.md) 的最小例子和 [`scripts/demo.py`](scripts/demo.py)。

交付时至少给出：图意图、选用骨架、数据到视觉元素的映射、可运行脚本、PNG/PDF 导出路径，以及缩小到论文栏宽后的可读性检查结果。

一个可直接查看的合成结果见 [`examples/njulink-style-demo.png`](examples/njulink-style-demo.png)；它不是任何论文的原图，也不包含论文数据。

### 3. 应用视觉 token

读取 [references/figure-grammar.md](references/figure-grammar.md) 的 token；代码实现位于 [scripts/njulink_style.py](scripts/njulink_style.py)，可直接导入。默认规则包括：

- 白底与近黑文字，浅色填充承载类别，彩色只用于语义区分；
- 8 色以内的低饱和 pastel cycle；同一类别跨子图保持同色；
- 圆角 8–12 px、1.2–1.6 pt 细边框、虚线分组边界、1.4–1.8 pt 主箭头；
- 图表弱网格、少边框、短标签、底部图例，避免阴影、渐变和厚重 3D 效果；
- 论文正文用兼容的衬线字体，图内标签优先 Arial/DejaVu Sans/Calibri 类无衬线，代码用等宽字体；
- 标题、阶段编号、动作标签、数据细节按四级信息层级递减。

### 4. 生成并复核

优先运行 `python scripts/demo.py --output-dir <dir>` 检查工具链，再用 `njulink_style.py` 生成实际图。保存 PNG（300 dpi）和 PDF/SVG 矢量版本；检查：

1. 关键结论在缩小到论文栏宽后仍可读；
2. 颜色在灰度和色觉缺陷模拟下仍有文字/线型冗余编码；
3. 面板、箭头、标题和图例在同一基线/网格上；
4. 同一类别在所有子图中颜色、缩写、顺序一致；
5. 没有复制原图的像素、数据、句子或独家图标；
6. 图注能独立解释输入、操作、输出和度量。

### 5. 按模式交付

- **复刻模式**：输出参考图拆解、token 表、布局草图、可运行代码和逐项差异清单；
- **新图模式**：输出图意图、骨架、数据映射、色彩语义、代码和导出参数；
- **审查模式**：按 0–2 分检查版式、层级、颜色一致性、可读性、可复现性和来源记录；
- **文献模式**：先更新论文清单与来源，再总结哪些特征跨论文稳定、哪些只属于单篇实验。

默认交付顺序是：**图意图 → 选用骨架 → 视觉 token → 面板布局 → 数据映射 → 可运行脚本 → QA 清单 → 来源与限制**。
