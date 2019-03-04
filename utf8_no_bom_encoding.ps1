$list = ls -name ${hostname}*.xml | Sort-Object -Descending | Select-Object -First 1
$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding($False)
foreach ($i in $list){
    $a = Get-Content $i
    [System.IO.File]::WriteAllLines($i, $a, $Utf8NoBomEncoding)
}