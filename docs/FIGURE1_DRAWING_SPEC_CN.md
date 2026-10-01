# 图 1 详细绘图规范

本图用于说明论文的系统边界、两个控制变量和六级结果阶梯。当前正式稿采用
TikZ 原生矢量绘制，源文件为 `figures/fig_system.tex`。设计目标是在 AAMAS
双栏版式的单栏宽度内，同时表达“信息如何流动”和“哪一层真正执行安全
约束”，并保证黑白打印、缩放和无障碍阅读时仍可辨认。

## 1. 信息结构

图由三个垂直层次组成。

1. **控制注释层**：最上方放置 `elevation a` 和 `write-back b` 两个小节点。
   它们分别垂直指向 Receiver model 和 Reference monitor，表示两个控制量
   作用于不同系统边界。
2. **主流程层**：从左向右依次为 Untrusted content、Receiver model、
   Reference monitor、Protected store。Protected store 下方另接 Downstream
   agent read，表示状态变异后的后续暴露。
3. **结果阶梯层**：横跨近一整栏，列出 attempt、unauthorized attempt、
   capability decision、mutation、unauthorized mutation 和 downstream exposure，
   并在第二行给出主估计量与符号含义。

读图顺序应当是左到右、上到下。主流程回答“发生了什么”，顶部控制回答
“谁决定什么”，底部阶梯回答“论文实际测量哪一个结果”。

## 2. 画布与尺度

- 目标版式：AAMAS 双栏中的单栏图。
- 图环境宽度：由正文 `\columnwidth` 决定；底部阶梯固定为
  `0.96\columnwidth`。
- 当前渲染宽度约为 80--82 mm，具体值由模板列宽决定。
- 主流程节点保持在同一水平基线上；节点之间的显式水平净间距为 6 mm。
- 顶部控制节点与目标节点的垂直净间距为 2.5 mm。
- Downstream 节点位于 Protected store 下方 5 mm。
- 结果阶梯的左上角与 Untrusted content 的左下角对齐，并下移 9 mm。
- TikZ 全局 `node distance=4mm and 5mm` 只提供默认值；关键位置均使用
  `right=6mm of`、`above=2.5mm of`、`below=5mm of` 等显式距离，避免模板
  字体变化导致布局漂移。

## 3. 节点几何

所有功能节点共享 `box` 样式：

```latex
box/.style={
  draw,
  rounded corners=1pt,
  align=center,
  inner sep=3pt,
  font=\scriptsize
}
```

具体含义如下。

- `draw`：0.4 pt 左右的默认黑色边框，不使用阴影。
- `rounded corners=1pt`：只做轻微圆角，保留系统框图的工程感。
- `align=center`：节点内部居中对齐。
- `inner sep=3pt`：文字与边框之间四边留白 3 pt。
- `font=\scriptsize`：与单栏图的最终物理尺寸匹配。
- 节点宽度由内容自动决定；长标签通过 `\\` 人工换行，避免固定宽度造成
  不必要的空白。

各节点的换行方式应保持不变：

| 节点 | 第一行 | 第二行 | 视觉作用 |
|---|---|---|---|
| Untrusted content | Untrusted content | (adversary-controlled) | 唯一浅灰填充，标记外部输入 |
| Receiver model | Receiver model | (structured actions) | 生成结构化动作但不执行策略 |
| Reference monitor | Reference monitor | policy × capability | 安全决策中心 |
| Protected store | Protected store | process-local | 被保护状态 |
| Downstream agent read | Downstream agent read | exposure rung | 后续影响 |
| elevation a | elevation a | 无 | 指令资格控制 |
| write-back b | write-back b | 无 | 写权限控制 |

Reference monitor、Protected store 和 Downstream 的第二行使用
`\footnotesize`，使主对象名称比属性说明更突出。

## 4. 配色

### 正式稿方案：印刷优先的灰度配色

- 背景：纯白 `#FFFFFF`。
- 文字、边框和箭头：纯黑 `#000000`。
- Untrusted content 填充：`black!8`，约等于 `#EBEBEB`。
- 其他节点：白色填充。
- 不使用仅靠红/绿区别的编码。

灰度方案的语义原则是：浅灰只标记“攻击者可写的数据来源”，而安全状态不
通过颜色判断。`a`、`b`、attempt 和 allow 均由文字与拓扑编码，因此复印、
投影或灰度打印不会丢失含义。

### 可选彩色演示方案

若用于幻灯片而非匿名论文 PDF，可使用以下色盲安全、低饱和度方案：

| 元素 | 填充色 | 边框色 |
|---|---|---|
| Untrusted content | `#FDE2E2` | `#9C2F2F` |
| Receiver model | `#E8F1FA` | `#356A9A` |
| Reference monitor | `#FFF1CC` | `#8A6A16` |
| Protected store | `#E2F3E8` | `#357A4F` |
| Downstream exposure | `#EEE8F7` | `#66518A` |
| 控制节点 a、b | `#F2F2F2` | `#4A4A4A` |

