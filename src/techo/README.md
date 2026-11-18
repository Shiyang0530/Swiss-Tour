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
| `engine/` | 通用引擎：两本书共用的页面程序和模板，见下；`engine/geo/` 是地理制图模块（Natural Earth 底图、海拔分层、标注避让） |
| `tools/` | 脚本，见下 |
| `books/swiss/src/` | 瑞士的结构与地理数据（`build.py`、`content/`、`tree/`、照片记录 `imgdb.json`、下载照片的 `fetch_img.py`）；由 `build_book.py swiss` 自动调用 |
| `reports/` | 检查报告和每周核实清单 |
| `tests/` | 逐页快照比较：`snap.py` 存下每一页渲染结果，`cmp.py` 比较两份快照 |

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

## 通用引擎

两本书用同一套页面程序 `engine/app.js` 和同一套模板（`head.html`、`body.html`、`tail.html`、`base.css`、`sw.js`）。书和书之间的差别都写在 `books/{书}/engine.json`（页面里叫 `CFG`）：

- 书名、文件夹名、分享网址、标签父子关系、时令（`SC_TAGS`、`SC_DEF`）、实用信息栏目、美食搜索网站、维基百科语言、目录分组、筛选细项、使用说明、搜索框提示、Logo；
- 自动行程的方式：`ap.planner` 为 `single`（住一个城市，京都）或 `multi`（按大区轮换住宿，瑞士），分别在 `engine/planner/` 里；住宿点、机场车站、偏好标签等也在 `ap` 里；
- 功能开关 `feat`：两本书目前全部打开（京都在 v72 打开）；新书可以按需要关掉某一项：

| 开关 | 作用 |
| --- | --- |
| `disp` | 路径、列表小字用条目名称（关闭时用文件夹名） |
| `og` | 正文括号里的外文原名用浅色斜体 |
| `countMarkers` | 地图圆点里的数字是景点数（关闭时是列表编号，筛选时在名称后显示数量） |
| `smartLabels` | 地图文字放不下时自动换到另一侧 |
| `smTags` | 时令月历也读取条目自带的时令月份 |
| `planRowData` | 只有能排进行程的景点显示“加入行程” |
| `relatedLeaves` | “相关景点”只列具体景点 |
| `photoNoMap` | 子项没有坐标时左页显示照片而不是空地图 |
| `termPaging` | 词典可以用 ‹ › 翻页 |
| `planMap` | 旅行计划页显示行程地图 |
| `autoDraft` | 自动行程生成后自动存成草稿版本 |
| `zoom` | 地图缩放按钮和在线底图切换（底图种类见 `basemaps`：瑞士 swisstopo 与 OpenStreetMap，京都 OpenStreetMap） |
| `back` | 顶部“‹ 返回”按钮 |

生成一本书：`python3 tools/build_book.py kyoto` 或 `swiss`。瑞士会先运行 `books/swiss/src/build.py` 画结构和地图（名称、经纬度等先从资料库读取），输出在 `build/swiss/`；加 `--skip-render` 可以跳过这一步。海拔分层图用 `engine/geo/hypso.py` 重新生成。

界面按规范第十四到十七部分：海军蓝品牌色和纸张米色；页头书名带英文小字和双细线；条目页的「＋ 加入我的行程」大按钮和两步底部弹层（选行程 → 书内日历选日期）；「♡ 收藏 / ✓ 已去过 / + 标签」次要操作栏和带日期的「已去过」印章；筛选栏吸顶、数量为 0 的细项变灰；分享行程的二维码（只含条目编号和日期，页面里的 `NID` 是旧键到编号的对照）和行程长图导出。`tools/make_engine.py` 是第一次合并时的记录，不用再运行。

合并的检查方法：用 `tests/snap.py` 把合并前后两个版本的每一页（全部景点、词条、标签、使用说明、计划页和两组自动行程）渲染出来逐页比较，京都 483 页、瑞士 495 页全部一致。

## 脚本

| 脚本 | 作用 |
| --- | --- |
| `tools/migrate.py` | 一次性迁移（已完成）。资料库存在时拒绝运行，避免覆盖修改 |
| `tools/export.py` | 从资料库导出各书引擎所需的数据 |
| `tools/build_book.py` | 用通用引擎和资料库生成一本书（index.html、sw.js、manifest） |
| `tools/build_kyoto.py` | 第一次迁移时给京都图片改名用；页面生成已改由 `build_book.py` 负责 |
| `tools/overlay_swiss.py` | 瑞士 `build.py` 末尾调用：用资料库内容覆盖节点、改用新图片文件名；开头调用 `ingest()` 把旧工具新下载的照片登记进资料库 |
| `tools/test_roundtrip.py` | 往返测试：导出结果必须与迁移前的原书一致；改资料库字段后导出必须随之变化 |
| `tools/schema.py` | 旧字段 ↔ 资料库字段对照表 |
| `tools/check.py` | 资料库检查：编号、必填字段、引用、标签、图片许可与署名；加 `--links` 检查官网和参考资料链接（需要能上网） |
| `tools/verify_queue.py` | 滚动核实：列出本周要核对的条目（从没核实过的、一级必去优先）；核对后用 `--mark` 写入核实日期 |

## 现状与限制

- **京都**：数据完全由资料库生成，改 `db/entries.json` 后运行 `build_kyoto.py` 即可。
- **瑞士**：结构和地图由 `books/swiss/src/build.py` 计算，名称和经纬度在画地图之前就从资料库读取，其余内容在最后覆盖，所以改资料库后地图和正文都会跟着变。景点的层级关系、徒步路线和列车站点的坐标仍在 `books/swiss/src/content/`；在那里新增的景点暂时不会自动进资料库（构建时会列出）。
- 中文热度等评分、核实日期还是空的，等滚动核实任务来填。
- 资料库暂存在 Swiss-Tour 仓库的 `src/techo/`，正式位置应是私有仓库 `techo-assets`。
