function Evalate-Process{
    $file, [System.Array]$arguments = $args;
    $psi = new-object System.Diagnostics.ProcessStartInfo $file;
    $psi.Arguments = $arguments;
    $psi.Verb = 'runas';
    $psi.WorkingDirectory = Get-Location;
    [System.Diagnostics.Process]::Start($psi);
}

Set-Alias sudof Evalate-Process


##############################
#.SYNOPSIS
#管理者権限で実行する関数群
#
#.DESCRIPTION
#Linuxのsudoのような、管理者権限で実行するための関数と、依存関数と、エイリアス。
#
#.EXAMPLE
#sudo New-Item -Type SymbolicLink -Name hoge -Target fuga
#
#.NOTES
#Pause関数の参考リンク https://qiita.com/twinkfrag/items/f3ecf79b68ea09eadec2
#Invoke-CommandRunAs,StartRunAs関数の参考リンク https://qiita.com/twinkfrag/items/3afb9032fd73eabe09be
##############################
function Pause
{
    if ($psISE) {
        $null = Read-Host 'Press Enter Key...'
    }
    else {
        Write-Host "Press Any Key..."
        (Get-Host).UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null
    }
}

function Invoke-CommandRunAs
{
    $cd = (Get-Location).Path
    $commands = "Set-Location $cd; Write-Host `"[Administrator] $cd> $args`"; $args; Pause; exit"
    $bytes = [System.Text.Encoding]::Unicode.GetBytes($commands)
    $encodedCommand = [Convert]::ToBase64String($bytes)
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoExit","-encodedCommand",$encodedCommand
}

Set-Alias sudo Invoke-CommandRunAs


function Start-RunAs
{
    $cd = (Get-Location).Path
    $commands = "Set-Location $cd; (Get-Host).UI.RawUI.WindowTitle += `" [Administrator]`""
    $bytes = [System.Text.Encoding]::Unicode.GetBytes($commands)
    $encodedCommand = [Convert]::ToBase64String($bytes)
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoExit","-encodedCommand",$encodedCommand
}

Set-Alias su Start-RunAs