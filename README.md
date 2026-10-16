# The QZhao Lab 网站

香港理工大学生命科学系赵倩课题组网站，中英双语。

- 网址：<https://wtbxsjy.github.io/qzhaolab/>（英文）、<https://wtbxsjy.github.io/qzhaolab/zh/>（中文）
- 构建工具：Hugo[^hugo] 0.139.4（extended 版）
- 托管：GitHub Pages[^pages]。推送到 `main` 分支后，GitHub Actions[^actions] 会自动构建并发布，通常 1–2 分钟生效。

[^hugo]: Hugo：静态网站生成器，把 Markdown 文本和数据文件转换成网页。
[^pages]: GitHub Pages：GitHub 提供的免费静态网站托管服务。
[^actions]: GitHub Actions：GitHub 内置的自动化工具，这里用来在每次修改后自动构建和发布网站。

## 日常维护：改哪个文件

大部分更新只需要改 `data/` 下的文件，不用碰模板。

| 想做的事 | 改这个文件 | 说明 |
| --- | --- | --- |
| 发一条新闻 | `data/news.yaml` | 在文件最上方加一条，写 `date`、`en`、`zh`。主页自动显示最新 3 条 |
| 新成员加入、成员毕业 | `data/team.yaml` | 在 `members` 中增删；毕业后移到 `alumni` 并写去向 |
| 加一篇论文 | `data/publications.yaml`，或运行「Update publications」工作流 | 见下文 |
| 改研究方向介绍 | `content/en/research/*.md` 和 `content/zh/research/*.md` | 中英文各一份 |
| 改首页研究概述 | `content/en/_index.md`、`content/zh/_index.md` | |
| 改招聘、联系方式 | `content/*/join.md`、`content/*/contact.md` | |
| 改系名、地址、导航栏 | `hugo.toml` | 中英文分别在 `languages.en`、`languages.zh` 下 |
| 改按钮、标题等界面文字 | `i18n/en.toml`、`i18n/zh.toml` | |

修改方式：可以直接在 GitHub 网页上点开文件、点铅笔图标编辑、提交，网站会自动更新；也可以在本地改完后 `git push`。

### 新闻格式

```yaml
- date: 2026-10-05
  en: Dr. Qiao joins the lab as a Postdoctoral Fellow.
  zh: Qiao 博士以博士后研究员身份加入课题组。
```

文字支持 Markdown[^md]，例如 `*Nature Communications*` 显示为斜体。

[^md]: Markdown：一种用简单符号标记格式的纯文本写法，例如用星号包住的文字显示为斜体。

### 成员格式

```yaml
- { name: "Dr. Yang Yang", role: postdoc }
- { name: "Li Kecheng", name_zh: "李可成", role: phd, photo: "images/team/li-kecheng.jpg" }
```

- `role` 可选：`postdoc`（博士后研究员）、`phd`（博士研究生）、`mphil`（哲学硕士研究生）、`visiting`（访问学者）、`uris`（本科生研究助理）、`fyp`（本科毕业设计学生）。
- `name_zh` 填中文名；不填时中文页面显示英文名。目前所有成员都没有填中文名，请逐个补上。
- `photo` 填 `static/` 下的路径；不填时显示首字母头像。建议照片裁成正方形、宽 400 像素左右。

### 论文

**推荐做法：按 DOI[^doi] 自动添加。** 打开仓库的 Actions 页面 → 左侧选「Update publications」→ 点「Run workflow」，填入：

- `doi`：新论文的 DOI，例如 `10.1021/jasms.1c00076`
- `topics`：属于哪个研究方向，`peptidein`、`immunopeptides`，可留空。填了的论文会出现在对应研究方向页面的「代表性论文」中
- `corresponding`：通讯作者，例如 `Zhao Q`

工作流会从 Crossref[^crossref] 拉取标题、完整作者、期刊、卷期页码，写入 `data/publications.yaml`，并自动重新发布网站。不填 DOI 直接运行，则会给已有条目补全作者列表和被截断的标题。

[^doi]: DOI（Digital Object Identifier，数字对象标识符）：每篇论文的唯一编号，形如 `10.xxxx/xxxxx`。
[^crossref]: Crossref：学术出版物元数据的登记机构，可按 DOI 查询论文的标题、作者等信息。

**手动添加**：在 `data/publications.yaml` 中照下面的格式加一条：

```yaml
- title: An integrated approach for discovering non-canonical MHC-I peptides encoded by small open reading frames
  authors: [Chen L, Zhang Y, Zhao Q]
  journal: Journal of the American Society for Mass Spectrometry
  year: 2021
  volume: 32(9)
  pages: 2346–2357
  doi: 10.1021/jasms.1c00076
  corresponding: [Zhao Q]     # 显示为 *
  equal: [Chen L, Zhang Y]    # 共同贡献，显示为 #
  topics: [peptidein, immunopeptides]
```

`hugo.toml` 中的 `highlightAuthors` 列出需要加粗的作者名，默认为 `Zhao Q`。

**迁移说明**：论文从旧网站迁移时只拿到了第一作者。第一次运行「Update publications」工作流会按 DOI 补全。以下 5 篇在旧网站上没有 DOI，需要手动补全作者和 DOI：*Biological Chemistry* 2021、*Nucleic Acids Research* 2021（小鼠翻译组）、*Cancer Research* 2021、*Science* 2018、*Proceedings of the National Academy of Sciences* 2018。其中 *Cancer Research* 2021 的标题在迁移时被截断，也需要补全。

### 研究方向配图

把图片放进 `static/images/research/`，再在对应研究方向 Markdown 文件的开头填写：

```yaml
image: "images/research/peptidein.jpg"
imageAlt: "图片内容的一句话描述"
```

不填时显示「示意图待补」占位框。

## 首页背景图

`static/images/hero-bg.webp` 和 `hero-bg.jpg` 是用 `scripts/make_hero_bg.py` 程序生成的原创插画（蛋白质团块和肽链串珠）。要换成别的图片，用同名文件替换这两个文件即可，建议宽 2000 像素、文件小于 500 KB。重新生成：

```bash
python scripts/make_hero_bg.py hero-bg.svg 11   # 最后的数字是随机种子，换一个数字得到不同的图
```

生成的是 SVG[^svg]，需要再转换成 JPG 和 WebP[^webp]。

[^svg]: SVG：可缩放矢量图形格式。
[^webp]: WebP：一种体积更小的网页图片格式；不支持 WebP 的浏览器会自动改用 JPG。

## 在本地预览

```bash
# 安装 Hugo extended 0.139.4：https://gohugo.io/installation/
hugo server
# 浏览器打开 http://localhost:1313/
```

## 以后绑定自有域名

1. 购买域名，例如 `zhaoqlab.org`。
2. 仓库 Settings → Pages → Custom domain 填入域名，按提示在域名服务商处添加 DNS[^dns] 记录。
3. 把 `hugo.toml` 第一行的 `baseURL` 改成新域名。

[^dns]: DNS（Domain Name System，域名系统）：把域名指向网站服务器的记录。

## 目录结构

```
hugo.toml            网站配置：标题、系名、地址、导航栏（中英文）
content/en, content/zh   各页面正文
data/                新闻、成员、论文数据
i18n/                界面文字翻译
layouts/             页面模板
static/              样式、字体、图片
scripts/             论文更新脚本、背景图生成脚本
.github/workflows/   自动发布、论文更新工作流
```
