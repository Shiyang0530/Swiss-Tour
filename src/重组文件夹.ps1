# 瑞士旅行手帖 · 本地文件夹重组脚本（按新结构：大区 → 目的地 → 子地点 → 景点）
# 用法：在「瑞士旅游」文件夹里右键 → 在终端中打开，运行：powershell -ExecutionPolicy Bypass -File .\重组文件夹.ps1
# 只会新建文件夹和移动文件，不会删除任何东西；旧文件夹清空后保留，确认无误后可自行删除。
$ErrorActionPreference = "Continue"
$root = Get-Location
$moved = 0; $made = 0
if (-not (Test-Path -LiteralPath "01_伯尔尼高地")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/01_何维克街与何维克草坪")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/01_何维克街与何维克草坪" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/02_哈德昆姆")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/02_哈德昆姆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/03_希尼格普拉特＋高山植物园")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/03_希尼格普拉特＋高山植物园" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/04_图恩湖与布里恩茨湖游船")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/04_图恩湖与布里恩茨湖游船" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/01_菲斯特与悬崖步道")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/01_菲斯特与悬崖步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/02_巴赫阿尔卑湖")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/02_巴赫阿尔卑湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/03_艾格快线")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/03_艾格快线" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/04_曼利兴–小沙伊德格全景步道")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/04_曼利兴–小沙伊德格全景步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/05_格林德瓦雪场")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/05_格林德瓦雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰/01_少女峰铁路")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰/01_少女峰铁路" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰/02_斯芬克斯观景台、冰宫")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰/02_斯芬克斯观景台、冰宫" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰/03_艾格北壁步道")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰/03_艾格北壁步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/01_施陶河瀑布")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/01_施陶河瀑布" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/02_特吕默尔巴赫瀑布")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/02_特吕默尔巴赫瀑布" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/03_文根小镇")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/03_文根小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/04_米伦小镇")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/04_米伦小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/05_雪朗峰 Piz Gloria")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/05_雪朗峰 Piz Gloria" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/02_图恩湖与布里恩茨湖")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/02_图恩湖与布里恩茨湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/02_图恩湖与布里恩茨湖/01_图恩城堡")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/02_图恩湖与布里恩茨湖/01_图恩城堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/02_图恩湖与布里恩茨湖/02_施皮茨")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/02_图恩湖与布里恩茨湖/02_施皮茨" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/02_图恩湖与布里恩茨湖/03_尼森山")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/02_图恩湖与布里恩茨湖/03_尼森山" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/02_图恩湖与布里恩茨湖/04_伊瑟尔瓦尔德码头")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/02_图恩湖与布里恩茨湖/04_伊瑟尔瓦尔德码头" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/02_图恩湖与布里恩茨湖/05_布里恩茨木雕村")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/02_图恩湖与布里恩茨湖/05_布里恩茨木雕村" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/02_图恩湖与布里恩茨湖/06_布里恩茨罗特洪蒸汽齿轨")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/02_图恩湖与布里恩茨湖/06_布里恩茨罗特洪蒸汽齿轨" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/02_图恩湖与布里恩茨湖/07_巴伦贝格露天博物馆")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/02_图恩湖与布里恩茨湖/07_巴伦贝格露天博物馆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/02_图恩湖与布里恩茨湖/08_迈林根·阿勒峡谷、莱辛巴赫瀑布")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/02_图恩湖与布里恩茨湖/08_迈林根·阿勒峡谷、莱辛巴赫瀑布" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/03_坎德施泰格与阿德尔博登")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/03_坎德施泰格与阿德尔博登" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/03_坎德施泰格与阿德尔博登/01_厄希嫩湖")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/03_坎德施泰格与阿德尔博登/01_厄希嫩湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/03_坎德施泰格与阿德尔博登/02_蓝湖")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/03_坎德施泰格与阿德尔博登/02_蓝湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/03_坎德施泰格与阿德尔博登/03_恩斯特利根瀑布")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/03_坎德施泰格与阿德尔博登/03_恩斯特利根瀑布" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/04_格施塔德")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/04_格施塔德" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/04_格施塔德/01_格施塔德小镇")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/04_格施塔德/01_格施塔德小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "01_伯尔尼高地/04_格施塔德/02_劳埃嫩湖")) { New-Item -ItemType Directory -Force -Path "01_伯尔尼高地/04_格施塔德/02_劳埃嫩湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/01_采尔马特小镇")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/01_采尔马特小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/02_马特洪峰")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/02_马特洪峰" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/03_戈尔内格拉特铁路")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/03_戈尔内格拉特铁路" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/04_马特洪冰川天堂")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/04_马特洪冰川天堂" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/05_苏内加与五湖步道")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/05_苏内加与五湖步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/06_里菲尔湖倒影")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/06_里菲尔湖倒影" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/07_黑湖")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/07_黑湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/08_高巴尔门步道")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/08_高巴尔门步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/09_采尔马特雪场")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/09_采尔马特雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_马特洪峰地区/10_蒙特罗莎山屋")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/01_马特洪峰地区/10_蒙特罗莎山屋" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/02_萨斯费")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/02_萨斯费" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/02_萨斯费/01_萨斯费小镇")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/02_萨斯费/01_萨斯费小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/02_萨斯费/02_阿拉林地铁＋旋转餐厅＋冰洞")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/02_萨斯费/02_阿拉林地铁＋旋转餐厅＋冰洞" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/02_萨斯费/03_萨斯费雪场")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/02_萨斯费/03_萨斯费雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/03_阿莱奇冰川区")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/03_阿莱奇冰川区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/03_阿莱奇冰川区/01_艾吉斯峰")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/03_阿莱奇冰川区/01_艾吉斯峰" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/03_阿莱奇冰川区/02_阿莱奇冰川")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/03_阿莱奇冰川区/02_阿莱奇冰川" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/03_阿莱奇冰川区/03_阿莱奇森林")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/03_阿莱奇冰川区/03_阿莱奇森林" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_罗讷河谷")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/04_罗讷河谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_罗讷河谷/01_锡永瓦莱尔与图尔比永城堡")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/04_罗讷河谷/01_锡永瓦莱尔与图尔比永城堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_罗讷河谷/02_瓦莱葡萄酒")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/04_罗讷河谷/02_瓦莱葡萄酒" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_罗讷河谷/03_洛伊克巴德温泉")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/04_罗讷河谷/03_洛伊克巴德温泉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_罗讷河谷/04_葛米山口")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/04_罗讷河谷/04_葛米山口" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/05_瓦莱滑雪胜地")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/05_瓦莱滑雪胜地" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/05_瓦莱滑雪胜地/01_韦尔比耶雪场")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/05_瓦莱滑雪胜地/01_韦尔比耶雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/05_瓦莱滑雪胜地/02_克兰-蒙塔纳雪场")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/05_瓦莱滑雪胜地/02_克兰-蒙塔纳雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/01_夏蒙尼小镇")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/01_夏蒙尼小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/02_南针峰")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/02_南针峰" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/03_蒙唐维尔铁路与冰海冰川")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/03_蒙唐维尔铁路与冰海冰川" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/04_白湖")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/04_白湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/05_北阳台步道")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/05_北阳台步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/06_布雷文")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/06_布雷文" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/07_白谷冰川野雪")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/07_白谷冰川野雪" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/08_夏蒙尼雪场")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/08_夏蒙尼雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/01_库马约尔小镇")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/01_库马约尔小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/02_勃朗峰天空之路")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/02_勃朗峰天空之路" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/03_意大利段费雷谷")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/03_意大利段费雷谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/04_奥斯塔罗马古城")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/04_奥斯塔罗马古城" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/03_尚佩与瑞士费雷谷")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/03_尚佩与瑞士费雷谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/03_尚佩与瑞士费雷谷/01_尚佩湖")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/03_尚佩与瑞士费雷谷/01_尚佩湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/03_尚佩与瑞士费雷谷/02_瑞士段费雷谷")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/03_尚佩与瑞士费雷谷/02_瑞士段费雷谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/01_第 1 段 · 莱乌什 → 莱孔塔米讷")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/01_第 1 段 · 莱乌什 → 莱孔塔米讷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/02_第 2 段 · 莱孔塔米讷 → 博诺姆十字架小屋")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/02_第 2 段 · 莱孔塔米讷 → 博诺姆十字架小屋" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/03_第 3 段 · 博诺姆十字架 → 伊丽莎白小屋")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/03_第 3 段 · 博诺姆十字架 → 伊丽莎白小屋" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/04_第 4 段 · 伊丽莎白小屋 → 库马约尔")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/04_第 4 段 · 伊丽莎白小屋 → 库马约尔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/05_第 5 段 · 库马约尔 → 博纳蒂小屋")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/05_第 5 段 · 库马约尔 → 博纳蒂小屋" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/06_第 6 段 · 博纳蒂小屋 → 拉富利")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/06_第 6 段 · 博纳蒂小屋 → 拉富利" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/07_第 7 段 · 拉富利 → 尚佩")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/07_第 7 段 · 拉富利 → 尚佩" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/08_第 8 段 · 尚佩 → 特里安")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/08_第 8 段 · 尚佩 → 特里安" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/09_第 9 段 · 特里安 → 特雷勒尚")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/09_第 9 段 · 特里安 → 特雷勒尚" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/10_第 10 段 · 特雷勒尚 → 拉弗雷热尔")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/10_第 10 段 · 特雷勒尚 → 拉弗雷热尔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/11_第 11 段 · 拉弗雷热尔 → 莱乌什")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/11_第 11 段 · 拉弗雷热尔 → 莱乌什" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途/01_大圣伯纳德山口、修道院与圣伯纳犬")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途/01_大圣伯纳德山口、修道院与圣伯纳犬" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途/02_拉韦莱班温泉")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途/02_拉韦莱班温泉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途/03_萨永温泉")) { New-Item -ItemType Directory -Force -Path "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途/03_萨永温泉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森市区")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/01_琉森市区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森市区/01_琉森老城")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/01_琉森市区/01_琉森老城" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森市区/01_琉森老城/01_卡佩尔廊桥")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/01_琉森市区/01_琉森老城/01_卡佩尔廊桥" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森市区/01_琉森老城/02_狮子纪念碑")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/01_琉森市区/01_琉森老城/02_狮子纪念碑" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森市区/02_瑞士交通博物馆")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/01_琉森市区/02_瑞士交通博物馆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森市区/03_琉森文化会议中心 KKL")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/01_琉森市区/03_琉森文化会议中心 KKL" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山/01_瑞吉铁路")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山/01_瑞吉铁路" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山/02_瑞吉卡尔特巴德温泉")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山/02_瑞吉卡尔特巴德温泉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山/03_瑞吉全景步道")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山/03_瑞吉全景步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/02_皮拉图斯山")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/02_皮拉图斯山" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/02_皮拉图斯山/01_皮拉图斯铁路")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/02_皮拉图斯山/01_皮拉图斯铁路" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/02_皮拉图斯山/02_龙之路")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/02_皮拉图斯山/02_龙之路" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克/01_施坦塞峰双层敞篷缆车")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克/01_施坦塞峰双层敞篷缆车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克/02_比尔根施托克悬崖步道与哈默施万德电梯")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克/02_比尔根施托克悬崖步道与哈默施万德电梯" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克/03_布尔根施托克高山水疗")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克/03_布尔根施托克高山水疗" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利/01_斯托斯缆索铁路")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利/01_斯托斯缆索铁路" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利/02_斯托斯山脊步道")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利/02_斯托斯山脊步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利/03_吕特利草地")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利/03_吕特利草地" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/02_琉森湖区/05_琉森湖游船")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/02_琉森湖区/05_琉森湖游船" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/03_铁力士与英格堡")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/03_铁力士与英格堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/03_铁力士与英格堡/01_英格堡修道院")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/03_铁力士与英格堡/01_英格堡修道院" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/03_铁力士与英格堡/02_铁力士旋转缆车")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/03_铁力士与英格堡/02_铁力士旋转缆车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/03_铁力士与英格堡/03_特吕布湖")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/03_铁力士与英格堡/03_特吕布湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/03_铁力士与英格堡/04_英格堡雪场")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/03_铁力士与英格堡/04_英格堡雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/04_琉森周边与沿途")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/04_琉森周边与沿途" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "03_琉森与瑞士中部/04_琉森周边与沿途/01_施拉滕弗卢喀斯特徒步")) { New-Item -ItemType Directory -Force -Path "03_琉森与瑞士中部/04_琉森周边与沿途/01_施拉滕弗卢喀斯特徒步" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/01_圣莫里茨小镇与湖")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/01_圣莫里茨小镇与湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/02_科尔瓦奇")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/02_科尔瓦奇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/03_穆奥塔斯穆拉尔")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/03_穆奥塔斯穆拉尔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/04_锡尔斯湖与费克斯谷")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/04_锡尔斯湖与费克斯谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/05_圣莫里茨雪场")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/05_圣莫里茨雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/06_恩加丁落叶松")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/06_恩加丁落叶松" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/01_迪亚沃莱扎")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/01_迪亚沃莱扎" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/02_莫特拉奇冰川步道")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/02_莫特拉奇冰川步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/03_布鲁西奥螺旋桥")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/03_布鲁西奥螺旋桥" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/04_波斯基亚沃小镇")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/04_波斯基亚沃小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/03_下恩加丁")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/03_下恩加丁" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/03_下恩加丁/01_斯库奥尔温泉")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/03_下恩加丁/01_斯库奥尔温泉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/03_下恩加丁/02_瓜尔达古村")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/03_下恩加丁/02_瓜尔达古村" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/03_下恩加丁/03_塔拉斯普城堡")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/03_下恩加丁/03_塔拉斯普城堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/01_恩加丁地区/03_下恩加丁/04_瑞士国家公园")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/01_恩加丁地区/03_下恩加丁/04_瑞士国家公园" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/02_达沃斯与克洛斯特斯")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/02_达沃斯与克洛斯特斯" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/02_达沃斯与克洛斯特斯/01_达沃斯小镇与湖")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/02_达沃斯与克洛斯特斯/01_达沃斯小镇与湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/02_达沃斯与克洛斯特斯/02_帕森·魏斯弗卢峰")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/02_达沃斯与克洛斯特斯/02_帕森·魏斯弗卢峰" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/02_达沃斯与克洛斯特斯/03_达沃斯–克洛斯特斯雪场")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/02_达沃斯与克洛斯特斯/03_达沃斯–克洛斯特斯雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/03_库尔与阿罗萨")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/03_库尔与阿罗萨" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/03_库尔与阿罗萨/01_库尔老城")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/03_库尔与阿罗萨/01_库尔老城" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/03_库尔与阿罗萨/02_阿罗萨魏斯峰")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/03_库尔与阿罗萨/02_阿罗萨魏斯峰" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/03_库尔与阿罗萨/03_迈恩菲尔德海蒂村")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/03_库尔与阿罗萨/03_迈恩菲尔德海蒂村" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/03_库尔与阿罗萨/04_巴特拉加茨温泉")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/03_库尔与阿罗萨/04_巴特拉加茨温泉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/04_弗利姆斯–拉克斯")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/04_弗利姆斯–拉克斯" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/04_弗利姆斯–拉克斯/01_考马湖")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/04_弗利姆斯–拉克斯/01_考马湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/04_弗利姆斯–拉克斯/02_莱茵大峡谷 Ruinaulta")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/04_弗利姆斯–拉克斯/02_莱茵大峡谷 Ruinaulta" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/04_弗利姆斯–拉克斯/03_拉克斯雪场")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/04_弗利姆斯–拉克斯/03_拉克斯雪场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/05_阿尔布拉线")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/05_阿尔布拉线" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/05_阿尔布拉线/01_兰德瓦瑟高架桥")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/05_阿尔布拉线/01_兰德瓦瑟高架桥" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/05_阿尔布拉线/02_贝尔金铁路博物馆与雪橇道")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/05_阿尔布拉线/02_贝尔金铁路博物馆与雪橇道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/06_格劳宾登周边与沿途")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/06_格劳宾登周边与沿途" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/06_格劳宾登周边与沿途/01_瓦尔斯温泉（卒姆托设计）")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/06_格劳宾登周边与沿途/01_瓦尔斯温泉（卒姆托设计）" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "04_格劳宾登/06_格劳宾登周边与沿途/02_维亚马拉峡谷")) { New-Item -ItemType Directory -Force -Path "04_格劳宾登/06_格劳宾登周边与沿途/02_维亚马拉峡谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺")) { New-Item -ItemType Directory -Force -Path "05_提契诺" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区/01_卢加诺")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区/01_卢加诺" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区/01_卢加诺/01_卢加诺湖游船")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区/01_卢加诺/01_卢加诺湖游船" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区/01_卢加诺/02_老城与改革广场")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区/01_卢加诺/02_老城与改革广场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区/01_卢加诺/03_圣萨尔瓦托雷山")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区/01_卢加诺/03_圣萨尔瓦托雷山" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区/02_莫尔科特与甘德里亚")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区/02_莫尔科特与甘德里亚" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区/02_莫尔科特与甘德里亚/01_莫尔科特")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区/02_莫尔科特与甘德里亚/01_莫尔科特" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区/02_莫尔科特与甘德里亚/02_甘德里亚湖畔步道")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区/02_莫尔科特与甘德里亚/02_甘德里亚湖畔步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区/03_门德里西奥")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区/03_门德里西奥" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/01_卢加诺湖区/03_门德里西奥/01_吉内罗索山铁路＋石之花")) { New-Item -ItemType Directory -Force -Path "05_提契诺/01_卢加诺湖区/03_门德里西奥/01_吉内罗索山铁路＋石之花" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/01_洛迦诺大广场")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/01_洛迦诺大广场" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/02_圣母岩修道院")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/02_圣母岩修道院" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/03_卡达达与奇梅塔")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/03_卡达达与奇梅塔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/04_阿斯科纳")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/04_阿斯科纳" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/01_拉韦尔泰佐双拱桥")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/01_拉韦尔泰佐双拱桥" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/02_韦尔扎斯卡水坝")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/02_韦尔扎斯卡水坝" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/03_马贾谷与福罗利奥瀑布")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/03_马贾谷与福罗利奥瀑布" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/04_莫尼奥圣约翰教堂（博塔设计）")) { New-Item -ItemType Directory -Force -Path "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/04_莫尼奥圣约翰教堂（博塔设计）" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/03_贝林佐纳")) { New-Item -ItemType Directory -Force -Path "05_提契诺/03_贝林佐纳" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/03_贝林佐纳/01_贝林佐纳三城堡")) { New-Item -ItemType Directory -Force -Path "05_提契诺/03_贝林佐纳/01_贝林佐纳三城堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/03_贝林佐纳/02_塔马罗山＋博塔教堂")) { New-Item -ItemType Directory -Force -Path "05_提契诺/03_贝林佐纳/02_塔马罗山＋博塔教堂" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/04_提契诺周边与沿途")) { New-Item -ItemType Directory -Force -Path "05_提契诺/04_提契诺周边与沿途" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "05_提契诺/04_提契诺周边与沿途/01_圣哥达山口")) { New-Item -ItemType Directory -Force -Path "05_提契诺/04_提契诺周边与沿途/01_圣哥达山口" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦市区")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/01_日内瓦市区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦市区/01_大喷泉")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/01_日内瓦市区/01_大喷泉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦市区/02_日内瓦老城")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/01_日内瓦市区/02_日内瓦老城" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦市区/02_日内瓦老城/01_圣皮埃尔大教堂")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/01_日内瓦市区/02_日内瓦老城/01_圣皮埃尔大教堂" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦市区/02_日内瓦老城/02_宗教改革纪念墙")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/01_日内瓦市区/02_日内瓦老城/02_宗教改革纪念墙" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦市区/03_万国宫")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/01_日内瓦市区/03_万国宫" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦市区/04_欧洲核子研究中心 CERN")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/01_日内瓦市区/04_欧洲核子研究中心 CERN" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑市区")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/02_洛桑市区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑市区/01_洛桑大教堂")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/02_洛桑市区/01_洛桑大教堂" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑市区/02_奥林匹克博物馆")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/02_洛桑市区/02_奥林匹克博物馆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑市区/03_乌希湖畔")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/02_洛桑市区/03_乌希湖畔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑市区/04_劳力士学习中心")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/02_洛桑市区/04_劳力士学习中心" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/03_蒙特勒与拉沃")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/03_蒙特勒与拉沃" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/03_蒙特勒与拉沃/01_梯田葡萄园步道")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/03_蒙特勒与拉沃/01_梯田葡萄园步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/03_蒙特勒与拉沃/02_西庸城堡")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/03_蒙特勒与拉沃/02_西庸城堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/03_蒙特勒与拉沃/03_湖畔步道与墨丘利雕像")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/03_蒙特勒与拉沃/03_湖畔步道与墨丘利雕像" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/03_蒙特勒与拉沃/04_蒙特勒圣诞市集")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/03_蒙特勒与拉沃/04_蒙特勒圣诞市集" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/03_蒙特勒与拉沃/05_纳伊岩铁路与土拨鼠园")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/03_蒙特勒与拉沃/05_纳伊岩铁路与土拨鼠园" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/03_蒙特勒与拉沃/06_卓别林世界")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/03_蒙特勒与拉沃/06_卓别林世界" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/03_蒙特勒与拉沃/07_湖边小屋（勒·柯布西耶）")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/03_蒙特勒与拉沃/07_湖边小屋（勒·柯布西耶）" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/04_格吕耶尔与布罗克")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/04_格吕耶尔与布罗克" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/04_格吕耶尔与布罗克/01_格吕耶尔古堡与小镇")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/04_格吕耶尔与布罗克/01_格吕耶尔古堡与小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/04_格吕耶尔与布罗克/02_格吕耶尔奶酪工坊")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/04_格吕耶尔与布罗克/02_格吕耶尔奶酪工坊" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/04_格吕耶尔与布罗克/03_Cailler 巧克力工厂")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/04_格吕耶尔与布罗克/03_Cailler 巧克力工厂" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/05_日内瓦湖区周边与沿途")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/05_日内瓦湖区周边与沿途" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "06_日内瓦湖区/05_日内瓦湖区周边与沿途/01_冰川 3000 与峰顶吊桥")) { New-Item -ItemType Directory -Force -Path "06_日内瓦湖区/05_日内瓦湖区周边与沿途/01_冰川 3000 与峰顶吊桥" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世市区")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/01_苏黎世市区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/01_苏黎世老城与班霍夫大街")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/01_苏黎世老城与班霍夫大街" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/01_苏黎世老城与班霍夫大街/01_苏黎世大教堂")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/01_苏黎世老城与班霍夫大街/01_苏黎世大教堂" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/01_苏黎世老城与班霍夫大街/02_圣母大教堂")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/01_苏黎世老城与班霍夫大街/02_圣母大教堂" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/02_于特利山")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/02_于特利山" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/03_瑞士国家博物馆")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/03_瑞士国家博物馆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/04_瑞士莲巧克力之家")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/04_瑞士莲巧克力之家" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/05_勒·柯布西耶馆")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/05_勒·柯布西耶馆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/02_沙夫豪森与莱茵瀑布")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/02_沙夫豪森与莱茵瀑布" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/02_沙夫豪森与莱茵瀑布/01_莱茵瀑布与劳芬城堡")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/02_沙夫豪森与莱茵瀑布/01_莱茵瀑布与劳芬城堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/02_沙夫豪森与莱茵瀑布/02_沙夫豪森 Munot 城堡")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/02_沙夫豪森与莱茵瀑布/02_沙夫豪森 Munot 城堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/02_沙夫豪森与莱茵瀑布/03_施泰因阿姆莱茵")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/02_沙夫豪森与莱茵瀑布/03_施泰因阿姆莱茵" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/01_阿彭策尔小镇")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/01_阿彭策尔小镇" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/02_森蒂斯山")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/02_森蒂斯山" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/03_埃本阿尔卑与崖壁客栈")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/03_埃本阿尔卑与崖壁客栈" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/04_西阿尔卑湖")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/04_西阿尔卑湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/05_圣加仑修道院图书馆")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/05_圣加仑修道院图书馆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/04_瓦伦湖与托根堡")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/04_瓦伦湖与托根堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/04_瓦伦湖与托根堡/01_瓦伦湖")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/04_瓦伦湖与托根堡/01_瓦伦湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/04_瓦伦湖与托根堡/02_沙瑟鲁格")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/04_瓦伦湖与托根堡/02_沙瑟鲁格" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/05_列支敦士登")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/05_列支敦士登" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/05_列支敦士登/01_瓦杜兹城堡")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/05_列支敦士登/01_瓦杜兹城堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/05_列支敦士登/02_瓦杜兹市区与邮票博物馆")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/05_列支敦士登/02_瓦杜兹市区与邮票博物馆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/05_列支敦士登/03_王子步道")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/05_列支敦士登/03_王子步道" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/06_东北部周边与沿途")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/06_东北部周边与沿途" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/06_东北部周边与沿途/01_巴登 FORTYSEVEN 温泉")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/06_东北部周边与沿途/01_巴登 FORTYSEVEN 温泉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/06_东北部周边与沿途/02_博登湖")) { New-Item -ItemType Directory -Force -Path "07_苏黎世、东北部与列支敦士登/06_东北部周边与沿途/02_博登湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼市区")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/01_伯尔尼市区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/01_伯尔尼钟楼")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/01_伯尔尼钟楼" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/02_熊公园")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/02_熊公园" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/03_联邦大厦")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/03_联邦大厦" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/04_爱因斯坦故居")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/04_爱因斯坦故居" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼市区/02_玫瑰园")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/01_伯尔尼市区/02_玫瑰园" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼市区/03_保罗·克利中心")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/01_伯尔尼市区/03_保罗·克利中心" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/02_巴塞尔市区")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/02_巴塞尔市区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城/01_巴塞尔大教堂")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城/01_巴塞尔大教堂" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城/02_莱茵河渡船与夏季漂流")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城/02_莱茵河渡船与夏季漂流" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城/03_巴塞尔圣诞市集")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城/03_巴塞尔圣诞市集" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/02_巴塞尔市区/02_贝耶勒基金会")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/02_巴塞尔市区/02_贝耶勒基金会" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/02_巴塞尔市区/03_巴塞尔美术馆")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/02_巴塞尔市区/03_巴塞尔美术馆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/02_巴塞尔市区/04_巴塞尔狂欢节")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/02_巴塞尔市区/04_巴塞尔狂欢节" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/03_汝拉与三湖区")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/03_汝拉与三湖区" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/03_汝拉与三湖区/01_范湖穹")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/03_汝拉与三湖区/01_范湖穹" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/03_汝拉与三湖区/02_拉绍德封与力洛克")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/03_汝拉与三湖区/02_拉绍德封与力洛克" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/03_汝拉与三湖区/03_圣于尔桑")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/03_汝拉与三湖区/03_圣于尔桑" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/03_汝拉与三湖区/04_穆尔滕古城")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/03_汝拉与三湖区/04_穆尔滕古城" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/03_汝拉与三湖区/05_伊韦尔东温泉")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/03_汝拉与三湖区/05_伊韦尔东温泉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/04_西北部周边与沿途")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/04_西北部周边与沿途" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/04_西北部周边与沿途/01_木廊桥与农庄")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/04_西北部周边与沿途/01_木廊桥与农庄" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "08_首都与西北部/04_西北部周边与沿途/02_维特拉设计园")) { New-Item -ItemType Directory -Force -Path "08_首都与西北部/04_西北部周边与沿途/02_维特拉设计园" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步")) { New-Item -ItemType Directory -Force -Path "09_长线徒步" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/01_第 1 段 · 加夫莱（列支敦士登）→ 萨尔甘斯")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/01_第 1 段 · 加夫莱（列支敦士登）→ 萨尔甘斯" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/02_第 2 段 · 萨尔甘斯 → 魏斯坦嫩")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/02_第 2 段 · 萨尔甘斯 → 魏斯坦嫩" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/03_第 3 段 · 魏斯坦嫩 → 埃尔姆")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/03_第 3 段 · 魏斯坦嫩 → 埃尔姆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/04_第 4 段 · 埃尔姆 → 林塔尔")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/04_第 4 段 · 埃尔姆 → 林塔尔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/05_第 5 段 · 林塔尔 → 乌尔纳博登")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/05_第 5 段 · 林塔尔 → 乌尔纳博登" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/06_第 6 段 · 乌尔纳博登 → 阿尔特多夫")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/06_第 6 段 · 乌尔纳博登 → 阿尔特多夫" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/07_第 7 段 · 阿尔特多夫 → 英格堡")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/07_第 7 段 · 阿尔特多夫 → 英格堡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/08_第 8 段 · 英格堡 → 恩斯特伦阿尔卑")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/08_第 8 段 · 英格堡 → 恩斯特伦阿尔卑" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/09_第 9 段 · 恩斯特伦阿尔卑 → 迈林根")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/09_第 9 段 · 恩斯特伦阿尔卑 → 迈林根" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/10_第 10 段 · 迈林根 → 格林德瓦")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/10_第 10 段 · 迈林根 → 格林德瓦" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/11_第 11 段 · 格林德瓦 → 劳特布龙嫩")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/11_第 11 段 · 格林德瓦 → 劳特布龙嫩" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/12_第 12 段 · 劳特布龙嫩 → 格里斯阿尔卑")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/12_第 12 段 · 劳特布龙嫩 → 格里斯阿尔卑" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/13_第 13 段 · 格里斯阿尔卑 → 坎德施泰格")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/13_第 13 段 · 格里斯阿尔卑 → 坎德施泰格" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/14_第 14 段 · 坎德施泰格 → 阿德尔博登")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/14_第 14 段 · 坎德施泰格 → 阿德尔博登" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/15_第 15 段 · 阿德尔博登 → 伦克")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/15_第 15 段 · 阿德尔博登 → 伦克" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/16_第 16 段 · 伦克 → 格施塔德")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/16_第 16 段 · 伦克 → 格施塔德" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/17_第 17 段 · 格施塔德 → 莱蒂瓦")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/17_第 17 段 · 格施塔德 → 莱蒂瓦" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/18_第 18–19 段 · 莱蒂瓦 → 罗西尼耶尔 → 纳伊岩")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/18_第 18–19 段 · 莱蒂瓦 → 罗西尼耶尔 → 纳伊岩" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/01_Via Alpina 全程/19_第 20 段 · 纳伊岩 → 蒙特勒")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/01_Via Alpina 全程/19_第 20 段 · 纳伊岩 → 蒙特勒" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/01_第 1 段 · 夏蒙尼 → 阿让蒂耶尔")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/01_第 1 段 · 夏蒙尼 → 阿让蒂耶尔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/02_第 2 段 · 阿让蒂耶尔 → 特里安")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/02_第 2 段 · 阿让蒂耶尔 → 特里安" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/03_第 3 段 · 特里安 → 尚佩")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/03_第 3 段 · 特里安 → 尚佩" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/04_第 4 段 · 尚佩 → 勒沙布勒")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/04_第 4 段 · 尚佩 → 勒沙布勒" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/05_第 5 段 · 勒沙布勒 → 蒙福小屋")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/05_第 5 段 · 勒沙布勒 → 蒙福小屋" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/06_第 6 段 · 蒙福小屋 → 普拉弗勒里小屋")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/06_第 6 段 · 蒙福小屋 → 普拉弗勒里小屋" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/07_第 7 段 · 普拉弗勒里小屋 → 阿罗拉")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/07_第 7 段 · 普拉弗勒里小屋 → 阿罗拉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/08_第 8 段 · 阿罗拉 → 莱奥代尔")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/08_第 8 段 · 阿罗拉 → 莱奥代尔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/09_第 9 段 · 莱奥代尔 → 莫伊里湖")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/09_第 9 段 · 莱奥代尔 → 莫伊里湖" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/10_第 10 段 · 莫伊里湖 → 齐纳尔")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/10_第 10 段 · 莫伊里湖 → 齐纳尔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/11_第 11 段 · 齐纳尔 → 格鲁本")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/11_第 11 段 · 齐纳尔 → 格鲁本" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/12_第 12 段 · 格鲁本 → 圣尼克劳斯")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/12_第 12 段 · 格鲁本 → 圣尼克劳斯" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/13_第 13 段 · 圣尼克劳斯 → 欧罗巴小屋")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/13_第 13 段 · 圣尼克劳斯 → 欧罗巴小屋" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "09_长线徒步/02_瑞士高山之路 Haute Route/14_第 14 段 · 欧罗巴小屋 → 采尔马特")) { New-Item -ItemType Directory -Force -Path "09_长线徒步/02_瑞士高山之路 Haute Route/14_第 14 段 · 欧罗巴小屋 → 采尔马特" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "10_全景列车")) { New-Item -ItemType Directory -Force -Path "10_全景列车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "10_全景列车/01_冰川快车")) { New-Item -ItemType Directory -Force -Path "10_全景列车/01_冰川快车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "10_全景列车/02_伯尔尼纳快车")) { New-Item -ItemType Directory -Force -Path "10_全景列车/02_伯尔尼纳快车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "10_全景列车/03_黄金山口快车")) { New-Item -ItemType Directory -Force -Path "10_全景列车/03_黄金山口快车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "10_全景列车/04_圣哥达全景快车")) { New-Item -ItemType Directory -Force -Path "10_全景列车/04_圣哥达全景快车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "10_全景列车/05_沃拉尔普快车")) { New-Item -ItemType Directory -Force -Path "10_全景列车/05_沃拉尔普快车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "10_全景列车/06_勃朗峰快车")) { New-Item -ItemType Directory -Force -Path "10_全景列车/06_勃朗峰快车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/01_齿轨铁路")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/01_齿轨铁路" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/02_缆索铁路")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/02_缆索铁路" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/03_空中缆车")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/03_空中缆车" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/04_吊厢")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/04_吊厢" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/05_吊椅")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/05_吊椅" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/06_瑞士通票")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/06_瑞士通票" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/07_瑞士半价卡")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/07_瑞士半价卡" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/08_少女峰通票")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/08_少女峰通票" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/09_伯尔尼高地通票")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/09_伯尔尼高地通票" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/10_琉森旅行通票")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/10_琉森旅行通票" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/11_勃朗峰多日通票")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/11_勃朗峰多日通票" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/12_检修停运期说明")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/12_检修停运期说明" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "11_山地交通与通票/13_FlixBus 长途巴士")) { New-Item -ItemType Directory -Force -Path "11_山地交通与通票/13_FlixBus 长途巴士" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产")) { New-Item -ItemType Directory -Force -Path "12_美食与特产" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产/01_芝士火锅")) { New-Item -ItemType Directory -Force -Path "12_美食与特产/01_芝士火锅" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产/02_烤奶酪 Raclette")) { New-Item -ItemType Directory -Force -Path "12_美食与特产/02_烤奶酪 Raclette" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产/03_苏黎世小牛肉")) { New-Item -ItemType Directory -Force -Path "12_美食与特产/03_苏黎世小牛肉" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产/04_土豆饼 Rösti")) { New-Item -ItemType Directory -Force -Path "12_美食与特产/04_土豆饼 Rösti" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产/05_格劳宾登大麦汤")) { New-Item -ItemType Directory -Force -Path "12_美食与特产/05_格劳宾登大麦汤" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产/06_恩加丁坚果塔")) { New-Item -ItemType Directory -Force -Path "12_美食与特产/06_恩加丁坚果塔" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产/07_栗子蛋糕 Vermicelles")) { New-Item -ItemType Directory -Force -Path "12_美食与特产/07_栗子蛋糕 Vermicelles" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产/08_瑞士巧克力")) { New-Item -ItemType Directory -Force -Path "12_美食与特产/08_瑞士巧克力" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "12_美食与特产/09_葡萄酒")) { New-Item -ItemType Directory -Force -Path "12_美食与特产/09_葡萄酒" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物")) { New-Item -ItemType Directory -Force -Path "13_野生动植物" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/01_阿尔卑斯旱獭")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/01_阿尔卑斯旱獭" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/02_阿尔卑斯羱羊")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/02_阿尔卑斯羱羊" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/03_岩羚羊")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/03_岩羚羊" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/04_胡兀鹫")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/04_胡兀鹫" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/05_金雕")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/05_金雕" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/06_黄嘴山鸦")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/06_黄嘴山鸦" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/07_马鹿")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/07_马鹿" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/08_岩雷鸟")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/08_岩雷鸟" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/09_瓦莱黑鼻羊")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/09_瓦莱黑鼻羊" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/10_雪绒花")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/10_雪绒花" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/11_龙胆")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/11_龙胆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/12_高山杜鹃")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/12_高山杜鹃" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/13_瑞士五针松")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/13_瑞士五针松" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/14_欧洲落叶松")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/14_欧洲落叶松" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/15_番红花")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/15_番红花" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/16_高山白头翁")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/16_高山白头翁" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/17_黄龙胆")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/17_黄龙胆" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "13_野生动植物/18_野生水仙")) { New-Item -ItemType Directory -Force -Path "13_野生动植物/18_野生水仙" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/01_U形谷")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/01_U形谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/02_悬谷与瀑布")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/02_悬谷与瀑布" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/03_冰碛")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/03_冰碛" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/04_冰川退缩")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/04_冰川退缩" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/05_喀斯特与溶沟")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/05_喀斯特与溶沟" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/06_山崩")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/06_山崩" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/07_峡谷")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/07_峡谷" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/08_推覆构造")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/08_推覆构造" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/09_汝拉褶皱山")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/09_汝拉褶皱山" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/10_永久冻土")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/10_永久冻土" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/11_片麻岩")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/11_片麻岩" | Out-Null; $made++ }
if (-not (Test-Path -LiteralPath "14_地质与地貌/12_冰湖")) { New-Item -ItemType Directory -Force -Path "14_地质与地貌/12_冰湖" | Out-Null; $made++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/01_因特拉肯") { Get-ChildItem -LiteralPath "01_伯尔尼高地/01_因特拉肯" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/01_因特拉肯/01_何维克街与何维克草坪") { Get-ChildItem -LiteralPath "01_伯尔尼高地/01_因特拉肯/01_何维克街与何维克草坪" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/01_何维克街与何维克草坪" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/01_因特拉肯/02_哈德昆姆") { Get-ChildItem -LiteralPath "01_伯尔尼高地/01_因特拉肯/02_哈德昆姆" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/02_哈德昆姆" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/01_因特拉肯/03_希尼格普拉特＋高山植物园") { Get-ChildItem -LiteralPath "01_伯尔尼高地/01_因特拉肯/03_希尼格普拉特＋高山植物园" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/03_希尼格普拉特＋高山植物园" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/01_因特拉肯/04_图恩湖、布里恩茨湖游船") { Get-ChildItem -LiteralPath "01_伯尔尼高地/01_因特拉肯/04_图恩湖、布里恩茨湖游船" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/01_因特拉肯/04_图恩湖与布里恩茨湖游船" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/02_格林德瓦") { Get-ChildItem -LiteralPath "01_伯尔尼高地/02_格林德瓦" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/02_格林德瓦/01_菲斯特与悬崖步道") { Get-ChildItem -LiteralPath "01_伯尔尼高地/02_格林德瓦/01_菲斯特与悬崖步道" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/01_菲斯特与悬崖步道" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/02_格林德瓦/02_巴赫阿尔卑湖") { Get-ChildItem -LiteralPath "01_伯尔尼高地/02_格林德瓦/02_巴赫阿尔卑湖" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/02_巴赫阿尔卑湖" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/02_格林德瓦/03_艾格快线") { Get-ChildItem -LiteralPath "01_伯尔尼高地/02_格林德瓦/03_艾格快线" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/03_艾格快线" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/02_格林德瓦/04_曼利兴–小沙伊德格全景步道") { Get-ChildItem -LiteralPath "01_伯尔尼高地/02_格林德瓦/04_曼利兴–小沙伊德格全景步道" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/04_曼利兴–小沙伊德格全景步道" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/02_格林德瓦/05_格林德瓦雪场") { Get-ChildItem -LiteralPath "01_伯尔尼高地/02_格林德瓦/05_格林德瓦雪场" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/02_格林德瓦/05_格林德瓦雪场" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/03_少女峰") { Get-ChildItem -LiteralPath "01_伯尔尼高地/03_少女峰" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/03_少女峰/01_少女峰铁路") { Get-ChildItem -LiteralPath "01_伯尔尼高地/03_少女峰/01_少女峰铁路" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰/01_少女峰铁路" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/03_少女峰/02_斯芬克斯观景台、冰宫") { Get-ChildItem -LiteralPath "01_伯尔尼高地/03_少女峰/02_斯芬克斯观景台、冰宫" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰/02_斯芬克斯观景台、冰宫" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/03_少女峰/03_艾格北壁步道") { Get-ChildItem -LiteralPath "01_伯尔尼高地/03_少女峰/03_艾格北壁步道" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/03_少女峰/03_艾格北壁步道" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/04_劳特布龙嫩与文根") { Get-ChildItem -LiteralPath "01_伯尔尼高地/04_劳特布龙嫩与文根" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/04_劳特布龙嫩与文根/01_施陶河瀑布") { Get-ChildItem -LiteralPath "01_伯尔尼高地/04_劳特布龙嫩与文根/01_施陶河瀑布" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/01_施陶河瀑布" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/04_劳特布龙嫩与文根/02_特吕默尔巴赫瀑布") { Get-ChildItem -LiteralPath "01_伯尔尼高地/04_劳特布龙嫩与文根/02_特吕默尔巴赫瀑布" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/02_特吕默尔巴赫瀑布" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/04_劳特布龙嫩与文根/03_文根小镇") { Get-ChildItem -LiteralPath "01_伯尔尼高地/04_劳特布龙嫩与文根/03_文根小镇" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/03_文根小镇" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/05_米伦与雪朗峰/01_米伦小镇") { Get-ChildItem -LiteralPath "01_伯尔尼高地/05_米伦与雪朗峰/01_米伦小镇" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/04_米伦小镇" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/05_米伦与雪朗峰/02_雪朗峰 Piz Gloria") { Get-ChildItem -LiteralPath "01_伯尔尼高地/05_米伦与雪朗峰/02_雪朗峰 Piz Gloria" -File | Move-Item -Destination "01_伯尔尼高地/01_少女峰与因特拉肯地区/04_劳特布龙嫩谷/05_雪朗峰 Piz Gloria" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖") { Get-ChildItem -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖" -File | Move-Item -Destination "01_伯尔尼高地/02_图恩湖与布里恩茨湖" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/01_图恩城堡") { Get-ChildItem -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/01_图恩城堡" -File | Move-Item -Destination "01_伯尔尼高地/02_图恩湖与布里恩茨湖/01_图恩城堡" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/02_施皮茨") { Get-ChildItem -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/02_施皮茨" -File | Move-Item -Destination "01_伯尔尼高地/02_图恩湖与布里恩茨湖/02_施皮茨" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/03_尼森山") { Get-ChildItem -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/03_尼森山" -File | Move-Item -Destination "01_伯尔尼高地/02_图恩湖与布里恩茨湖/03_尼森山" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/04_伊瑟尔瓦尔德码头") { Get-ChildItem -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/04_伊瑟尔瓦尔德码头" -File | Move-Item -Destination "01_伯尔尼高地/02_图恩湖与布里恩茨湖/04_伊瑟尔瓦尔德码头" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/05_布里恩茨木雕村") { Get-ChildItem -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/05_布里恩茨木雕村" -File | Move-Item -Destination "01_伯尔尼高地/02_图恩湖与布里恩茨湖/05_布里恩茨木雕村" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/06_布里恩茨罗特洪蒸汽齿轨") { Get-ChildItem -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/06_布里恩茨罗特洪蒸汽齿轨" -File | Move-Item -Destination "01_伯尔尼高地/02_图恩湖与布里恩茨湖/06_布里恩茨罗特洪蒸汽齿轨" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/07_巴伦贝格露天博物馆") { Get-ChildItem -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/07_巴伦贝格露天博物馆" -File | Move-Item -Destination "01_伯尔尼高地/02_图恩湖与布里恩茨湖/07_巴伦贝格露天博物馆" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/08_迈林根·阿勒峡谷、莱辛巴赫瀑布") { Get-ChildItem -LiteralPath "01_伯尔尼高地/06_图恩湖与布里恩茨湖/08_迈林根·阿勒峡谷、莱辛巴赫瀑布" -File | Move-Item -Destination "01_伯尔尼高地/02_图恩湖与布里恩茨湖/08_迈林根·阿勒峡谷、莱辛巴赫瀑布" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登" -File | Move-Item -Destination "01_伯尔尼高地/03_坎德施泰格与阿德尔博登" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/01_厄希嫩湖") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/01_厄希嫩湖" -File | Move-Item -Destination "01_伯尔尼高地/03_坎德施泰格与阿德尔博登/01_厄希嫩湖" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/02_蓝湖") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/02_蓝湖" -File | Move-Item -Destination "01_伯尔尼高地/03_坎德施泰格与阿德尔博登/02_蓝湖" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/03_恩斯特利根瀑布") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/03_恩斯特利根瀑布" -File | Move-Item -Destination "01_伯尔尼高地/03_坎德施泰格与阿德尔博登/03_恩斯特利根瀑布" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/08_格施塔德") { Get-ChildItem -LiteralPath "01_伯尔尼高地/08_格施塔德" -File | Move-Item -Destination "01_伯尔尼高地/04_格施塔德" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/08_格施塔德/01_格施塔德小镇") { Get-ChildItem -LiteralPath "01_伯尔尼高地/08_格施塔德/01_格施塔德小镇" -File | Move-Item -Destination "01_伯尔尼高地/04_格施塔德/01_格施塔德小镇" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/08_格施塔德/02_劳埃嫩湖") { Get-ChildItem -LiteralPath "01_伯尔尼高地/08_格施塔德/02_劳埃嫩湖" -File | Move-Item -Destination "01_伯尔尼高地/04_格施塔德/02_劳埃嫩湖" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/01_采尔马特小镇") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/01_采尔马特小镇" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/01_采尔马特小镇" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/02_马特洪峰") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/02_马特洪峰" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/02_马特洪峰" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/03_戈尔内格拉特铁路") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/03_戈尔内格拉特铁路" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/03_戈尔内格拉特铁路" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/04_马特洪冰川天堂") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/04_马特洪冰川天堂" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/04_马特洪冰川天堂" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/05_苏内加与五湖步道") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/05_苏内加与五湖步道" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/05_苏内加与五湖步道" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/06_里菲尔湖倒影") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/06_里菲尔湖倒影" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/06_里菲尔湖倒影" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/07_黑湖") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/07_黑湖" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/07_黑湖" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/08_高巴尔门步道") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/08_高巴尔门步道" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/08_高巴尔门步道" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/09_采尔马特雪场（含夏季冰川滑雪、跨境切尔维尼亚）") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/09_采尔马特雪场（含夏季冰川滑雪、跨境切尔维尼亚）" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/09_采尔马特雪场" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/11_蒙特罗莎山屋") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/11_蒙特罗莎山屋" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/01_马特洪峰地区/10_蒙特罗莎山屋" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/04_罗讷河谷" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/01_锡永 Valère·Tourbillon 城堡") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/01_锡永 Valère·Tourbillon 城堡" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/04_罗讷河谷/01_锡永瓦莱尔与图尔比永城堡" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/02_瓦莱葡萄酒") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/02_瓦莱葡萄酒" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/04_罗讷河谷/02_瓦莱葡萄酒" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/03_洛伊克巴德温泉") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/03_洛伊克巴德温泉" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/04_罗讷河谷/03_洛伊克巴德温泉" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/04_葛米山口") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/04_葛米山口" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/04_罗讷河谷/04_葛米山口" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/05_马蒂尼与大圣伯纳德/02_韦尔比耶雪场") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/05_马蒂尼与大圣伯纳德/02_韦尔比耶雪场" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/05_瓦莱滑雪胜地/01_韦尔比耶雪场" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/05_克兰-蒙塔纳雪场") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/04_锡永与洛伊克巴德/05_克兰-蒙塔纳雪场" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/05_瓦莱滑雪胜地/02_克兰-蒙塔纳雪场" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/01_夏蒙尼小镇") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/01_夏蒙尼小镇" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/01_夏蒙尼小镇" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/02_南针峰") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/02_南针峰" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/02_南针峰" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/03_蒙唐维尔铁路与冰海冰川") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/03_蒙唐维尔铁路与冰海冰川" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/03_蒙唐维尔铁路与冰海冰川" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/04_白湖") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/04_白湖" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/04_白湖" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/05_北阳台步道") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/05_北阳台步道" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/05_北阳台步道" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/06_布雷文") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/06_布雷文" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/06_布雷文" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/07_白谷冰川野雪") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/07_白谷冰川野雪" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/07_白谷冰川野雪" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/08_夏蒙尼雪场") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/08_夏蒙尼雪场" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/01_夏蒙尼/08_夏蒙尼雪场" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/10_库马约尔小镇") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/10_库马约尔小镇" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/01_库马约尔小镇" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/11_勃朗峰天空之路") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/11_勃朗峰天空之路" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/02_勃朗峰天空之路" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/12_意大利段费雷谷") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/12_意大利段费雷谷" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/03_意大利段费雷谷" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/13_奥斯塔罗马古城") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/13_奥斯塔罗马古城" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/02_库马约尔与奥斯塔/04_奥斯塔罗马古城" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/14_尚佩湖") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/14_尚佩湖" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/03_尚佩与瑞士费雷谷/01_尚佩湖" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/15_瑞士段费雷谷") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/15_瑞士段费雷谷" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/03_尚佩与瑞士费雷谷/02_瑞士段费雷谷" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/01_第1段 莱乌什 → 莱孔塔米讷") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/01_第1段 莱乌什 → 莱孔塔米讷" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/01_第 1 段 · 莱乌什 → 莱孔塔米讷" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/02_第2段 莱孔塔米讷 → 博诺姆十字架小屋") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/02_第2段 莱孔塔米讷 → 博诺姆十字架小屋" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/02_第 2 段 · 莱孔塔米讷 → 博诺姆十字架小屋" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/03_第3段 博诺姆十字架 → 伊丽莎白小屋") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/03_第3段 博诺姆十字架 → 伊丽莎白小屋" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/03_第 3 段 · 博诺姆十字架 → 伊丽莎白小屋" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/04_第4段 伊丽莎白小屋 → 库马约尔") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/04_第4段 伊丽莎白小屋 → 库马约尔" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/04_第 4 段 · 伊丽莎白小屋 → 库马约尔" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/05_第5段 库马约尔 → 博纳蒂小屋") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/05_第5段 库马约尔 → 博纳蒂小屋" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/05_第 5 段 · 库马约尔 → 博纳蒂小屋" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/06_第6段 博纳蒂小屋 → 拉富利") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/06_第6段 博纳蒂小屋 → 拉富利" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/06_第 6 段 · 博纳蒂小屋 → 拉富利" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/07_第7段 拉富利 → 尚佩") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/07_第7段 拉富利 → 尚佩" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/07_第 7 段 · 拉富利 → 尚佩" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/08_第8段 尚佩 → 特里安") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/08_第8段 尚佩 → 特里安" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/08_第 8 段 · 尚佩 → 特里安" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/09_第9段 特里安 → 特雷勒尚") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/09_第9段 特里安 → 特雷勒尚" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/09_第 9 段 · 特里安 → 特雷勒尚" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/10_第10段 特雷勒尚 → 拉弗雷热尔") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/10_第10段 特雷勒尚 → 拉弗雷热尔" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/10_第 10 段 · 特雷勒尚 → 拉弗雷热尔" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/11_第11段 拉弗雷热尔 → 莱乌什") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/06_勃朗峰区域/09_环勃朗峰徒步 TMB/11_第11段 拉弗雷热尔 → 莱乌什" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/06_勃朗峰地区/04_环勃朗峰徒步 TMB/11_第 11 段 · 拉弗雷热尔 → 莱乌什" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/05_马蒂尼与大圣伯纳德/01_大圣伯纳德山口、修道院与圣伯纳犬") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/05_马蒂尼与大圣伯纳德/01_大圣伯纳德山口、修道院与圣伯纳犬" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途/01_大圣伯纳德山口、修道院与圣伯纳犬" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/05_马蒂尼与大圣伯纳德/03_拉韦莱班温泉") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/05_马蒂尼与大圣伯纳德/03_拉韦莱班温泉" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途/02_拉韦莱班温泉" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/05_马蒂尼与大圣伯纳德/04_萨永温泉") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/05_马蒂尼与大圣伯纳德/04_萨永温泉" -File | Move-Item -Destination "02_瓦莱州与勃朗峰/07_瓦莱周边与沿途/03_萨永温泉" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森城") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/01_琉森城" -File | Move-Item -Destination "03_琉森与瑞士中部/01_琉森市区" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森城/01_琉森老城") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/01_琉森城/01_琉森老城" -File | Move-Item -Destination "03_琉森与瑞士中部/01_琉森市区/01_琉森老城" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森城/01_琉森老城/01_卡佩尔廊桥") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/01_琉森城/01_琉森老城/01_卡佩尔廊桥" -File | Move-Item -Destination "03_琉森与瑞士中部/01_琉森市区/01_琉森老城/01_卡佩尔廊桥" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森城/01_琉森老城/02_狮子纪念碑") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/01_琉森城/01_琉森老城/02_狮子纪念碑" -File | Move-Item -Destination "03_琉森与瑞士中部/01_琉森市区/01_琉森老城/02_狮子纪念碑" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森城/02_瑞士交通博物馆") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/01_琉森城/02_瑞士交通博物馆" -File | Move-Item -Destination "03_琉森与瑞士中部/01_琉森市区/02_瑞士交通博物馆" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森城/04_琉森文化会议中心 KKL") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/01_琉森城/04_琉森文化会议中心 KKL" -File | Move-Item -Destination "03_琉森与瑞士中部/01_琉森市区/03_琉森文化会议中心 KKL" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/02_瑞吉山") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/02_瑞吉山" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/02_瑞吉山/01_瑞吉铁路（欧洲第一条齿轨）") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/02_瑞吉山/01_瑞吉铁路（欧洲第一条齿轨）" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山/01_瑞吉铁路" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/02_瑞吉山/02_瑞吉卡尔特巴德温泉") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/02_瑞吉山/02_瑞吉卡尔特巴德温泉" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山/02_瑞吉卡尔特巴德温泉" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/02_瑞吉山/03_全景步道") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/02_瑞吉山/03_全景步道" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/01_瑞吉山/03_瑞吉全景步道" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/03_皮拉图斯山") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/03_皮拉图斯山" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/02_皮拉图斯山" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/03_皮拉图斯山/01_皮拉图斯铁路（世界最陡齿轨，仅夏季）") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/03_皮拉图斯山/01_皮拉图斯铁路（世界最陡齿轨，仅夏季）" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/02_皮拉图斯山/01_皮拉图斯铁路" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/03_皮拉图斯山/02_龙之路") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/03_皮拉图斯山/02_龙之路" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/02_皮拉图斯山/02_龙之路" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/05_施坦塞峰与比尔根施托克") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/05_施坦塞峰与比尔根施托克" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/05_施坦塞峰与比尔根施托克/01_施坦塞峰双层敞篷缆车") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/05_施坦塞峰与比尔根施托克/01_施坦塞峰双层敞篷缆车" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克/01_施坦塞峰双层敞篷缆车" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/05_施坦塞峰与比尔根施托克/02_比尔根施托克悬崖步道与哈默施万德电梯") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/05_施坦塞峰与比尔根施托克/02_比尔根施托克悬崖步道与哈默施万德电梯" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克/02_比尔根施托克悬崖步道与哈默施万德电梯" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/05_施坦塞峰与比尔根施托克/03_布尔根施托克高山水疗") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/05_施坦塞峰与比尔根施托克/03_布尔根施托克高山水疗" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/03_施坦塞峰与比尔根施托克/03_布尔根施托克高山水疗" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/06_斯托斯与退尔故乡") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/06_斯托斯与退尔故乡" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/06_斯托斯与退尔故乡/01_斯托斯缆索铁路（世界最陡）") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/06_斯托斯与退尔故乡/01_斯托斯缆索铁路（世界最陡）" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利/01_斯托斯缆索铁路" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/06_斯托斯与退尔故乡/02_斯托斯山脊步道") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/06_斯托斯与退尔故乡/02_斯托斯山脊步道" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利/02_斯托斯山脊步道" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/06_斯托斯与退尔故乡/03_吕特利草地") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/06_斯托斯与退尔故乡/03_吕特利草地" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/04_斯托斯与吕特利/03_吕特利草地" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/01_琉森城/03_琉森湖游船") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/01_琉森城/03_琉森湖游船" -File | Move-Item -Destination "03_琉森与瑞士中部/02_琉森湖区/05_琉森湖游船" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡" -File | Move-Item -Destination "03_琉森与瑞士中部/03_铁力士与英格堡" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡/01_英格堡修道院") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡/01_英格堡修道院" -File | Move-Item -Destination "03_琉森与瑞士中部/03_铁力士与英格堡/01_英格堡修道院" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡/02_铁力士旋转缆车") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡/02_铁力士旋转缆车" -File | Move-Item -Destination "03_琉森与瑞士中部/03_铁力士与英格堡/02_铁力士旋转缆车" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡/03_特吕布湖") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡/03_特吕布湖" -File | Move-Item -Destination "03_琉森与瑞士中部/03_铁力士与英格堡/03_特吕布湖" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡/04_英格堡雪场") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/04_铁力士与英格堡/04_英格堡雪场" -File | Move-Item -Destination "03_琉森与瑞士中部/03_铁力士与英格堡/04_英格堡雪场" -Force; $moved++ }
if (Test-Path -LiteralPath "03_琉森与瑞士中部/03_皮拉图斯山/03_施拉滕弗卢喀斯特徒步") { Get-ChildItem -LiteralPath "03_琉森与瑞士中部/03_皮拉图斯山/03_施拉滕弗卢喀斯特徒步" -File | Move-Item -Destination "03_琉森与瑞士中部/04_琉森周边与沿途/01_施拉滕弗卢喀斯特徒步" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁") { Get-ChildItem -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/01_圣莫里茨小镇与湖") { Get-ChildItem -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/01_圣莫里茨小镇与湖" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/01_圣莫里茨小镇与湖" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/02_科尔瓦奇") { Get-ChildItem -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/02_科尔瓦奇" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/02_科尔瓦奇" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/03_穆奥塔斯穆拉尔") { Get-ChildItem -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/03_穆奥塔斯穆拉尔" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/03_穆奥塔斯穆拉尔" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/04_锡尔斯湖与费克斯谷") { Get-ChildItem -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/04_锡尔斯湖与费克斯谷" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/04_锡尔斯湖与费克斯谷" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/05_圣莫里茨雪场") { Get-ChildItem -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/05_圣莫里茨雪场" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/05_圣莫里茨雪场" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/06_恩加丁落叶松") { Get-ChildItem -LiteralPath "04_格劳宾登/01_圣莫里茨与上恩加丁/06_恩加丁落叶松" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/01_圣莫里茨与上恩加丁/06_恩加丁落叶松" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃") { Get-ChildItem -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃/01_迪亚沃莱扎") { Get-ChildItem -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃/01_迪亚沃莱扎" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/01_迪亚沃莱扎" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃/02_莫特拉奇冰川步道") { Get-ChildItem -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃/02_莫特拉奇冰川步道" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/02_莫特拉奇冰川步道" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃/03_布鲁西奥螺旋桥") { Get-ChildItem -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃/03_布鲁西奥螺旋桥" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/03_布鲁西奥螺旋桥" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃/04_波斯基亚沃小镇") { Get-ChildItem -LiteralPath "04_格劳宾登/02_伯尔尼纳山口与波斯基亚沃/04_波斯基亚沃小镇" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/02_伯尔尼纳山口与波斯基亚沃/04_波斯基亚沃小镇" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/03_下恩加丁") { Get-ChildItem -LiteralPath "04_格劳宾登/03_下恩加丁" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/03_下恩加丁" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/03_下恩加丁/01_斯库奥尔温泉") { Get-ChildItem -LiteralPath "04_格劳宾登/03_下恩加丁/01_斯库奥尔温泉" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/03_下恩加丁/01_斯库奥尔温泉" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/03_下恩加丁/02_瓜尔达古村") { Get-ChildItem -LiteralPath "04_格劳宾登/03_下恩加丁/02_瓜尔达古村" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/03_下恩加丁/02_瓜尔达古村" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/03_下恩加丁/03_塔拉斯普城堡") { Get-ChildItem -LiteralPath "04_格劳宾登/03_下恩加丁/03_塔拉斯普城堡" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/03_下恩加丁/03_塔拉斯普城堡" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/03_下恩加丁/04_瑞士国家公园") { Get-ChildItem -LiteralPath "04_格劳宾登/03_下恩加丁/04_瑞士国家公园" -File | Move-Item -Destination "04_格劳宾登/01_恩加丁地区/03_下恩加丁/04_瑞士国家公园" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/04_达沃斯与克洛斯特斯") { Get-ChildItem -LiteralPath "04_格劳宾登/04_达沃斯与克洛斯特斯" -File | Move-Item -Destination "04_格劳宾登/02_达沃斯与克洛斯特斯" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/04_达沃斯与克洛斯特斯/01_达沃斯小镇与湖") { Get-ChildItem -LiteralPath "04_格劳宾登/04_达沃斯与克洛斯特斯/01_达沃斯小镇与湖" -File | Move-Item -Destination "04_格劳宾登/02_达沃斯与克洛斯特斯/01_达沃斯小镇与湖" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/04_达沃斯与克洛斯特斯/02_帕森·魏斯弗卢峰") { Get-ChildItem -LiteralPath "04_格劳宾登/04_达沃斯与克洛斯特斯/02_帕森·魏斯弗卢峰" -File | Move-Item -Destination "04_格劳宾登/02_达沃斯与克洛斯特斯/02_帕森·魏斯弗卢峰" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/04_达沃斯与克洛斯特斯/03_达沃斯–克洛斯特斯雪场") { Get-ChildItem -LiteralPath "04_格劳宾登/04_达沃斯与克洛斯特斯/03_达沃斯–克洛斯特斯雪场" -File | Move-Item -Destination "04_格劳宾登/02_达沃斯与克洛斯特斯/03_达沃斯–克洛斯特斯雪场" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村") { Get-ChildItem -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村" -File | Move-Item -Destination "04_格劳宾登/03_库尔与阿罗萨" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村/01_库尔老城") { Get-ChildItem -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村/01_库尔老城" -File | Move-Item -Destination "04_格劳宾登/03_库尔与阿罗萨/01_库尔老城" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村/02_阿罗萨魏斯峰") { Get-ChildItem -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村/02_阿罗萨魏斯峰" -File | Move-Item -Destination "04_格劳宾登/03_库尔与阿罗萨/02_阿罗萨魏斯峰" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村/03_迈恩菲尔德海蒂村") { Get-ChildItem -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村/03_迈恩菲尔德海蒂村" -File | Move-Item -Destination "04_格劳宾登/03_库尔与阿罗萨/03_迈恩菲尔德海蒂村" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村/04_巴特拉加茨温泉") { Get-ChildItem -LiteralPath "04_格劳宾登/05_库尔、阿罗萨与海蒂村/04_巴特拉加茨温泉" -File | Move-Item -Destination "04_格劳宾登/03_库尔与阿罗萨/04_巴特拉加茨温泉" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯") { Get-ChildItem -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯" -File | Move-Item -Destination "04_格劳宾登/04_弗利姆斯–拉克斯" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯/01_考马湖") { Get-ChildItem -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯/01_考马湖" -File | Move-Item -Destination "04_格劳宾登/04_弗利姆斯–拉克斯/01_考马湖" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯/02_莱茵大峡谷 Ruinaulta") { Get-ChildItem -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯/02_莱茵大峡谷 Ruinaulta" -File | Move-Item -Destination "04_格劳宾登/04_弗利姆斯–拉克斯/02_莱茵大峡谷 Ruinaulta" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯/03_拉克斯雪场") { Get-ChildItem -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯/03_拉克斯雪场" -File | Move-Item -Destination "04_格劳宾登/04_弗利姆斯–拉克斯/03_拉克斯雪场" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/06_阿尔布拉线与维亚马拉") { Get-ChildItem -LiteralPath "04_格劳宾登/06_阿尔布拉线与维亚马拉" -File | Move-Item -Destination "04_格劳宾登/05_阿尔布拉线" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/06_阿尔布拉线与维亚马拉/01_兰德瓦瑟高架桥") { Get-ChildItem -LiteralPath "04_格劳宾登/06_阿尔布拉线与维亚马拉/01_兰德瓦瑟高架桥" -File | Move-Item -Destination "04_格劳宾登/05_阿尔布拉线/01_兰德瓦瑟高架桥" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/06_阿尔布拉线与维亚马拉/02_贝尔金铁路博物馆与雪橇道") { Get-ChildItem -LiteralPath "04_格劳宾登/06_阿尔布拉线与维亚马拉/02_贝尔金铁路博物馆与雪橇道" -File | Move-Item -Destination "04_格劳宾登/05_阿尔布拉线/02_贝尔金铁路博物馆与雪橇道" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯/04_瓦尔斯温泉（卒姆托设计）") { Get-ChildItem -LiteralPath "04_格劳宾登/07_弗利姆斯–拉克斯/04_瓦尔斯温泉（卒姆托设计）" -File | Move-Item -Destination "04_格劳宾登/06_格劳宾登周边与沿途/01_瓦尔斯温泉（卒姆托设计）" -Force; $moved++ }
if (Test-Path -LiteralPath "04_格劳宾登/06_阿尔布拉线与维亚马拉/03_维亚马拉峡谷") { Get-ChildItem -LiteralPath "04_格劳宾登/06_阿尔布拉线与维亚马拉/03_维亚马拉峡谷" -File | Move-Item -Destination "04_格劳宾登/06_格劳宾登周边与沿途/02_维亚马拉峡谷" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/01_卢加诺") { Get-ChildItem -LiteralPath "05_提契诺/01_卢加诺" -File | Move-Item -Destination "05_提契诺/01_卢加诺湖区/01_卢加诺" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/01_卢加诺/01_卢加诺湖") { Get-ChildItem -LiteralPath "05_提契诺/01_卢加诺/01_卢加诺湖" -File | Move-Item -Destination "05_提契诺/01_卢加诺湖区/01_卢加诺/01_卢加诺湖游船" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/01_卢加诺/02_老城与改革广场") { Get-ChildItem -LiteralPath "05_提契诺/01_卢加诺/02_老城与改革广场" -File | Move-Item -Destination "05_提契诺/01_卢加诺湖区/01_卢加诺/02_老城与改革广场" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/01_卢加诺/03_圣萨尔瓦托雷山") { Get-ChildItem -LiteralPath "05_提契诺/01_卢加诺/03_圣萨尔瓦托雷山" -File | Move-Item -Destination "05_提契诺/01_卢加诺湖区/01_卢加诺/03_圣萨尔瓦托雷山" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/01_卢加诺/05_莫尔科特") { Get-ChildItem -LiteralPath "05_提契诺/01_卢加诺/05_莫尔科特" -File | Move-Item -Destination "05_提契诺/01_卢加诺湖区/02_莫尔科特与甘德里亚/01_莫尔科特" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/01_卢加诺/04_甘德里亚湖畔步道") { Get-ChildItem -LiteralPath "05_提契诺/01_卢加诺/04_甘德里亚湖畔步道" -File | Move-Item -Destination "05_提契诺/01_卢加诺湖区/02_莫尔科特与甘德里亚/02_甘德里亚湖畔步道" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/02_门德里西奥") { Get-ChildItem -LiteralPath "05_提契诺/02_门德里西奥" -File | Move-Item -Destination "05_提契诺/01_卢加诺湖区/03_门德里西奥" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/02_门德里西奥/01_吉内罗索山铁路＋石之花") { Get-ChildItem -LiteralPath "05_提契诺/02_门德里西奥/01_吉内罗索山铁路＋石之花" -File | Move-Item -Destination "05_提契诺/01_卢加诺湖区/03_门德里西奥/01_吉内罗索山铁路＋石之花" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖") { Get-ChildItem -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖/01_洛迦诺大广场") { Get-ChildItem -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖/01_洛迦诺大广场" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/01_洛迦诺大广场" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖/02_圣母岩修道院") { Get-ChildItem -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖/02_圣母岩修道院" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/02_圣母岩修道院" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖/03_卡达达与奇梅塔") { Get-ChildItem -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖/03_卡达达与奇梅塔" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/03_卡达达与奇梅塔" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖/04_阿斯科纳") { Get-ChildItem -LiteralPath "05_提契诺/03_洛迦诺与马焦雷湖/04_阿斯科纳" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/01_洛迦诺与阿斯科纳/04_阿斯科纳" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷") { Get-ChildItem -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷/01_拉韦尔泰佐双拱桥") { Get-ChildItem -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷/01_拉韦尔泰佐双拱桥" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/01_拉韦尔泰佐双拱桥" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷/02_韦尔扎斯卡水坝") { Get-ChildItem -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷/02_韦尔扎斯卡水坝" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/02_韦尔扎斯卡水坝" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷/03_马贾谷与福罗利奥瀑布") { Get-ChildItem -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷/03_马贾谷与福罗利奥瀑布" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/03_马贾谷与福罗利奥瀑布" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷/04_莫尼奥圣约翰教堂（博塔设计）") { Get-ChildItem -LiteralPath "05_提契诺/04_韦尔扎斯卡与马贾谷/04_莫尼奥圣约翰教堂（博塔设计）" -File | Move-Item -Destination "05_提契诺/02_马焦雷湖区/02_韦尔扎斯卡与马贾谷/04_莫尼奥圣约翰教堂（博塔设计）" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/05_贝林佐纳与圣哥达") { Get-ChildItem -LiteralPath "05_提契诺/05_贝林佐纳与圣哥达" -File | Move-Item -Destination "05_提契诺/03_贝林佐纳" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/05_贝林佐纳与圣哥达/01_贝林佐纳三城堡") { Get-ChildItem -LiteralPath "05_提契诺/05_贝林佐纳与圣哥达/01_贝林佐纳三城堡" -File | Move-Item -Destination "05_提契诺/03_贝林佐纳/01_贝林佐纳三城堡" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/05_贝林佐纳与圣哥达/02_塔马罗山＋博塔教堂") { Get-ChildItem -LiteralPath "05_提契诺/05_贝林佐纳与圣哥达/02_塔马罗山＋博塔教堂" -File | Move-Item -Destination "05_提契诺/03_贝林佐纳/02_塔马罗山＋博塔教堂" -Force; $moved++ }
if (Test-Path -LiteralPath "05_提契诺/05_贝林佐纳与圣哥达/03_圣哥达山口") { Get-ChildItem -LiteralPath "05_提契诺/05_贝林佐纳与圣哥达/03_圣哥达山口" -File | Move-Item -Destination "05_提契诺/04_提契诺周边与沿途/01_圣哥达山口" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦") { Get-ChildItem -LiteralPath "06_日内瓦湖区/01_日内瓦" -File | Move-Item -Destination "06_日内瓦湖区/01_日内瓦市区" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦/01_大喷泉") { Get-ChildItem -LiteralPath "06_日内瓦湖区/01_日内瓦/01_大喷泉" -File | Move-Item -Destination "06_日内瓦湖区/01_日内瓦市区/01_大喷泉" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦/02_日内瓦老城") { Get-ChildItem -LiteralPath "06_日内瓦湖区/01_日内瓦/02_日内瓦老城" -File | Move-Item -Destination "06_日内瓦湖区/01_日内瓦市区/02_日内瓦老城" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦/02_日内瓦老城/01_圣皮埃尔大教堂") { Get-ChildItem -LiteralPath "06_日内瓦湖区/01_日内瓦/02_日内瓦老城/01_圣皮埃尔大教堂" -File | Move-Item -Destination "06_日内瓦湖区/01_日内瓦市区/02_日内瓦老城/01_圣皮埃尔大教堂" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦/02_日内瓦老城/02_宗教改革纪念墙") { Get-ChildItem -LiteralPath "06_日内瓦湖区/01_日内瓦/02_日内瓦老城/02_宗教改革纪念墙" -File | Move-Item -Destination "06_日内瓦湖区/01_日内瓦市区/02_日内瓦老城/02_宗教改革纪念墙" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦/03_万国宫") { Get-ChildItem -LiteralPath "06_日内瓦湖区/01_日内瓦/03_万国宫" -File | Move-Item -Destination "06_日内瓦湖区/01_日内瓦市区/03_万国宫" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/01_日内瓦/04_欧洲核子研究中心 CERN") { Get-ChildItem -LiteralPath "06_日内瓦湖区/01_日内瓦/04_欧洲核子研究中心 CERN" -File | Move-Item -Destination "06_日内瓦湖区/01_日内瓦市区/04_欧洲核子研究中心 CERN" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑") { Get-ChildItem -LiteralPath "06_日内瓦湖区/02_洛桑" -File | Move-Item -Destination "06_日内瓦湖区/02_洛桑市区" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑/01_洛桑大教堂") { Get-ChildItem -LiteralPath "06_日内瓦湖区/02_洛桑/01_洛桑大教堂" -File | Move-Item -Destination "06_日内瓦湖区/02_洛桑市区/01_洛桑大教堂" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑/02_奥林匹克博物馆") { Get-ChildItem -LiteralPath "06_日内瓦湖区/02_洛桑/02_奥林匹克博物馆" -File | Move-Item -Destination "06_日内瓦湖区/02_洛桑市区/02_奥林匹克博物馆" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑/03_乌希湖畔") { Get-ChildItem -LiteralPath "06_日内瓦湖区/02_洛桑/03_乌希湖畔" -File | Move-Item -Destination "06_日内瓦湖区/02_洛桑市区/03_乌希湖畔" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/02_洛桑/04_劳力士学习中心") { Get-ChildItem -LiteralPath "06_日内瓦湖区/02_洛桑/04_劳力士学习中心" -File | Move-Item -Destination "06_日内瓦湖区/02_洛桑市区/04_劳力士学习中心" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦") { Get-ChildItem -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦" -File | Move-Item -Destination "06_日内瓦湖区/03_蒙特勒与拉沃" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/03_拉沃葡萄园/01_梯田葡萄园步道") { Get-ChildItem -LiteralPath "06_日内瓦湖区/03_拉沃葡萄园/01_梯田葡萄园步道" -File | Move-Item -Destination "06_日内瓦湖区/03_蒙特勒与拉沃/01_梯田葡萄园步道" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/01_西庸城堡") { Get-ChildItem -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/01_西庸城堡" -File | Move-Item -Destination "06_日内瓦湖区/03_蒙特勒与拉沃/02_西庸城堡" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/02_湖畔步道与墨丘利雕像") { Get-ChildItem -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/02_湖畔步道与墨丘利雕像" -File | Move-Item -Destination "06_日内瓦湖区/03_蒙特勒与拉沃/03_湖畔步道与墨丘利雕像" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/03_蒙特勒圣诞市集") { Get-ChildItem -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/03_蒙特勒圣诞市集" -File | Move-Item -Destination "06_日内瓦湖区/03_蒙特勒与拉沃/04_蒙特勒圣诞市集" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/04_纳伊岩铁路与土拨鼠园") { Get-ChildItem -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/04_纳伊岩铁路与土拨鼠园" -File | Move-Item -Destination "06_日内瓦湖区/03_蒙特勒与拉沃/05_纳伊岩铁路与土拨鼠园" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/05_卓别林世界") { Get-ChildItem -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/05_卓别林世界" -File | Move-Item -Destination "06_日内瓦湖区/03_蒙特勒与拉沃/06_卓别林世界" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/06_湖边小屋（勒·柯布西耶）") { Get-ChildItem -LiteralPath "06_日内瓦湖区/04_蒙特勒与沃韦/06_湖边小屋（勒·柯布西耶）" -File | Move-Item -Destination "06_日内瓦湖区/03_蒙特勒与拉沃/07_湖边小屋（勒·柯布西耶）" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/05_格吕耶尔与布罗克") { Get-ChildItem -LiteralPath "06_日内瓦湖区/05_格吕耶尔与布罗克" -File | Move-Item -Destination "06_日内瓦湖区/04_格吕耶尔与布罗克" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/05_格吕耶尔与布罗克/01_格吕耶尔古堡与小镇") { Get-ChildItem -LiteralPath "06_日内瓦湖区/05_格吕耶尔与布罗克/01_格吕耶尔古堡与小镇" -File | Move-Item -Destination "06_日内瓦湖区/04_格吕耶尔与布罗克/01_格吕耶尔古堡与小镇" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/05_格吕耶尔与布罗克/02_格吕耶尔奶酪工坊") { Get-ChildItem -LiteralPath "06_日内瓦湖区/05_格吕耶尔与布罗克/02_格吕耶尔奶酪工坊" -File | Move-Item -Destination "06_日内瓦湖区/04_格吕耶尔与布罗克/02_格吕耶尔奶酪工坊" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/05_格吕耶尔与布罗克/03_Cailler 巧克力工厂") { Get-ChildItem -LiteralPath "06_日内瓦湖区/05_格吕耶尔与布罗克/03_Cailler 巧克力工厂" -File | Move-Item -Destination "06_日内瓦湖区/04_格吕耶尔与布罗克/03_Cailler 巧克力工厂" -Force; $moved++ }
if (Test-Path -LiteralPath "06_日内瓦湖区/06_莱迪亚布勒雷与维拉尔/01_冰川 3000 与峰顶吊桥") { Get-ChildItem -LiteralPath "06_日内瓦湖区/06_莱迪亚布勒雷与维拉尔/01_冰川 3000 与峰顶吊桥" -File | Move-Item -Destination "06_日内瓦湖区/05_日内瓦湖区周边与沿途/01_冰川 3000 与峰顶吊桥" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/01_苏黎世市区" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/01_苏黎世老城与班霍夫大街") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/01_苏黎世老城与班霍夫大街" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/01_苏黎世老城与班霍夫大街" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/01_苏黎世老城与班霍夫大街/01_大教堂") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/01_苏黎世老城与班霍夫大街/01_大教堂" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/01_苏黎世老城与班霍夫大街/01_苏黎世大教堂" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/01_苏黎世老城与班霍夫大街/02_圣母大教堂（夏加尔彩窗）") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/01_苏黎世老城与班霍夫大街/02_圣母大教堂（夏加尔彩窗）" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/01_苏黎世老城与班霍夫大街/02_圣母大教堂" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/02_于特利山") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/02_于特利山" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/02_于特利山" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/03_瑞士国家博物馆") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/03_瑞士国家博物馆" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/03_瑞士国家博物馆" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/04_瑞士莲巧克力之家") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/04_瑞士莲巧克力之家" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/04_瑞士莲巧克力之家" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/06_勒·柯布西耶馆") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/06_勒·柯布西耶馆" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/01_苏黎世市区/05_勒·柯布西耶馆" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔/01_阿彭策尔小镇") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔/01_阿彭策尔小镇" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/01_阿彭策尔小镇" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔/02_森蒂斯山") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔/02_森蒂斯山" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/02_森蒂斯山" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔/03_埃本阿尔卑与崖壁客栈") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔/03_埃本阿尔卑与崖壁客栈" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/03_埃本阿尔卑与崖壁客栈" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔/04_西阿尔卑湖") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/04_阿彭策尔/04_西阿尔卑湖" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/04_西阿尔卑湖" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/03_圣加仑与博登湖/01_圣加仑修道院图书馆") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/03_圣加仑与博登湖/01_圣加仑修道院图书馆" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/03_阿彭策尔地区/05_圣加仑修道院图书馆" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/05_瓦伦湖与托根堡") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/05_瓦伦湖与托根堡" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/04_瓦伦湖与托根堡" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/05_瓦伦湖与托根堡/01_瓦伦湖") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/05_瓦伦湖与托根堡/01_瓦伦湖" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/04_瓦伦湖与托根堡/01_瓦伦湖" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/05_瓦伦湖与托根堡/02_沙瑟鲁格（选峰）") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/05_瓦伦湖与托根堡/02_沙瑟鲁格（选峰）" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/04_瓦伦湖与托根堡/02_沙瑟鲁格" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/06_列支敦士登") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/06_列支敦士登" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/05_列支敦士登" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/06_列支敦士登/01_瓦杜兹城堡") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/06_列支敦士登/01_瓦杜兹城堡" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/05_列支敦士登/01_瓦杜兹城堡" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/06_列支敦士登/02_瓦杜兹市区与邮票博物馆") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/06_列支敦士登/02_瓦杜兹市区与邮票博物馆" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/05_列支敦士登/02_瓦杜兹市区与邮票博物馆" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/06_列支敦士登/03_王子步道") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/06_列支敦士登/03_王子步道" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/05_列支敦士登/03_王子步道" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/05_巴登 FORTYSEVEN 温泉") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/01_苏黎世/05_巴登 FORTYSEVEN 温泉" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/06_东北部周边与沿途/01_巴登 FORTYSEVEN 温泉" -Force; $moved++ }
if (Test-Path -LiteralPath "07_苏黎世、东北部与列支敦士登/03_圣加仑与博登湖/02_博登湖") { Get-ChildItem -LiteralPath "07_苏黎世、东北部与列支敦士登/03_圣加仑与博登湖/02_博登湖" -File | Move-Item -Destination "07_苏黎世、东北部与列支敦士登/06_东北部周边与沿途/02_博登湖" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼") { Get-ChildItem -LiteralPath "08_首都与西北部/01_伯尔尼" -File | Move-Item -Destination "08_首都与西北部/01_伯尔尼市区" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）") { Get-ChildItem -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）" -File | Move-Item -Destination "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）/01_钟楼") { Get-ChildItem -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）/01_钟楼" -File | Move-Item -Destination "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/01_伯尔尼钟楼" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）/02_熊公园") { Get-ChildItem -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）/02_熊公园" -File | Move-Item -Destination "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/02_熊公园" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）/03_联邦大厦") { Get-ChildItem -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）/03_联邦大厦" -File | Move-Item -Destination "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/03_联邦大厦" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）/04_爱因斯坦故居") { Get-ChildItem -LiteralPath "08_首都与西北部/01_伯尔尼/01_伯尔尼老城（世界遗产）/04_爱因斯坦故居" -File | Move-Item -Destination "08_首都与西北部/01_伯尔尼市区/01_伯尔尼老城/04_爱因斯坦故居" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼/02_玫瑰园") { Get-ChildItem -LiteralPath "08_首都与西北部/01_伯尔尼/02_玫瑰园" -File | Move-Item -Destination "08_首都与西北部/01_伯尔尼市区/02_玫瑰园" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/01_伯尔尼/03_保罗·克利中心") { Get-ChildItem -LiteralPath "08_首都与西北部/01_伯尔尼/03_保罗·克利中心" -File | Move-Item -Destination "08_首都与西北部/01_伯尔尼市区/03_保罗·克利中心" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/03_巴塞尔") { Get-ChildItem -LiteralPath "08_首都与西北部/03_巴塞尔" -File | Move-Item -Destination "08_首都与西北部/02_巴塞尔市区" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/03_巴塞尔/01_巴塞尔老城") { Get-ChildItem -LiteralPath "08_首都与西北部/03_巴塞尔/01_巴塞尔老城" -File | Move-Item -Destination "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/03_巴塞尔/01_巴塞尔老城/01_大教堂与莱茵河") { Get-ChildItem -LiteralPath "08_首都与西北部/03_巴塞尔/01_巴塞尔老城/01_大教堂与莱茵河" -File | Move-Item -Destination "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城/01_巴塞尔大教堂" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/03_巴塞尔/01_巴塞尔老城/02_莱茵河渡船与夏季漂流") { Get-ChildItem -LiteralPath "08_首都与西北部/03_巴塞尔/01_巴塞尔老城/02_莱茵河渡船与夏季漂流" -File | Move-Item -Destination "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城/02_莱茵河渡船与夏季漂流" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/03_巴塞尔/01_巴塞尔老城/03_巴塞尔圣诞市集") { Get-ChildItem -LiteralPath "08_首都与西北部/03_巴塞尔/01_巴塞尔老城/03_巴塞尔圣诞市集" -File | Move-Item -Destination "08_首都与西北部/02_巴塞尔市区/01_巴塞尔老城/03_巴塞尔圣诞市集" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/03_巴塞尔/02_贝耶勒基金会") { Get-ChildItem -LiteralPath "08_首都与西北部/03_巴塞尔/02_贝耶勒基金会" -File | Move-Item -Destination "08_首都与西北部/02_巴塞尔市区/02_贝耶勒基金会" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/03_巴塞尔/03_巴塞尔美术馆") { Get-ChildItem -LiteralPath "08_首都与西北部/03_巴塞尔/03_巴塞尔美术馆" -File | Move-Item -Destination "08_首都与西北部/02_巴塞尔市区/03_巴塞尔美术馆" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/03_巴塞尔/05_巴塞尔狂欢节") { Get-ChildItem -LiteralPath "08_首都与西北部/03_巴塞尔/05_巴塞尔狂欢节" -File | Move-Item -Destination "08_首都与西北部/02_巴塞尔市区/04_巴塞尔狂欢节" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/04_汝拉与三湖区") { Get-ChildItem -LiteralPath "08_首都与西北部/04_汝拉与三湖区" -File | Move-Item -Destination "08_首都与西北部/03_汝拉与三湖区" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/04_汝拉与三湖区/01_范湖穹") { Get-ChildItem -LiteralPath "08_首都与西北部/04_汝拉与三湖区/01_范湖穹" -File | Move-Item -Destination "08_首都与西北部/03_汝拉与三湖区/01_范湖穹" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/04_汝拉与三湖区/02_拉绍德封·力洛克制表城（世界遗产）") { Get-ChildItem -LiteralPath "08_首都与西北部/04_汝拉与三湖区/02_拉绍德封·力洛克制表城（世界遗产）" -File | Move-Item -Destination "08_首都与西北部/03_汝拉与三湖区/02_拉绍德封与力洛克" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/04_汝拉与三湖区/03_圣于尔桑") { Get-ChildItem -LiteralPath "08_首都与西北部/04_汝拉与三湖区/03_圣于尔桑" -File | Move-Item -Destination "08_首都与西北部/03_汝拉与三湖区/03_圣于尔桑" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/04_汝拉与三湖区/04_穆尔滕古城") { Get-ChildItem -LiteralPath "08_首都与西北部/04_汝拉与三湖区/04_穆尔滕古城" -File | Move-Item -Destination "08_首都与西北部/03_汝拉与三湖区/04_穆尔滕古城" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/04_汝拉与三湖区/05_伊韦尔东温泉") { Get-ChildItem -LiteralPath "08_首都与西北部/04_汝拉与三湖区/05_伊韦尔东温泉" -File | Move-Item -Destination "08_首都与西北部/03_汝拉与三湖区/05_伊韦尔东温泉" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/02_埃门塔尔/01_木廊桥与农庄") { Get-ChildItem -LiteralPath "08_首都与西北部/02_埃门塔尔/01_木廊桥与农庄" -File | Move-Item -Destination "08_首都与西北部/04_西北部周边与沿途/01_木廊桥与农庄" -Force; $moved++ }
if (Test-Path -LiteralPath "08_首都与西北部/03_巴塞尔/04_维特拉设计园") { Get-ChildItem -LiteralPath "08_首都与西北部/03_巴塞尔/04_维特拉设计园" -File | Move-Item -Destination "08_首都与西北部/04_西北部周边与沿途/02_维特拉设计园" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/01_第1段 加夫莱（列支敦士登）→ 萨尔甘斯") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/01_第1段 加夫莱（列支敦士登）→ 萨尔甘斯" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/01_第 1 段 · 加夫莱（列支敦士登）→ 萨尔甘斯" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/02_第2段 萨尔甘斯 → 魏斯坦嫩") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/02_第2段 萨尔甘斯 → 魏斯坦嫩" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/02_第 2 段 · 萨尔甘斯 → 魏斯坦嫩" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/03_第3段 魏斯坦嫩 → 埃尔姆") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/03_第3段 魏斯坦嫩 → 埃尔姆" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/03_第 3 段 · 魏斯坦嫩 → 埃尔姆" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/04_第4段 埃尔姆 → 林塔尔") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/04_第4段 埃尔姆 → 林塔尔" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/04_第 4 段 · 埃尔姆 → 林塔尔" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/05_第5段 林塔尔 → 乌尔纳博登") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/05_第5段 林塔尔 → 乌尔纳博登" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/05_第 5 段 · 林塔尔 → 乌尔纳博登" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/06_第6段 乌尔纳博登 → 阿尔特多夫") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/06_第6段 乌尔纳博登 → 阿尔特多夫" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/06_第 6 段 · 乌尔纳博登 → 阿尔特多夫" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/07_第7段 阿尔特多夫 → 英格堡") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/07_第7段 阿尔特多夫 → 英格堡" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/07_第 7 段 · 阿尔特多夫 → 英格堡" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/08_第8段 英格堡 → 恩斯特伦阿尔卑") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/08_第8段 英格堡 → 恩斯特伦阿尔卑" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/08_第 8 段 · 英格堡 → 恩斯特伦阿尔卑" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/09_第9段 恩斯特伦阿尔卑 → 迈林根") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/09_第9段 恩斯特伦阿尔卑 → 迈林根" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/09_第 9 段 · 恩斯特伦阿尔卑 → 迈林根" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/10_第10段 迈林根 → 格林德瓦") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/10_第10段 迈林根 → 格林德瓦" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/10_第 10 段 · 迈林根 → 格林德瓦" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/11_第11段 格林德瓦 → 劳特布龙嫩") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/11_第11段 格林德瓦 → 劳特布龙嫩" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/11_第 11 段 · 格林德瓦 → 劳特布龙嫩" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/12_第12段 劳特布龙嫩 → 格里斯阿尔卑") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/12_第12段 劳特布龙嫩 → 格里斯阿尔卑" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/12_第 12 段 · 劳特布龙嫩 → 格里斯阿尔卑" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/13_第13段 格里斯阿尔卑 → 坎德施泰格") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/13_第13段 格里斯阿尔卑 → 坎德施泰格" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/13_第 13 段 · 格里斯阿尔卑 → 坎德施泰格" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/14_第14段 坎德施泰格 → 阿德尔博登") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/14_第14段 坎德施泰格 → 阿德尔博登" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/14_第 14 段 · 坎德施泰格 → 阿德尔博登" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/15_第15段 阿德尔博登 → 伦克") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/15_第15段 阿德尔博登 → 伦克" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/15_第 15 段 · 阿德尔博登 → 伦克" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/16_第16段 伦克 → 格施塔德") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/16_第16段 伦克 → 格施塔德" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/16_第 16 段 · 伦克 → 格施塔德" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/17_第17段 格施塔德 → 莱蒂瓦") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/17_第17段 格施塔德 → 莱蒂瓦" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/17_第 17 段 · 格施塔德 → 莱蒂瓦" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/18_第18–19段 莱蒂瓦 → 罗西尼耶尔 → 纳伊岩") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/18_第18–19段 莱蒂瓦 → 罗西尼耶尔 → 纳伊岩" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/18_第 18–19 段 · 莱蒂瓦 → 罗西尼耶尔 → 纳伊岩" -Force; $moved++ }
if (Test-Path -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/19_第20段 纳伊岩 → 蒙特勒") { Get-ChildItem -LiteralPath "01_伯尔尼高地/07_坎德施泰格与阿德尔博登/04_Via Alpina 全程/19_第20段 纳伊岩 → 蒙特勒" -File | Move-Item -Destination "09_长线徒步/01_Via Alpina 全程/19_第 20 段 · 纳伊岩 → 蒙特勒" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/01_第1段 夏蒙尼 → 阿让蒂耶尔") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/01_第1段 夏蒙尼 → 阿让蒂耶尔" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/01_第 1 段 · 夏蒙尼 → 阿让蒂耶尔" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/02_第2段 阿让蒂耶尔 → 特里安") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/02_第2段 阿让蒂耶尔 → 特里安" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/02_第 2 段 · 阿让蒂耶尔 → 特里安" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/03_第3段 特里安 → 尚佩") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/03_第3段 特里安 → 尚佩" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/03_第 3 段 · 特里安 → 尚佩" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/04_第4段 尚佩 → 勒沙布勒") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/04_第4段 尚佩 → 勒沙布勒" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/04_第 4 段 · 尚佩 → 勒沙布勒" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/05_第5段 勒沙布勒 → 蒙福小屋") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/05_第5段 勒沙布勒 → 蒙福小屋" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/05_第 5 段 · 勒沙布勒 → 蒙福小屋" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/06_第6段 蒙福小屋 → 普拉弗勒里小屋") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/06_第6段 蒙福小屋 → 普拉弗勒里小屋" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/06_第 6 段 · 蒙福小屋 → 普拉弗勒里小屋" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/07_第7段 普拉弗勒里小屋 → 阿罗拉") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/07_第7段 普拉弗勒里小屋 → 阿罗拉" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/07_第 7 段 · 普拉弗勒里小屋 → 阿罗拉" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/08_第8段 阿罗拉 → 莱奥代尔") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/08_第8段 阿罗拉 → 莱奥代尔" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/08_第 8 段 · 阿罗拉 → 莱奥代尔" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/09_第9段 莱奥代尔 → 莫伊里湖") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/09_第9段 莱奥代尔 → 莫伊里湖" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/09_第 9 段 · 莱奥代尔 → 莫伊里湖" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/10_第10段 莫伊里湖 → 齐纳尔") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/10_第10段 莫伊里湖 → 齐纳尔" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/10_第 10 段 · 莫伊里湖 → 齐纳尔" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/11_第11段 齐纳尔 → 格鲁本") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/11_第11段 齐纳尔 → 格鲁本" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/11_第 11 段 · 齐纳尔 → 格鲁本" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/12_第12段 格鲁本 → 圣尼克劳斯") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/12_第12段 格鲁本 → 圣尼克劳斯" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/12_第 12 段 · 格鲁本 → 圣尼克劳斯" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/13_第13段 圣尼克劳斯 → 欧罗巴小屋") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/13_第13段 圣尼克劳斯 → 欧罗巴小屋" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/13_第 13 段 · 圣尼克劳斯 → 欧罗巴小屋" -Force; $moved++ }
if (Test-Path -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/14_第14段 欧罗巴小屋 → 采尔马特") { Get-ChildItem -LiteralPath "02_瓦莱州与勃朗峰/01_采尔马特/10_瑞士高山之路 Haute Route/14_第14段 欧罗巴小屋 → 采尔马特" -File | Move-Item -Destination "09_长线徒步/02_瑞士高山之路 Haute Route/14_第 14 段 · 欧罗巴小屋 → 采尔马特" -Force; $moved++ }
if (Test-Path -LiteralPath "09_专题_全景列车") { Get-ChildItem -LiteralPath "09_专题_全景列车" -File | Move-Item -Destination "10_全景列车" -Force; $moved++ }
if (Test-Path -LiteralPath "09_专题_全景列车/01_冰川快车") { Get-ChildItem -LiteralPath "09_专题_全景列车/01_冰川快车" -File | Move-Item -Destination "10_全景列车/01_冰川快车" -Force; $moved++ }
if (Test-Path -LiteralPath "09_专题_全景列车/02_伯尔尼纳快车") { Get-ChildItem -LiteralPath "09_专题_全景列车/02_伯尔尼纳快车" -File | Move-Item -Destination "10_全景列车/02_伯尔尼纳快车" -Force; $moved++ }
if (Test-Path -LiteralPath "09_专题_全景列车/03_黄金山口快车") { Get-ChildItem -LiteralPath "09_专题_全景列车/03_黄金山口快车" -File | Move-Item -Destination "10_全景列车/03_黄金山口快车" -Force; $moved++ }
if (Test-Path -LiteralPath "09_专题_全景列车/04_圣哥达全景快车") { Get-ChildItem -LiteralPath "09_专题_全景列车/04_圣哥达全景快车" -File | Move-Item -Destination "10_全景列车/04_圣哥达全景快车" -Force; $moved++ }
if (Test-Path -LiteralPath "09_专题_全景列车/05_沃拉尔普快车") { Get-ChildItem -LiteralPath "09_专题_全景列车/05_沃拉尔普快车" -File | Move-Item -Destination "10_全景列车/05_沃拉尔普快车" -Force; $moved++ }
if (Test-Path -LiteralPath "09_专题_全景列车/06_勃朗峰快车") { Get-ChildItem -LiteralPath "09_专题_全景列车/06_勃朗峰快车" -File | Move-Item -Destination "10_全景列车/06_勃朗峰快车" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）" -File | Move-Item -Destination "11_山地交通与通票" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/01_齿轨铁路") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/01_齿轨铁路" -File | Move-Item -Destination "11_山地交通与通票/01_齿轨铁路" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/02_缆索铁路") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/02_缆索铁路" -File | Move-Item -Destination "11_山地交通与通票/02_缆索铁路" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/03_空中缆车") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/03_空中缆车" -File | Move-Item -Destination "11_山地交通与通票/03_空中缆车" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/04_吊厢") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/04_吊厢" -File | Move-Item -Destination "11_山地交通与通票/04_吊厢" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/05_吊椅") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/05_吊椅" -File | Move-Item -Destination "11_山地交通与通票/05_吊椅" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/06_瑞士通票 Swiss Travel Pass") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/06_瑞士通票 Swiss Travel Pass" -File | Move-Item -Destination "11_山地交通与通票/06_瑞士通票" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/07_半价卡 Half Fare Card") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/07_半价卡 Half Fare Card" -File | Move-Item -Destination "11_山地交通与通票/07_瑞士半价卡" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/08_少女峰通票") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/08_少女峰通票" -File | Move-Item -Destination "11_山地交通与通票/08_少女峰通票" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/09_伯尔尼高地通票") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/09_伯尔尼高地通票" -File | Move-Item -Destination "11_山地交通与通票/09_伯尔尼高地通票" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/10_Tell-Pass") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/10_Tell-Pass" -File | Move-Item -Destination "11_山地交通与通票/10_琉森旅行通票" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/11_Mont-Blanc Multipass") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/11_Mont-Blanc Multipass" -File | Move-Item -Destination "11_山地交通与通票/11_勃朗峰多日通票" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/12_检修停运期说明") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/12_检修停运期说明" -File | Move-Item -Destination "11_山地交通与通票/12_检修停运期说明" -Force; $moved++ }
if (Test-Path -LiteralPath "10_专题_山地交通与通票（小辞典）/13_FlixBus 长途巴士") { Get-ChildItem -LiteralPath "10_专题_山地交通与通票（小辞典）/13_FlixBus 长途巴士" -File | Move-Item -Destination "11_山地交通与通票/13_FlixBus 长途巴士" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）" -File | Move-Item -Destination "12_美食与特产" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）/01_芝士火锅") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）/01_芝士火锅" -File | Move-Item -Destination "12_美食与特产/01_芝士火锅" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）/02_烤奶酪 Raclette") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）/02_烤奶酪 Raclette" -File | Move-Item -Destination "12_美食与特产/02_烤奶酪 Raclette" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）/03_苏黎世小牛肉") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）/03_苏黎世小牛肉" -File | Move-Item -Destination "12_美食与特产/03_苏黎世小牛肉" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）/04_土豆饼 Rösti") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）/04_土豆饼 Rösti" -File | Move-Item -Destination "12_美食与特产/04_土豆饼 Rösti" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）/05_格劳宾登大麦汤") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）/05_格劳宾登大麦汤" -File | Move-Item -Destination "12_美食与特产/05_格劳宾登大麦汤" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）/06_恩加丁坚果塔") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）/06_恩加丁坚果塔" -File | Move-Item -Destination "12_美食与特产/06_恩加丁坚果塔" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）/07_栗子蛋糕 Vermicelles") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）/07_栗子蛋糕 Vermicelles" -File | Move-Item -Destination "12_美食与特产/07_栗子蛋糕 Vermicelles" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）/08_瑞士巧克力") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）/08_瑞士巧克力" -File | Move-Item -Destination "12_美食与特产/08_瑞士巧克力" -Force; $moved++ }
if (Test-Path -LiteralPath "11_专题_美食与特产（小辞典）/09_葡萄酒") { Get-ChildItem -LiteralPath "11_专题_美食与特产（小辞典）/09_葡萄酒" -File | Move-Item -Destination "12_美食与特产/09_葡萄酒" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）" -File | Move-Item -Destination "13_野生动植物" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/01_阿尔卑斯旱獭") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/01_阿尔卑斯旱獭" -File | Move-Item -Destination "13_野生动植物/01_阿尔卑斯旱獭" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/02_阿尔卑斯羱羊") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/02_阿尔卑斯羱羊" -File | Move-Item -Destination "13_野生动植物/02_阿尔卑斯羱羊" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/03_岩羚羊") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/03_岩羚羊" -File | Move-Item -Destination "13_野生动植物/03_岩羚羊" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/04_胡兀鹫") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/04_胡兀鹫" -File | Move-Item -Destination "13_野生动植物/04_胡兀鹫" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/05_金雕") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/05_金雕" -File | Move-Item -Destination "13_野生动植物/05_金雕" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/06_黄嘴山鸦") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/06_黄嘴山鸦" -File | Move-Item -Destination "13_野生动植物/06_黄嘴山鸦" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/07_马鹿") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/07_马鹿" -File | Move-Item -Destination "13_野生动植物/07_马鹿" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/08_岩雷鸟") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/08_岩雷鸟" -File | Move-Item -Destination "13_野生动植物/08_岩雷鸟" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/09_瓦莱黑鼻羊") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/09_瓦莱黑鼻羊" -File | Move-Item -Destination "13_野生动植物/09_瓦莱黑鼻羊" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/10_雪绒花") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/10_雪绒花" -File | Move-Item -Destination "13_野生动植物/10_雪绒花" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/11_龙胆") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/11_龙胆" -File | Move-Item -Destination "13_野生动植物/11_龙胆" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/12_高山杜鹃") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/12_高山杜鹃" -File | Move-Item -Destination "13_野生动植物/12_高山杜鹃" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/13_瑞士五针松") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/13_瑞士五针松" -File | Move-Item -Destination "13_野生动植物/13_瑞士五针松" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/14_欧洲落叶松") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/14_欧洲落叶松" -File | Move-Item -Destination "13_野生动植物/14_欧洲落叶松" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/15_番红花") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/15_番红花" -File | Move-Item -Destination "13_野生动植物/15_番红花" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/16_高山白头翁") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/16_高山白头翁" -File | Move-Item -Destination "13_野生动植物/16_高山白头翁" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/17_黄龙胆") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/17_黄龙胆" -File | Move-Item -Destination "13_野生动植物/17_黄龙胆" -Force; $moved++ }
if (Test-Path -LiteralPath "12_专题_野生动植物（小辞典）/18_野生水仙") { Get-ChildItem -LiteralPath "12_专题_野生动植物（小辞典）/18_野生水仙" -File | Move-Item -Destination "13_野生动植物/18_野生水仙" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）" -File | Move-Item -Destination "14_地质与地貌" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/01_U形谷") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/01_U形谷" -File | Move-Item -Destination "14_地质与地貌/01_U形谷" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/02_悬谷与瀑布") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/02_悬谷与瀑布" -File | Move-Item -Destination "14_地质与地貌/02_悬谷与瀑布" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/03_冰碛") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/03_冰碛" -File | Move-Item -Destination "14_地质与地貌/03_冰碛" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/04_冰川退缩") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/04_冰川退缩" -File | Move-Item -Destination "14_地质与地貌/04_冰川退缩" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/05_喀斯特与溶沟") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/05_喀斯特与溶沟" -File | Move-Item -Destination "14_地质与地貌/05_喀斯特与溶沟" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/06_山崩") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/06_山崩" -File | Move-Item -Destination "14_地质与地貌/06_山崩" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/07_峡谷") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/07_峡谷" -File | Move-Item -Destination "14_地质与地貌/07_峡谷" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/08_推覆构造") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/08_推覆构造" -File | Move-Item -Destination "14_地质与地貌/08_推覆构造" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/09_汝拉褶皱山") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/09_汝拉褶皱山" -File | Move-Item -Destination "14_地质与地貌/09_汝拉褶皱山" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/10_永久冻土") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/10_永久冻土" -File | Move-Item -Destination "14_地质与地貌/10_永久冻土" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/11_片麻岩") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/11_片麻岩" -File | Move-Item -Destination "14_地质与地貌/11_片麻岩" -Force; $moved++ }
if (Test-Path -LiteralPath "13_专题_地质与地貌（小辞典）/12_冰湖") { Get-ChildItem -LiteralPath "13_专题_地质与地貌（小辞典）/12_冰湖" -File | Move-Item -Destination "14_地质与地貌/12_冰湖" -Force; $moved++ }
Write-Host "新建文件夹 $made 个，已从旧位置移动文件的文件夹 $moved 个。"