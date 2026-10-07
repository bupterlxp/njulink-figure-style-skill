# NJU-LINK Figure Style × Plot Is All You Need

把 NJU-LINK 科研图的视觉语法与 [Plot Is All You Need](https://github.com/liouhai/plot-is-all-you-need) 的看图选图工作流整合为一个 skill：**挑参考 → 组合布局与配色 → 用自己的数据重画 → 并排验收**。仍通过 `$njulink-figure-style` 调用。

## 综合成图

以一个完整的多模态评测问题组织画面：上方是文本与视频/音频两条支路，经过整理、描述和审核形成测试集；下方是七方向能力比较、提示词分布、两组约束通过率和三层任务环图。

![NJU-LINK 多模态评测综合成图](examples/njulink-style-demo.png)

[PNG 原尺寸](examples/njulink-style-demo.png) · [矢量 PDF](examples/njulink-style-demo.pdf) · [SVG](examples/njulink-style-demo.svg) · [生成脚本](scripts/demo.py) · [数据](assets/compass-demo.json) · [构图说明](references/compass-composition.md)

所有数值为合成值。布局参照 T2AV-Compass 的主图与数据流程图，帧带、波形、中心图案和流程部件独立绘制。径向图和横向条形图读取同一份得分，模型颜色、顺序和数值保持一致；环图表达任务层级，不代表样本占比。

<details>
<summary>查看综合示例重做前后</summary>

![综合示例重做前后对照](examples/njulink-demo-before-after.png)

重做集中在面板比例、信息密度、共享数据、字体和具体流程部件。旧图取自提交 `7738b4c`。

</details>

## 图库结构与配色组合

上排是上游 MIT 自产示例，下排是本项目的 NJU-LINK 改绘：保留雨云图、百分比连接带、上三角气泡矩阵的结构，使用统一的字体、pastel 类别色和连续强度色。

![上游参考与 NJU-LINK 改绘三组对照](examples/plot-integration-demo.png)

这些图使用不同的模拟数据，展示结构和视觉部件的迁移，不表示相同实验结果，也不宣称像素级复刻。三张改绘的 [代码](scripts/gallery_examples.py) 可生成 PNG、PDF、SVG；需要贴近一比一时按指定参考图测量布局、字体与色值。

## T2AV-Compass 的精髓图参考

下面三张图直接从 NJU-LINK 官方仓库的固定 commit 加载，可查看 radial comparison、prompt pipeline、六面板 radar 和层级 sunburst。原图由官方项目托管，本仓库记录链接、版本和哈希。完整说明见 [T2AV-Compass 参考锚点](references/t2av-compass.md)。

<p>
  <img src="https://raw.githubusercontent.com/NJU-LINK/T2AV-Compass/7575ae07cf969c3f5d439644ecb9979862370523/docs/static/images/main_00.jpg" alt="T2AV-Compass official overview reference" width="100%">
</p>
<p><em>主图：放射状模型比较 + 分布/条形统计 + 多层 sunburst。它是这套 skill 里“总览—证据—层级”组合的首要参考。</em></p>

<p>
  <img src="https://raw.githubusercontent.com/NJU-LINK/T2AV-Compass/7575ae07cf969c3f5d439644ecb9979862370523/docs/static/images/datapipe.jpg" alt="T2AV-Compass official prompt pipeline reference" width="100%">
</p>
<p><em>流程图：大虚线容器、浅色圆角阶段、短标签和模态色。</em></p>

<p>
  <img src="https://raw.githubusercontent.com/NJU-LINK/T2AV-Compass/7575ae07cf969c3f5d439644ecb9979862370523/docs/static/images/radar_six_panels_integrated.svg" alt="T2AV-Compass official six-panel radar reference" width="100%">
</p>
<p><em>比较图：用 small multiples 保持多维评测可读，跨面板复用颜色语义。</em></p>

需要离线查看上述同一版本时运行：

~~~bash
python scripts/fetch_t2av_references.py
~~~

下载内容会进入 Git 忽略的 `reference-cache/t2av-compass/`，脚本会逐个校验 SHA-256。公开可分发的独立重绘示例在 [t2av-compass-style-demo.png](examples/t2av-compass-style-demo.png)，生成代码在 [t2av_style_demo.py](scripts/t2av_style_demo.py)；它使用合成数据和自造标签，不复制 T2AV 原图。

![T2AV-Compass-inspired independent reimplementation](examples/t2av-compass-style-demo.png)

上图与综合成图使用同一套绘图部件，提供独立的横版总览。它保留左侧 radial、中部分布与横向条、右侧三层 sunburst 的比例关系，不代表 T2AV 的实验结果。

## 这次整合了什么

| 能力 | 入口 |
|---|---|
| 完整多模态评测图、独立横版总览 | [成图部件](scripts/compass_panels.py)、[构图说明](references/compass-composition.md) |
| 基础流程图、radar、bar、heatmap 与 NJU-LINK token | [绘图原语](scripts/njulink_style.py)、[视觉语法](references/figure-grammar.md) |
| 14 套上游自产模板，原图 + 卡片 + Python，1 套另附 CSV | [可浏览图库索引](gallery/INDEX.md) |
| 3 张使用 NJU-LINK token 的改绘例子 | [生成脚本](scripts/gallery_examples.py) |
| 按数据选图、“A 的布局 + B 的配色”、六部件拆解 | [参考工作流](references/gallery-workflow.md) |
| 候选样板册、成品对照、配色卡 | [contact_sheet.py](scripts/contact_sheet.py) |
| 本地图库入库、重复检查、索引重建 | [ingest.py](scripts/ingest.py)、[build_index.py](scripts/build_index.py) |
| T2AV-Compass 官方锚点、离线抓取与独立重绘 | [参考文档](references/t2av-compass.md)、[fetch_t2av_references.py](scripts/fetch_t2av_references.py)、[t2av_style_demo.py](scripts/t2av_style_demo.py) |

原有风格预设是默认值；用户指定的参考和部件组合优先。上游样例仍保留各自原配色，不能把整个新图库都称为 NJU-LINK 原有风格。

## 图库预览

下图展示 14 套上游模板中的 6 套。点击 [索引](gallery/INDEX.md) 可查看全部 **17 张**图片和卡片，再按卡片里的代码生成。

![可复用图库预览](examples/plot-gallery-preview.png)

14 套上游模板包含雨云/小提琴、分组堆叠柱、百分比连接带、冲积流图、气泡矩阵、排序柱与玫瑰环、SHAP 蜂群、依赖图、预测值对照、模型结果面板等。上游 13 套使用模拟数据；排序玫瑰环据上游说明采用公开 diabetes 数据集导出的特征重要性，仓库未重新训练该模型。

## 直接这样调用

> `$njulink-figure-style` 用我的 CSV 比较四个 agent 的逐任务得分。参考图库里的雨云图布局，使用 NJU-LINK 配色，保留每个样本和中位数，直接给成品及参考对照。

> `$njulink-figure-style` 给我几种适合这份错误分析数据的草图，让我看图选。确认数据是否支持转移流图；如果只有阶段占比，就不要画成个体流向。

> `$njulink-figure-style` 按这张参考图尽量一比一重画，替换为我的数据。测量面板比例、间距、字体和颜色，交付可运行脚本、矢量图、并排对照及未匹配细节。

> `$njulink-figure-style` 将这张图加入我的本地图库，保留来源并写鉴赏卡片；不要改公开图库。

## 安装与复现

将仓库放到 skills 目录，环境依赖建议装进虚拟环境：

~~~bash
git clone https://github.com/bupterlxp/njulink-figure-style-skill.git ~/.codex/skills/njulink-figure-style
cd ~/.codex/skills/njulink-figure-style
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
~~~

已有目录时更新现有仓库即可。以下命令从仓库根目录运行：

~~~bash
# 综合成图：PNG / PDF / SVG + 字体与合成样本记录
.venv/bin/python scripts/demo.py --output-dir figures/base

# 跨平台固定使用随仓库分发的 Comic Neue
.venv/bin/python scripts/demo.py --font portable --output-dir figures/portable

# 三张 NJU-LINK 改绘：PNG / PDF / SVG
.venv/bin/python scripts/gallery_examples.py --output-dir figures/njulink

# T2AV-Compass 横版总览：PNG / PDF / SVG
.venv/bin/python scripts/t2av_style_demo.py --output-dir figures/t2av

# 上游模板：复制代码/CSV 到工作目录，并输出 PNG / PDF / SVG
.venv/bin/python scripts/render_gallery.py raincloud-median-badges --out figures/reference

# 制作选图样板册、参考与成品对照、配色卡
.venv/bin/python scripts/contact_sheet.py sheet --out figures/options.png raincloud-median-badges njulink-raincloud
.venv/bin/python scripts/contact_sheet.py compare --out figures/compare.png --labels "上游参考,NJU-LINK 改绘" raincloud-median-badges njulink-raincloud
.venv/bin/python scripts/contact_sheet.py swatches --out figures/palette.png njulink-raincloud

# 用户图默认进入被 Git 忽略的 gallery-local/
.venv/bin/python scripts/ingest.py /path/to/figure.png --source "我的参考图"
.venv/bin/python scripts/build_index.py
~~~

render_gallery.py 只执行本库已审读的模板，输出已存在时要求另选目录。上游模板的数据数组与标签需要按脚本注释替换；这不是对任意 CSV 的自动推断接口。图的 KDE、归一化、堆叠合计与色条含义由 skill 在实际任务中核验。

默认 `--font reference` 优先使用本机 Chalkboard，与官方 SVG 中的字体一致；缺少时使用随仓库分发的 Comic Neue。`--font portable` 固定使用后者。成图旁的 JSON 记录实际字体、尺寸、种子生成的样本和编码说明；PNG、PDF、SVG 使用同一张 Figure 导出。替换实验结果时编辑 [compass-demo.json](assets/compass-demo.json)，并按真实数据移除模拟标签。

## 来源与范围

NJU-LINK 视觉观察基于截至 2026-10-06 个人主页列出的 9 篇 Jiaming Wang 合著论文及公开项目交叉核验；主页精选集不等于所有公开论文，详见 [论文语料表](references/paper-corpus.md)。

上游固定到 [70898b8](https://github.com/liouhai/plot-is-all-you-need/tree/70898b877dc2455704070e4542db1939ff7d9ec0)。本库引入其 14 套自产示例及图库工具，保留 **Copyright (c) 2026 qc** 和 [MIT 原文](licenses/plot-is-all-you-need-MIT.txt)；上游收集的论文截图明确不属其 MIT 授权，未一并复制。完整列表、变更与文件哈希见 [整合记录](references/upstream-integration.md) 和 [manifest](references/upstream-manifest.json)。

本地 gallery-local/、taste.md、figures/、虚拟环境均被 Git 忽略。相似布局只提醒，完全相同像素才自动跳过；用户编辑过的卡片受保护。

Comic Neue 由 The Comic Neue Project Authors 提供，按 [SIL OFL 1.1](licenses/ComicNeue-OFL.txt) 随仓库分发；固定来源与哈希见 [字体清单](references/demo-fonts.json)。仓库不包含 Chalkboard 字体文件。

## 验证

~~~bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m compileall -q scripts gallery
~~~

入库测试覆盖重复、同名冲突、私有图不改公开卡片及 edited 卡片保护。图库模板可通过 render_gallery.py 逐一复现；代码能运行后仍需查看实际 PNG 和目标尺寸下的文字。
