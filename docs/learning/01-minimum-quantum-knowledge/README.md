# 阶段 1：最小量子知识包

## 本阶段要解决的问题

这一阶段不追求完整学习量子力学，只补齐理解 QEC 和 surface code 必须具备的最小知识：

1. Z basis 和 X basis 是在问什么。
2. Pauli X、Y、Z error 会改变什么。
3. Bell Pair 为什么不是普通的随机 `00/11`。
4. `XX`、`ZZ` 联合测量提供了什么信息，又刻意隐藏了什么信息。
5. `commute` 和 `anticommute` 在错误检查中是什么意思。

这一阶段最重要的结论是：

> QEC 可以只测量 Qubit 之间的关系，获得错误线索，同时不读取被保护的具体量子信息。

如果某个结论看起来跳得太快，可以同时阅读[阶段 1 真实问题详解](questions.md)。补充章节保留了 basis、H、Bell Pair、联合测量和 error check 学习中真正容易卡住的细节，以及尚未宣称掌握的数学内容。

## 1. 先区分三类动作

学习后续内容前，先把下面三件事分开：

- **Preparation**：把 Qubit 准备成指定状态，例如 `|0⟩` 或 `|+⟩`。
- **Gate / operation**：改变状态，例如 H、X、Z 和 CNOT。
- **Measurement**：向 Qubit 提出一个指定方向的问题，并得到经典结果。

Qubit 不是一个可以随时读取内部值的普通 bit。对它做 measurement 会产生结果，也可能改变之后的状态。因此，每次看到量子操作时，都应该先问：

1. 开始准备了什么状态？
2. 中间执行了什么操作？
3. 最后用什么 basis 测量？
4. 实际能够观察到什么结果？

## 2. Basis 是测量方向

同一个 Qubit 可以沿不同方向测量。`basis` 可以先理解成“这次 measurement 选择了哪一组问题和答案”。

### Z basis

Z measurement 区分：

| 状态 | Readout bit | `+1/-1` 表示 |
| --- | --- | --- |
| <code>&#124;0⟩</code> | `0` | `+1` |
| <code>&#124;1⟩</code> | `1` | `-1` |

如果输入 `|+⟩` 或 `|−⟩`，Z measurement 会随机得到 `0` 或 `1`，各占 50%。

### X basis

X measurement 区分：

| 状态 | X measurement 结果 |
| --- | --- |
| <code>&#124;+⟩</code> | `+1` |
| <code>&#124;−⟩</code> | `-1` |

如果输入 `|0⟩` 或 `|1⟩`，X measurement 会随机得到 `+1` 或 `-1`，各占 50%。

所以 `|+⟩` 和 `|−⟩` 不是“一个更像 0，一个更像 1”。它们是 X 方向上的两个相反状态。

Bloch Sphere 是一张表示单 Qubit 状态方向的地图。图上的球不是一个真实存在的物体；箭头指向哪里，表示这个状态在哪个 measurement 方向上具有确定答案。图里把这种具有明确方向的状态称为 pure state（纯态）。

![Z basis 与 X basis 的 Bloch Sphere](assets/bloch-sphere-z-x-basis.png)

读这张图时只需要注意：

- `|0⟩` 和 `|1⟩` 位于 Z 轴两端。
- `|+⟩` 和 `|−⟩` 位于 X 轴两端。
- 状态方向和 measurement 方向一致时，结果确定。
- 两个方向垂直时，结果是 50/50。
- 图里的 `mixture` 表示机器随机准备 `|0⟩` 或 `|1⟩`，不是一个具有确定方向的状态。

### 为什么只看 Z measurement 不够

下面两个状态做 Z measurement 时，结果完全相同：

```text
|+⟩  →  0、1 各 50%
|−⟩  →  0、1 各 50%
```

但做 X measurement 时：

```text
|+⟩  →  一定得到 +1
|−⟩  →  一定得到 -1
```

因此，只知道 Z measurement 的概率，无法判断状态是 `|+⟩` 还是 `|−⟩`。还需要换一个 basis 提问。

### Superposition 不是普通的随机 mixture

比较两台机器：

```text
机器 A：每次都准备 |+⟩
机器 B：抛硬币后准备 |0⟩ 或 |1⟩
```

对它们做 Z measurement，结果都是 `0/1` 各 50%。但换成 X measurement：

```text
机器 A：一定得到 +1
机器 B：+1/-1 各 50%
```

`|+⟩` 是一个 superposition state。这里可以先把 superposition 理解成：它不是“Qubit 其实已经偷偷选了 0 或 1，只是我们不知道”。换一个 measurement basis 后，它能表现出普通随机 mixture 没有的确定结果。

