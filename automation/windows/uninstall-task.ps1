#Requires -Version 5.1
[CmdletBinding(SupportsShouldProcess)]
param()
$ErrorActionPreference = 'Stop'
$taskName = 'DLinkSSHRestore'
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if (-not $task) { Write-Output 'Task absent'; return }
if ($task.Description -ne 'DLinkSSHRestore Phase8 external RAM SSH monitor v1') {
    throw 'Description differs; refusing to remove an unrelated task.'
}
if ($PSCmdlet.ShouldProcess($taskName,'Stop and unregister only this monitor task')) {
    Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Output 'Task removed. Router RAM state remains; use the reviewed rollback command separately.'
}
