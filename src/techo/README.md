# techo · 旅行手帖共享资料库

按《互动旅游电子书 · 通用规范 v2.0》第六部分建立的共享资料库。所有书共用这一份资料库，每本书只是资料库的一个“视图”。目前收录两本书：京都旅行手帖（kyoto）、瑞士旅行手帖（swiss）。

## 目录

| 路径 | 内容 |
| --- | --- |
| `db/entries.json` | 全部条目，键为 7 位编号（819 条） |
| `db/images.json` | 图片记录，键为文件名（595 张），文件名 = 编号 + 用途后缀 |
| `db/ids.json` | 旧键 → 编号对照表；编号唯一、永不更改、永不复用 |
| `db/sources.json` | 各书的参考资料表 |
| `books/{书}/book.json` | 书的配置：书名、范围、大区与行政区对照、建议住宿点、时令、主题线路、词典分类、筛选细项、国家信息、标签表 |
| `books/{书}/tree.json` | 这本书用到哪些条目、目录顺序，以及引擎需要的顺序表 |
| `books/{书}/layout.json` | 只跟这本书版面有关的数据（插画地图坐标、标签位置、航空照片标注等） |
| `assets/img/` | 全部图片（按新文件名），不进 Git；可从各书仓库的 `img/` 还原 |
| `legacy/` | 迁移前的原始数据，供往返测试使用 |
| `tools/` | 脚本，见下 |

## 编号

| 首位 | 类型 | 号段 | 例子 |
| --- | --- | --- | --- |
| 1 | 点（spot、subspot） | 1000001 起 | 1000001 金阁寺 |
| 2 | 线（徒步、观景火车、山地交通、游船、多日路线及其分段） | 2000001 起 | 2000001 哲学之道 |
| 3 | 面：大区 | 3000101–3000999 | 3000101 伯尔尼高地 |
| 3 | 面：目的地、老城区、雪场 | 3001001 起 | |
| 4 | 词典词条 | 4001001 起（4000101–4000999 留给装饰图标） | 4001001 齿轨铁路 |
| 5 | 美食 | 5000001 起 | 5000001 宇治茶 |
| 6 | 节庆活动 | 6000001 起 | 6000001 祇园祭·山鉾 |
| 7 | 专题章节 | 7000001 起 | 7000001 长线徒步 |

编号不含国家或地区。引擎内部和网址（`#n-kinkakuji`）暂时仍用旧键，这样读者手机里已存的收藏、标签和行程不会丢；对照见 `db/ids.json`。

## 条目字段

规范字段：`id`、`type`（region / area / spot / subspot / line / dict / food / event / chapter）、`subtype`（如 ski_area、old_town、scenic_train、stage）、`parent`、`name`（zh / local）、`geo`（经纬度；面为子项中心，标 `approx`；线可带 `path`）、`country`、`admin`（ISO 3166-2 代码和中文名，按 Natural Earth 行政区边界判定）、`tier`（1 必去 / 2 推荐 / 3 深度）、`score`（中文热度、国际评论数、官方推荐、特殊身份，暂空）、`tags`、`season`、`summary`、`detail`、`practical`（info 开放时间/门票/交通、tip、url、通票、建议游览分钟数…）、`icon`、`cover`、`images`、`dictionary`、`verified`（最后核实日期，迁移时为空，表示尚未核实）、`sources`。

线的附加字段：`mode`、`is_transport`、`stages`、`geo.path` 等。词典：`category`、`aliases`、`related`、`related_spots`、`search_query`。

`ext.{书}.{来源}`：旧引擎专用、规范里没有对应字段的数据（如京都的知识卡片 `cards`、时令图 `season`，瑞士的热门徒步 `hot`）原样保存在这里，`_o` 记录原来的键顺序。这样导出结果与原书逐项一致。

## 图片

文件名 `{编号}_cover`、`_cover_sakura` / `_autumn` / `_snow` / `_matsuri`、`_map`、`_02`、`_03`… 京都的总图为 `kyoto_map.webp`。每条记录有 kind（photo / illustration）、source、author、license、commercial、attribution、season、quality、url、title、owner（所属条目）、role（用途），以及 `legacy`（旧键和旧文件名，引擎按旧键查图）。

## 脚本

| 脚本 | 作用 |
| --- | --- |
| `tools/migrate.py` | 一次性迁移（已完成）。资料库存在时拒绝运行，避免覆盖修改 |
| `tools/export.py` | 从资料库导出各书引擎所需的数据 |
| `tools/build_kyoto.py` | 用资料库重新生成京都 `index.html` 的数据部分、图片改名、重建 `sw.js` |
| `tools/overlay_swiss.py` | 瑞士 `build.py` 末尾调用：用资料库内容覆盖节点、改用新图片文件名；开头调用 `ingest()` 把旧工具新下载的照片登记进资料库 |
| `tools/test_roundtrip.py` | 往返测试：导出结果必须与迁移前的原书一致；改资料库字段后导出必须随之变化 |
| `tools/schema.py` | 旧字段 ↔ 资料库字段对照表 |

## 现状与限制

- **京都**：数据完全由资料库生成，改 `db/entries.json` 后运行 `build_kyoto.py` 即可。
- **瑞士**：地图、图例、编号、交通方块等仍由 `build.py` 根据 `content/*.py` 计算，资料库在最后覆盖内容。正文、标签、实用信息、通票、经纬度、分段、图片署名改资料库就生效；名称和经纬度如果改了，地图上的文字和位置要等 `content/*.py` 同步后才会变。在 `content/*.py` 里新增的景点暂时不会自动进资料库（构建时会列出）。
- 中文热度等评分、核实日期还是空的，等滚动核实任务来填。
- 资料库暂存在 Swiss-Tour 仓库的 `src/techo/`，正式位置应是私有仓库 `techo-assets`。
