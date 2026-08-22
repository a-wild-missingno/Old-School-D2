[CmdletBinding()]
param([Parameter(Mandatory = $true)][int]$TargetProcessId)
$ErrorActionPreference='Stop'
function U16([byte[]]$b,[int]$o){[BitConverter]::ToUInt16($b,$o)}
function U32([byte[]]$b,[int]$o){[BitConverter]::ToUInt32($b,$o)}
function I32([byte[]]$b,[int]$o){[BitConverter]::ToInt32($b,$o)}
Add-Type @'
using System; using System.Runtime.InteropServices;
public static class ReadOnlyProcessMemory {
 [DllImport("kernel32.dll", SetLastError=true)] public static extern IntPtr OpenProcess(uint access, bool inherit, int pid);
 [DllImport("kernel32.dll", SetLastError=true)] public static extern bool ReadProcessMemory(IntPtr process, IntPtr address, byte[] buffer, IntPtr size, out IntPtr read);
 [DllImport("kernel32.dll", SetLastError=true)] public static extern bool CloseHandle(IntPtr handle);
}
'@
$process=[Diagnostics.Process]::GetProcessById($TargetProcessId); $module=$process.MainModule
$handle=[ReadOnlyProcessMemory]::OpenProcess(0x0410,$false,$TargetProcessId)
if($handle -eq [IntPtr]::Zero){throw 'PROCESS_OPEN=FAIL'}
function ReadMem([int64]$address,[int]$size){$buf=New-Object byte[] $size;$got=[IntPtr]::Zero;if(-not[ReadOnlyProcessMemory]::ReadProcessMemory($handle,[IntPtr]$address,$buf,[IntPtr]$size,[ref]$got)){return $null};if($got.ToInt64() -ne $size){return $null};return ,$buf}
try {
 $base=$module.BaseAddress.ToInt64(); $header=ReadMem $base 4096
 if($null -eq $header -or $header[0] -ne 0x4d -or $header[1] -ne 0x5a){throw 'LOADED_PE=INVALID_DOS_HEADER'}
 $pe=I32 $header 0x3c;if($pe -lt 0 -or $pe+24 -ge $header.Length -or $header[$pe] -ne 0x50 -or $header[$pe+1] -ne 0x45){throw 'LOADED_PE=INVALID_NT_HEADER'}
 $n=U16 $header ($pe+6);$opt=U16 $header ($pe+20);$table=$pe+24+$opt;$sections=@()
 for($i=0;$i -lt $n;$i++){$o=$table+$i*40;if($o+40 -gt $header.Length){throw 'LOADED_PE=TRUNCATED_SECTION_TABLE'};$sections += [PSCustomObject]@{VA=U32 $header ($o+12);Size=U32 $header ($o+8);RawSize=U32 $header ($o+16);Flags=U32 $header ($o+36)}}
 $sig=[Collections.Generic.List[object]]::new();foreach($token in '40 53 48 83 EC ? 48 8B D9 C7 41 38 FF FF FF FF 66 C7 41 3C 00 00 33 D2'.Split(' ')){if($token -eq '?'){[void]$sig.Add($null)}else{[void]$sig.Add([Convert]::ToByte($token,16))}}
 $matches=[Collections.Generic.List[uint32]]::new();$loaded=@();$readSections=0;$scannedBytes=[int64]0;$prefix4Matches=0
 foreach($s in $sections){$len=[int][Math]::Max([int64]$s.Size,[int64]$s.RawSize);if($len -le 0){continue};$data=ReadMem ($base+[int64]$s.VA) $len;if($null -eq $data){continue};$loaded += [PSCustomObject]@{VA=$s.VA;Data=$data;Flags=$s.Flags};$readSections++;$scannedBytes += $data.Length;for($o=0;$o -le $data.Length-$sig.Count;$o++){$ok=$true;if($data[$o] -eq 0x40 -and $data[$o+1] -eq 0x53 -and $data[$o+2] -eq 0x48 -and $data[$o+3] -eq 0x83){$prefix4Matches++};for($j=0;$j -lt $sig.Count;$j++){if($null -ne $sig[$j]-and$data[$o+$j] -ne $sig[$j]){$ok=$false;break}};if($ok){$matches.Add([uint32]($s.VA+$o))}}}
 Write-Output 'LOADED_MODULE_ANALYSIS=READ_ONLY';Write-Output ('MODULE_IMAGE_SIZE='+$module.ModuleMemorySize);Write-Output ('SECTIONS_READ='+$readSections);Write-Output ('BYTES_SCANNED='+$scannedBytes);Write-Output ('PREFIX4_MATCHES='+$prefix4Matches);Write-Output ('TARGET_SIGNATURE_MATCHES='+$matches.Count)
 if($matches.Count -ne 1){exit 0};$target=$matches[0];Write-Output ('TARGET_RVA=0x{0:X}' -f $target)
 $callers=[Collections.Generic.List[uint32]]::new();foreach($s in $loaded){if(($s.Flags -band 0x20000000) -eq 0){continue};for($o=0;$o -le $s.Data.Length-5;$o++){if($s.Data[$o] -ne 0xE8){continue};$dst=[int64]$s.VA+$o+5+(I32 $s.Data ($o+1));if($dst -eq [int64]$target){$callers.Add([uint32]($s.VA+$o))}}}
 Write-Output ('DIRECT_REL32_CALLERS='+$callers.Count);if($callers.Count -eq 0){Write-Output 'NO_DIRECT_CALLER=YES'}else{$xs=$callers|select -First 16|%{'0x{0:X}' -f $_};Write-Output ('CALLER_RVAS='+($xs -join ','));if($callers.Count -gt 16){Write-Output 'CALLER_RVAS_TRUNCATED=YES'}}
} finally { [void][ReadOnlyProcessMemory]::CloseHandle($handle) }
