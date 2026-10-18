# The QZhao Lab 网站

香港理工大学生命科学系赵倩课题组网站，中英双语。

- 网址：<https://wtbxsjy.github.io/qzhaolab/>（英文）、<https://wtbxsjy.github.io/qzhaolab/zh/>（中文）
- 构建工具：Hugo[^hugo] 0.139.4（extended 版）
- 托管：GitHub Pages[^pages]。推送到 `main` 分支后，GitHub Actions[^actions] 会先检查数据文件，再自动构建并发布，通常 1–2 分钟生效。

[^hugo]: Hugo：静态网站生成器，把数据文件和模板组合生成网页。
[^pages]: GitHub Pages：GitHub 提供的免费静态网站托管服务。
[^actions]: GitHub Actions：GitHub 内置的自动化工具，这里用来在每次修改后自动检查、构建和发布网站。

## 内容与模板分离

网站上的所有内容都保存在 `data/` 下的 JSON[^json] 文件中，模板（`layouts/`）只负责排版，不写任何具体内容。日常更新只需改 JSON 文件。

[^json]: JSON（JavaScript Object Notation）：一种用花括号、方括号和引号组织数据的纯文本格式。

| 文件 | 内容 |
| --- | --- |
| `data/site.json` | 课题组名称、标语、首页研究概述、系/学院/大学名称、首页背景图、联系方式、论文中需要加粗的作者名 |
| `data/research.json` | 研究方向：标题、简介、配图、正文各小节、术语说明。每个方向自动生成一个页面 |
| `data/team.json` | 课题组负责人、在组成员、已毕业成员 |
| `data/publications.json` | 论文列表 |
| `data/news.json` | 新闻动态 |
| `data/join.json` | 招聘信息：申请方式、岗位、要求、经费来源 |

其余文件一般不需要改：

| 文件 | 用途 |
| --- | --- |
| `hugo.toml` | 网站结构：语言设置、导航栏菜单名称 |
| `i18n/en.toml`、`i18n/zh.toml` | 界面上的固定文字，如「研究亮点」「全部论文」 |
| `content/` | 每个页面的占位文件，只写页面标题，正文都来自 `data/` |
| `layouts/`、`static/css/` | 模板和样式 |

### 中英文写法

需要双语的字段都写成：

```json
{ "en": "English text", "zh": "中文内容" }
```

`zh` 留空时，中文页面显示英文。大部分文字字段支持 Markdown[^md]，例如 `**粗体**`、`*斜体*`、`[链接文字](https://...)`。

[^md]: Markdown：一种用简单符号标记格式的纯文本写法。

### 编辑 JSON 时的注意事项

- 每一项之间用英文逗号分隔，最后一项后面**不能**有逗号。
- 文字里的英文双引号要写成 `\"`。
- 改完提交后，如果格式有误，发布流程会在「Check data files」一步失败，并指出是哪个文件第几行出错。在 GitHub 仓库的 Actions 页面可以看到。也可以在本地运行 `python3 scripts/check_data.py` 检查。

修改方式：可以直接在 GitHub 网页上打开文件，点铅笔图标编辑并提交，网站会自动更新；也可以在本地修改后 `git push`。

## 常见更新

### 发一条新闻

在 `data/news.json` 的方括号内任意位置加一条，网站会按日期自动排序。首页显示条数由 `site.json` 中的 `homeNewsCount` 决定，默认 3 条。

```json
{
  "date": "2026-10-05",
  "en": "Dr. Qiao joins the lab as a Postdoctoral Fellow.",
  "zh": "Qiao 博士以博士后研究员身份加入课题组。"
},
```

#### 给新闻配图

1. 把图片放进 `assets/images/news/` 文件夹。在 GitHub 网页上：打开这个文件夹，点「Add file → Upload files」。原图直接上传即可，包括手机照片。网站会自动生成缩略图和适合网页显示的大图，访客下载的是压缩后的版本。
2. 在对应新闻里加上 `images`：

