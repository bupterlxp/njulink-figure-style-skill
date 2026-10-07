---
name: njulink-figure-style
description: "Create, reproduce, and review research figures using NJU-LINK visual presets and a curated Plot Is All You Need gallery. Select visual references, combine layout and palette, render user data with reproducible Python, and compare results side by side. Includes gallery maintenance."
metadata:
  short-description: "NJU-LINK 风格 × 看图选图、部件组合与可复现绘图"
---

# NJU-LINK Figure Style

将 NJU-LINK 论文视觉语法与 Plot Is All You Need 的“鉴赏 → 选图 → 演绎 → 对照”结合。支持参考图高保真重画、数据驱动的新图、成图审查和个人图库维护。不要把共同作者论文的视觉特征归因为某个人的独家风格。

## 先选入口

| 请求 | 动作 | 按需读取 |
|---|---|---|
| 有参考图，要求同款或接近一比一 | 看原图，测量六部件，直接重画并输出对照 | [参考工作流](references/gallery-workflow.md) |
| 有数据，想选画法 | 自己读数据，展示匹配候选；方向明确时直接画 | [图库索引](gallery/INDEX.md)、相关卡片 |
| “直接画”“你定”，或已选好样式 | 完成首选，不强制选图轮次 | [视觉语法](references/figure-grammar.md) |
| 要求 T2AV 风格的完整成图、综合示例 | 确定一个图意图，复用完整构图再替换数据和具体流程部件 | [综合构图](references/compass-composition.md) |
| “A 的布局 + B 的配色” | 写六部件来源表；连续与类别配色分别处理 | [参考工作流](references/gallery-workflow.md) |
| 审查成品 | 核对数值和视觉映射，展示并排图与差异 | [对照验收](references/gallery-workflow.md#4-对照验收) |
| 加图、整理图库、改卡片 | 使用本地入库工具，保留用户编辑与来源 | [图库维护](references/gallery-workflow.md#5-图库维护) |
| 扩充 NJU-LINK 论文风格语料 | 核验作者和来源，更新语料范围再归纳 | [论文索引](references/paper-corpus.md) |
| 复用 T2AV-Compass 精髓图的视觉关系 | 先看官方主图/流水线/radar，再用自己的数据独立重绘 | [T2AV 参考锚点](references/t2av-compass.md) |

上游版本和 MIT 许可见 [整合记录](references/upstream-integration.md)。公开图库有 14 套上游自产示例及 3 张 NJU-LINK 改绘；未导入上游论文截图。先检索索引，再打开匹配图片和卡片，不要起手读取整个图库。

T2AV-Compass 的官方参考图单独列在 [t2av-compass.md](references/t2av-compass.md)：主图的 radial + distribution + hierarchical sunburst、prompt pipeline 和六面板 radar 都通过固定 commit 的外链展示。由于官方仓库没有为这些图片声明统一再分发许可，不要把原始图片提交到公开 skill；需要离线查看时使用 [fetch_t2av_references.py](scripts/fetch_t2av_references.py) 写入被忽略的缓存。公开交付使用 [t2av_style_demo.py](scripts/t2av_style_demo.py) 的独立重绘，并标注合成数据。

## 样式如何合并

优先级：**用户明确选择 → 用户参考图/六部件组合 → NJU-LINK 默认 token**。图库扩大图形结构，NJU-LINK 提供默认皮肤；新图库不是 NJU-LINK 论文的风格证据。

- 接近一比一：测量宽高比、面板归一化坐标、留白、轴域、文字层级、字体、线宽和颜色。差异表区分有意改动、缺少字体/素材、尚未匹配；仅换配色不能称为高保真。
- 默认用白底、近黑文字、浅色模块、细圆角边框、轻网格和稳定类别色，参数见 [figure-grammar.md](references/figure-grammar.md)。
- 六部件：结构布局、图形元素、配色、文字与标注、装饰细节、图例与色条。用户指定的特点优先；默认 token 不禁止其他风格。
- T2AV 风格的综合图先参考 [完整成图](examples/njulink-style-demo.png) 的主次比例、字体和具体流程部件。`njulink_style.py` 是基础绘图原语；把几个默认子图拼起来、加 pastel 色不足以达到参考图的构图质量。相关面板应共享问题、数据和颜色语义。
- 连续值使用连续色阶，正负值考虑零中心发散色，类别才用 pastel cycle。记录单位、归一化和面积/长度编码。

## 四步完成

1. **读数据与看参考。** 自己读取文件，判断分组、范围、缺失和图意图。仅在无法推断且影响科学含义时提问。
2. **定结构与部件。** 要求选图时展示少量实质不同的候选或真实数据草图；明确参考则直接执行。用 [contact_sheet.py](scripts/contact_sheet.py) 展示候选、配色与成品对照。
3. **用数据重画。** 优先复用卡片 code 脚本或 [njulink_style.py](scripts/njulink_style.py)。记录排序、变换、随机种子和字体。复制到工作目录后修改，保留原始数据。缺数据的样稿在画面标明 SIMULATED DATA；不把合成数值补进真实结果。
4. **渲染后验收。** 打开 PNG 对照参考，抽查极值、总和、分组、轴范围和图例。修复遮挡、截断、对比度和缺字，再按论文栏宽检查。像素差不能单独证明科学含义或风格匹配。

## 可运行资源

命令从 skill 根目录运行；脚本也支持绝对路径。依赖见 [requirements.txt](requirements.txt)，优先使用现有或项目虚拟环境。

~~~bash
# 完整多模态评测图，输出 PNG/PDF/SVG 与数据/字体 JSON
python scripts/demo.py --output-dir figures/base

# 无系统字体依赖的版本：随仓库分发的 OFL Comic Neue
python scripts/demo.py --font portable --output-dir figures/portable

# 三种结构用 NJU-LINK token 改绘，输出 PNG/PDF/SVG
python scripts/gallery_examples.py --output-dir figures/njulink

# 复制上游模板及数据到工作目录，渲染 PNG/PDF/SVG
python scripts/render_gallery.py raincloud-median-badges --out figures/reference

# 候选样板册、对照图与色卡
python scripts/contact_sheet.py sheet --out figures/options.png "raincloud-median-badges::上游布局" "njulink-raincloud::NJU-LINK 配色"
python scripts/contact_sheet.py compare --out figures/compare.png --labels "参考,改绘" raincloud-median-badges njulink-raincloud
python scripts/contact_sheet.py swatches --out figures/palette.png njulink-raincloud

# T2AV-Compass 视觉关系独立重绘
python scripts/t2av_style_demo.py --output-dir figures/t2av
~~~

查看 [综合成图](examples/njulink-style-demo.png)、[重做前后](examples/njulink-demo-before-after.png)、[改绘对照图](examples/plot-integration-demo.png)、[上游图库预览](examples/plot-gallery-preview.png) 和 [T2AV 横版总览](examples/t2av-compass-style-demo.png)。上游参考保留原配色；独立成图保留具体参考关系，不宣称像素一致。

## 交付和保存

交付最终图片、PNG + PDF/SVG、可运行脚本、数据来源/变换说明、参考对照及已知差异。不要只交提示词或让用户运行代码才能看到结果。

研究图留在项目目录或 Git 忽略的 gallery-local/；用户要求入库才维护图库，既有公开授权可沿用。taste.md 只记录用户明确表达的偏好；edited: true 卡片不能自动重写。公开材料保留来源与许可。具体命令见 [图库维护](references/gallery-workflow.md#5-图库维护)。
