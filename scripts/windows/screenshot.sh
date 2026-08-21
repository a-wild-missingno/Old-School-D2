#!/usr/bin/env bash
# Capture the currently logged-in Windows desktop through a short-lived Interactive task.
set -euo pipefail
source "$(dirname "$0")/common.sh"
alias=${1:?usage: screenshot.sh <oracle|external-validation|external-trace> [local-png-path]}
runtime=$(require_runtime "$alias")
stamp=$(date -u +%Y%m%dT%H%M%SZ)
local_image=${2:-"$ROOT/artifacts/screenshots/$alias-$stamp.png"}
case "$local_image" in *.png|*.PNG) ;; *) echo 'local screenshot path must end in .png' >&2; exit 64;; esac
mkdir -p "$(dirname "$local_image")"
script_body='param([string]$OutputPath)
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
if ($bounds.Width -le 0 -or $bounds.Height -le 0) { throw "interactive desktop bounds unavailable" }
$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
try {
  $graphics.CopyFromScreen($bounds.X, $bounds.Y, 0, 0, $bounds.Size)
  $bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
  $graphics.Dispose()
  $bitmap.Dispose()
}'
local_script=$(mktemp)
trap 'rm -f "$local_script"' EXIT
printf '%s' "$script_body" > "$local_script"
remote_script="$runtime\\.lab-control-state\\screenshot-$stamp.ps1"
win_ps "New-Item -ItemType Directory -Force -Path (Split-Path -Parent $(ps_quote "$remote_script")) | Out-Null"
win_scp_to "$local_script" "$remote_script"
result=$(win_ps "\$root=$(ps_quote "$runtime"); \$scriptPath=$(ps_quote "$remote_script"); if (!(Test-Path -LiteralPath \$root -PathType Container)) { Write-Error 'RUNTIME_EXISTS=FAIL'; exit 2 }; if (!(Test-Path -LiteralPath \$scriptPath -PathType Leaf)) { Write-Error 'SCREENSHOT_SCRIPT=MISSING'; exit 3 }; \$shell=@(Get-CimInstance Win32_Process -Filter \"Name='explorer.exe'\" -ErrorAction SilentlyContinue | Sort-Object SessionId | Select-Object -First 1); if (\$shell.Count -ne 1) { Write-Error 'INTERACTIVE_SESSION=NONE'; exit 4 }; \$owner=Invoke-CimMethod -InputObject \$shell[0] -MethodName GetOwner; if ([string]::IsNullOrWhiteSpace(\$owner.User)) { Write-Error 'INTERACTIVE_SESSION_OWNER=UNKNOWN'; exit 5 }; \$state=Split-Path -Parent \$scriptPath; \$runId='$(printf '%s' "$stamp")'; \$imagePath=Join-Path \$state ('screenshot-' + \$runId + '.png'); \$identity=\$owner.Domain + '\\' + \$owner.User; \$taskName='OldSchoolD2Screenshot-' + \$runId; \$args='-NoProfile -NonInteractive -ExecutionPolicy Bypass -File ' + ('\"' + \$scriptPath + '\"') + ' -OutputPath ' + ('\"' + \$imagePath + '\"'); \$action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument \$args; \$principal=New-ScheduledTaskPrincipal -UserId \$identity -LogonType Interactive -RunLevel Limited; \$task=New-ScheduledTask -Action \$action -Principal \$principal; Register-ScheduledTask -TaskName \$taskName -InputObject \$task -Force | Out-Null; try { Start-ScheduledTask -TaskName \$taskName; \$ready=\$false; for (\$i=0; \$i -lt 30; \$i++) { Start-Sleep -Seconds 1; if ((Test-Path -LiteralPath \$imagePath -PathType Leaf) -and ((Get-Item -LiteralPath \$imagePath).Length -gt 0)) { \$ready=\$true; break } }; if (!\$ready) { \$info=Get-ScheduledTaskInfo -TaskName \$taskName -ErrorAction SilentlyContinue; Write-Error ('SCREENSHOT_CAPTURE=FAIL;TASK_RESULT=' + \$info.LastTaskResult); exit 6 }; Write-Output 'SCREENSHOT_CAPTURE=PASS'; Write-Output ('REMOTE_SCREENSHOT_PATH=' + \$imagePath); Write-Output ('INTERACTIVE_SESSION_ID=' + \$shell[0].SessionId); Write-Output ('INTERACTIVE_OWNER=' + \$identity) } finally { Unregister-ScheduledTask -TaskName \$taskName -Confirm:\$false -ErrorAction SilentlyContinue; Remove-Item -LiteralPath \$scriptPath -Force -ErrorAction SilentlyContinue }")
printf '%s\n' "$result"
remote_image=$(printf '%s\n' "$result" | awk -F= '/^REMOTE_SCREENSHOT_PATH=/{print substr($0, index($0,"=")+1); exit}')
[ -n "$remote_image" ] || { echo 'SCREENSHOT_RETRIEVAL=SKIPPED (capture did not return a PNG path)' >&2; exit 5; }
win_scp_from "$remote_image" "$local_image"
if [ ! -s "$local_image" ] || [ "$(head -c 8 "$local_image" | od -An -tx1 | tr -d ' \n')" != 89504e470d0a1a0a ]; then
  rm -f "$local_image"
  echo 'SCREENSHOT_RETRIEVAL=FAIL (download was not a PNG)' >&2
  exit 6
fi
win_ps "Remove-Item -LiteralPath $(ps_quote "$remote_image") -Force -ErrorAction Stop"
printf 'LOCAL_SCREENSHOT_PATH=%s\nSCREENSHOT_RETRIEVAL=PASS\n' "$local_image"
