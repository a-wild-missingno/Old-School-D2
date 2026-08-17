#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
ipv4=$(sysctl -n net.ipv4.ip_forward 2>/dev/null || echo unknown); ipv6=$(sysctl -n net.ipv6.conf.all.forwarding 2>/dev/null || echo unknown)
echo "IPV4_FORWARDING=$([ "$ipv4" = 0 ] && echo DISABLED || echo ENABLED_OR_UNKNOWN)"
echo "IPV6_FORWARDING=$([ "$ipv6" = 0 ] && echo DISABLED || echo ENABLED_OR_UNKNOWN)"
hosts=${LEGION_ISOLATION_PUBLIC_HOSTS:-1.1.1.1,8.8.8.8}
result=$(win_ps "\$hosts=$(ps_quote "$hosts").Split(','); \$open=@(); foreach(\$h in \$hosts) { \$c=New-Object Net.Sockets.TcpClient; try { \$ar=\$c.BeginConnect(\$h.Trim(),443,\$null,\$null); if(\$ar.AsyncWaitHandle.WaitOne(3000) -and \$c.Connected){\$open += \$h.Trim()} } catch {} finally {\$c.Close()} }; if(\$open.Count -eq 0){Write-Output 'LEGION_PUBLIC_HTTPS=BLOCKED'}else{Write-Output ('LEGION_PUBLIC_HTTPS=REACHABLE:' + (\$open -join ','))}")
printf '%s\n' "$result"
if [ "$ipv4" = 0 ] && [ "$ipv6" = 0 ] && grep -qx 'LEGION_PUBLIC_HTTPS=BLOCKED' <<<"$result"; then echo 'ISOLATION=PASS'; else echo 'ISOLATION=FAIL'; exit 1; fi
