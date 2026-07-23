# 阶段 3：学会玩 surface-code patch 游戏

## 本阶段要解决的问题

这一阶段学习 Litinski 论文开头的 tile game。目标不是立即理解每个 physical check，而是能够在棋盘抽象上完成三件事：

1. 看懂 tile、patch、boundary 和 logical qubit 分别表示什么。
2. 根据 initialization、measurement 和 deformation 规则复述一个协议。
3. 计算协议最多占用多少 tiles、经过多少 time steps。

读完后，应该能够独立复述论文 Fig. 2a 的 Bell-pair preparation 和 Fig. 2d 的 logical Y measurement，并解释它们的空间、时间成本。

本阶段采用一个明确的停止点：

> 先会正确使用 tile-game 规则。Physical stabilizer circuit、syndrome history、decoder 和 check-generator replacement 留到阶段 4、5。

## 1. 最小心智模型

### Tile 是空间计价单位

一个 tile 不是一个 physical qubit，也不是一个 logical qubit。对于 code distance `d` 的 surface code，一个 tile 大致代表一块包含 `d²` 个 physical data qubits 的区域。

在游戏中只需要把它理解成：

```text
tile 数量越多 → 占用的 physical 空间越多
```

### Patch 是棋盘上的编码区域

Patch 是由许多 physical qubits 实现的 surface-code 区域。它可以改变形状、跨越多个 tiles，也可以在 measurement 后被移除。

Patch 和 logical qubit 不是同义词：

- 一个 patch 可以保存一个 logical qubit。
- 一个 patch 也可以保存两个 logical qubits。
- 一个 logical qubit 的 patch 可以为了操作而临时拉长，占用多个 tiles。

### Logical qubit 是 patch 保存的信息

Logical qubit 不是 patch 中额外藏着的一个 physical qubit。它是一份由整个 patch 的编码关系共同保存的信息。

因此，判断 logical qubit 数量要看 patch 类型，而不能数 tiles：

```text
Fig. 1a：1 tile，1 patch，1 logical qubit
Fig. 1b：3 tiles，1 patch，1 logical qubit
Fig. 1c：2 tiles，1 patch，2 logical qubits
```

![论文 Fig. 1：one-qubit 与 two-qubit patches](../../arxiv/images/21016cb94492e92e0fd7c5dfea7909623f82c3f73f64137f63052093a55ad668.jpg)

### Time step 是主要时间成本

论文把大约随 code distance `d` 增长的操作记为 `1 time step`。一个 code cycle 可以先理解成“把当前全部底层 checks 各执行一轮”；一个 time step 通常对应约 `d` 轮 code cycles，但不是严格等号。

`0 time step` 不表示：

- 现实中完全不耗时间；
- 操作一定很可靠；
- 不会引入 logical error。

它只表示这项成本不作为随 `d` 增长的主要时间项计算，或者能够与紧接着的操作重叠完成。

## 2. Boundary 表示什么

One-qubit patch 有两类边界：

- 论文图中的虚线边表示 logical X。
- 论文图中的实线边表示 logical Z。

“边界表示 logical operator”可以用下面这句话理解：

> 沿这条边存在一整串 physical Pauli operators，它们联合起来具有 logical X 或 logical Z 的效果。

边界标签本身不是一次 measurement。它只告诉协议设计者：

- 这个位置能够作为相应 logical operator 的接口；
- 如果另一条合适的边靠近这里，可以安排 joint logical measurement。

例如，两块 patch 的 Z 边相邻时，可以安排：

```text
logical Z₁ ⊗ Z₂ measurement
```

这次 measurement 只返回一个联合结果，不返回 `Z₁、Z₂` 的两个单独答案。

Two-qubit patch 的六条边还可以表示 `X₁`、`Z₁`、`X₂`、`Z₂`，以及 `X₁⊗X₂`、`Z₁⊗Z₂`。一个 patch 因此可以保存两个 logical qubits，但仍然只是一块连续的 patch。

## 3. 三类游戏操作