```json
{
  "date": "2026-09-27",
  "en": "PhD candidate Ms YANG Chenxi wins the HUPO Travel Award! Congratulations!",
  "zh": "博士研究生杨晨曦荣获 HUPO 旅行奖！祝贺！",
  "images": [
    "images/news/2026-09-27-hupo-award.jpg",
    {
      "src": "images/news/2026-09-27-poster.jpg",
      "caption": { "en": "Chenxi presenting her poster", "zh": "杨晨曦介绍壁报" }
    }
  ]
}
```

- 每张图可以只写路径，也可以写成带 `src`、`caption`（图注）、`alt`（图片描述，供读屏软件[^alt]使用）的形式。不写 `alt` 时，会依次用图注或新闻正文代替。
- 新闻页显示全部配图，点击放大，可用方向键或两侧按钮切换同一条新闻的图片；首页只显示每条新闻的第一张小图。
- 文件名建议以日期开头，只用小写英文字母、数字和连字符。图片路径写错时，发布前的数据检查会报错。
- 图片也可以放在 `static/` 下，但那样不会自动压缩，原图多大访客就下载多大，所以新闻图片请放在 `assets/images/news/`。

[^alt]: 读屏软件：视障用户用来朗读网页内容的辅助工具；图片描述也会在图片加载失败时显示。

### 成员加入或毕业

在 `data/team.json` 的 `members` 中增删。毕业后，把该成员移到 `alumni`，并加上去向：

```json
{ "name": "Li Kecheng", "name_zh": "李克成", "role": "phd", "photo": "images/team/li-kecheng.jpg" }
```

```json
{ "name": "Dr. Yang Ying", "role": "phd", "now": { "en": "Assistant Professor, Chongqing Medical University", "zh": "重庆医科大学 助理教授" } }
```

- `role` 可选：`postdoc`（博士后研究员）、`phd`（博士研究生）、`mphil`（哲学硕士研究生）、`visiting`（访问学者）、`uris`（本科生研究助理）、`fyp`（本科毕业设计学生）。
- 英文名统一写成「姓在前、名在后」，例如 `Dr. Yang Ying`、`Zhan Hongyu`；英文名字（如 Chloe Tse）按本人习惯写。
- `name_zh` 填中文名；不填时中文页面显示英文名。
- 成员顺序就是网页上的显示顺序。

#### 成员照片

1. 把照片放进 `assets/images/team/` 文件夹。在 GitHub 网页上：打开这个文件夹，点「Add file → Upload files」。原图直接上传即可。
2. 在该成员的条目里加上 `"photo": "images/team/文件名.jpg"`。负责人（`pi`）和已毕业成员也可以加。

- 网站会自动裁剪：在组成员裁成正方形、负责人裁成竖版、已毕业成员显示为小头像，并自动对准画面主体。访客下载的是压缩后的版本。
- 照片里人物最好居中、头肩入画、背景简洁；全组风格统一会更好看。
- 文件名建议用姓名拼音，只用小写英文字母、数字和连字符，例如 `zhang-yuanliang.jpg`。
- 不填 `photo` 时显示姓氏首字母头像。路径写错时，发布前的数据检查会报错。

### 添加论文

**推荐做法：按 DOI[^doi] 自动添加。** 打开仓库的 Actions 页面，左侧选「Update publications」，点「Run workflow」，填入：

- `doi`：新论文的 DOI，例如 `10.1021/jasms.1c00076`
- `topics`：所属研究方向的 `id`，即 `research.json` 中的 `peptidein`、`immunopeptides`，多个用逗号分隔，可以留空。填了的论文会出现在对应研究方向页面的「代表性论文」中
- `corresponding`：通讯作者，例如 `Zhao Q`

工作流会从 Crossref[^crossref] 获取标题、完整作者、期刊和卷期页码，写入 `data/publications.json`，然后自动重新发布。不填 DOI 直接运行，则会给已有条目补全作者列表和被截断的标题。

[^doi]: DOI（Digital Object Identifier，数字对象标识符）：每篇论文的唯一编号，形如 `10.xxxx/xxxxx`。
[^crossref]: Crossref：学术出版物元数据的登记机构，可按 DOI 查询论文的标题、作者等信息。

**手动添加**的格式：

