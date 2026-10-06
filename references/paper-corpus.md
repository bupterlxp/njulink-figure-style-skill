# Jiaming Wang / NJU-LINK 公开样本清单

## 语料范围

- **身份消歧**：本次采用 [Jiaming Wang 个人主页](https://w-jessamine.github.io/) 所链接的 Google Scholar 账号（`e8DzN6AAAAAJ`），主页注明 Undergraduate Researcher、Nanjing University，研究方向为 MLLM、Agentic、World Model。
- **组织交叉核验**：使用 [NJU-LINK GitHub organization](https://github.com/NJU-LINK) 和公开 README。CoVEBench、DRIFT、CodeTracer、T2AV-Compass 等项目在组织仓库中可直接核对。
- **时间快照**：2026-10-06。主页是精选论文列表，不保证等于作者全部投稿、在审稿件或未公开项目；需要“全集”时应重新抓取主页、Scholar、ORCID、arXiv 和组织仓库并去重。
- **版权边界**：本技能只保留元数据、来源和抽象视觉规则，不再分发论文 PDF、原始 figure、数据或项目图片。

## 主页列出的 9 篇含 Jiaming Wang 论文

| # | 论文 | 署名/状态 | 公开来源 | 样本中可观察的图形 |
|---:|---|---|---|---|
| 1 | **Winning the Pruning Gamble: A Unified Approach to Joint Sample and Token Pruning for Efficient Supervised Fine-Tuning** | ICLR 2026 DATA-FM | [arXiv:2509.23873](https://arxiv.org/abs/2509.23873) · [Q-Tuning code](https://github.com/gszfwsb/Q-tuning) | EU 四象限卡片、阶段流程、浅色模块、细箭头与小图标 |
| 2 | **Train in Vain: Functionality-Preserving Poisoning to Prevent Unauthorized Use of Code Datasets** | ACL 2026 Findings | [arXiv:2604.22291](https://arxiv.org/abs/2604.22291) · [FunPoison code](https://github.com/xiaoyuanpigo/FunPoison) | pastel 分组柱图、端到端流程、代码/编译/安全图标、算法框 |
| 3 | **T2AV-Compass: Towards Unified Evaluation for Text-to-Audio-Video Generation** | ICML 2026；主页同时标为 CVPR 2026 VGBE Oral | [arXiv:2512.21094](https://arxiv.org/abs/2512.21094) · [code](https://github.com/NJU-LINK/T2AV-Compass) · [data](https://huggingface.co/datasets/NJU-LINK/T2AV-Compass) | 多环 radial 总览、sunburst、pastel 统计柱、流程图、radar |
| 4 | **Where Do Deep-Research Agents Go Wrong? Span-Level Error Localization in Agent Trajectories** | Under Review | [arXiv:2606.02060](https://arxiv.org/abs/2606.02060) · [DRIFT code](https://github.com/NJU-LINK/DRIFT) · [project page](https://nju-link.github.io/DRIFT/) | 紫色摘要卡、分阶段数据管线、错误 taxonomy 旭日、heatmap、Venn |
| 5 | **CoVEBench: Can Video Editing Models Handle Complex Instructions?** | Under Review | [arXiv:2606.08415](https://arxiv.org/abs/2606.08415) · [code](https://github.com/NJU-LINK/CoVEBench) · [project page](https://nju-link.github.io/CoVEBench/) | 虚线大容器、彩色 filmstrip、圆角流程、sunburst、radar、统计小图 |
| 6 | **Agentic-MME: What Agentic Capability Really Brings to Multimodal Intelligence?** | arXiv | [arXiv:2604.03016](https://arxiv.org/abs/2604.03016) · [code](https://github.com/ChoS3nE11ven/Agentic-MME) · [project page](https://agenticmme.github.io/) | 真实截图 + 彩色标注、三难度案例、过程表格、错误 heatmap |
| 7 | **ContextBench: A Benchmark for Context Retrieval in Coding Agents** | arXiv | [arXiv:2602.05892](https://arxiv.org/abs/2602.05892) · [code](https://github.com/EuniAI/ContextBench) · [project page](https://contextbench.github.io/) | 双 radar、pipeline 卡片、浅色标签、简洁表格 |
| 8 | **CodeTracer: Towards Traceable Agent** | arXiv | [arXiv:2604.11641](https://arxiv.org/abs/2604.11641) · [code](https://github.com/NJU-LINK/CodeTracer) · [project page](https://nju-link.github.io/CodeTracer/) | 彩色阶段框、分层 trace 树、Venn、黑色 takeaway 条 |
| 9 | **A Survey of Linear Attention: Algorithm, Theory, Application, and Infrastructure** | Survey / TechRxiv | [TechRxiv PDF](https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.177032877.70562626/v1) · [code](https://github.com/btzyd/Awesome-Linear-Attention-Survey) | 主页没有 cover；本次未能从 TechRxiv 下载 PDF，因此不把它的图形细节纳入高置信度规则 |

## T2AV-Compass 图级参考索引

T2AV-Compass 的“精髓图”不再只停留在论文条目里，而是固定到项目仓库同一 commit 的图像资源。以下链接用于视觉观察和复现前测量；没有把原始文件作为本 skill 的公开资产提交。

| 官方资源 | 适合观察的部件 | 固定版本 |
|---|---|---|
| [main_00.jpg](https://github.com/NJU-LINK/T2AV-Compass/blob/7575ae07cf969c3f5d439644ecb9979862370523/docs/static/images/main_00.jpg) · [raw](https://raw.githubusercontent.com/NJU-LINK/T2AV-Compass/7575ae07cf969c3f5d439644ecb9979862370523/docs/static/images/main_00.jpg) | radial comparison、分布图、横向条、三层 sunburst 的总览编排 | `7575ae07cf969c3f5d439644ecb9979862370523` |
| [datapipe.jpg](https://github.com/NJU-LINK/T2AV-Compass/blob/7575ae07cf969c3f5d439644ecb9979862370523/docs/static/images/datapipe.jpg) | 大虚线容器、阶段卡片、短箭头、LLM/人工 QA 交接 | 同上 |
| [radar_six_panels_integrated.svg](https://github.com/NJU-LINK/T2AV-Compass/blob/7575ae07cf969c3f5d439644ecb9979862370523/docs/static/images/radar_six_panels_integrated.svg) | small multiples、共享轴语义、跨面板颜色复用 | 同上 |
| [avbench_00.jpg](https://github.com/NJU-LINK/T2AV-Compass/blob/7575ae07cf969c3f5d439644ec9979862370523/docs/static/images/avbench_00.jpg) | prompt 高亮、视频 filmstrip、音频波形、定性分数 | 同上 |

精确文件哈希、离线抓取命令和许可边界见 [t2av-compass-assets.json](t2av-compass-assets.json) 与 [t2av-compass.md](t2av-compass.md)。

## NJU-LINK 组织仓库中的作者核验

公开 README 的 BibTeX 中明确出现 `Jiaming Wang` 的仓库至少包括：

- [NJU-LINK/DRIFT](https://github.com/NJU-LINK/DRIFT)：论文题名与 arXiv `2606.02060` 一致；
- [NJU-LINK/CoVEBench](https://github.com/NJU-LINK/CoVEBench)：论文题名与 arXiv `2606.08415` 一致。

组织仓库的项目数会随时间变化；不能用当前仓库 README 的命中数声称“作者全部论文”。

## 复刻时的引用写法

建议在项目 README 或图注中写：

> Figure grammar adapted from publicly available NJU-LINK/Jiaming Wang paper figures; layout and palette are independently reimplemented with synthetic/user-owned data.

如需发布原始图片、项目 logo 或论文数据，必须另行核对许可证和作者/项目要求。
