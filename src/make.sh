#!/bin/sh
# 瑞士旅行手帖：先算结构和地图（build.py，叠加共享资料库），再用通用引擎生成页面
set -e
cd "$(dirname "$0")"
python3 build.py
python3 /home/claude/techo/tools/build_book.py swiss
