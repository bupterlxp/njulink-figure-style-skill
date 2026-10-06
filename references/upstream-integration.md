# Plot Is All You Need 整合记录

- 上游：[liouhai/plot-is-all-you-need](https://github.com/liouhai/plot-is-all-you-need)
- 固定版本：[70898b877dc2455704070e4542db1939ff7d9ec0](https://github.com/liouhai/plot-is-all-you-need/tree/70898b877dc2455704070e4542db1939ff7d9ec0)
- 版权：Copyright (c) 2026 qc
- 许可：[MIT 全文](../licenses/plot-is-all-you-need-MIT.txt)
- 文件级清单及原始 SHA-256：[upstream-manifest.json](upstream-manifest.json)

## 纳入内容

上游该版本有 364 张图，本库纳入 14 套上游标为“自产”的 PNG、卡片、Python 和一份 CSV。图片、脚本和 CSV 原样保留；卡片只清理行尾空白。13 套是模拟数据，一套据上游说明是公开 diabetes 数据集导出的特征重要性。原卡片里的参考图 ID 保留，不代表对应论文截图已导入。

上游 README 明确把代码、文档、鉴赏卡片和“自产”图纳入 MIT；论文截图不在该许可范围，未复制进本仓库。完整参考集可在上游查看。新增三张 NJU-LINK 改绘使用模拟数据，图上有显式标签。

## 本地变更

| 内容 | 处理 |
|---|---|
| 14 套上游自产示例 | 进入 gallery/，卡片仅清理行尾空白，其他文件保持原样 |
| 四阶段工作流 | 改写为 gallery-workflow.md，连接 NJU-LINK 风格和高保真参考模式 |
| cards.py | 保护 edited: true 卡片，检测重名 ID |
| build_index.py | 增加图/卡片链接，保留用户编辑过的孤儿卡片 |
| contact_sheet.py | 增加字体回退、透明图白底、空输入检查 |
| ingest.py | 只自动跳过相同像素，相似图保留；私有入库不改公开卡片；同名加序号；移除过时缓存 |
| render_gallery.py | 复制上游模板与 CSV 到工作目录，追加 PDF/SVG 导出 |
| gallery_examples.py | 雨云图、堆叠连接带、气泡矩阵适配 NJU-LINK token |
| njulink_style.py / njulink.mplstyle | 修复热图文字对比与网格穿字、hex 颜色解析 |

上游固定候选数、安装/入库前重复询问的操作约定，改为依据用户当前任务与既有授权执行。直接出图不要求多轮选图；明确要挑选时才等待选择。

## 两套来源的角色

NJU-LINK 论文只支持 figure-grammar.md 中列出的视觉观察。新增图库属于独立来源，不能据此扩大作者个人风格的证据。默认可组合结构与 NJU-LINK 皮肤，精确参考与用户选择优先。

上游原图保留原配色；README 的三组对照展示有意改绘，不声称一比一像素复刻。后续修改 imported 文件时更新 manifest 的 modified 字段和本记录，保留 MIT 声明。