### H gate 的操作性理解

目前可以把 H gate 当成 Z basis 和 X basis 之间的转换器：

| 输入状态 | 执行 H 后 |
| --- | --- |
| <code>&#124;0⟩</code> | <code>&#124;+⟩</code> |
| <code>&#124;1⟩</code> | <code>&#124;−⟩</code> |
| <code>&#124;+⟩</code> | <code>&#124;0⟩</code> |
| <code>&#124;−⟩</code> | <code>&#124;1⟩</code> |

硬件如果只有 Z readout，可以先执行 H，再做 Z measurement，从而实现 X measurement：

```text
X measurement ≈ H gate + Z measurement
```

这里的重点不是所有硬件都必须用同一种脉冲实现，而是两种操作在抽象层上的效果相同。

## 3. Basis 的矩阵表示：只用于认符号

论文或代码里常用一列数字表示一个 Qubit 状态。为了避免矩阵依靠空格对齐，这里使用软件里常见的一行写法：

```text
col(a, b) = 上面是 a、下面是 b 的二行一列向量
```

四个状态的坐标是：

| 状态 | 列向量的一行写法 |
| --- | --- |
| <code>&#124;0⟩</code> | `col(1, 0)` |
| <code>&#124;1⟩</code> | `col(0, 1)` |
| <code>&#124;+⟩</code> | `(1/√2) × col(1, 1)` |
| <code>&#124;−⟩</code> | `(1/√2) × col(1, -1)` |

把一组 basis 的两个列向量并排放置，就得到 basis matrix：

```text
Z basis matrix：B_Z = [[1, 0], [0, 1]]
X basis matrix：B_X = (1/√2) × [[1, 1], [1, -1]]
```

`[[a, b], [c, d]]` 采用代码里的二维数组写法：第一个方括号 `[a, b]` 是矩阵第一行，第二个方括号 `[c, d]` 是第二行。

现在只需要知道：

- 这是状态在一组 basis 下的坐标，不是两次 measurement 的输出。
- `|−⟩` 里的负号不是“负概率”。
- 这个负号不会让 Z measurement 的 50/50 发生变化，但会让 X measurement 区分 `|+⟩` 和 `|−⟩`。

不需要在当前主线中计算这些矩阵。

## 4. Pauli X、Z、Y 做了什么

### Pauli X：bit flip

X 会交换 Z 方向的两个状态：

```text
|0⟩ ↔ |1⟩
```

因此，X error 会翻转 Z measurement 的答案。在 Bloch Sphere 上，它相当于绕 X 轴旋转 180°。

### Pauli Z：phase flip

Z 不会改变 `|0⟩` 和 `|1⟩` 的 Z measurement 结果，但会交换 X 方向的两个状态：

```text
|+⟩ ↔ |−⟩
```

因此，Z error 会翻转 X measurement 的答案。在 Bloch Sphere 上，它相当于绕 Z 轴旋转 180°。

### Pauli Y：同时影响两类信息

在当前关心的错误检查效果上，可以把 Y error 看成同时带有 X error 和 Z error 的作用：

- Z measurement 的答案会翻转。
- X measurement 的答案也会翻转。

![Pauli X、Y、Z 的 Bloch Sphere 旋转](assets/pauli-rotations-bloch-sphere.png)

这里不用记旋转公式，只需要记住：

| Error | Z measurement | X measurement |
| --- | --- | --- |
| X | 翻转 | 不翻转 |
| Z | 不翻转 | 翻转 |
| Y | 翻转 | 翻转 |

## 5. 从两个 Qubit 到 Bell Pair

两个 Qubit 在一个 basis 下“单独随机、合起来相关”，还不足以证明存在 **entanglement**，因为普通机器随机准备 `00/11` 也能做到这一点。

Bell Pair 是最简单的 entangled two-qubit state。它的特点是：不能用“机器只是随机准备一对普通单 Qubit 状态”复制它在不同 measurement basis 下的全部关系。下面会用 `ZZ` 和 `XX` 两组结果看到这个区别。

### CNOT 的操作性理解

CNOT 有一个 control Qubit 和一个 target Qubit：

- control 是 `0`：target 不变。
- control 是 `1`：target 翻转。

例如：

```text
CNOT(1, 1) → 10
```

第一个 Qubit 是 control，所以第二个 Qubit 从 `1` 翻成 `0`。

### 制备 Bell Pair

从 `|00⟩` 开始：

```text
准备 |00⟩
   ↓
对 A 执行 H
   ↓
执行 CNOT(A → B)
   ↓
得到 Bell Pair |Φ+⟩
```

