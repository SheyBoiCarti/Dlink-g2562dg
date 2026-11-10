#Requires -Version 5.1
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)][string]$Python,
    [string]$Config = "$env:LOCALAPPDATA\DLinkSSHRestore\config.toml"
)
$ErrorActionPreference = 'Stop'
$taskName = 'DLinkSSHRestore'
$description = 'DLinkSSHRestore Phase8 external RAM SSH monitor v1'
$pythonPath = (Resolve-Path -LiteralPath $Python).Path
$configPath = (Resolve-Path -LiteralPath $Config).Path
if ($pythonPath.Contains('"') -or $configPath.Contains('"')) { throw 'Invalid quoted path' }
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    throw 'A task with this name exists. Review/remove it explicitly before installing.'
}
# The current user's vault is required. Do not use SYSTEM or save a Windows password.
$userId = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "-m dlink_ssh_restore.cli --config `"$configPath`" watch" -WorkingDirectory (Split-Path -Parent $configPath)
$logon = New-ScheduledTaskTrigger -AtLogOn -User $userId
$startup = New-ScheduledTaskTrigger -AtStartup
$subscription = '<QueryList><Query Id="0" Path="Microsoft-Windows-NetworkProfile/Operational"><Select Path="Microsoft-Windows-NetworkProfile/Operational">*[System[EventID=10000]]</Select></Query></QueryList>'
# Load class metadata so the client-only instance retains its MSFT_TaskTrigger base type.
$eventClass = Get-CimClass -Namespace 'root/Microsoft/Windows/TaskScheduler' -ClassName 'MSFT_TaskEventTrigger'
$network = New-CimInstance -ClientOnly -CimClass $eventClass -Property @{ Enabled = $true; Subscription = $subscription }
$principal = New-ScheduledTaskPrincipal -UserId $userId -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -RunOnlyIfNetworkAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit ([TimeSpan]::Zero)
$task = New-ScheduledTask -Action $action -Trigger @($startup,$logon,$network) -Settings $settings -Principal $principal -Description $description
if ($PSCmdlet.ShouldProcess($taskName,'Register startup, logon and network monitor task (does not start it now)')) {
    Register-ScheduledTask -TaskName $taskName -InputObject $task | Out-Null
    Write-Output 'Task registered; no immediate restore was started. Interactive user session is required.'
}