### Initialization

One-qubit patch 可以初始化为 logical `|0⟩` 或 logical `|+⟩`，游戏成本为 `0 time step`。

Two-qubit patch 可以同时初始化为：

```text
logical |0⟩ ⊗ |0⟩

或者

logical |+⟩ ⊗ |+⟩
```

任意 logical state 也可以通过 state injection 初始化，但结果可能带有未检测的 logical Pauli error。这个规则的底层预览单独放在 [state injection 补充笔记](state-injection.md) 中，不属于本阶段的必考细节。

### Single-patch measurement

Single-patch X/Z measurement 会直接读出一个 patch 保存的 logical qubit，并移除该 patch：

```text
测量前：棋盘上有一个 logical qubit
测量后：得到一个经典结果，logical qubit 与 patch 被移除，tile 释放
```

对于 two-qubit patch，两个 logical qubits 必须同时使用相同 basis 测量。它会产生两个经典结果，并移除整个 patch。

需要区分：

- `logical Z measurement` 说明测什么。
- `single-patch Z measurement` 说明怎样测，以及测完会移除 patch。

### Two-patch joint measurement

如果两个 patch 的相应边界相邻，可以测量 logical Pauli product，例如：

```text
Z₁ ⊗ Z₂
```

它只返回一个 `+1/-1`，表示两个 logical answers 的联合关系。它不会分别告诉我们 `Z₁` 和 `Z₂`，也不会移除两个 data patches。

这类操作成本为 `1 time step`。

### Multi-patch measurement

可以在多个 data patches 之间临时初始化一块 ancilla patch，使它同时接触多个 logical boundaries。

整个操作只测量一个 Pauli product，例如：

```text
Y₁ ⊗ X₃ ⊗ Z₄ ⊗ X₅
```

它只产生一个全局结果，不能从中推出任何一个因子的单独答案。Measurement 完成后移除 ancilla，data logical qubits 保留。

### Patch deformation

Patch 可以改变形状，但形状变化不等于 logical state 变化。

- 向空闲区域扩张：需要建立新区域的保护关系，成本为 `1 time step`。
- 从已有区域收缩：通过 measurement 移除旧区域，成本记为 `0 time step`。
- Corner movement：改变 X/Z boundaries 的相对位置，成本为 `1 time step`。
- Qubit movement：先扩张，再从另一端收缩；总成本为 `1 time step`。

能够并行完成的 expansion 与 corner movement 可以共用同一段主要等待时间，不必机械地相加。

## 4. 怎样计算 tile 与 time cost

计算空间时，找协议任意时刻同时占用 tiles 最多的那一步：

```text
space cost = 最大同时占用 tile 数
```

计算时间时，看图上累计的时钟数字，而不是数 Step 标签：

```text
time cost = 最后一步的累计 time-step 数
```

多个互不依赖的操作可以在同一个 time step 内并行。收缩、single-patch measurement 等 `0 time step` 操作不会增加主要累计时间。

## 5. Fig. 2a：Bell-pair preparation

![论文 Fig. 2a：Bell-pair preparation](../../arxiv/images/159f660a76c50c622a9ff67c7546fbee4d46e7b977abf9d251aef3b819f1d17f.jpg)

Step 1 初始化两个独立的 logical `|+⟩` patches：

```text
|+⟩₁ ⊗ |+⟩₂
```

这时还没有 Bell pair。

Step 2 测量：

```text
logical Z₁ ⊗ Z₂
```

- 结果 `+1`：得到 `(|00⟩+|11⟩)/√2`。
- 结果 `-1`：得到 `(|01⟩+|10⟩)/√2`。

这里是两个 branches 共同保留的 coherent superposition，不是经典地随机挑中了其中一个 bit string。

这是 two-patch joint measurement。两个 patches 都保留，两个 logical qubits 组成 Bell pair；必要的已知 Pauli correction 可以记录在 Pauli frame 中。

资源成本：

```text
最大空间：2 tiles
总时间：1 time step
```

