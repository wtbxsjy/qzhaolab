# The QZhao Lab 网站

香港理工大学生命科学系赵倩课题组网站，中英双语。

- 英文：<https://wtbxsjy.github.io/qzhaolab/>
- 中文：<https://wtbxsjy.github.io/qzhaolab/zh/>

**维护说明见 [docs/MAINTENANCE.md](docs/MAINTENANCE.md)。**

## 工作方式

- 网站内容全部保存在 `data/` 下的 JSON 文件中，模板只负责排版。日常更新只需修改这些文件并上传图片。
- 用 Hugo[^hugo] 0.139.4（extended 版）构建，托管在 GitHub Pages。
- 推送到 `main` 分支后，GitHub Actions 自动检查数据、构建并发布，1–2 分钟生效。

[^hugo]: Hugo：静态网站生成器，把数据文件和模板组合生成网页。

## 想改什么

| 内容 | 文件 | 说明 |
| --- | --- | --- |
| 新闻（含配图） | `data/news.json` | [发布新闻](docs/MAINTENANCE.md#发布新闻) |
| 成员（含照片） | `data/team.json` | [更新成员](docs/MAINTENANCE.md#更新成员) |
| 组内生活相册 | `data/gallery.json` | [组内生活相册](docs/MAINTENANCE.md#组内生活相册) |
| 论文 | `data/publications.json`，或 Actions 中的「Update publications」 | [添加论文](docs/MAINTENANCE.md#添加论文) |
| 研究方向 | `data/research.json` | [修改研究方向](docs/MAINTENANCE.md#修改研究方向) |
| 简介、联系方式、招聘 | `data/site.json`、`data/join.json` | [修改简介、联系方式和招聘信息](docs/MAINTENANCE.md#修改简介联系方式和招聘信息) |

## 目录结构

```
data/                网站全部内容（JSON）
assets/images/       自动压缩的图片：news/ 新闻配图，team/ 成员照片，gallery/ 组内生活相册
static/              样式、脚本、字体，以及原样使用的图片（研究方向配图、首页背景图）
content/             页面占位文件（只有标题）
layouts/             页面模板
i18n/                界面固定文字（中英文）
hugo.toml            语言与导航栏
scripts/             数据检查、论文更新、背景图生成脚本
docs/                维护指南
.github/workflows/   自动发布、论文更新工作流
```

## 本地预览

```bash
python3 scripts/check_data.py
hugo server   # 打开 http://localhost:1313/
```
