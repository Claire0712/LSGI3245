# LSGI3245 小组协作仓库

用于集中管理 LSGI3245 课程小组项目、代码及学习资料，让组员在同一个仓库提交、检查和整合工作。

## 当前目录

| 路径 | 内容 |
| --- | --- |
| `Group_Project/` | 小组项目说明与分工资料；项目成果也统一放在此目录 |
| `Lecture/` | 课程讲义 |
| `pastpaper/` | 历年试题资料 |
| `code.py` | 当前为空的 Python 文件，尚未实现程序 |

项目要求请查看 [Final Project Instruction](Group_Project/LSGI3245%20Final%20Project%20Instruction2026-2027.pdf)，分工请查看 [分工图片](Group_Project/分工.jpg)。具体要求以课程发布的文件为准。

随着项目推进，可以在 `Group_Project/` 下按需建立 `sql/`、`src/`、`docs/` 和 `results/`，分别存放 SQL、程序、报告及结果。提交可运行代码时，请同时说明依赖、输入文件和运行方式。

## 加入协作

仓库地址：https://github.com/Claire0712/LSGI3245

本仓库为公开仓库，任何人都可以查看和克隆。需要直接推送分支的组员，请先将 GitHub 用户名提供给仓库管理员，由管理员在仓库 **Settings → Collaborators** 中添加成员。接受邀请后即可推送自己的分支；未加入协作者的用户也可以 Fork 仓库后提交 Pull Request。

```bash
git clone https://github.com/Claire0712/LSGI3245.git
cd LSGI3245
```

第一次使用 Git 时，先配置提交署名（将示例替换为自己的信息）：

```bash
git config user.name "Your Name"
git config user.email "your-email@example.com"
```

## 每次提交的流程

推荐每人针对一项任务建立分支，通过 Pull Request 合并到 `main`，便于组员检查和避免互相覆盖。开始前请先提交或暂存已有改动。

```bash
# 获取最新主分支
git switch main
git pull --ff-only origin main

# 建立自己的任务分支，例如 feat/alice-database-schema
git switch -c feat/your-name-task

# 修改文件后检查差异，只添加本次任务涉及的文件
git status
git diff
git add Group_Project/
git commit -m "Add database schema draft"
git push -u origin feat/your-name-task
```

推送后，在 GitHub 打开 **Pull requests → New pull request**，选择自己的分支合并到 `main`。说明本次修改了什么、如何检查，以及哪些地方需要其他组员协助。请另一位组员检查后再合并。

上面的分支名和提交说明均为示例；每项新任务使用不同的分支名，`git add` 的路径也应按本次修改调整。

不熟悉命令行的组员也可以用 GitHub Desktop 克隆仓库、创建分支、提交并推送；少量文档可以在 GitHub 网页通过 **Add file → Upload files** 上传到自己的分支，再发起 Pull Request。

## 协作约定

- 开始任务前先确认分工，可使用 Issues 记录任务、负责人和待解决问题。
- 提交信息写清楚实际变化，例如 `Add initial SQL tables` 或 `Update report methodology`。
- 尽量一次提交一项完整修改；避免同时编辑同一份 Word、PDF 或图片，这些文件难以自动合并。
- 遇到冲突时与相关组员确认内容后再解决，不要强制推送覆盖别人的工作。
- 不提交密码、访问令牌、数据库凭据、个人隐私数据或本地虚拟环境。
- 本地临时文件、缓存和 `.DS_Store` 已由 `.gitignore` 排除。
- 课程资料仅供获授权的组员学习与协作使用；对外分享前确认课程规定和资料授权。

## 运行说明

当前仓库主要包含课程资料和项目说明，尚无可运行的项目实现，也没有配置依赖或自动化测试。后续加入代码时，请在此补充安装、数据库初始化、运行和验证步骤。