现在分别看 A 或 B：

- Z measurement 都是 `0/1` 各 50%。
- X measurement 都是 `+1/-1` 各 50%。

但把两边结果放在一起比较，会看到稳定关系：

- 两边都做 Z measurement：只出现 `00` 或 `11`，所以 `ZZ = +1`。
- 两边都做 X measurement：只出现 `++` 或 `−−`，所以 `XX = +1`。

![Bell Pair 的单 Qubit 状态和联合关系](assets/bell-pair-correlations.png)

### Bell Pair 不是普通的随机 `00/11`

如果一台普通机器随机准备 `00` 或 `11`：

- Z measurement 也会始终相同。
- 但 X measurement 会出现 `++`、`+−`、`−+`、`−−`，各占 25%。

因此，仅看到 `ZZ = +1` 不能证明存在 Bell Pair。Bell Pair 还具有 `XX = +1` 的确定关系。

这也是为什么单独看 A 或 B 不够：Bell Pair 的关键信息存在于两者的联合关系中。单 Qubit Bloch Sphere 无法独自表达这份关系。

## 6. `ZZ` 和 `XX` 在测量什么

`Z⊗Z` 经常简写成 `ZZ`。这里的 `⊗` 可以先读成“把 A 的 Z 和 B 的 Z 组成一个联合关系检查”。`XX` 同理。

### `ZZ` 的结果

| A、B 的 Z 结果 | `ZZ` |
| --- | --- |
| 相同：`00` 或 `11` | `+1` |
| 不同：`01` 或 `10` | `-1` |

### `XX` 的结果

| A、B 的 X 结果 | `XX` |
| --- | --- |
| 相同：`++` 或 `−−` | `+1` |
| 不同：`+−` 或 `−+` | `-1` |

在理解结果含义时，可以先想象分别测量再比较。但真正用于 QEC 的联合测量与“分别读取 A、B”有关键区别。

### 分别测量与联合测量不是一回事

假设 Bell Pair 在 Z basis 下只会表现为 `00` 或 `11`：

| 操作 | 得到的信息 | 对被保护信息的影响 |
| --- | --- | --- |
| 分别测量 A、B | 明确知道 `00` 或 `11` | 泄露每个 Qubit 的值，破坏 Bell Pair |
| 联合测量 `ZZ` | 只知道“相同”，即 `+1` | 不知道是 `00` 还是 `11`，可以保留被保护的信息 |

联合 `ZZ` measurement 可以先看成下面的黑盒接口：

```text
输入：Qubit A、Qubit B

输出：
  +1  →  A、B 的 Z 关系相同
  -1  →  A、B 的 Z 关系不同
```

它不会输出 `A=0, B=0` 这种单 Qubit 信息。以后学习 surface code 时，会看到 ancilla Qubit 怎样帮助硬件只带出这个关系结果。Ancilla 是临时参与检查、最后被测量的辅助 Qubit，不用于直接保存逻辑内容。

这说明 QEC 中“获得更少的信息”反而是一项必要能力：只提取错误线索，不读取需要保护的量子内容。

## 7. Error 怎样翻转 relationship check

下面都假设只有 A、B 中的一个 Qubit 发生 error。

### 单个 X error 翻转 `ZZ`

原本 `ZZ = +1`，说明两边的 Z 结果相同。假设 B 发生 X error：

```text
00 → 01
11 → 10
```

原来的“相同”变成“不同”，所以 `ZZ` 从 `+1` 变成 `-1`。

![单个 X error 怎样翻转 ZZ](assets/x-error-flips-zz-bloch.png)

X error 不会翻转 X measurement 的答案，所以 `XX` 保持不变。

### 单个 Z error 翻转 `XX`

Z error 会让受影响 Qubit 的 X measurement 答案 `+ ↔ −`：

```text
++ → +−
−− → −+
```

原来的“相同”变成“不同”，所以 `XX` 从 `+1` 变成 `-1`。Z error 不改变 Z measurement 的答案，因此 `ZZ` 保持不变。

### 单个 Y error 同时翻转两种 check

Y error 同时具有上面两类效果：

```text
ZZ：+1 → -1
XX：+1 → -1
```

### 一个 check 没报警，不代表没有 error

如果 A、B 同时发生 X error：

```text
00 → 11
11 → 00
```

两边仍然相同，因此 `ZZ` 还是 `+1`。两个 Z error 对 `XX` 也有类似效果。

所以 check 只提供一条关系线索：

- `-1` 表示这条关系被改变了。
- `+1` 表示这条关系当前仍然满足。
- 单独一个结果不能证明系统完全没有 error，也通常不能确定哪个 Qubit 出错。

