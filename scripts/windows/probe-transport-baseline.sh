#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
: "${OLD_SCHOOL_D2_BIND_HOST:?set OLD_SCHOOL_D2_BIND_HOST in local .env}"
DISCOVERY_PORTS=${OLD_SCHOOL_D2_DISCOVERY_PORTS:-"3074 3075"}
: "${OLD_SCHOOL_D2_HTTPS_PORT:?set OLD_SCHOOL_D2_HTTPS_PORT in local .env}"
ports_ps=$(printf '%s,' $DISCOVERY_PORTS); ports_ps=${ports_ps%,}
win_ps "\$hostName=$(ps_quote "$OLD_SCHOOL_D2_BIND_HOST"); \$discoveryPorts=@($ports_ps); foreach (\$port in \$discoveryPorts) { \$client=[System.Net.Sockets.UdpClient]::new(); try { \$client.Client.ReceiveTimeout=3000; [void]\$client.Send([byte[]](0,1,0,1),4,\$hostName,[int]\$port); \$remote=[System.Net.IPEndPoint]::new([System.Net.IPAddress]::Any,0); \$reply=\$client.Receive([ref]\$remote); if (\$reply.Length -eq 16 -and \$reply[0] -eq 0 -and \$reply[1] -eq 1 -and \$reply[2] -eq 0 -and \$reply[3] -eq 1) { Write-Output ('NAT_PROBE_REPLY=PASS;PORT=' + \$port + ';BYTES=' + \$reply.Length) } else { throw 'unexpected NatProbe reply shape' } } finally { \$client.Dispose() } }; \$tcp=[System.Net.Sockets.TcpClient]::new(); try { \$connect=\$tcp.BeginConnect(\$hostName,[int]$(ps_quote "$OLD_SCHOOL_D2_HTTPS_PORT"),\$null,\$null); if (!\$connect.AsyncWaitHandle.WaitOne(3000)) { throw 'HTTPS connect timed out' }; \$tcp.EndConnect(\$connect); Write-Output 'HTTPS_CONNECT=PASS' } finally { \$tcp.Dispose() }; Write-Output 'TRANSPORT_BASELINE=PASS'"
