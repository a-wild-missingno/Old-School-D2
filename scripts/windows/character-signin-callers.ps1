[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$Exe)
$ErrorActionPreference = 'Stop'
function U16([byte[]]$b,[int]$o){[BitConverter]::ToUInt16($b,$o)}
function U32([byte[]]$b,[int]$o){[BitConverter]::ToUInt32($b,$o)}
function I32([byte[]]$b,[int]$o){[BitConverter]::ToInt32($b,$o)}
if(-not(Test-Path -LiteralPath $Exe -PathType Leaf)){throw 'EXECUTABLE=NOT_FOUND'}
$b=[IO.File]::ReadAllBytes($Exe)
if($b.Length -lt 64 -or $b[0] -ne 0x4d -or $b[1] -ne 0x5a){throw 'PE=INVALID_DOS_HEADER'}
$pe=I32 $b 0x3c
if($pe -lt 0 -or $pe+24 -ge $b.Length -or $b[$pe] -ne 0x50 -or $b[$pe+1] -ne 0x45){throw 'PE=INVALID_NT_HEADER'}
$n=U16 $b ($pe+6); $opt=U16 $b ($pe+20); $table=$pe+24+$opt; $sections=@()
for($i=0;$i -lt $n;$i++){$o=$table+$i*40;if($o+40 -gt $b.Length){throw 'PE=TRUNCATED_SECTION_TABLE'};$sections += [PSCustomObject]@{VA=U32 $b ($o+12);Size=U32 $b ($o+16);Raw=U32 $b ($o+20);Flags=U32 $b ($o+36)}}
function Rva([int]$raw){foreach($s in $sections){if($raw -ge [int64]$s.Raw -and $raw -lt ([int64]$s.Raw+[int64]$s.Size)){return [uint32]($s.VA+($raw-$s.Raw))}};throw 'PE=RAW_OFFSET_OUTSIDE_SECTION'}
# Exact source-hook signature; ? retains only displacement/frame wildcards.
$sig=[Collections.Generic.List[object]]::new(); foreach($token in '40 53 48 83 EC ? 48 8B D9 C7 41 38 FF FF FF FF 66 C7 41 3C 00 00 33 D2'.Split(' ')){if($token -eq '?'){[void]$sig.Add($null)}else{[void]$sig.Add([Convert]::ToByte($token,16))}}
$matches=[Collections.Generic.List[int]]::new()
foreach($s in $sections){$start=[int]$s.Raw;$end=[Math]::Min([int64]$b.Length,[int64]$s.Raw+[int64]$s.Size);for($o=$start;$o -le $end-$sig.Count;$o++){$ok=$true;for($j=0;$j -lt $sig.Count;$j++){if($null -ne $sig[$j] -and $b[$o+$j] -ne $sig[$j]){$ok=$false;break}};if($ok){$matches.Add($o)}}}
Write-Output 'STATIC_ANALYSIS=READ_ONLY'
Write-Output ('IMAGE_SHA256='+(Get-FileHash -Algorithm SHA256 -LiteralPath $Exe).Hash.ToLowerInvariant())
Write-Output ('TARGET_SIGNATURE_MATCHES='+$matches.Count)
if($matches.Count -ne 1){exit 0}
$target=Rva $matches[0];Write-Output ('TARGET_RVA=0x{0:X}' -f $target)
$callers=[Collections.Generic.List[uint32]]::new()
foreach($s in $sections){$start=[int]$s.Raw;$end=[Math]::Min([int64]$b.Length,[int64]$s.Raw+[int64]$s.Size);for($o=$start;$o -le $end-5;$o++){if($b[$o]-ne 0xE8){continue};$r=Rva $o;$dst=[int64]$r+5+(I32 $b ($o+1));if($dst -eq [int64]$target){$callers.Add($r)}}}
Write-Output ('DIRECT_REL32_CALLERS='+$callers.Count)
if($callers.Count -eq 0){Write-Output 'NO_DIRECT_CALLER=YES'}else{$xs=$callers|select -First 16|%{'0x{0:X}' -f $_};Write-Output ('CALLER_RVAS='+($xs -join ','));if($callers.Count -gt 16){Write-Output 'CALLER_RVAS_TRUNCATED=YES'}}
