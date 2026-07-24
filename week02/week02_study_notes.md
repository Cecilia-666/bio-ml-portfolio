# 第二周学习笔记
> 覆盖范围：条件判断 · 正则表达式 · 模块化编程 · Biopython · NumPy · pandas进阶 · seaborn可视化 · Volcano Plot · Git分支

---

## 一、条件判断进阶

### 1.1 逻辑运算符

```python
# and：两个条件都要满足
if gc > 60 and length > 200:
    print("高GC且长序列")

# or：满足其中一个就行
if gc > 60 or length > 500:
    print("高GC或长序列")

# not：取反
if not gc < 40:
    print("GC含量不低")
```

| 运算符 | 含义 | 记忆点 |
|--------|------|--------|
| `and` | 两个都满足 | 英文"且" |
| `or` | 满足一个即可 | 英文"或" |
| `not` | 取反 | 英文"非" |

### 1.2 多分支判断 if / elif / else

```python
if seq["gc"] > 60 and seq["length"] > 200:
    category = "高GC长序列"
elif seq["gc"] > 60 and seq["length"] <= 200:
    category = "高GC短序列"
elif seq["gc"] <= 60 and seq["length"] > 200:
    category = "低GC长序列"
else:
    category = "低GC短序列"
```

- **执行逻辑**：从上到下依次判断，满足哪个就执行哪个，后面的跳过
- **记忆点**：`elif` = "不然如果..."，是 if 和 else 的中间档

### 1.3 f-string 格式化字符串

```python
name = "seq1"
gc = 72
print(f"{name}: GC={gc}%")   # 输出：seq1: GC=72%
```

- **是什么**：字符串前加 `f`，用 `{}` 嵌入变量，Python自动把值插进去
- **记忆点**：f-string = "字符串里直接插变量"

---

## 二、正则表达式

### 2.1 什么是正则表达式

一种**描述文字模式**的迷你语言，用简短符号表达"我想找什么样的文字"。

生物学应用：找起始密码子ATG、找TATA box、找Kozak序列、匹配特定氨基酸模式。

### 2.2 核心符号速查表

| 符号 | 含义 | 生物学例子 |
|------|------|-----------|
| `[ABC]` | 匹配A或B或C任意一个 | `[ATGC]` = 任意碱基 |
| `.` | 匹配任意一个字符 | `A.G` = A开头G结尾中间任意 |
| `+` | 前面字符1次或多次 | `A+` = 一个或多个A |
| `*` | 前面字符0次或多次 | `A*` = 零个或多个A |
| `\d` | 任意数字(0-9) | `\d+` = 一串数字 |
| `\d+$` | 字符串末尾的数字 | 用于提取样本编号 |
| `^` | 字符串开头 | `^ATG` = 以ATG开头 |
| `$` | 字符串结尾 | `TAA$` = 以TAA结尾 |

### 2.3 三个核心函数

```python
import re

dna = "ATGCGATCGATGCGATCGATG"

# re.findall()：找出所有匹配，返回列表
matches = re.findall("ATG", dna)
print(len(matches))          # 3

# re.search()：找第一个匹配，返回位置信息
match = re.search("ATG", dna)
if match:                    # 先判断是否找到
    print(match.start())     # 0（第一个ATG的起始位置）

# re.finditer()：找所有匹配，同时返回位置
for m in re.finditer("ATG", dna):
    print(f"ATG在位置 {m.start()}–{m.end()}")
```

| 函数 | 返回值 | 用途 |
|------|--------|------|
| `findall` | 字符串列表 | 只要内容，不要位置 |
| `search` | match对象（第一个） | 找第一个，要位置 |
| `finditer` | match对象迭代器 | 找所有，要位置 |

---

## 三、模块化编程

### 3.1 为什么要分函数

```
实验流程：读取数据 → 清洗 → 分析 → 出图
每一步写成一个函数，主程序只负责"指挥"
优点：清晰易维护，出错容易定位，可以单独测试每一步
```

### 3.2 函数的标准写法

```python
def calculate_gc(sequence):
    """计算单条序列的GC含量百分比"""   # 文档字符串，说明函数用途
    sequence = sequence.upper()
    if len(sequence) == 0:
        return 0
    gc = (sequence.count("G") + sequence.count("C")) / len(sequence) * 100
    return round(gc, 2)    # round()保留2位小数
```

### 3.3 enumerate() — 同时获取序号和值

```python
sequences = ["ATGC", "GCTA", "TTTT"]
for i, seq in enumerate(sequences):
    print(f"第{i+1}条：{seq}")
# i从0开始，所以显示时+1
```