## 6. Fig. 2b/c：改变形状与移动 qubit

### Moving corners

![论文 Fig. 2b：moving corners](../../arxiv/images/62d2aa14fc19ef4687e3567c5ef02623b7380fa7e17839f84c4c7c14db661d27.jpg)

Corner movement 改变 patch 上 X/Z boundaries 的接口位置。Patch 保存的 logical state 不会因为边界几何变化而自动改变。

这类变化需要约 `d` 轮底层关系检查，所以游戏成本为 `1 time step`。

### Qubit movement

![论文 Fig. 2c：qubit movement](../../arxiv/images/bfebf23e33a18d22b769b905a7317e8e3b67581c99158ca605ba15c08cacdbac.jpg)

Step 1：一个 one-tile patch 保存 logical `|q⟩`。

Step 2：patch 向右扩张，占满三个 tiles，成本累计到 `1 time step`。

Step 3：从左侧收缩，只留下最右 tile。收缩不增加主要时间成本。

```text
最大空间：3 tiles
总时间：1 time step
logical qubit 数量：始终为 1
```

## 7. Fig. 2d：logical Y measurement

![论文 Fig. 2d：logical Y measurement](../../arxiv/images/0eaa8a9ed7199b44f9bd63cf56bcd94f3d871cd0407585b5ce7303b2a4033500.jpg)

Step 1：棋盘有四个 tiles，logical `|q⟩` patch 占一个 tile。

Step 2：

- data patch 扩张并移动 corners，使同一侧能够访问 logical X 和 Z boundaries；
- 下方两个 tiles 初始化一个 logical `|0⟩` ancilla；
- 这些变化共用一个 deformation 时段，累计为 `1 time step`。

Step 3 测量：

```text
Z_ancilla ⊗ Y_data
```

Ancilla 的 Z boundary 同时邻接 data patch 的 X、Z boundaries。Tile-game 规则把相邻的 Pauli factors 乘在一起，而 `Y=iXZ`，所以 data qubit 以 logical Y 参与这次 measurement。

因为 ancilla 初始化为 logical `|0⟩`，它的 logical Z answer 已知为 `+1`，所以 joint result 就是 data qubit 的 logical Y measurement result。

Step 4：

- 对 ancilla 做 single-patch Z measurement，将 ancilla logical qubit 和 patch 移除；
- data logical qubit 保留，但原来的未知状态已经被 Y measurement 改成与测量结果对应的 Y state；
- data patch 收缩回原形，不增加主要时间成本。

资源成本：

```text
最大空间：4 tiles
总时间：2 time steps
```

## 8. Fig. 2e：multi-patch measurement

![论文 Fig. 2e：multi-patch measurement](../../arxiv/images/c6db0daca0364fd2f39dabb3e2aa170eb3c2a5d4e2c7c99d06a83d99d3ca603c.jpg)

图中的 ancilla patch 同时接触多个 data boundaries，因此测量一个整体 operator：

```text
Y₁ ⊗ X₃ ⊗ Z₄ ⊗ X₅
```

- `q₂` 没有接触 ancilla，所以不参加 measurement。
- 整次 measurement 只有一个 `+1/-1` 结果。
- 不能从一个结果推出 `Y₁`、`X₃`、`Z₄`、`X₅` 的单独答案。
- Measurement 后 ancilla 被移除，五个 data logical qubits 仍然存在。
- 主要时间成本为 `1 time step`。

## 9. 必须分清的概念

### Pauli operation 不等于 Pauli measurement

Pauli X operation 会交换 Z-basis states：

```text
|0⟩ ↔ |1⟩
```

X measurement 不会“执行一次 X flip”。它返回 `+1/-1`，并让 qubit 进入相应的 X state：

```text
X measurement = +1 → |+⟩
X measurement = -1 → |−⟩
```

如果一个 measurement 使另一条旧关系失去确定性，不能把它描述成“measurement 对 qubit 施加了 Pauli flip”。更完整的 compatibility 解释留到阶段 4。

