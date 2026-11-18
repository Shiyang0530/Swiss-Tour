# 本书原创的小插画（40×40 坐标），用在总览图和大区图上标出最热门的景点。
# 颜色全部用 CSS 变量或中性色，深色模式下也能看清。
ST = 'stroke="var(--ink-2)" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round"'
ROCK = 'fill="#C9B79A"'
SNOW = 'style="fill:var(--page)"'
RED = 'style="fill:var(--shu)"'
WAT = 'style="fill:var(--water)"'
WOOD = 'fill="#B07D4A"'
STONE = 'fill="#D9CDB6"'
GRN = 'style="fill:var(--matcha)"'

def _waves(y=33):
    return (f'<path d="M1 {y} Q5 {y-2} 9 {y} T17 {y} T25 {y} T33 {y} T39 {y} V39 H1Z" {WAT}/>'
            f'<path d="M4 {y+3} Q7 {y+1.6} 10 {y+3} M22 {y+3.4} Q25 {y+2} 28 {y+3.4}" fill="none" stroke="var(--page)" stroke-width="1" stroke-linecap="round"/>')

ICONS = {
"peak": (f'<path d="M4 35 L16 15 L20 6 L24 13 L28 16 L37 35Z" {ROCK} {ST}/>'
         f'<path d="M16 15 L20 6 L24 13 L28 16 L25.5 20 L22.5 17.5 L19.5 21 L16.5 18Z" {SNOW} {ST}/>'
         f'<path d="M22 22 L24 30 M18 26 L17 32" fill="none" stroke="var(--ink-2)" stroke-width=".9" opacity=".6"/>'
         f'<path d="M1 35 H39" fill="none" {ST}/>'),
"cog": (f'<path d="M1 35 L12 14 L17 21 L26 7 L39 35Z" {ROCK} {ST}/>'
        f'<path d="M9.2 19.3 L12 14 L14.6 17.6 L12.5 19 L11 17.5Z M22.7 12.4 L26 7 L29.6 14.3 L27 13 L25 15.5Z" {SNOW} {ST}/>'
        f'<path d="M5 35 L33 22.5" fill="none" stroke="var(--ink-2)" stroke-width="1.6" stroke-dasharray="1.6 1.4"/>'
        f'<g transform="translate(15 26.6) rotate(-24)"><rect x="-6.5" y="-6" width="13" height="7" rx="1.6" {RED} {ST}/>'
        f'<rect x="-4.6" y="-4.4" width="3.4" height="2.4" fill="var(--page)"/><rect x="1" y="-4.4" width="3.4" height="2.4" fill="var(--page)"/></g>'),
"glacier": (f'<path d="M1 35 L9 11 L17 33Z" {ROCK} {ST}/><path d="M39 35 L31 9 L23 33Z" {ROCK} {ST}/>'
            f'<path d="M12 9 Q20 4 28 9 Q25 22 23.5 35 H16.5 Q15 22 12 9Z" {SNOW} {ST}/>'
            f'<path d="M15.5 15 Q20 17.5 24.5 15 M16.2 21.5 Q20 23.5 23.6 21.5 M16.8 28 Q20 29.6 23.2 28" fill="none" stroke="#7FA6BF" stroke-width="1.2" stroke-linecap="round"/>'),
"castle": (_waves(32) +
           f'<rect x="7" y="19" width="26" height="13" {STONE} {ST}/>'
           f'<rect x="10" y="13" width="6" height="19" {STONE} {ST}/><rect x="24" y="10" width="7" height="22" {STONE} {ST}/>'
           f'<path d="M9.3 13 L13 6.5 L16.7 13Z M23.2 10 L27.5 2.5 L31.8 10Z M17 19 L20 15.5 L23 19Z" {RED} {ST}/>'
           f'<path d="M12.2 17 h1.6 M26.6 14.5 h1.8 M19 23.5 h2" fill="none" stroke="var(--ink-2)" stroke-width="1.6"/>'),
"bridge": (_waves(30) +
           f'<path d="M1 27 L28 22 L28 25 L1 30Z" {WOOD} {ST}/>'
           f'<path d="M1 22.5 L28 17.5 L28 20 L1 25Z" {RED} {ST}/>'
           f'<path d="M6 24.1 V28.3 M12 23 V27.2 M18 21.9 V26 M24 20.8 V24.9" fill="none" stroke="var(--ink-2)" stroke-width="1"/>'
           f'<path d="M28 31 V14 L30 12 H36 L38 14 V31Z" {STONE} {ST}/>'
           f'<path d="M27.5 13 L33 4.5 L38.5 13Z" {RED} {ST}/>'
           f'<path d="M32 18 v2.4 M32 24 v2.4" fill="none" stroke="var(--ink-2)" stroke-width="1.6"/>'),
"waterfall": (f'<path d="M1 13 L14 11 L15 35 L1 35Z" {ROCK} {ST}/><path d="M25 9 L39 12 L39 35 L25 35Z" {ROCK} {ST}/>'
              f'<path d="M14 11 Q19.5 9 25 9 L25 29 Q19.5 31 15 29Z" {WAT} {ST}/>'
              f'<path d="M17 13 V27 M20 11.5 V28.5 M23 11 V27" fill="none" stroke="var(--page)" stroke-width="1.3" stroke-linecap="round"/>'
              f'<circle cx="15.5" cy="31" r="3.3" {SNOW} {ST}/><circle cx="20.5" cy="32.2" r="3.8" {SNOW} {ST}/><circle cx="25.5" cy="31" r="3.2" {SNOW} {ST}/>'),
"tower": (f'<rect x="3" y="22" width="10" height="13" {SNOW} {ST}/><path d="M2 22 L8 16.5 L14 22Z" {RED} {ST}/>'
          f'<rect x="27" y="23" width="10" height="12" {SNOW} {ST}/><path d="M26 23 L32 17.5 L38 23Z" {RED} {ST}/>'
          f'<rect x="14" y="11" width="12" height="24" {STONE} {ST}/><path d="M13 11 L20 2 L27 11Z" {RED} {ST}/>'
          f'<circle cx="20" cy="18" r="3.7" {SNOW} {ST}/><path d="M20 18 V15.6 M20 18 L21.8 19" fill="none" stroke="var(--ink-2)" stroke-width="1"/>'
          f'<path d="M17.4 35 V29.5 Q20 26.5 22.6 29.5 V35" fill="var(--ink-2)" opacity=".75"/>'
          f'<path d="M1 35 H39" fill="none" {ST}/>'),
"fountain": (_waves(33) +
             f'<path d="M18.6 33 Q19.2 17 20 4 Q20.8 17 21.4 33Z" {SNOW} stroke="#7FA6BF" stroke-width="1.2" stroke-linejoin="round"/>'
             f'<path d="M20.6 5 Q26 7 28.5 15 M21 9 Q25 11 26.5 18" fill="none" stroke="#7FA6BF" stroke-width="1.1" stroke-dasharray="1.2 1.8" stroke-linecap="round"/>'
             f'<path d="M14 33 H26 L25 30.5 H15Z" {STONE} {ST}/>'),
"vineyard": (_waves(31) +
             f'<path d="M1 31 V15 Q15 8 39 5 V31Z" fill="#CFD8B0" {ST}/>'
             f'<path d="M2 28 Q18 23 38 21 M2 24.5 Q17 18.5 38 16 M3 21 Q16 15 38 11 M6 17.5 Q18 12 38 7.5" fill="none" style="stroke:var(--matcha)" stroke-width="1.5" stroke-dasharray="2.2 1.4"/>'
             f'<rect x="8" y="21.5" width="5" height="5" {SNOW} {ST}/><path d="M7.4 21.5 L10.5 18.5 L13.6 21.5Z" {RED} {ST}/>'
             f'<path d="M30 15 V8.5 L31.6 4.5 L33.2 8.5 V15Z" {SNOW} {ST}/>'),
"boat": (_waves(30) +
         f'<path d="M4 25 H36 L32.5 31 H8Z" {SNOW} {ST}/><path d="M5.5 27.6 H35" fill="none" style="stroke:var(--shu)" stroke-width="1.6"/>'
         f'<rect x="10" y="19" width="19" height="6" {SNOW} {ST}/>'
         f'<path d="M12.5 21.3 h2 M17 21.3 h2 M21.5 21.3 h2 M26 21.3 h1" fill="none" stroke="var(--ink-2)" stroke-width="1.5"/>'
         f'<rect x="17.5" y="12" width="4" height="7" fill="#E1B54B" {ST}/>'
         f'<circle cx="23" cy="8.6" r="2" fill="#E8E6DE" opacity=".9"/><circle cx="27" cy="6.2" r="2.6" fill="#E8E6DE" opacity=".8"/>'
         f'<path d="M33 25 V16 M33 16 L37 17.6 L33 19.2" fill="none" {ST}/><path d="M33 16 L37 17.6 L33 19.2Z" {RED}/>'),
"viaduct": (f'<path d="M1 37 Q10 31 20 36 Q30 31 39 37 V39 H1Z" {GRN} opacity=".55"/>'
            f'<path d="M3 19 H37 V37 H33 V30 Q31 25 29 30 V37 H25 V30 Q23 25 21 30 V37 H19 V30 Q17 25 15 30 V37 H11 V30 Q9 25 7 30 V37 H3Z" {STONE} {ST}/>'
            f'<path d="M3 23 H37" fill="none" stroke="var(--ink-2)" stroke-width=".9" opacity=".6"/>'
            f'<rect x="7" y="11.5" width="24" height="7" rx="2" {RED} {ST}/>'
            f'<path d="M10 14 h3 M15.5 14 h3 M21 14 h3 M26.5 14 h2" fill="none" stroke="var(--page)" stroke-width="2"/>'),
"cable": (f'<path d="M14 35 L28 12 L39 35Z" {ROCK} {ST}/><path d="M24.2 18.2 L28 12 L31.3 19 L28.5 17.5 L26.5 20Z" {SNOW} {ST}/>'
          f'<path d="M1 5 L39 15" fill="none" stroke="var(--ink-2)" stroke-width="1.3"/>'
          f'<path d="M16 9 V15" fill="none" {ST}/><circle cx="16" cy="9" r="1.4" fill="var(--ink-2)"/>'
          f'<rect x="9" y="15" width="14" height="12" rx="3" {RED} {ST}/>'
          f'<rect x="11" y="17.5" width="10" height="4" rx="1" fill="var(--page)"/>'
          f'<path d="M1 35 H39" fill="none" {ST}/>'),
}