- **记忆点**：enumerate = "编号+内容一起给"

### 3.4 列表推导式（第8章）

```python
sequences = ["ATGCGC", "ATATAT", "GCGCGC"]

# 传统写法（3行）
gc_list = []
for seq in sequences:
    gc_list.append((seq.count("G") + seq.count("C")) / len(seq) * 100)

# 列表推导式（1行，结果一样）
gc_list = [(seq.count("G") + seq.count("C")) / len(seq) * 100
           for seq in sequences]

# 带条件过滤：只保留GC > 50%的序列
high_gc = [seq for seq in sequences
           if (seq.count("G") + seq.count("C")) / len(seq) > 0.5]
```

- **格式**：`[表达式 for 变量 in 列表 if 条件]`
- **记忆点**：把for循环"压缩"成一行，更Pythonic

### 3.5 异常处理（第9章）

```python
def safe_gc(sequence):
    try:
        # try里放可能出错的代码
        gc = (sequence.count("G") + sequence.count("C")) / len(sequence) * 100
        return gc
    except ZeroDivisionError:
        # 序列长度为0时触发
        print("警告：序列长度为0")
        return 0
    except AttributeError:
        # 传入None等非字符串时触发
        print("警告：输入不是有效序列")
        return None
```

- **记忆点**：try/except = "先试试，出错了别崩溃，优雅处理"

---

## 四、Biopython

### 4.1 安装

```bash
pip install biopython -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4.2 Seq 对象——比字符串更聪明的序列

```python
from Bio.Seq import Seq

dna = Seq("ATGCGATCGATCGATCG")

print(dna.complement())          # 互补链
print(dna.reverse_complement())  # 反向互补链（即Rosalind REVC题）
print(dna.transcribe())          # 转录：DNA → RNA
print(dna.translate())           # 翻译：RNA → 蛋白质
```

### 4.3 读取FASTA文件

```python
from Bio import SeqIO

for record in SeqIO.parse("test.fasta", "fasta"):
    print(record.id)          # 序列ID
    print(record.seq)         # 序列内容（Seq对象）
    print(record.description) # 完整描述行
    print(len(record.seq))    # 序列长度
```

- **记忆点**：SeqIO.parse = "解析序列文件"，像pandas的read_csv，但专门处理FASTA/GenBank格式

---

## 五、NumPy

### 5.1 NumPy vs Python列表

| | Python列表 | NumPy数组 |
|---|---|---|
| 数学运算 | 需要for循环 | 直接对整个数组操作 |
| 速度 | 慢 | 快几十倍 |
| 用途 | 通用数据 | 数值计算 |

### 5.2 创建数组和基本统计

```python
import numpy as np

expression = np.array([12.5, 8.3, 45.2, 3.1, 22.8])

print(np.mean(expression))    # 均值
print(np.std(expression))     # 标准差
print(np.median(expression))  # 中位数
print(np.max(expression))     # 最大值
print(np.min(expression))     # 最小值
```

### 5.3 向量化运算（NumPy最强特性）

```python
# 不需要for循环，直接对整个数组操作
log2_expr = np.log2(expression + 1)    # log2转换（+1避免log(0)）
z_scores = (expression - np.mean(expression)) / np.std(expression)  # Z-score标准化
```

- **记忆点**：向量化 = "一行代码对所有数据同时操作"，不需要for循环

### 5.4 二维数组（基因表达矩阵）

```python
# 行=基因，列=样本——这就是转录组数据的基本结构
matrix = np.array([
    [12.5, 13.1, 11.8],   # 基因1，3个重复
    [45.2, 43.8, 46.1],   # 基因2
    [8.3,  9.1,  7.9],    # 基因3
])

print(matrix.shape)                    # (3, 3) = (基因数, 样本数)
print(np.mean(matrix, axis=1))        # 每个基因的均值（沿列方向）
print(np.mean(matrix, axis=0))        # 每个样本的均值（沿行方向）
```

- **axis=0**：沿行方向（对每一列计算），结果是每个样本的统计
- **axis=1**：沿列方向（对每一行计算），结果是每个基因的统计
- **记忆点**：axis=0 压缩行→得到列的统计；axis=1 压缩列→得到行的统计

### 5.5 常用函数速查

```python
np.random.seed(42)              # 设置随机种子（保证结果可复现）
np.random.normal(0, 1, 100)     # 正态分布随机数（均值, 标准差, 数量）
np.random.uniform(0, 1, 100)    # 均匀分布随机数
np.concatenate([arr1, arr2])    # 拼接两个数组
arr.clip(lower=1e-300)          # 把小于1e-300的值替换成1e-300
arr.round(2)                    # 保留2位小数
```

---

## 六、pandas 进阶

### 6.1 多条件筛选

```python
# & 表示且，| 表示或，条件要用括号括起来
sig_genes = df[
    (df["padj"] < 0.05) &
    (df["log2FoldChange"].abs() > 1)   # .abs()取绝对值
]