### Joint measurement 不是分别测量

`Z₁⊗Z₂` 只问一个联合问题。它不会先读出 `Z₁、Z₂` 再在经典软件里相乘。

### Patch 被移除不等于 logical qubit 被搬到别处

Single-patch measurement 会消耗并移除该 logical qubit。之后在空 tile 上初始化的是一个新的 logical qubit。

### Boundary label 不代表 measurement 已经发生

边界只标出 logical operator 的支持位置和可用接口。只有协议明确安排 measurement 时，才会产生经典结果并改变量子状态。

## 10. 本阶段到哪里停止

### 必须理解

- tile、patch、logical qubit 是不同层次的对象。
- boundary 表示 logical operator 接口，不是 measurement result。
- single-patch measurement 会移除 patch；joint measurement 通常保留 data patches。
- Pauli-product measurement 只产生一个整体结果。
- expansion、shrink、corner movement 怎样计时。
- 能复述 Bell-pair preparation 与 logical Y measurement。

### 简单工作模型即可

- `1 time step` 大约对应 `d` 轮 code cycles。
- joint measurement 的底层会临时改变 physical checks。
- state injection 用固定轮数把 noisy physical state 编码成 noisy logical state。

### 留到后续阶段

- 每个 face check 的 measurement circuit。
- stabilizer generators 怎样替换。
- odd/even overlap 的完整 algebra。
- syndrome history 怎样交给 decoder。
- lattice surgery merge/split 的 physical error paths。

## 阶段结论

可以用下面这段话概括阶段 3：

> Tile game 用 tiles 计算主要空间成本，用 time steps 计算随 code distance 增长的主要时间成本。Patch 是 surface-code 编码区域，logical qubit 是 patch 保存的信息，boundary 是 logical Pauli operator 的可用接口。Initialization、single-patch measurement、joint measurement 和 patch deformation 能组合成 Bell preparation、qubit movement、logical Y measurement 与 multi-patch measurement。Joint measurement 只返回一个整体关系结果，通常保留 data patches；single-patch measurement 则读出并移除 patch。

## 验收记录

本阶段已经能够独立说明：

- Fig. 1a/b/c 中 tile、patch 与 logical-qubit 数量的区别。
- logical boundary label 与实际 measurement 的区别。
- logical measurement 描述“测什么”，single-patch measurement 描述“怎样测以及是否移除 patch”。
- Bell-pair preparation 的初始化、`Z₁⊗Z₂` measurement、最终 patch 状态和 `2 tiles × 1 time step` 成本。
- logical Y measurement 的 deformation、ancilla、`Z_ancilla⊗Y_data` measurement、清理步骤和 `4 tiles × 2 time steps` 成本。
- multi-patch measurement 为什么只有一个结果，而且不能推出各个 Pauli factors 的单独答案。
- qubit movement 为什么 expansion 计时而 shrink 不增加主要时间。
- Pauli X operation 与 X measurement 的区别。

## 自测问题

1. 一个 patch 从 1 tile 拉长到 3 tiles 后，为什么仍可能只保存一个 logical qubit？
2. Boundary 上写着 logical X，是否表示 X measurement 已经发生？
3. `Z₁⊗Z₂=-1` 能否推出 `Z₁=-1`？为什么？
4. Two-qubit patch 做 single-patch X measurement 后，会留下几个 logical qubits 和几个经典结果？
5. Fig. 2c 为什么占 3 tiles，却只花 1 time step？
6. Fig. 2d 的 ancilla 为什么初始化为 logical `|0⟩`？
7. 为什么 X measurement 不能描述成“对 qubit 施加一次 Pauli X”？

## 下一阶段

阶段 4 将掀开 tile game 的抽象层，逐项学习 physical data qubit、measurement ancilla、X/Z stabilizer、code cycle、syndrome history、detection event 和 decoder。届时再严格解释一个 physical error 怎样改变 surface-code checks，以及为什么一个 time step 通常需要约 `d` 轮 code cycles。