def icon(kind, x, y, size=34):
    """Return the icon centred on (x, y) in map units."""
    s = size / 40
    return (f'<g class="ill" data-cx="{x:.1f}" data-cy="{y:.1f}"><g transform="translate({x - size / 2:.1f} {y - size / 2:.1f}) scale({s:.3f})">'
            f'<ellipse cx="20" cy="22" rx="21" ry="19" style="fill:var(--page)" opacity=".55"/>{ICONS[kind]}</g></g>')

# 景点 id → 插画；ROOT 用于总览图，其余按大区图使用（同一张图最多放 MAXN 个）
ROOT = ["matterhorn", "sphinx", "aletschglacier", "kapellbruecke", "chillon", "lavauxwalk", "jetdeau", "rheinfall",
        "zytglogge", "landwasser", "lagolugano", "rotair"]
KIND = {"matterhorn": "peak", "sphinx": "cog", "aletschglacier": "glacier", "kapellbruecke": "bridge", "chillon": "castle",
        "lavauxwalk": "vineyard", "jetdeau": "fountain", "rheinfall": "waterfall", "zytglogge": "tower", "landwasser": "viaduct",
        "lagolugano": "boat", "rotair": "cable", "gornergrat": "cog", "aiguilledumidi": "cable", "staubbach": "waterfall",
        "lakeboat": "boat", "schilthorn": "cable", "rigibahn": "cog", "seeboat": "boat", "castelli": "castle",
        "gruyerestown": "castle", "baslermuenster": "tower", "grossmuenster": "tower", "saentis": "cable",
        "brusio": "viaduct", "diavolezza": "glacier", "pilatusbahn": "cog"}
REGION = {
 "berner": ["sphinx", "staubbach", "lakeboat", "schilthorn"],
 "wallis": ["matterhorn", "aletschglacier", "gornergrat", "aiguilledumidi"],
 "luzern": ["kapellbruecke", "rigibahn", "rotair", "pilatusbahn"],
 "graubuenden": ["landwasser", "brusio", "diavolezza"],
 "ticino": ["lagolugano", "castelli"],
 "leman": ["chillon", "lavauxwalk", "jetdeau", "gruyerestown"],
 "zuerich": ["rheinfall", "grossmuenster", "saentis"],
 "bernbasel": ["zytglogge", "baslermuenster"],
}
