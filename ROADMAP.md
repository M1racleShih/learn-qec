# QEC 与 Surface Code 学习 Roadmap

## 1. 学习者与目标

本 Roadmap 面向一名量子测控方向的软件开发工程师。学习者具备软件工程经验，但量子纠错、量子物理和相关数学基础较弱。

主线完成后的目标是：能够不依赖特定硬件或指令集，完整解释 QEC 与 surface code 的工作过程，并能在与科研人员沟通时识别需求涉及的对象、步骤、指标和约束。

未来需要设计 QEC DSL 和 DSL-to-Binary Compiler，但这一工程目标不会改变当前学习顺序。先建立平台无关的 QEC 心智模型，再讨论具体实现。

## 2. 为什么不完全按论文顺序阅读

论文主要讨论基于 surface-code patch 的容错计算架构和时空资源权衡。开头的 tile game 有意隐藏了 stabilizer measurement、syndrome decoding 等底层机制。

只按正文顺序阅读，容易学会 patch 游戏和资源估算，却仍然说不清物理错误究竟怎样被纠正。因此学习采用两条交替推进的线索：

- 棋盘之上：理解论文中的 tile、patch、逻辑测量和计算协议。
- 棋盘之下：理解 physical qubit、stabilizer、code cycle、syndrome、decoder 和 Pauli frame。

## 3. 核心学习路线

### [x] 阶段 0：建立全局地图

**论文锚点：** 摘要、Overview、Conclusion。

**要解决的问题：**

- 量子计算为什么需要主动纠错？
- QEC、fault tolerance 和 error mitigation 有什么区别？
- physical qubit、logical qubit 和 surface code 位于系统的哪一层？
- 论文真正试图优化什么？

**过关标准：** 能用两分钟解释“QEC 在解决什么问题，以及 surface code 扮演什么角色”。

### [x] 阶段 1：最小量子知识包

**论文锚点：** 论文默认的 qubit 与 measurement 前置知识。

**核心概念：**

- qubit、计算基和测量。
- X、Y、Z 基的直觉含义。
- Pauli X/Y/Z 操作。
- superposition、entanglement 和 Bell pair。
- 单量子比特测量与联合奇偶校验测量。
- commuting 与 anticommuting 的操作直觉。

**过关标准：** 能读懂论文图中初始化、X/Z measurement，以及 `X⊗X`、`Z⊗Z` 这类联合测量的含义。

### [x] 阶段 2：从一般纠错理解 QEC

**补充内容：** 从经典 repetition code 逐步过渡到量子纠错。

**核心概念：**

- 为什么不能通过直接读取量子态来检查错误。
- bit-flip、phase-flip 与 Pauli error。
- parity check、stabilizer、syndrome 和 detection event。
- decoder 推断的是什么，而不是什么。
- correction 与 Pauli frame。
- code distance、logical error 和 threshold。
- 为什么测量本身也会出错，以及为什么要重复多轮。

**过关标准：** 能讲清“错误发生 → syndrome 变化 → decoder 推断 → 更新 Pauli frame”的纠错闭环。

### [x] 阶段 3：学会玩 surface-code patch 游戏

**论文锚点：** 开头规则 I–III、Fig. 1–2。

**核心概念：**

- tile、one-qubit patch 和 two-qubit patch。
- 虚线/实线边界与 logical X/Z。
- initialization、single-patch measurement 和 multi-patch measurement。
- patch deformation、corner movement 和 qubit movement。
- Bell-pair preparation 与 Y-basis measurement。
- tile 与 time step 表达的空间、时间成本。

**过关标准：** 能逐步复述 Fig. 2 中至少两个协议，并计算其 tile 数和时间步。

### [x] 阶段 4：掀开棋盘看真实 surface code

**论文锚点：** Appendix A，并与阶段 3 的游戏规则逐项对照。

**核心概念：**

- data qubit 与 measurement/ancilla qubit。
- X-type 与 Z-type stabilizer。
- stabilizer measurement circuit 和 code cycle。
- syndrome history、detection event 与 decoder。
- error chain 与 logical error。
- logical string operator 与 surface-code boundary。
- patch、edge、tile、time step 的底层对应关系。

**过关标准：** 能解释一个物理错误怎样影响 stabilizer measurement、怎样形成 detection event，以及为什么一个论文时间步通常需要约 `d` 轮 code cycle。

### [ ] 阶段 5：理解 lattice surgery

**论文锚点：** 开头的 two/multi-patch measurement 与 Appendix A。

**核心概念：**

- patch merge、split 和 code deformation。
- logical `X⊗X`、`Z⊗Z` 与一般 Pauli-product measurement。
- 如何在不直接读取逻辑量子态的情况下测量逻辑奇偶性。
- lattice surgery 怎样生成纠缠和执行逻辑操作。
- 操作过程中为什么仍需维持 code distance。

**过关标准：** 能从 patch 图和 stabilizer 变化两个视角解释一次 logical `Z⊗Z` measurement。

### [ ] 阶段 6：从量子线路走到容错操作

**论文锚点：** Sec. 1 和 Sec. 1.1。

**核心概念：**

