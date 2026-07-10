# learn-qec

这是一个面向量子测控软件工程师的 QEC 学习仓库。

当前学习从接近零基础开始，以 Daniel Litinski 的论文 *A Game of Surface Codes: Large-Scale Quantum Computing with Lattice Surgery* 为主要阅读材料，目标不是记住术语或公式，而是逐步建立一套能够用于科研沟通的完整心智模型：

> 物理错误如何被发现和解码，surface code 如何保护逻辑量子比特，以及逻辑操作如何通过 patch、code cycle 和 lattice surgery 执行。

## 学习目标

完成主线后，应当能够：

- 用通俗语言解释 QEC 在解决什么问题。
- 区分 physical qubit、logical qubit、stabilizer、syndrome 和 decoder。
- 描述一轮 surface-code error-correction cycle 的完整数据流。
- 解释 logical operator、boundary、code distance 和 threshold 的意义。
- 解释 patch initialization、measurement、deformation 与 lattice surgery。
- 理解 Clifford+T、Pauli product measurement 和 magic state 在容错计算中的作用。
- 从物理错误一路讲到逻辑计算结果，并听懂科研人员提出的主要 QEC 需求。

DSL、Compiler 和硬件 ISA 是本项目的后续工程背景，不是当前学习主线。只有在 QEC 与 surface code 的核心知识建立起来之后，才会单独讨论如何把这些概念表达成 DSL，并 Lower 到具体硬件。

## 当前进度

- 已确认学习目标与教学方式。
- 已制定完整学习 Roadmap。
- 已完成阶段 0：建立 QEC 与 surface code 的全局地图。
- 下一阶段：阶段 1——最小量子知识包。

## 仓库导航

- [学习 Roadmap](ROADMAP.md)：阶段安排、验收标准和选修内容。
- [阶段学习笔记](docs/learning/README.md)：已完成阶段的知识、验收和遗留问题。
- [论文转换稿](docs/arxiv/A_Game_of_surface_code-1808.02892v3.md)：主阅读材料。
- [论文来源与许可](docs/arxiv/README.md)：原始论文、CC BY 4.0 许可和转换说明。

后续每完成一个阶段，都会将阶段笔记、术语、练习和遗留问题记录到仓库，并以独立提交同步到 GitHub。

## 学习原则

- 先理解问题，再引入术语。
- 优先使用直觉、图示和具体例子。
- 数学只在无法替代或进行工程估算时引入。
- 关键英文术语与中文解释同时保留，方便后续阅读论文和参与技术讨论。
- 当空间关系、流程或状态变化用图更容易理解时，主动生成并保存 Mermaid、SVG/PNG、Draw.io 或其他合适的教学图。
- 每个阶段必须通过复述或小练习验收，而不是仅仅“读过”。
- 工程视角只作为简短旁注，不让硬件指令集干扰 QEC 主线。