后续 QEC 会组合很多相邻 check，并比较多轮结果，再由 decoder 推断最可能的错误位置或错误链。

## 8. `commute` 与 `anticommute` 的操作直觉

现阶段不需要做矩阵乘法。只看 error 是否翻转 check：

- **Commuting**：error 发生后，check 结果不变。
- **Anticommuting**：error 发生后，check 结果翻转。

| 单个 error | `ZZ` check | `XX` check |
| --- | --- | --- |
| X | anticommute：翻转 | commute：不变 |
| Z | commute：不变 | anticommute：翻转 |
| Y | anticommute：翻转 | anticommute：翻转 |

这张表是以后理解 stabilizer syndrome 的直接入口：一个 error 与哪些 checks anticommute，哪些 check 结果就会改变。

## 9. 几个容易混淆的地方

### “X measurement 是随机的”不等于“Qubit 没有状态”

它只说明当前状态没有给出确定的 X measurement 答案。例如 `|0⟩` 的 Z measurement 确定，但 X measurement 随机。

### `|+⟩` 和 `|−⟩` 不是同一个状态

它们的 Z measurement 都是 50/50，但 X measurement 一个固定为 `+1`，另一个固定为 `-1`。

### Bell Pair 不是提前藏着一个确定的 `00` 或 `11`

普通随机 `00/11` 只能复制 Bell Pair 的 Z 关系，不能复制它的 X 关系。

### `ZZ` 联合测量不是先读取 A、B 再让软件相乘

后者会暴露单 Qubit 信息。QEC 需要一种只输出关系、而不输出各自取值的物理操作。

### Syndrome 不是错误位置报告

即使 `ZZ` 从 `+1` 变成 `-1`，也只能知道 A、B 的关系变了。A 或 B 中任意一个发生 X error，都可能造成相同结果。

## 10. 工程师视角

这一阶段已经出现了未来 QEC DSL 必须区分的几类语义：

```text
prepare_z(A, 0)          # 准备单 Qubit
measure_z(A)             # 读取 A 的 Z 信息
measure_product(ZZ, A,B) # 只读取 A、B 的联合关系
```

这不是最终 DSL 设计，只是在说明三个操作不能混为一谈。尤其是：

```text
measure_z(A) + measure_z(B) + classical_compare
```

不能直接替代不会泄露单 Qubit 信息的 `ZZ` 联合测量。以后做 DSL 和 Compiler 时，怎样把这种抽象操作翻译成目标硬件操作，会成为单独的 lowering 问题。

## 阶段结论

可以用下面这段话概括阶段 1：

> Z basis 和 X basis 是两种不同的测量方向。Pauli X 会翻转 Z 信息，Pauli Z 会翻转 X 信息，Pauli Y 会同时影响两类信息。Bell Pair 的单个 Qubit 测量结果是随机的，但 `ZZ` 和 `XX` 联合关系可以是确定的。QEC 利用联合测量只读取 Qubit 之间的关系；与某个 check anticommute 的 error 会翻转它的结果，从而留下 syndrome 线索，但单条线索通常不能唯一定位 error。

## 验收记录

本阶段已经能够独立判断：

- 为什么只做 Z measurement 不能区分 `|+⟩` 与 `|−⟩`。
- Bell Pair 和普通随机 `00/11` 在 X measurement 下有什么区别。
- 为什么单个 X error 会翻转 `ZZ`，单个 Z error 会翻转 `XX`。
- 为什么 Y error 会同时翻转 `ZZ` 与 `XX`。
- 为什么联合 relationship measurement 比分别读取 data Qubits 更适合提取 syndrome。
- 为什么 syndrome 不能直接告诉 decoder 到底是哪一个 Qubit 出错。

## 自测问题

1. `|1⟩` 经过 H 后是什么状态？再做 Z measurement 会得到什么？
2. `ZZ = +1` 告诉了我们什么？又没有告诉我们什么？
3. 为什么普通随机 `00/11` 不能代替 Bell Pair？
4. Bell Pair 原本 `ZZ = +1, XX = +1`。只有 B 发生 Y error 后，两项结果怎样变化？
5. 为什么不能通过分别测量 data Qubits 来代替 QEC 中的联合关系测量？

## 下一阶段

阶段 2 将从经典 repetition code 开始，建立 parity check、stabilizer、syndrome 和 decoder 的完整纠错闭环。之后再解释为什么量子系统需要同时处理 bit flip 与 phase flip，以及为什么 measurement 本身的错误要求我们重复多轮检查。