```json
{
  "title": "An integrated approach for discovering non-canonical MHC-I peptides encoded by small open reading frames",
  "authors": ["Chen L", "Zhang Y", "Zhao Q"],
  "journal": "Journal of the American Society for Mass Spectrometry",
  "year": 2021,
  "volume": "32(9)",
  "pages": "2346–2357",
  "doi": "10.1021/jasms.1c00076",
  "corresponding": ["Zhao Q"],
  "equal": ["Chen L", "Zhang Y"],
  "topics": ["peptidein", "immunopeptides"]
}
```

`corresponding` 中的作者后面显示 `*`，`equal`（共同贡献）中的显示 `#`。如果作者列表里有同名作者（例如两位 `Yang Y`），或者 Crossref 给出的缩写和你写的不一致（例如 `Wang H` 与 `Wang HW`），按名字标注会标错或标不上。这时改用作者序号（从 1 开始数）：`"equalPositions": [1, 2]`、`"correspondingPositions": [9]`。数据检查会自动发现这类问题并提示。`site.json` 中的 `highlightAuthors` 列出需要加粗的作者名。没有 DOI 时可以用 `"url"` 给出论文链接。

**迁移说明**：论文从旧网站迁移时只拿到了第一作者。第一次运行「Update publications」工作流会按 DOI 补全。以下 5 篇在旧网站上没有 DOI，需要手动补全作者和 DOI：*Biological Chemistry* 2021、*Nucleic Acids Research* 2021（小鼠翻译组）、*Cancer Research* 2021、*Science* 2018、*Proceedings of the National Academy of Sciences* 2018。其中 *Cancer Research* 2021 的标题在迁移时被截断，也需要补全。

### 修改或新增研究方向

在 `data/research.json` 的 `directions` 中编辑。新增一个方向就是复制一段已有方向、改掉 `id` 和内容，网站会自动生成新页面并在首页加一张卡片。

- `id`：页面地址，只能用小写英文字母、数字和连字符，例如 `chemical-proteomics` 对应 `/research/chemical-proteomics/`。
- `image`：配图路径，图片放进 `static/images/research/`。目前两张配图是从首页背景插画裁出的临时图，建议换成课题组的科研示意图，比例约 3:2。
- `sections`：正文小节，每节一个标题加若干条目。
- `notes`：术语说明，显示在页面底部。只在对应语言有文字时显示，所以可以只给中文版写解释。

## 首页背景图

由 `site.json` 中的 `heroImage` 指定，目前是 `images/hero-bg.jpg`，一张用 `scripts/make_hero_bg.py` 生成的原创插画（蛋白质团块和肽链串珠）。要换图，把新图片放进 `static/images/`，再改 `heroImage` 即可，建议宽 2000 像素、小于 500 KB。重新生成插画：

```bash
python scripts/make_hero_bg.py hero-bg.svg 11   # 最后的数字是随机种子，换一个数字得到不同的图
```

生成的是 SVG[^svg] 矢量图，需要再转换成 JPG。

[^svg]: SVG（Scalable Vector Graphics，可缩放矢量图形）：一种矢量图片格式。

## 在本地预览

```bash
# 安装 Hugo extended 0.139.4：https://gohugo.io/installation/
python3 scripts/check_data.py
hugo server
# 浏览器打开 http://localhost:1313/
```

## 以后绑定自有域名

1. 购买域名，例如 `zhaoqlab.org`。
2. 在仓库的 Settings → Pages → Custom domain 中填入域名，按提示在域名服务商处添加 DNS[^dns] 记录。
3. 把 `hugo.toml` 第一行的 `baseURL` 改成新域名。

[^dns]: DNS（Domain Name System，域名系统）：把域名指向网站服务器的记录。

## 目录结构

```
data/                网站全部内容（JSON）
content/en, content/zh   页面占位文件（只有标题）；research/_content.gotmpl 按 research.json 生成研究方向页面
hugo.toml            语言与导航栏
i18n/                界面固定文字
layouts/             页面模板
assets/              需要自动压缩的图片（新闻配图、成员照片）
static/              样式、脚本、字体、图片
scripts/             数据检查、论文更新、背景图生成脚本
.github/workflows/   自动发布、论文更新工作流
```