# 上调/下调基因
up_genes = sig_genes[sig_genes["log2FoldChange"] > 1]
down_genes = sig_genes[sig_genes["log2FoldChange"] < -1]
```

### 6.2 merge — 合并两个表格

```python
# 类似Excel的VLOOKUP，以gene_id列为索引匹配
merged = de_results.merge(gene_annotation, on="gene_id")
```

- **记忆点**：merge = "两张表按共同列对齐合并"

### 6.3 groupby + agg — 分组统计

```python
pathway_stats = merged.groupby("pathway").agg(
    total_genes=("gene_id", "count"),               # 计数
    mean_log2fc=("log2FoldChange", "mean"),          # 均值
    sig_genes=("padj", lambda x: (x < 0.05).sum())  # 自定义：显著基因数
).reset_index()
```

- **lambda**：匿名函数，`lambda x: x*2` = "输入x，返回x*2"，用于agg里的自定义计算
- **reset_index()**：把groupby产生的索引变回普通列

### 6.4 apply — 对每行应用函数

```python
def classify_gene(row):
    """对每一行数据进行分类"""
    if row["padj"] < 0.05 and row["log2FoldChange"] > 1:
        return "Up"
    elif row["padj"] < 0.05 and row["log2FoldChange"] < -1:
        return "Down"
    else:
        return "NS"

df["category"] = df.apply(classify_gene, axis=1)
# axis=1：对每一行应用函数
```

- **记忆点**：apply = "对每一行/列应用一个函数"，axis=1表示逐行操作

---

## 七、Seaborn 可视化

### 7.1 四种核心图

| 图类型 | 函数 | 用途 |
|--------|------|------|
| 箱线图 | `sns.boxplot()` | 比较各组分布，展示中位数和四分位数 |
| 小提琴图 | `sns.violinplot()` | 比箱线图更直观地展示分布形状 |
| 散点+回归 | `sns.regplot()` | 看两个变量的相关性 |
| 热图 | `sns.heatmap()` | 展示矩阵数据，看样本间模式 |

### 7.2 常用参数速查

```python
sns.boxplot(
    data=long_df,
    x="condition",           # x轴：分组变量
    y="log2_expression",     # y轴：数值变量
    order=["R","CO","CT","CR"],  # 指定分组顺序
    hue="condition",         # 按哪列上色
    palette={"R": "#1F3A6E"},    # 自定义颜色字典
    legend=False,            # 不显示图例
    linecolor="black",       # 边框颜色
    flierprops={"marker": "o",   # 离群点形状
                "markersize": 2,
                "markerfacecolor": "none"},  # 空心圆
    ax=ax                    # 指定画在哪个子图上
)
```

### 7.3 自定义渐变色板

```python
from matplotlib.colors import LinearSegmentedColormap

nature_cmap = LinearSegmentedColormap.from_list(
    'nature_corr',
    ['#A8C8E8', '#FFFFFF', '#8B1A1A']  # 浅蓝→白→深红
)
# 注意：传给cmap时不加引号（cmap=nature_cmap，不是cmap="nature_cmap"）
```

---

## 八、Volcano Plot（火山图）

### 8.1 坐标轴逻辑

```
X轴：log2FoldChange（处理组vs对照组的倍数变化）
     正值 = 上调，负值 = 下调
Y轴：-log10(padj)（显著性）
     值越大 = 越显著（padj越小）
```

### 8.2 完整绘图流程

```python
# 第一步：计算Y轴
df["neg_log10_padj"] = -np.log10(df["padj"].clip(lower=1e-300))

# 第二步：基因分类
def classify_gene(row):
    sig = row["padj"] < 0.05
    if sig and row["log2FoldChange"] > 1:   return "Up"
    elif sig and row["log2FoldChange"] < -1: return "Down"
    elif sig:                                return "Sig"
    else:                                    return "NS"

df["category"] = df.apply(classify_gene, axis=1)

# 第三步：画散点（先画不显著的，再画显著的，避免遮挡）
colors = {"Up": "#8B1A1A", "Down": "#1F3A6E",
          "Sig": "#A8C8E8", "NS": "#CCCCCC"}

