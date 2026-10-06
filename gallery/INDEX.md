# gallery 索引

共 17 张，已鉴赏 17 张。张扬度 1=平铺直叙，3=中规中矩，5=花里胡哨。
先按「用途」「需要的数据」筛出候选，再打开图片和卡片确认。
用途词：构成占比 7、模型解释 7、特征重要性 5、组间比较 4、相关关系 4、分布 3、趋势变化 3、模型性能 2、排序 2、网络与流向 2

| id | 标题 | 用途 | 需要的数据 | 张扬度 | 标记 |
|---|---|---|---|---|---|
| [njulink-raincloud](njulink-raincloud.png) · [卡片](njulink-raincloud.md) | 雨云图（NJU-LINK pastel，中位数圆标） | 分布、组间比较 | 少量模型各有多个逐样本得分；需要组内原始观测 | 2 | 有代码 有提醒 |
| [raincloud-median-badges](raincloud-median-badges.png) · [卡片](raincloud-median-badges.md) | 雨云图（十组，左侧点云加右侧半小提琴，圆标写中位数，每组一色） | 分布、组间比较 | 8–12 个组，每组几十到上百个观测值 | 3 | 有代码 |
| [violin-median-badges](violin-median-badges.png) · [卡片](violin-median-badges.md) | 小提琴图（十组，灰色须线贯穿，圆标写中位数，每组一色） | 分布、组间比较 | 8–12 个组，每组几十到上百个观测值 | 3 | 有代码 |
| [njulink-ribbons](njulink-ribbons.png) · [卡片](njulink-ribbons.md) | 百分比堆叠连接带（NJU-LINK pastel） | 构成占比、趋势变化 | 类别 × 阶段占比表，每列非负且合计 100% | 2 | 有代码 有提醒 |
| [grouped-stacked-rounded-bars](grouped-stacked-rounded-bars.png) · [卡片](grouped-stacked-rounded-bars.md) | 分组堆叠柱状图（三个情景各三根柱，圆角色块，顶部写合计，虚线空框标缺失部分） | 构成占比、组间比较 | 3 个大场景 × 每组 3 根柱，每根柱由 3–8 个成分叠成，每根柱有一个合计数 | 3 | 有代码 |
| [stacked-percent-bars-ribbons](stacked-percent-bars-ribbons.png) · [卡片](stacked-percent-bars-ribbons.md) | 百分比堆叠柱状图（柱间用淡色带连接，三类成分逐月变化） | 构成占比、趋势变化 | 6–12 个时间点（或类别），每个时间点有 3 个互相合计 100% 的成分占比 | 3 | 有代码 |
| [pred-vs-obs-model-grid](pred-vs-obs-model-grid.png) · [卡片](pred-vs-obs-model-grid.md) | 预测值对实测值散点（3×3 对比九个模型，按误差着色，虚线误差带，红框突出主角面板） | 模型性能、相关关系 | 每个模型一组实测值和预测值（几百个样本），分训练集和测试集；可以同时比较 6–9 个模型 | 3 | 有代码 有提醒 |
| [dependence-small-multiples](dependence-small-multiples.png) · [卡片](dependence-small-multiples.md) | 依赖图小多图（3×3，散点按贡献值着色，红色平滑线，黑色虚线标零） | 模型解释、相关关系 | 6–10 个特征，每个特征有各样本的取值和对应的贡献值 | 2 | 有代码 |
| [shap-beeswarm-blue-pink](shap-beeswarm-blue-pink.png) · [卡片](shap-beeswarm-blue-pink.md) | SHAP 蜂群图（蓝到粉红的柔和渐变，点线行引导，含交互项） | 模型解释、特征重要性 | 10–15 个特征（可含交互项），每个特征在几百个样本上的贡献值和特征取值 | 2 | 有代码 |
| [stacked-bars-two-part-rank](stacked-bars-two-part-rank.png) · [卡片](stacked-bars-two-part-rank.md) | 堆叠横向柱状图（每根柱子分蓝和粉两段，标题压在通栏横线下） | 特征重要性、构成占比、排序 | 8–12 个特征，每个特征的重要性可以拆成两个部分的贡献 | 1 | 有代码 |
| [ranked-bars-rose-ring](ranked-bars-rose-ring.png) · [卡片](ranked-bars-rose-ring.md) | 排序横向柱状图 + 嵌入式玫瑰环（图例兼做变量说明） | 特征重要性、排序、构成占比 | 5–12 个项目各有一个数值，可以换算成占比；每个项目有一个较长的说明文字 | 3 | 有代码 |
| [shap-bars-beeswarm-spine](shap-bars-beeswarm-spine.png) · [卡片](shap-bars-beeswarm-spine.md) | SHAP 重要性横向柱 + 蜂群图背靠背（共用特征轴，左下嵌螺旋玫瑰图） | 特征重要性、模型解释、构成占比 | 10–20 个特征，各有一个总体重要性数值，以及每个特征在每个样本上的贡献值和特征取值 | 4 | 有代码 |
| [njulink-bubble](njulink-bubble.png) · [卡片](njulink-bubble.md) | 上三角气泡矩阵（NJU-LINK 连续蓝色） | 相关关系、模型解释 | 变量间对称非负强度矩阵，对角为零 | 2 | 有代码 有提醒 |
| [bubble-matrix-upper](bubble-matrix-upper.png) · [卡片](bubble-matrix-upper.md) | 上三角气泡矩阵（大小和颜色双重编码，图例嵌在空白角） | 相关关系、模型解释 | 一组变量（10–20 个）两两之间各有一个强度值 | 3 | 有代码 有提醒 |
| [alluvial-stages-outlined](alluvial-stages-outlined.png) · [卡片](alluvial-stages-outlined.md) | 冲积图（五个阶段，带黑描边的竖条做节点，半透明飘带，横向虚线做刻度） | 网络与流向、构成占比、趋势变化 | 一批对象在 4–6 个阶段各属于 3–4 个类别之一，需要相邻阶段之间每对类别的转移数量 | 3 | 有代码 |
| [model-results-panel](model-results-panel.png) · [卡片](model-results-panel.md) | 分类模型结果一页图（分类指标柱、混淆矩阵、ROC、蜂群图、两幅依赖图） | 模型性能、模型解释 | 一个多分类模型的评估和解释结果：各类指标、混淆矩阵、ROC 曲线、SHAP 值 | 3 | 组合图 有代码 有提醒 |
| [interaction-ring-waterfall](interaction-ring-waterfall.png) · [卡片](interaction-ring-waterfall.md) | 环形交互网络图（两套配色并排）加 SHAP 瀑布图（箭头形柱子） | 模型解释、网络与流向、特征重要性 | 15–20 个特征的重要性和两两交互强度（可以有两组）；以及一个样本上各特征的贡献值 | 4 | 组合图 有代码 |
