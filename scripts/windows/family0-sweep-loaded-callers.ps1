[CmdletBinding()]
param([Parameter(Mandatory = $true)][int]$TargetProcessId)
$ErrorActionPreference = 'Stop'
function U16([byte[]]$b,[int]$o){[BitConverter]::ToUInt16($b,$o)}
function U32([byte[]]$b,[int]$o){[BitConverter]::ToUInt32($b,$o)}
function U64([byte[]]$b,[int]$o){[BitConverter]::ToUInt64($b,$o)}
function I32([byte[]]$b,[int]$o){[BitConverter]::ToInt32($b,$o)}
Add-Type @'
using System; using System.Runtime.InteropServices;
public static class FamilyZeroReadOnlyMemory {
 [DllImport("kernel32.dll", SetLastError=true)] public static extern IntPtr OpenProcess(uint access, bool inherit, int pid);
 [DllImport("kernel32.dll", SetLastError=true)] public static extern bool ReadProcessMemory(IntPtr process, IntPtr address, byte[] buffer, IntPtr size, out IntPtr read);
 [DllImport("kernel32.dll", SetLastError=true)] public static extern bool CloseHandle(IntPtr handle);
}
public static class FamilyZeroAggregateScanner {
 static int I32(byte[] b,int o){return b[o]|(b[o+1]<<8)|(b[o+2]<<16)|(b[o+3]<<24);}
 static ulong U64(byte[] b,int o){ulong v=0;for(int i=0;i<8;i++)v|=((ulong)b[o+i])<<(8*i);return v;}
 public static long[] Scan(byte[] b,long rva,bool executable,long targetRva,ulong targetVa){
  long calls=0,jumps=0,pointers=0;
  for(int o=0;o<b.Length;o++){
   if(executable && o+5<=b.Length && (b[o]==0xE8 || b[o]==0xE9) && rva+o+5+(long)I32(b,o+1)==targetRva){if(b[o]==0xE8)calls++;else jumps++;}
   if(o+8<=b.Length && U64(b,o)==targetVa)pointers++;
  }
  return new long[]{calls,jumps,pointers};
 }
}
'@
$process=[Diagnostics.Process]::GetProcessById($TargetProcessId); $module=$process.MainModule
$handle=[FamilyZeroReadOnlyMemory]::OpenProcess(0x0410,$false,$TargetProcessId)
if($handle -eq [IntPtr]::Zero){throw 'PROCESS_OPEN=FAIL'}
function ReadMem([int64]$address,[int]$size){$buf=New-Object byte[] $size;$got=[IntPtr]::Zero;if(-not[FamilyZeroReadOnlyMemory]::ReadProcessMemory($handle,[IntPtr]$address,$buf,[IntPtr]$size,[ref]$got)){return $null};if($got.ToInt64() -ne $size){return $null};return ,$buf}
try {
 $base=$module.BaseAddress.ToInt64(); $header=ReadMem $base 4096
 if($null -eq $header -or $header[0] -ne 0x4d -or $header[1] -ne 0x5a){throw 'LOADED_PE=INVALID_DOS_HEADER'}
 $pe=I32 $header 0x3c;if($pe -lt 0 -or $pe+24 -ge $header.Length -or $header[$pe] -ne 0x50 -or $header[$pe+1] -ne 0x45){throw 'LOADED_PE=INVALID_NT_HEADER'}
 $n=U16 $header ($pe+6);$opt=U16 $header ($pe+20);$table=$pe+24+$opt;$sections=@()
 for($i=0;$i -lt $n;$i++){$o=$table+$i*40;if($o+40 -gt $header.Length){throw 'LOADED_PE=TRUNCATED_SECTION_TABLE'};$sections += [PSCustomObject]@{VA=U32 $header ($o+12);Size=U32 $header ($o+8);RawSize=U32 $header ($o+16);Flags=U32 $header ($o+36)}}
 $sig=[Collections.Generic.List[object]]::new();foreach($token in '4C 8B DC 55 57 49 8D AB ? ? ? ? 48 81 EC ? ? ? ? 48 8B 05 ? ? ? ? 48 33 C4 48 89 85 ? ? ? ? 49 89 5B ? 49 89 73 ? 4D 89 63 ? 4D 89 6B ? 4C 8B E9 4D 89 73 ? 4D 89 7B ? 48 89 4C 24 ? E8'.Split(' ')){if($token -eq '?'){[void]$sig.Add($null)}else{[void]$sig.Add([Convert]::ToByte($token,16))}}
 $matches=[Collections.Generic.List[uint32]]::new();$loaded=@()
 foreach($s in $sections){$len=[int][Math]::Max([int64]$s.Size,[int64]$s.RawSize);if($len -le 0){continue};$data=ReadMem ($base+[int64]$s.VA) $len;if($null -eq $data){continue};$loaded += [PSCustomObject]@{VA=$s.VA;Data=$data;Flags=$s.Flags};for($o=0;$o -le $data.Length-$sig.Count;$o++){$ok=$true;for($j=0;$j -lt $sig.Count;$j++){if($null -ne $sig[$j] -and$data[$o+$j] -ne $sig[$j]){$ok=$false;break}};if($ok){$matches.Add([uint32]($s.VA+$o))}}}
 Write-Output 'LOADED_PROCESS_ANALYSIS=READ_ONLY';Write-Output ('TARGET_SIGNATURE_MATCHES='+$matches.Count)
 if($matches.Count -ne 1){exit 0};$target=$matches[0];$targetVa=[uint64]($base+[int64]$target)
 $directCalls=0;$tailJumps=0;$pointerReferences=0
 foreach($s in $loaded){$counts=[FamilyZeroAggregateScanner]::Scan($s.Data,[int64]$s.VA,(($s.Flags -band 0x20000000) -ne 0),[int64]$target,[uint64]$targetVa);$directCalls+=$counts[0];$tailJumps+=$counts[1];$pointerReferences+=$counts[2]}
 Write-Output ('DIRECT_REL32_CALLERS='+$directCalls);Write-Output ('DIRECT_REL32_TAIL_JUMPS='+$tailJumps);Write-Output ('ABSOLUTE_POINTER_REFERENCES='+$pointerReferences)
} finally { [void][FamilyZeroReadOnlyMemory]::CloseHandle($handle) }
