# 阶段 0：QEC 与 Surface Code 全局地图

## 本阶段要解决的问题

在接触 qubit、stabilizer 和 patch 的具体细节前，先建立三个层次的关系：

1. QEC 为什么存在、总体上怎样工作。
2. Surface code 在 QEC 中扮演什么角色。
3. *A Game of Surface Codes* 主要关注哪一层问题。

## QEC 在解决什么问题

物理量子比特会受到环境噪声、控制误差和测量误差影响。QEC 并不阻止这些物理错误发生，而是尝试阻止它们积累成 logical error。

它的基本策略是：

> 将一个 logical qubit 的信息编码到多个 physical qubits 组成的整体状态中，再通过精心设计的关系检查寻找错误留下的线索。

Logical qubit 不是其中某一个 physical qubit，也不是把一个未知量子态简单复制很多份。量子信息由多个 physical qubits 共同承载。

## 为什么不能直接检查逻辑量子态

直接测量逻辑信息，会把量子态投影到测量基的某个结果，从而破坏原本需要保护的叠加或相位信息。未知量子态也不能被随意复制出来作为备份。

QEC 因此不直接询问“逻辑信息是什么”，而是测量一组不会泄露逻辑信息的一致性关系。这些关系称为 stabilizer checks。

需要区分两种测量：

- 直接测量逻辑信息：可能破坏被保护的状态。
- 测量 stabilizer checks：只判断编码约束是否被破坏，不读取逻辑内容。

所以准确说法不是“量子系统不能测量”，而是“不能随意测量要保护的逻辑信息，但可以测量与它兼容的校验关系”。

## Syndrome 与 Decoder

Stabilizer checks 的结果模式称为 syndrome。存在测量错误时，更有用的往往是多轮结果之间的变化，之后会进一步称为 detection events。

Syndrome 是错误留下的线索，而不是：

- logical qubit 保存的内容；
- 对真实物理错误位置的直接观察；
- decoder 一定能够唯一解释的答案。

Decoder 会结合多轮 syndrome history 和噪声模型，寻找最可能的错误链或等价解释。它的任务更接近“根据多个告警诊断故障”，而不是读取一份准确的错误报告。

Decoder 得出结果后，也不一定马上对 physical qubit 施加一个修复门。很多情况下，只需要在经典系统中更新 Pauli frame，并在解释后续操作和测量结果时考虑这项修正。

## QEC 的持续闭环

QEC 是计算期间持续运行的过程：

```text
物理噪声持续发生
    ↓
执行一轮 stabilizer checks
    ↓
获得 syndrome measurements
    ↓
比较多轮结果
    ↓
decoder 推断可能的错误链
    ↓
更新 correction 或 Pauli frame
    ↓
进入下一轮
```

这里的核心不是将每个 physical qubit 恢复成某个“完美状态”，而是持续保持 logical information 的正确性。

## Surface Code 是什么

Surface code 是实现 QEC 的一种具体代码家族。它把 physical qubits 组织在二维结构中，主要依靠局部相邻操作反复测量 stabilizer checks。

现阶段只需要保留下面的轮廓：

- data qubits 共同承载逻辑信息；
- measurement/ancilla qubits 帮助测量局部校验关系；
- 完成一遍预定检查称为一个 code cycle；
- 多轮检查产生 syndrome history；
- decoder 根据这些记录推断错误；
- logical qubit 由整个二维编码区域共同承载。

Surface code 的具体格点、X/Z stabilizer、boundary 和 logical operator 将在后续阶段逐步展开。

## 三个容易混淆的概念

### QEC

编码量子信息、检测错误线索，并阻止物理错误演变成逻辑错误。

### Fault tolerance

不仅存储过程要受保护，初始化、逻辑门、测量和纠错过程自身发生少量故障时，也不能让错误灾难性扩散。

### Error mitigation

通常不在单次运行中完整检测并纠正错误，而是利用多次有噪声运行和统计处理改善最终估计。

## 论文主要关注什么

*A Game of Surface Codes* 将一个 surface-code logical qubit 抽象成 patch，将空间抽象成 tile，将一段容错操作的时间抽象成 time step。

论文主要研究：

- 怎样通过 patch initialization、measurement 和 deformation 操作 logical qubit；
- 怎样使用 lattice surgery 完成联合逻辑测量；
- 怎样组织 data block 和 magic-state distillation block；
- 怎样用更多 physical qubits 换取更短运行时间。

这种游戏抽象有意隐藏了大量底层工作，包括 physical-qubit operations、stabilizer measurements、重复 code cycles、syndrome processing 和 decoding。本学习路线会在理解游戏规则的同时逐层揭开这些内容。

## 系统分层地图

```text
量子算法
  ↓
逻辑线路与 Clifford+T
  ↓
logical qubit、patch 与 lattice surgery
  ↓
stabilizer checks、code cycles、syndrome 与 decoder
  ↓
physical gates、reset 与 measurement
  ↓
量子芯片
```

当前学习目标是先理解这张图中的 QEC 和 surface-code 层。DSL、Compiler 与硬件 ISA 会在核心知识建立之后单独讨论。

## 阶段结论

可以用下面这段话概括阶段 0：

> QEC 将 logical qubit 编码在多个 physical qubits 的整体状态中。它不直接读取要保护的逻辑信息，而是反复测量 stabilizer checks，得到错误留下的 syndrome 线索。Decoder 根据多轮线索推断最可能的错误链，并通过 correction 或 Pauli frame 防止物理错误演变成逻辑错误。Surface code 是在二维局部结构上实现这一闭环的一类 QEC，而论文主要研究其 logical patches 怎样被组织和操作。

## 自测问题

1. 为什么“测量会破坏量子态”不等于“QEC 不能进行任何测量”？
2. Syndrome、真实物理错误和 decoder 输出三者有什么区别？
3. QEC 试图修复的是每一个 physical qubit，还是 logical information？
4. Surface code 的二维局部结构与论文中的 patch/tile 抽象是什么关系？

## 下一阶段

阶段 1 将补齐阅读论文必须具备的最小量子知识，包括 qubit、测量基、Pauli X/Y/Z、superposition、entanglement、Bell pair，以及联合奇偶校验测量。