for category in ["NS", "Sig", "Down", "Up"]:
    mask = df["category"] == category
    ax.scatter(df.loc[mask, "log2FoldChange"],
               df.loc[mask, "neg_log10_padj"],
               c=colors[category], s=8, alpha=0.6)

# 第四步：添加阈值线
ax.axhline(y=-np.log10(0.05), color="black",
           linestyle="--", linewidth=0.8)
ax.axvline(x=1,  color="black", linestyle="--", linewidth=0.8)
ax.axvline(x=-1, color="black", linestyle="--", linewidth=0.8)

# 第五步：标注最显著的基因
top_up = df[df["category"] == "Up"].nlargest(5, "neg_log10_padj")
for _, row in top_up.iterrows():
    ax.annotate(row["gene"],
                xy=(row["log2FoldChange"], row["neg_log10_padj"]),
                fontsize=7)
```

### 8.3 关键函数解释

| 函数 | 作用 |
|------|------|
| `ax.axhline(y=...)` | 画水平参考线 |
| `ax.axvline(x=...)` | 画垂直参考线 |
| `df.nlargest(5, "列名")` | 取某列最大的前5行 |
| `df.iterrows()` | 逐行遍历DataFrame，返回(index, row)对 |
| `ax.annotate()` | 在图上标注文字 |
| `mpatches.Patch()` | 手动创建图例色块 |

---

## 九、Git 分支

### 9.1 分支是什么

分支 = 平行宇宙：在新分支上做实验性修改，主分支(main)的代码不受影响，确认没问题再合并回来。

### 9.2 分支常用命令

```bash
git branch                        # 查看所有分支（*号标记当前分支）
git checkout -b week02-experiments # 创建并切换到新分支
git checkout main                  # 切回主分支
git merge week02-experiments       # 把新分支合并回主分支
git push origin main               # 推送到GitHub
```

### 9.3 日常推送三步走（复习）

```bash
git add 文件名        # 选择要提交的文件（. 表示全部）
git commit -m "说明"  # 记录这个版本，写清楚做了什么
git push origin main  # 上传到GitHub
```

---

## 十、Rosalind 新题

### FIB — 斐波那契兔子（递归）

```python
def rabbit_count(n, k):
    if n <= 2:
        return 1
    return rabbit_count(n-1, k) + k * rabbit_count(n-2, k)
# 递归：函数调用自身，每次问题规模缩小，直到触底（n<=2）
```

### GC — 最高GC含量序列

```python
# max(字典, key=字典.get)：找字典里值最大的那个键
best_id = max(gc_contents, key=gc_contents.get)
```

### HAMM — 汉明距离

```python
def hamming_distance(s1, s2):
    # zip()把两个序列配对，c1!=c2返回True(=1)/False(=0)，sum求和
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))
```

---

## 十一、本周配色和风格规范（Nature风格）

```python
# 四组颜色
nature_colors = {
    'R':  '#A8C8E8',   # 浅蓝（常温对照）
    'CO': '#F5A8A0',   # 浅珊瑚红（10天低温）
    'CT': '#1F3A6E',   # 深海军蓝（20天低温）
    'CR': '#8B1A1A',   # 深暗红（30天低温）
}

# 每张图必做的四件事
ax.spines['top'].set_visible(False)      # 去掉上边框
ax.spines['right'].set_visible(False)    # 去掉右边框
ax.spines['bottom'].set_color('black')   # 下边框黑色
ax.spines['left'].set_color('black')     # 左边框黑色

# 保存时透明背景
plt.savefig("figure.png", dpi=300, transparent=True)
```

---

## 十二、常见报错速查

| 报错类型 | 常见原因 | 解决方法 |
|---------|---------|---------|
| `ModuleNotFoundError` | 包没装或装错了环境 | 确认(.venv)激活，重新pip install |
| `NameError` | 变量不存在（cell没按顺序运行） | Restart Kernel and Run All Cells |
| `KeyError` | 字典/DataFrame里找不到这个键/列名 | 检查拼写，或变量名加了多余引号 |
| `SyntaxError` | 代码写法有问题（括号/引号/特殊字符） | 检查括号是否闭合，有无多余字符 |
| `ValueError` | 传入了错误类型的值 | 检查参数，如fmt=".2f"不要写成fmt="af" |
| `ZeroDivisionError` | 除以零 | 加判断：if len(sequence) == 0: return 0 |
| `FutureWarning` | 写法将被废弃（不是错误） | 按提示更新写法，暂时不影响运行 |
