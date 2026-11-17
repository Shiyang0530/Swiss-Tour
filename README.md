# 瑞士旅行手帖 · Swiss-Tour

一本可以翻页、搜索、按兴趣筛选的中文瑞士旅行电子书，参照「京都旅行手帖」的做法制作。

- **在线阅读**：在仓库设置里开启 GitHub Pages（Branch: `main`，目录 `/`）后，打开 `https://shiyang0530.github.io/Swiss-Tour/`。
- **离线阅读**：下载整个仓库（Code → Download ZIP），解压后用浏览器打开 `index.html`。地图、字体和文字都已内置，图片在 `img/` 文件夹里。

## 内容结构

大区 → 目的地（城市或地区）→ 子地点 → 景点，共约 200 处景点，另有五个专题：

- **交通**：8 条观光火车线路（附高亮线路图），以及山地交通种类和各类通票
- **长线徒步**：Via Alpina、瑞士高山之路（各段可单独查看）
- **美食与特产**、**野生动植物**、**地质与地貌** 三个小辞典

地图图例分四类：户外景点、小镇、老城区、人文景点；徒步路线、滑雪场、山地交通另有专用图标。

## 目录

| 路径 | 内容 |
|---|---|
| `index.html`、`sw.js`、`manifest.webmanifest`、`icon-*.png` | 电子书本体（单个 HTML 文件，可离线使用） |
| `img/` | 景点照片（维基共享资源，CC BY / CC BY-SA / CC0，页面上标注作者和许可）与作者提供的 AI 插画 |
| `src/build.py` | 读取 `src/content/` 生成数据（地图、标签、结构） |
| `src/assemble.py` | 把数据和 `src/base/` 里的页面模板组装成 `index.html` |
| `src/content/` | 全部文字内容：各大区景点（`r01`–`r08.py`）、专题（`r09.py`、`wild.py`、`geo.py`）、目的地结构（`dest.py`）、徒步路线坐标（`topo.py`、`multi.py`）等 |
| `src/tests/` | Playwright 截图与功能检查脚本 |
| `src/data/folder_map.json` | 本地「瑞士旅游」文件夹新旧结构对照 |

## 数据与版权

- 底图：Natural Earth（公有领域）；海拔分层为根据书中已知海拔点推算的示意图。
- 照片：Wikimedia Commons，均为可商用的知识共享许可，作者与许可见每张图片下方。
- 部分插画由 Microsoft Copilot 生成（作者提供），页面上标注为「AI 插画」。
- 文字为本书原创；票价、时刻和开放时间请以官方信息为准。

构建需要 Natural Earth 的 10m 国界、湖泊、河流 GeoJSON（放在 `/home/claude/geo/`，未包含在仓库中）。