彩色版仍须保留黑色标签和不同节点位置；颜色只能作为冗余提示。打印论文中
建议继续使用当前灰度方案，以免颜色暗示实验中不存在的风险等级。

## 5. 箭头与边标签

箭头样式为：

```latex
arr/.style={thick, ->},
>={Stealth[length=2mm]}
```

- 线宽采用 TikZ `thick`，最终约 0.8 pt。
- 箭头头部使用长度 2 mm 的 Stealth，不使用开放箭头或双向箭头。
- 主流程箭头全部水平，控制箭头全部垂直。
- 边标签放在水平箭头正上方，字号 `\scriptsize`。
- `data plane` 标注 Untrusted content 到 Receiver model。
- `attempt` 标注 Receiver model 到 Reference monitor。
- `allow` 标注 Reference monitor 到 Protected store。
- Protected store 到 Downstream 不再加文字，避免与 exposure rung 节点重复。

箭头只表示事件或控制作用，不表示信任关系。特别是 Receiver 到 monitor 的
箭头是“提出尝试”，monitor 到 store 才是“允许状态改变”。

## 6. 底部结果阶梯

结果阶梯使用与功能节点相同的边框样式，但设置
`text width=.96\columnwidth`，形成横跨整栏的说明框。左边与第一个节点
对齐，避免视觉中心偏向右侧。

第一行使用六个带圈数字：

```text
1 attempt → 2 unauthorized attempt → 3 capability decision
→ 4 mutation → 5 unauthorized mutation → 6 downstream exposure
```

第二行说明：

```text
Primary estimand: R = Pr(rung 5);
r1,r0 = attempt rates at a=1,0; only b enforces mutation.
```

阶梯使用箭头符号表示结果递进，而不是因果充分性。一个事件可以在较早层级
停止，例如模型产生 unauthorized attempt，但 capability decision 拒绝后不会
进入 mutation。

## 7. 对齐和视觉层级

- 主流程五个功能节点构成第一视觉层级。
- Reference monitor 的标签最重要，但不通过更深颜色突出，以避免把 monitor
  错读成模型组件；它的位置和 `policy × capability` 已提供足够强调。
- 顶部 a/b 节点面积最小，是第二视觉层级。
- 底部结果框面积最大但字号相同，通过较长阅读路径形成第三层级。
- 所有文字均水平放置，不旋转标签。
- 元素不交叉，主流程箭头不穿过任何节点。
- Downstream 节点位于右下方，使“暴露是变异之后的下一步”在空间上清楚。

## 8. TikZ 构建顺序

推荐按以下顺序编写，保证定位引用存在且图层稳定：

1. 定义全局 node distance、box、arrow 和 arrow-tip 样式。
2. 放置 Untrusted content 作为坐标原点。
3. 用相对定位从左到右放置 Receiver、Monitor 和 Store。
4. 在 Store 下方放置 Downstream。
5. 在 Receiver 和 Monitor 上方放置 a、b。
6. 先绘制 a/b 垂直控制箭头。
7. 再绘制四条主数据流箭头及其标签。
8. 最后放置底部阶梯，避免其尺寸影响上方相对定位。

## 9. 字体与数学符号

- 字体继承 AAMAS 模板，不在 TikZ 内指定字体族。
- 功能节点使用 `\scriptsize`，属性行可降为 `\footnotesize`。
- 数学变量 `a`、`b`、`R`、`r_1`、`r_0` 使用数学斜体。
- 普通动作名使用罗马体文本，不把 `attempt`、`allow` 写成数学变量。
- 乘号使用 `\times`，不使用字母 x。
- 概率符号使用论文统一宏 `\Prob`，保证正文和图一致。

## 10. 导出与质量检查

- 优先直接随 LaTeX 编译为 PDF 矢量图，不导出 PNG 后再嵌入。
- 在 100% 和 200% 缩放下检查边标签是否碰触箭头。
- 将整页缩至实际打印尺寸，确认第二行属性仍可读。
- 转成灰度检查 Untrusted content 的 8% 填充仍可区分。
- 使用 `pdftotext` 确认节点文本存在于 PDF 文本层。
- 检查图宽不超过 `\columnwidth`，LaTeX 日志无 `Overfull \\hbox`。
- 图注应解释视觉结论，而不是逐字重复节点。
- `\Description` 应独立描述流程、控制点和结果阶梯，便于无障碍阅读。

## 11. 当前源代码的位置

- TikZ 图源：`figures/fig_system.tex`
- 图环境和图注：`sections/02_threat.tex`
- 全局 TikZ/PGFPlots 宏包：`main.tex`

如需重画到 Figma、Illustrator 或 PowerPoint，应严格复用以上层级、节点顺序、
标签和箭头语义；最重要的不是外观，而是保持 `a` 只作用于 Receiver、`b`
只作用于 Reference monitor，以及 attempt 与 mutation 之间存在明确的执行边界。

