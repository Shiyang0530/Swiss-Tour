# 把同目录下的 瑞士旅行手帖_配图版.zip 解压到 _电子书（覆盖旧版本文件，不删除其他文件）
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$zip = Join-Path $root "瑞士旅行手帖_配图版.zip"
$dst = Join-Path $root "_电子书"
Expand-Archive -Path $zip -DestinationPath $dst -Force
Write-Host "已更新：$dst\index.html"
