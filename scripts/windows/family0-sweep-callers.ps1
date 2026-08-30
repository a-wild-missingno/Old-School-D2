[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$Exe)
$ErrorActionPreference = 'Stop'
function U16([byte[]]$b,[int]$o){[BitConverter]::ToUInt16($b,$o)}
function U32([byte[]]$b,[int]$o){[BitConverter]::ToUInt32($b,$o)}
function U64([byte[]]$b,[int]$o){[BitConverter]::ToUInt64($b,$o)}
function I32([byte[]]$b,[int]$o){[BitConverter]::ToInt32($b,$o)}
if(-not(Test-Path -LiteralPath $Exe -PathType Leaf)){throw 'EXECUTABLE=NOT_FOUND'}
$b=[IO.File]::ReadAllBytes($Exe)
if($b.Length -lt 64 -or $b[0] -ne 0x4d -or $b[1] -ne 0x5a){throw 'PE=INVALID_DOS_HEADER'}
$pe=I32 $b 0x3c
if($pe -lt 0 -or $pe+24 -ge $b.Length -or $b[$pe] -ne 0x50 -or $b[$pe+1] -ne 0x45){throw 'PE=INVALID_NT_HEADER'}
$n=U16 $b ($pe+6); $opt=U16 $b ($pe+20); $optStart=$pe+24
if((U16 $b $optStart) -ne 0x20b){throw 'PE=NOT_PE32_PLUS'}
$imageBase=U64 $b ($optStart+24); $table=$optStart+$opt; $sections=@()
for($i=0;$i -lt $n;$i++){$o=$table+$i*40;if($o+40 -gt $b.Length){throw 'PE=TRUNCATED_SECTION_TABLE'};$sections += [PSCustomObject]@{VA=U32 $b ($o+12);Size=U32 $b ($o+16);Raw=U32 $b ($o+20);Flags=U32 $b ($o+36)}}
function Rva([int]$raw){foreach($s in $sections){if($raw -ge [int64]$s.Raw -and $raw -lt ([int64]$s.Raw+[int64]$s.Size)){return [uint32]($s.VA+($raw-$s.Raw))}};throw 'PE=RAW_OFFSET_OUTSIDE_SECTION'}
# Exact source-hook signature. Wildcards retain only frame/displacement fields.
$sig=[Collections.Generic.List[object]]::new(); foreach($token in '4C 8B DC 55 57 49 8D AB ? ? ? ? 48 81 EC ? ? ? ? 48 8B 05 ? ? ? ? 48 33 C4 48 89 85 ? ? ? ? 49 89 5B ? 49 89 73 ? 4D 89 63 ? 4D 89 6B ? 4C 8B E9 4D 89 73 ? 4D 89 7B ? 48 89 4C 24 ? E8'.Split(' ')){if($token -eq '?'){[void]$sig.Add($null)}else{[void]$sig.Add([Convert]::ToByte($token,16))}}
$matches=[Collections.Generic.List[int]]::new()
foreach($s in $sections){$start=[int]$s.Raw;$end=[Math]::Min([int64]$b.Length,[int64]$s.Raw+[int64]$s.Size);for($o=$start;$o -le $end-$sig.Count;$o++){$ok=$true;for($j=0;$j -lt $sig.Count;$j++){if($null -ne $sig[$j] -and $b[$o+$j] -ne $sig[$j]){$ok=$false;break}};if($ok){$matches.Add($o)}}}
Write-Output 'STATIC_ANALYSIS=READ_ONLY'
Write-Output ('TARGET_SIGNATURE_MATCHES='+$matches.Count)
if($matches.Count -ne 1){exit 0}
$target=Rva $matches[0]
$targetVa=[uint64]($imageBase+[uint64]$target)
$directCalls=0;$tailJumps=0;$pointerReferences=0
foreach($s in $sections){
  $start=[int]$s.Raw;$end=[Math]::Min([int64]$b.Length,[int64]$s.Raw+[int64]$s.Size)
  $code=(([uint32]$s.Flags -band 0x20000000) -ne 0)
  for($o=$start;$o -le $end-5;$o++){
    if($code -and (($b[$o] -eq 0xE8) -or ($b[$o] -eq 0xE9))){$r=Rva $o;$dst=[int64]$r+5+(I32 $b ($o+1));if($dst -eq [int64]$target){if($b[$o] -eq 0xE8){$directCalls++}else{$tailJumps++}}}
    if($o -le $end-8 -and (U64 $b $o) -eq $targetVa){$pointerReferences++}
  }
}
Write-Output ('DIRECT_REL32_CALLERS='+$directCalls)
Write-Output ('DIRECT_REL32_TAIL_JUMPS='+$tailJumps)
Write-Output ('ABSOLUTE_POINTER_REFERENCES='+$pointerReferences)
