# Engineering Figure Banana

`engineering-figure-banana` 不是一个通用配图平台，而是一个面向 agent 工作流的工程论文配图 skill，专门把概念图和精确定量图分开处理。

## 项目定位

这个仓库主要服务于工程与计算机论文中的“图形生产层”，而不是做一个完整的论文上传平台。

它更适合：

- 已经知道自己需要什么图的研究者
- 希望把论文图生产接入 Codex / agent 工作流的人
- 需要同时处理方法图和定量图的人
- 计算机、算法、系统、电子、嵌入式方向的作者

它不主打：

- 完整 Web 平台
- 上传论文后一键包办所有工作
- 面向所有学科的通用学术插图

## 核心差异化

### 1. 面向 agent，而不是面向平台表单

- 适合接在研究写作、代码、实验分析工作流后面
- 可以作为 Codex skill 被直接调用
- 更强调可控性、可组合性和可复用性

### 2. 概念图和定量图分开处理

- `image mode`：适合系统架构图、算法流程图、graphical abstract、工程示意图
- `plot mode`：适合柱状图、曲线图、热力图、散点图、多面板 publication plot

这点很关键：它不把所有图都当作同一种 prompt 生图问题来处理。

### 3. 更偏工程 / CS 论文，而不是泛学科

- system architecture
- algorithm workflow
- hardware block diagram
- benchmark / ablation / heatmap / scatter

### 4. 更强调论文图的准确性与可读性

- 白底、清晰层级、短标签
- 中英技术标签混合可读
- 定量图优先本地精确绘制
- 适合导出 `png / pdf / svg`

## 推荐工作流

最推荐的用法是两步走：

1. 先用 `ai-research-writing-guide` 确定：
   - 图要证明什么 claim
   - 图的类型
   - 面板结构 / 模块结构
   - caption 要保留什么信息
2. 再用 `engineering-figure-banana` 生成最终图

建议上游传给本 skill 的字段：

- figure goal
- figure type
- panel plan / module list
- must-keep terms
- output language
- visual constraints

## 仓库结构

- `README.md`：GitHub 首页双语 landing
- `README.zh-CN.md`：中文完整说明
- `README.en.md`：英文完整说明
- `SKILL.md`：Codex skill 内部说明
- `scripts/`：安装、检查、prompt 构建、图片生成、定量绘图
- `references/`：模板与论文风格参考
- `examples/figure-briefs/`：可直接复用的 figure brief 模板
- `docs/examples/`：公开示例图和说明
- `providers.md`：Provider 兼容说明

## 两种模式

### `image mode`

适合：

- 系统架构图
- 算法流程图
- 图形摘要
- 电子 / 嵌入式示意图
- 参考风格重绘

当“结构表达”比“数值精确”更重要时，用这个模式。

### `plot mode`

适合：

- benchmark 柱状图
- ablation 图
- trend curve
- heatmap
- scatter
- 多面板结果图

当数值、坐标、几何关系必须保持准确时，用这个模式。

经验法则：

- 如果数值真实性重要，用 `plot mode`
- 如果图是概念表达，用 `image mode`
- 如果一张图里两者都有，先本地渲染定量部分，再补概念部分

## 快速开始

### 1. 放到 Codex skill 目录

```powershell
$HOME/.codex/skills/engineering-figure-banana
```

### 2. 配置本地 secrets

在仓库外准备：

- `$HOME/.codex/secrets/nanobanana.env`
- `$HOME/.codex/secrets/nanobanana_api_key.txt`

模板见：

- `secrets/nanobanana.env.example`
- `secrets/nanobanana_api_key.txt.example`

### 3. 跑安装与检查

```powershell
& "$HOME/.codex/skills/engineering-figure-banana/scripts/install_and_test.ps1" -RunSetupCheck
```

### 4. 加载环境变量

```powershell
. "$HOME/.codex/skills/engineering-figure-banana/scripts/load_nanobanana_env.ps1"
```

### 5. 跑一个最小示例

```powershell
python "$HOME/.codex/skills/engineering-figure-banana/scripts/generate_image.py" `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

## 示例图

当前仓库包含：

- 自动驾驶高密度总览图
- 协同目标跟踪图
- 多智能体安全总览图
- Linux kernel 系统架构图
- 一张补充性的“健康监测与预警系统部署场景”参考图

说明见：

- `docs/examples/README.md`

## 为什么值得中英双语

我建议这个仓库长期保持中英双语：

- GitHub 自然传播更偏英文
- 小红书 / CSDN / 小黑盒传播更偏中文
- 目标用户既包括国内研究生，也包括国际 agent / open-source 用户
- 双语能显著降低理解门槛

推荐文档策略：

- `README.md`：双语 landing
- `README.zh-CN.md`：中文完整说明
- `README.en.md`：英文完整说明
- 后续重要文档如 `providers.md` 也可以逐步双语化

## 项目简介

`engineering-figure-banana` 是一个面向工程与计算机论文的 agent-native figure skill：概念图走图像模型，定量图走本地精确渲染。它更强调图形生产流程的可控性、学术风格约束和定量结果的准确表达，而不是把所有论文图都当作同一种通用生图任务来处理。

## 注意事项

- 不要把真实 API Key 提交到仓库
- 定量图尽量使用本地绘图链
- 公共文档里尽量不要硬编码私人 relay 地址
