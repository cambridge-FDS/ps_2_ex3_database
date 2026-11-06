# PS2 Exercise 3 — collaboration setup

## 组员先看：本机安装与验证

**每个人在自己的 clone 中执行一次以下步骤，再开始自己的分析。** 第3题使用
Pixi 的 `nba` 环境（Python 3.12）；分工表在本节之后。

### 1. 准备自己的仓库

先安装 Git 和 [Pixi](https://pixi.sh/latest/installation/)，将
[小组仓库](https://github.com/starries-creator/ps_2_ex3_database)的最新 `main`
fork 到自己的账号，再 clone 自己的 fork。已有 fork 的同学先同步小组 `main`。
以下所有命令均在仓库根目录运行，即包含 `pixi.toml` 的目录。

作业另行要求创建 Kaggle 账号并生成 API key，请自行私下完成；不要提交或分享
密钥。当前公开下载可以匿名完成，但这不能代替作业中的账号要求。

### 2. 安装环境、项目包和 pre-commit

按顺序执行：

```bash
pixi install --locked -e nba
pixi run -e nba python -m ensurepip
pixi run -e nba python -m pip install --no-deps --no-build-isolation .
pixi run -e nba pre-commit install
pixi run -e nba pre-commit run --all-files
```

最后一条应全部通过。首次运行 pre-commit 会联网下载检查工具，请等待完成。
每个 clone 都要安装 hooks；其他同学安装过不会自动替你安装。

**已有 `nba` 环境的组员**请先同步小组 `main`，再在仓库根目录重新安装项目包，
把 SQL 查询文件一起更新到已安装的包中。

```bash
pixi run -e nba python -m pip install --no-deps --no-build-isolation .
```

### 3. 获取数据库并验证

数据库不包含在 fork/clone 中。**没有 `data/nba.sqlite` 时**运行：

```bash
pixi run -e nba python -m nba.data_loader
```

也可以接收组员分享的同一份 `nba.sqlite`，放到 `data/` 后跳过下载。已有文件时
下载器会拒绝覆盖。下载时需要同时容纳约 0.73 GB 压缩包和 2.35 GB 数据库，
另留环境安装空间。然后运行：

```bash
pixi run -e nba validate --data data/nba.sqlite
```

检查应通过，并显示 `game` 表行数和数据库 SHA-256。整合分析前，按
[数据入口说明](docs/data_loader_notes.md)核对组员使用的文件相同。
`.csv`、`.sqlite` 和本地 `data/` 已被 Git 忽略，不要强制提交数据库。

### 4. 开始自己的工作

```bash
pixi run -e nba jupyter
```

选择本仓库 `nba` 环境的 Python 内核，打开 `warm_up.ipynb`，先运行前两个代码
单元确认数据入口。后续 TODO 和洞见分析由对应成员完成。编辑项目 Python 文件后，
再次运行第2步的包安装命令，以更新已安装的包。

本机验证平台为 macOS Apple Silicon；其他已列平台仅完成锁文件依赖解析。
完成上述安装即可开始分析；后面的分工表与详细说明供工作时查阅。

---

<!-- PS2_FINAL_TEAM_PLAN_START -->
## PS2 最终分工与前置顺序

本组完成第1、2、3、5题，A-E为成员占位。第1、5题沿用PS1的Conda；第2、3题使用Pixi。每人按表完成自己的分析、工程或报告部分；第2、3、5题在PR阶段统一审核和整合，不预先指定人员。最终验收均不指定人员。

### 仓库与环境

| 题目 | 小组仓库 | 环境安排 |
| --- | --- | --- |
| 第1题 | [first_repo](https://github.com/zcyMary/first_repo) | 沿用PS1的Conda，补充检查工具 |
| 第2题 | [Smoking](https://github.com/starries-creator/ps_2_ex2_smoking_is_bad) | Pixi，环境名 smoke；B先配置并验证，A-E各自安装/确认 |
| 第3题 | [NBA](https://github.com/starries-creator/ps_2_ex3_database) | 老师的Pixi，Python 3.12，nba；C先验证，A-E各自安装/确认 |
| 第5题 | [Titanic](https://github.com/starries-creator/ps1_ex4_nb_to_repo_forked) | 沿用Conda，Python 3.13.16、pandas 2.3；A-E各自激活/确认 |

### 成员分工

| 成员 | 第1题 | 第2题 | 第3题 | 第5题 |
| --- | --- | --- | --- | --- |
| A | 工具配置、全文件检查、跟进工具PR；审查忽略及类型PR | 变量分布图与解释 | 洞见①；数据库结构小题 | 筛选最终图表，撰写≤500词报告正文 |
| B | 忽略规则、CSV验证、跟进忽略PR；审查工具PR | 优先完成Pixi smoke环境、锁文件、nbstripout及环境README | 洞见②；表清单小题 | 年龄/票价分析；完善README内容并保留原项目介绍 |
| C | data_cleaner.py类型标注；协调类型PR | 年龄分组敏感性分析 | 先验证老师的nba环境、准备数据入口；打包、loader说明及安装/导入验证 | 家庭变量分析 |
| D | data_loader.py、visualizer.py类型标注；审查忽略及工具PR | 数据准备、基础统计与总体生存率（基础TODO） | 洞见③；字段小题 | 性别/舱位分析 |
| E | 验证mypy依赖、完成两问说明；审查类型PR | 按年龄分组比较吸烟与生存率，解释混杂关系 | 洞见④；日期范围小题 | 缺失值与特征可用性分析 |

### 工作边界

- NBA四个洞见选择相近复杂度；A/B/D/E各自交付SQL、分析/绘图函数、图和解释。C负责数据入口、打包及安装/导入验证。
- 第5题优先复用已有分析和图；B/C/D/E各交图及简短解释，供A筛选和写作。报告正文≤500词，不含图；B完善README并保留原项目说明及备份。
- 每人负责自己部分的代码、图和解释，并自行修正。第2、3、5题提交PR后统一审核、整合和完整复跑，不预先指定审核或整合人员。
- 环境需各自在本机安装/激活并确认可用：第2题B先配置验证，第3题C先验证教师配置，第5题沿用各自原Conda。开工前划清函数、文件及notebook修改范围；PR合并后删除对应已合并的远程和本地分支，未合并分支保留。

### 前置顺序

箭头表示先后；【并行】内的工作可同时开展。各题最后的“最终验收”不指定人员。以下为组员后续完成作业的流程。

#### 第1题：沿用Conda，三个主要PR，工具PR最后

**【并行：A工具配置｜B忽略规则｜C/D类型标注｜E依赖验证、两问初稿】→【并行：B忽略PR，由A/D审查、B跟进合并｜C/D类型PR，由A/E审查、C跟进合并】→ A同步两项结果并做全文件检查，B/C/D修复所属部分，E补全两问并交A收录 → A提交工具PR，B/D审查，A跟进合并 → 最终验收**

每条PR均需两名非作者批准。C标注data_cleaner.py；D标注data_loader.py和visualizer.py。E结合B的CSV结果与依赖验证完成两问，随A的工具PR提交。A/B/C分别负责工具/忽略/类型PR的合并跟进和已合并来源分支清理；按仓库权限执行。各人在合并后同步并安装hooks。

#### 第2题：B准备环境，各自完成分析

**B配置并验证Pixi smoke环境，A-E各自安装并确认可用 →【各自完成：A变量分布图与解释｜B锁文件、nbstripout及环境README｜C年龄分组敏感性｜D数据准备、基础统计与总体生存率｜E按年龄分组比较吸烟与生存率】 → A-E分别提交各自PR → 审核、整合并完整复跑 → 合并PR并删除已合并的远程和本地分支 → 最终验收**

D先共享准备好的数据，A/C/E再基于同一数据分析；可并行的部分同时开展。C/E先约定基础年龄分组和生存率口径。各成员在自己的clone安装hook；B负责环境配置和使用说明，每个人确认自己的本机环境。

#### 第3题NBA：C验证环境与数据，各自完成小题和洞见

**C先验证老师的Pixi nba配置，A-E各自安装并确认环境 →【各自完成：A洞见①、数据库结构小题｜B洞见②、表清单小题｜C数据入口、打包、loader说明及安装/导入验证｜D洞见③、字段小题｜E洞见④、日期范围小题】 → A-E分别提交各自PR → 审核、整合并完整复跑 → 合并PR并删除已合并的远程和本地分支 → 最终验收**

C先提供可复现的下载/建库步骤和数据库入口；A-E在本机确认数据可读后即可开展各自部分，无须等待整份warm-up或打包完成。C负责warm-up路径/连接，四位洞见作者的其余小题见流程；最终整合前完成安装/导入验证。

#### 第5题：各自确认Conda，分析后完成报告

**A-E各自激活并确认原Conda环境（缺少时安装） →【各自完成：A筛图、撰写≤500词报告｜B年龄/票价分析、完善README｜C家庭变量分析｜D性别/舱位分析｜E缺失值与特征可用性分析】 → A-E分别提交各自PR → 审核、整合并完整复跑 → 合并PR并删除已合并的远程和本地分支 → 最终验收**

优先复用已有图表，可并行的分析同时开展；B/C/D/E交齐图和简短解释后，A定稿选图与报告。B保留原项目介绍及docs/readme-history中的README备份；沿用Python 3.13.16、pandas 2.3，不另设新环境。

### 作业占位

作业占位文件和原notebook中的TODO留给对应成员完成；本次只同步分工和流程，不预填分析、答案或报告。
<!-- PS2_FINAL_TEAM_PLAN_END -->

## Start here

For the complete per-clone command sequence, use the installation guide at the
top of this README. The details below explain the environment and file roles.

The PS2 setup uses Python 3.12 and a committed lock file. Four platforms are
resolved: macOS Apple Silicon, macOS Intel, Linux x86-64, and Windows x86-64.
Runtime validation is performed on macOS Apple Silicon; other platforms are
dependency-resolved, not runtime-tested. Install Pixi from https://pixi.sh/ .

Each member should install Git and Pixi, fork the current group `main`, and clone
their fork. Each clone needs its own environment and installed Git hook. From
the repository root:

```bash
pixi install --locked -e nba
pixi run -e nba python -m ensurepip
pixi run -e nba python -m pip install --no-deps --no-build-isolation .
pixi run -e nba pre-commit install
pixi run -e nba pre-commit run --all-files
```

Use the Python kernel from that environment. Do not use a global Python or a
teammate's absolute environment path. Other CPU architectures require a team
manifest/lock update first. See [CONTRIBUTING.md](CONTRIBUTING.md) for branches,
reviews, notebook editing, and local-file rules.
Reinstall the package with the same pip command after changing its Python files.
The first pre-commit run downloads its own check environments and needs internet
access. The committed hook configuration does not install hooks in another clone.

The assignment also explicitly asks each member to create a Kaggle account and
generate an API key. Complete that step privately even though the public download
below currently works without login. Do not share or commit the key. Environment
verification does not verify completion of that personal coursework step.

## Files and unfinished coursework

- `warm_up.ipynb`: database entry prepared; coursework questions remain for their owners.
- `nba/data_loader.py`: public dataset download and read-only connection helper.
- `.pre-commit-config.yaml`: teaching hooks, with Click in the mypy environment.
- `nba/wrangling.py`, `nba/visualisation.py`: intentionally EMPTY function modules.
- `queries/insight_1.sql` through `insight_4.sql`: intentionally EMPTY query files.
- `analysis.ipynb`: valid empty notebook for the final four-or-more insights.
- `docs/data_loader_notes.md`: data download, connection, and verification instructions.
- `pyproject.toml`: package metadata for installation.
- `figures/` and `data/`: final exports and local downloaded data respectively.

Run commands from the repository root. See [data entry notes](docs/data_loader_notes.md)
for download and verification. Each insight author supplies their query,
appropriate figure, modular functions, and explanation. The integrator assembles
them in `analysis.ipynb`.

The hook configuration is provided upstream. Each member can install it with
`pixi run -e nba pre-commit install`; existing coursework may require fixes before
all hooks pass. Do not confuse environment verification with assignment completion.
Keep each member's Kaggle token local and never commit or paste it into PRs.
Run the checks manually with `pixi run -e nba pre-commit run --all-files`.


## Setup verification

Verified on 2026-11-04 on macOS Apple Silicon with Python 3.12.16 and pandas
2.3.3. The teacher's dependency configuration and committed lock file are retained.

- Locked environment installation and standard package installation pass.
- The installed package imports outside the repository.
- Anonymous download and extraction of the actual Kaggle database pass.
- The read-only connection reads the `game` table (65,698 rows in this copy).
- Both notebooks validate; headless plotting, SQLite/DuckDB checks, and a fresh
  Jupyter kernel with the intended interpreter and a real-data query pass.
- Eight focused data-entry tests and all configured pre-commit hooks pass.
- A clean source copy without local environments or data installs using the
  README commands and passes package imports, tests, plotting and kernel checks
  against the separately held local database.
- A fresh clone from remote `main` also passes the same install commands,
  pre-commit with an independent cache, an actual local commit invoking its hook,
  all eight tests, its own anonymous database download and the data/kernel checks.

Other platforms are dependency-resolved, not runtime-tested. The remaining
warm-up questions, four insights, and final analysis notebook remain for their
assigned authors. See the data notes for the verified database hash.

## Getting the data

Follow [the data entry notes](docs/data_loader_notes.md) to download the public
dataset; local Kaggle credentials are only needed if access requires them.
The notebook expects `data/nba.sqlite` when launched from the repository root.

```bash
pixi run -e nba python -m nba.data_loader
pixi run -e nba validate --data data/nba.sqlite
pixi run -e nba jupyter
```

The database is ignored by Git. Each member downloads a local copy or receives
the same file from a teammate; a fork or clone contains code, not the database.