- Clifford+T gate set。
- Pauli rotation 与 Pauli-product measurement。
- T count 和 T depth。
- 为什么 Clifford operation 相对便宜，而 T gate 昂贵。
- magic-state injection、consumption、conditional correction 和 Pauli frame tracking。

**过关标准：** 能描述“普通量子线路 → Pauli-product measurements + magic states”的转换链路，并解释 T gate 为什么成为主要资源瓶颈。

### [ ] 阶段 7：数据区与 magic-state factory

**论文锚点：** Sec. 2、Sec. 3.1、Sec. 3.3 和 Sec. 3.5。

**核心概念：**

- compact、intermediate 和 fast data block。
- patch 边界可达性与空间/速度权衡。
- raw magic state 为什么不够可靠。
- 15-to-1 distillation 的输入、检测、拒绝与输出。
- factory throughput、success probability、output fidelity 和 storage。
- 多级 distillation 的直觉。

**过关标准：** 能用“工厂质检”的方式解释 magic-state distillation，并根据空间与吞吐需求比较三种 data block。

### [ ] 阶段 8：拼出完整的 surface-code 量子计算机

**论文锚点：** Sec. 4。

**核心概念：**

- 从算法规模建立 logical error budget。
- 根据目标精度选择 distillation protocol。
- 由物理错误率和运行时间选择 code distance。
- physical-qubit count、code cycle 和 wall-clock time 的关系。
- data block 的消费速度与 factory 的生产速度。
- 通过增加空间换取时间的基本方法。

**过关标准：** 给定逻辑 qubit 数、物理错误率、T count、cycle time 和目标失败率，能说出完整的资源估算和瓶颈分析步骤。

### [ ] 阶段 9：并行化、实时反馈与控制系统

**论文锚点：** Sec. 5，重点阅读 teleportation、post-correction、measurement 和 classical processing。

**核心概念：**

- quantum teleportation 的任务级直觉。
- T layer 与 T-depth parallelization。
- auto-corrected 和 post-corrected rotation。
- measurement、decoding、feed-forward 的实时性。
- decoder latency、throughput、storage 和调度为什么会限制量子计算速度。
- distributed quantum computing 只作概念了解。

**过关标准：** 能从 QEC 原理出发列出实时控制软件需要处理的数据、状态、时限和反馈关系，而不绑定某个硬件 ISA。

### [ ] 阶段 10：扩展、边界与总验收

**论文锚点：** Sec. 6–7 和 Appendix C。

**核心概念：**

- arbitrary-angle rotation 与额外 resource state。
- measurement speed、fidelity 和 code distance 的权衡。
- 论文的 tile abstraction 隐藏了哪些现实问题。
- 48-data-qubit proof-of-principle device 如何串起主要操作。

**最终验收：**

1. 完成一次从物理噪声到逻辑计算结果的端到端讲解。
2. 对一个小型 surface-code 场景画出数据流和控制流。
3. 完成一次模拟 QEC 需求沟通，能够主动确认 code variant、distance、noise model、cycle time、decoder、logical operation 和 failure budget。
4. 明确区分 QEC/surface code 的平台无关原理与后续 DSL、Compiler、ISA 的工程实现。

## 4. 首轮选修内容

以下内容不会阻塞主线，只有在项目需要或主线完成后再深入：

- Sec. 3.2 的 triorthogonal matrix 及推导。
- 完整 stabilizer formalism 的代数证明。
- surface code 的 topology/homology 数学。
- MWPM、Union-Find 等 decoder 算法实现细节。
- Appendix B 的 multi-corner patch。
- Appendix D 的 7-to-1 protocol。
- 大规模 unit、distributed architecture 和任意角蒸馏工厂的具体资源优化。

## 5. 每个阶段的推进方式

每个阶段采用相同节奏：

1. 说明本阶段要解决的实际问题。
2. 用直觉、类比和具体例子建立心智模型。
3. 对照论文中少量关键段落和图。
4. 将游戏抽象映射到底层 surface-code 机制。
5. 完成一个小练习或场景题。
6. 由学习者用自己的话复述，及时修正常见误区。
7. 将阶段笔记、术语、练习答案和遗留问题同步到仓库。

每个概念可以附带一小段“工程师视角”，说明它未来可能如何影响 DSL 或软件接口，但不会在主线完成前展开硬件指令和 Binary 细节。

## 6. 数学使用原则

- **主线层：** 尽量不依赖公式，先获得正确直觉。
- **工程层：** 只保留 code distance、错误预算和资源估算需要的公式，并逐项翻译含义。
- **理论层：** 稳定子代数、代码构造和公式推导作为选修。

公式不是验收目标。能够准确解释公式表达的物理或工程关系，才是验收目标。

## 7. 主线完成后的工程阶段

完成本 Roadmap 后，另行制定 QEC DSL 与 Compiler Roadmap。届时再引入目标硬件执行模型，讨论：

```text
QEC 概念
  ↓
QEC 操作的精确定义
  ↓
平台无关 DSL / IR
  ↓
目标相关 Machine IR
  ↓
硬件 ISA 与 Binary
```

该阶段不会反向替代本 Roadmap 中的平台无关知识。
