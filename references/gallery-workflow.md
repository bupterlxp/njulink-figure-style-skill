# 看图选图与部件组合

改编自 liouhai/plot-is-all-you-need 的四阶段文档（MIT，Copyright 2026 qc）。以用户当前要求为准，不强制多轮选图或重复确认。

## 1. 鉴赏与检索

先看 gallery/INDEX.md 的用途统计，用 rg 检索“分布、组间比较、模型性能、网络与流向”等词；打开 PNG，再读对应卡片。索引不替代视觉检查，gallery-local/ 若存在也参与检索。

卡片描述用途、所需数据、六部件、caveat。loudness 是视觉复杂程度，不是质量分数。caveat 用于数据适配，例如：

- 雨云图要有逐样本观测；只有均值时不能伪造分布；
- 真正的 alluvial 需要相邻阶段的联合转移数量；
- 百分比堆叠图的连接带只连接边际占比，不能据此推断个体流向；
- SHAP 图要有对应模型的贡献值，合成值不是解释证据；
- 气泡矩阵要说明面积与数值的关系，连续色不能随意改成类别色。

14 套上游参考各附原始 Python 模板；3 张 NJU-LINK 改绘由 scripts/gallery_examples.py 生成，见卡片 code/render 字段。没有匹配图时，提出数据支持的新设计并标明它不在图库中。

## 2. 选图与六部件清单

自己检查数据列、单位、分组、缺失与范围。用户要求“让我选”时展示候选后等待选择；已指定参考或要求直接画时完成首选。候选数量依复杂程度决定，不为凑数做近乎相同的草图。

例如“A 的布局 + NJU-LINK 配色”：

| 部件 | 来源 | 执行动作 |
|---|---|---|
| 布局 | raincloud-median-badges | 左侧散点、右侧半小提琴、中位数圆标 |
| 图形元素 | 同一参考 | 每个点显示真实观测，密度只辅助展示分布 |
| 配色 | NJU-LINK palette | 四个模型用 teal、sky、lavender、rose |
| 文字 | 论文约束 | 最终图宽 89 mm 时核对实际字号 |
| 装饰 | NJU-LINK 默认 | 去阴影，细灰轴与淡网格 |
| 图例 | 数据语义 | 模型轴标签 + 中位数说明 |

高保真模式记录各面板 (x, y, w, h) / 画布尺寸。先匹配布局，再匹配字体行距，最后调整细线、箭头和颜色。低质量截图不能当精确 RGB 来源；新数据造成的柱高变化不是布局失败。用户指定的参考部件优先于默认皮肤。

## 3. 演绎与可复现性

用 render_gallery.py 复制原始模板与同名 CSV 到工作目录，避免覆盖图库。已有输出会报错，另选目录并保留用户修改。

~~~bash
python scripts/render_gallery.py raincloud-median-badges bubble-matrix-upper --out figures/reference
python scripts/gallery_examples.py --output-dir figures/njulink
~~~

复制得到的脚本保留上游绘图逻辑，并追加 PDF/SVG 导出。替换脚本注释指定的数据与标签后，重新检查计算。上游 13 套是模拟数据；ranked-bars-rose-ring 的 CSV 据上游说明来自公开 diabetes 数据集的特征重要性，本仓库未重新训练该模型。这些数值都不是用户实验结果。

改绘只改变所选部件，保留统计语义。说明 KDE、平滑、归一化、排序和误差带含义，不能把装饰色带冒充置信区间。模型较多时分面，避免多条 radar 曲线堆叠。

## 4. 对照验收

~~~bash
python scripts/contact_sheet.py compare --out figures/comparison.png --labels "参考,成品" raincloud-median-badges figures/njulink/njulink-raincloud.png
~~~

先检查科学含义，再看六部件：

- 抽查最大/最小类别与若干点：数值、排序、单位、总和/比例；
- 检查零点、截断轴、颜色范围、色条、线型、图例；
- 检查换行、裁切、重叠、中文字形和对比度；
- 按目标栏宽查看，不能只看放大图；
- 列出有意改变、未解决差异与限制。

每次修复后重新渲染。对照图用于视觉验收，不代表实际模型成绩；不宣称无法验证的“相似度百分比”。

## 5. 图库维护

默认入库到被 Git 忽略的 gallery-local/。用户要求维护图库时才入库；普通出图不自动收集新图或建立偏好记录。

~~~bash
python scripts/ingest.py /path/to/figure.png --source "用户提供的本地参考"
python scripts/build_index.py
~~~

- 入库压缩长边至 2000 px，生成待鉴赏卡片；需要打开图填写，不能自动声称已鉴赏。
- 相同像素可跳过；近似布局只提醒并保留，避免误删数据不同的实验图。
- 同名不同图自动加序号，原始文件不变。
- 私有图的配色不会自动追加到公开卡片。
- edited: true 卡片不自动改写，--prune 也保留这类孤儿卡片。
- 增删后重建索引，明确要清理孤儿卡片时才加 --prune。
- 已授权公开时可显式 --gallery gallery；公共材料附来源和许可。
- 本版不使用易过时的布局缓存。

卡片沿用上游简单 YAML frontmatter（标量、内联数组、palettes 列表）及 Markdown 正文。purpose 写用途，data 写所需形状，code 相对于卡片目录。写明数据来源与参考出处；人工查看后才设 appreciated: true。taste.md 只追加用户明确表达的选择，保持本地。
