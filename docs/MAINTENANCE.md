# 网站维护指南

本指南面向负责更新课题组网站的同学，不需要编程基础。日常更新只需编辑 `data/` 下的 JSON[^json] 文件并上传图片，网站会自动重新发布。

[^json]: JSON（JavaScript Object Notation）：一种用花括号、方括号和引号组织数据的纯文本格式。

## 目录

- [修改网站的两种方式](#修改网站的两种方式)
- [JSON 文件的写法](#json-文件的写法)
- [内容文件一览](#内容文件一览)
- [发布新闻](#发布新闻)
- [更新成员](#更新成员)
- [组内生活相册](#组内生活相册)
- [添加论文](#添加论文)
- [修改研究方向](#修改研究方向)
- [修改简介、联系方式和招聘信息](#修改简介联系方式和招聘信息)
- [图片规范](#图片规范)
- [发布与排错](#发布与排错)
- [在本地预览](#在本地预览)
- [绑定自有域名](#绑定自有域名)
- [待完善事项](#待完善事项)

## 修改网站的两种方式

**在 GitHub 网页上修改（推荐）**

1. 打开仓库，进入要改的文件，例如 `data/news.json`，点右上角的铅笔图标进入编辑。
2. 改完后点「Commit changes」提交。
3. 上传图片：进入对应文件夹（如 `assets/images/news/`），点「Add file → Upload files」。

提交后 1–2 分钟网站自动更新。

**在本地修改**：克隆仓库，修改后 `git push` 到 `main` 分支，效果相同。

## JSON 文件的写法

**中英文字段**统一写成：

```json
{ "en": "English text", "zh": "中文内容" }
```

`zh` 留空时，中文页面显示英文。大部分文字支持 Markdown[^md]，例如 `**粗体**`、`*斜体*`、`[链接文字](https://...)`。

[^md]: Markdown：一种用简单符号标记格式的纯文本写法。

**容易出错的地方：**

- 每一项之间用英文逗号分隔，最后一项后面**不能**有逗号。
- 引号、逗号、冒号都必须是英文半角符号；中文内容里可以用中文标点。
- 文字里出现英文双引号时，写成 `\"`。

写错了也不用担心：发布前会自动检查，出错时网站保持原样不变，并告诉你哪个文件第几行有问题（见[发布与排错](#发布与排错)）。

**人名写法：** 英文名「姓在前、名在后」，姓氏全部大写，例如 `Dr. YANG Ying`、`ZHAN Hongyu`；有英文名的成员写成「英文名 + 大写姓氏」，例如 `Ms. Chloe TSE`。新闻正文里提到人名时同样处理。论文作者列表按期刊惯例写，例如 `Zhao Q`，不受此规则影响。

## 内容文件一览

| 文件 | 内容 |
| --- | --- |
| `data/site.json` | 课题组名称、标语、首页研究概述、系/学院/大学、首页背景图、联系方式、首页显示的新闻条数、论文中加粗的作者名 |
| `data/research.json` | 研究方向：标题、简介、配图、正文、术语说明。每个方向自动生成一个页面 |
| `data/team.json` | 课题组负责人、在组成员、已毕业成员 |
| `data/publications.json` | 论文列表 |
| `data/news.json` | 新闻动态 |
| `data/gallery.json` | 团队成员页底部的「组内生活」相册 |
| `data/join.json` | 招聘信息：岗位、要求、申请方式、平台、经费来源 |

一般不需要改的文件：

| 文件 | 用途 |
| --- | --- |
| `hugo.toml` | 语言设置、导航栏菜单名称 |
| `i18n/en.toml`、`i18n/zh.toml` | 界面上的固定文字，如「研究亮点」「全部论文」 |
| `content/` | 页面占位文件，只写页面标题 |
| `layouts/`、`static/css/`、`static/js/` | 模板、样式、脚本 |

## 发布新闻

在 `data/news.json` 的方括号内任意位置加一条，网站会按日期自动排序。首页显示最新几条，条数由 `site.json` 的 `homeNewsCount` 决定（默认 3 条）。

```json
{
  "date": "2026-10-05",
  "en": "Dr. QIAO Sitan joins the lab as a Postdoctoral Fellow.",
  "zh": "乔斯坦博士以博士后研究员身份加入课题组。"
},
```

日期一律写成 `年-月-日`，月和日要补零。

### 给新闻配图

1. 把图片上传到 `assets/images/news/`，原图即可，手机照片也行。
2. 在该条新闻里加上 `images`：

```json
{
  "date": "2026-09-29",
  "en": "PhD candidate Ms. YANG Chenxi wins the HUPO Travel Award and the AOHUPO Outstanding Poster Award! Congratulations!",
  "zh": "博士研究生杨晨曦荣获 HUPO 旅行奖及 AOHUPO 优秀壁报奖！祝贺！",
  "images": [
    "images/news/2026-09-29-aohupo-award-ceremony.jpg",
    {
      "src": "images/news/2026-09-29-aohupo-certificate.jpg",
      "caption": { "en": "Award certificate", "zh": "获奖证书" }
    }
  ]
}
```

- 每张图可以只写路径，也可以写成带 `src`、`caption`（图注）、`alt`（图片描述，供读屏软件[^alt]使用）的形式。不写 `alt` 时，依次用图注或新闻正文代替。
- 新闻页显示全部配图，点击可放大，用方向键切换同一条新闻的图片；首页每条新闻只显示第一张小图，所以最有代表性的图放在第一张。
- 论文首页截图、海报这类特别宽或特别窄的图片会完整显示，不会被裁剪。

[^alt]: 读屏软件：视障用户用来朗读网页内容的辅助工具。图片描述也会在图片加载失败时显示。

## 更新成员

成员信息在 `data/team.json`，分为 `pi`（课题组负责人）、`members`（在组成员）、`alumni`（已毕业成员）三部分。列表顺序就是网页上的显示顺序。

**新成员加入**：在 `members` 中加一项：

```json
{ "name": "LI Kecheng", "name_zh": "李克成", "role": "phd", "photo": "images/team/li-kecheng.jpg" }
```

`role` 可选：

| 值 | 显示为 |
| --- | --- |
| `postdoc` | 博士后研究员 |
| `phd` | 博士研究生 |
| `mphil` | 哲学硕士研究生 |
| `visiting` | 访问学者 |
| `uris` | 本科生研究助理 |
| `fyp` | 本科毕业设计学生 |

`name_zh` 是中文名，不填时中文页面显示英文名。

**成员毕业**：把这一项从 `members` 移到 `alumni`，加上 `now`（现在的去向），毕业后获得博士学位的在名字前加 `Dr.`：

```json
{ "name": "Dr. YANG Ying", "name_zh": "杨颖", "role": "phd", "photo": "images/team/yang-ying.jpg", "now": { "en": "Assistant Professor, Chongqing Medical University", "zh": "重庆医科大学 助理教授" } }
```

**成员照片**：上传到 `assets/images/team/`，在该成员条目里写上 `"photo": "images/team/文件名.jpg"`。

- 网站会自动裁剪：在组成员显示为圆形头像，负责人为竖版照片，已毕业成员为小圆头像，并自动对准画面主体。
- 人物居中、头肩入画、背景简洁的照片效果最好。
- 文件名用姓名拼音，例如 `zhang-yuanliang.jpg`。
- 没有照片时显示姓氏首字母。

## 组内生活相册

显示在团队成员页底部。照片上传到 `assets/images/gallery/`，然后在 `data/gallery.json` 里加一项。列表顺序就是显示顺序，新照片建议加在最前面：

```json
[
  {
    "src": "images/gallery/2026-12-christmas.jpg",
    "caption": { "en": "Christmas party 2026", "zh": "2026 年圣诞聚会" }
  },
  "images/gallery/lab-life-01.jpg"
]
```

- 每项可以只写路径，也可以加 `caption`（图注，显示在照片下方和放大视图中）。
- 缩略图统一裁成 3:2；点开后可用方向键浏览整个相册。
- 相册为空（`[]`）时，这一栏不显示。

## 添加论文

### 按 DOI 自动添加（推荐）

DOI[^doi] 是每篇论文的唯一编号。打开仓库的 **Actions** 页面，左侧选「Update publications」，点「Run workflow」，填写：

| 栏目 | 填什么 | 示例 |
| --- | --- | --- |
| `doi` | 新论文的 DOI | `10.1021/jasms.1c00076` |
| `topics` | 所属研究方向的 `id`，可多个，用逗号分隔；可留空 | `peptidein,immunopeptides` |
| `corresponding` | 通讯作者，可多个，用逗号分隔 | `Zhao Q` |

工作流会从 Crossref[^crossref] 获取标题、全部作者、期刊、卷期和页码，写入 `data/publications.json`，并自动重新发布。填了 `topics` 的论文还会出现在对应研究方向页面的「代表性论文」中。

不填 DOI 直接运行，会给已有条目补全作者列表和被截断的标题。

[^doi]: DOI（Digital Object Identifier，数字对象标识符）：每篇论文的唯一编号，形如 `10.xxxx/xxxxx`。
[^crossref]: Crossref：学术出版物元数据的登记机构，可按 DOI 查询论文的标题、作者等信息。

### 手动添加

在 `data/publications.json` 中加一项（顺序不限，网页按年份排列）：

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

- `corresponding` 中的作者名后显示 `*`，`equal`（共同贡献）中的显示 `#`。
- 作者列表中有同名作者（例如两位 `Yang Y`），或者缩写和你写的不一致（例如 `Wang H` 与 `Wang HW`）时，按名字标注会标错或标不上。这时改用作者序号，从 1 开始数：`"equalPositions": [1, 2]`、`"correspondingPositions": [9]`。数据检查会自动发现这类问题。
- 没有 DOI 时，可以用 `"url"` 给出论文链接。
- 需要加粗的作者名（默认 `Zhao Q`）在 `site.json` 的 `highlightAuthors` 中设置。

## 修改研究方向

研究方向在 `data/research.json` 的 `directions` 中。新增一个方向：复制一段已有方向，改掉 `id` 和内容即可。网站会自动生成新页面，并在首页增加一张卡片。

| 字段 | 说明 |
| --- | --- |
| `id` | 页面地址，只能用小写英文字母、数字和连字符；例如 `chemical-proteomics` 对应 `/research/chemical-proteomics/` |
| `title`、`summary` | 标题和一句话简介，显示在首页卡片上 |
| `intro`、`sections` | 研究方向页面的正文，`sections` 每节一个标题加若干条目 |
| `image`、`imageAlt` | 配图（放在 `static/images/research/`，比例约 3:2）和图片描述 |
| `notes` | 术语说明，显示在页面底部；只在对应语言有文字时显示，可以只给中文版写解释 |

## 修改简介、联系方式和招聘信息

- **课题组名称、标语、首页研究概述、系名、地址、邮箱**：都在 `data/site.json`。
- **首页背景图**：`site.json` 的 `heroImage`。把新图片放进 `static/images/`，再改这个路径。建议宽约 2000 像素、文件小于 500 KB。现在的背景图是用 `scripts/make_hero_bg.py` 生成的原创插画，可以换一个随机种子重新生成：`python scripts/make_hero_bg.py hero-bg.svg 11`。生成的是 SVG[^svg] 矢量图，需要再转成 JPG。
- **招聘信息**：`data/join.json`，包括各岗位（`positions`，每个岗位可有状态标签 `status`、简介 `lead` 和若干分组 `groups`，申请方式写在各岗位的分组里）、培训与平台介绍（`environment`）以及经费来源（`funding`）。岗位招满后，删除该岗位或把 `status` 改成已结束即可。增删岗位或条目时照现有格式复制修改即可。

[^svg]: SVG（Scalable Vector Graphics，可缩放矢量图形）：一种矢量图片格式。

## 图片规范

| 用途 | 放在哪里 | 网站如何处理 |
| --- | --- | --- |
| 新闻配图 | `assets/images/news/` | 自动生成缩略图和大图，宽或窄的图完整显示 |
| 成员照片 | `assets/images/team/` | 自动裁剪并对准人物 |
| 组内生活相册 | `assets/images/gallery/` | 自动裁成 3:2 缩略图 |
| 研究方向配图、首页背景图 | `static/images/` | 原样使用，请先自行压缩 |

- 放在 `assets/` 下的图片可以直接上传原图，访客下载的是压缩后的 WebP[^webp] 版本。
- 单张原图建议不超过 8 MB，超过时数据检查会提示，以免仓库变得过大。
- 文件名只用小写英文字母、数字和连字符，不要用空格和中文；新闻图片建议以日期开头，例如 `2026-09-29-aohupo-certificate.jpg`。

[^webp]: WebP：一种体积较小的网页图片格式。

## 发布与排错

每次提交到 `main` 分支后，GitHub Actions[^actions] 会依次：

1. **检查数据**（Check data files）：JSON 格式、必填字段、日期格式、图片路径、作者标注等。
2. **构建网站**：生成所有网页并压缩图片。
3. **发布**到 GitHub Pages[^pages]。

在仓库的 **Actions** 页面可以看到每次发布的结果：绿色对勾表示成功，红色叉号表示失败。

**发布失败怎么办：**

1. 点进失败的那次运行，展开红色的步骤。
2. 如果是「Check data files」失败，日志会列出问题，例如 `news.json: JSON syntax error at line 12, column 5`，或者 `team.json → members[3]: image "images/team/x.jpg" not found`。按提示修改对应文件再提交即可。
3. 发布失败时，线上网站保持上一次成功的版本，不会出现坏掉的页面。

也可以在本地先检查：`python3 scripts/check_data.py`。

[^actions]: GitHub Actions：GitHub 内置的自动化工具，这里用来在每次修改后自动检查、构建和发布网站。
[^pages]: GitHub Pages：GitHub 提供的免费静态网站托管服务。

## 在本地预览

需要安装 Hugo[^hugo] extended 版 0.139.4（[安装说明](https://gohugo.io/installation/)）：

```bash
python3 scripts/check_data.py   # 检查数据
hugo server                     # 启动预览
# 浏览器打开 http://localhost:1313/ ，修改文件后页面自动刷新
```

[^hugo]: Hugo：静态网站生成器，把数据文件和模板组合生成网页。

## 绑定自有域名

1. 购买域名，例如 `zhaoqlab.org`。
2. 在仓库的 Settings → Pages → Custom domain 中填入域名，按提示在域名服务商处添加 DNS[^dns] 记录。
3. 把 `hugo.toml` 第一行的 `baseURL` 改成新域名。

[^dns]: DNS（Domain Name System，域名系统）：把域名指向网站服务器的记录。

## 待完善事项

- **研究方向配图**：目前两张是从首页背景插画裁出的临时图，建议换成课题组的科研示意图。
- **旧照片清晰度**：从旧网站搬来的新闻配图大多分辨率较低，如有原图可按原文件名替换。
- **相册图注**：组内生活相册的 24 张照片暂无图注，可按需补充。
