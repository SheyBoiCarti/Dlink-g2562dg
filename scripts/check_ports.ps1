<#
.SYNOPSIS
Read-only TCP discovery restricted to the owner's router.
.EXAMPLE
powershell -NoProfile -File .\check_ports.ps1
.NOTES
No authentication; no commands sent. Banner contents are withheld to avoid
accidentally recording secrets. Open TCP does not establish shell access.
#>
[CmdletBinding()]
param([ValidateSet('10.0.0.2')][string]$Router = '10.0.0.2')
$ErrorActionPreference = 'Stop'
if ($args.Count) { throw 'Unexpected arguments. Only 10.0.0.2 is allowed.' }
$labels = @{21='FTP candidate';22='SSH candidate';23='Telnet candidate';53='DNS candidate (TCP only)';80='HTTP candidate';443='HTTPS candidate';8080='HTTP candidate';8443='HTTPS candidate'}
Write-Output ('UTC ' + [DateTime]::UtcNow.ToString('o') + ' target=' + $Router)
foreach ($port in @(21,22,23,53,80,443,8080,8443)) {
    $client = [Net.Sockets.TcpClient]::new()
    $state = 'unknown'; $evidence = ''; $protocol = $labels[$port]
    try {
        $pending = $client.BeginConnect($Router,$port,$null,$null)
        if (-not $pending.AsyncWaitHandle.WaitOne(2000)) {
            $state = 'timeout'; $evidence = 'No TCP completion within 2000ms; filtering vs loss unknown'
        } else {
            $client.EndConnect($pending)
            $state = 'open'; $evidence = 'TCP connection completed from this LAN host'
            if ($port -in @(21,22,23)) {
                $stream = $client.GetStream(); $stream.ReadTimeout = 2000
                $buffer = New-Object byte[] 512
                try {
                    $count = $stream.Read($buffer,0,$buffer.Length)
                    $banner = [Text.Encoding]::ASCII.GetString($buffer,0,$count)
                    if ($banner -match '(?m)^SSH-[12]\.[0-9]+-[A-Za-z0-9_.-]+') {
                        $protocol = 'SSH'; $evidence += '; SSH identification received (value withheld)'
                    } elseif ($port -eq 21 -and $banner -match '^220[ -]') {
                        $protocol = 'FTP greeting'; $evidence += '; 220 greeting received (text withheld)'
                    } elseif ($count -gt 0) {
                        $evidence += '; greeting/negotiation bytes received; contents withheld'
                    } else { $evidence += '; peer closed without greeting' }
                } catch { $evidence += '; no readable greeting within 2000ms' }
            }
        }
    } catch {
        $cause = $_.Exception.GetBaseException()
        if ($cause -is [Net.Sockets.SocketException]) {
            if ($cause.SocketErrorCode -eq 'ConnectionRefused') { $state='closed' } else { $state='error' }
            $evidence = 'SocketError=' + $cause.SocketErrorCode
        } else { $state='error'; $evidence='Connection failed; details withheld' }
    } finally { $client.Dispose() }
    [pscustomobject]@{Port=$port; State=$state; Protocol=$protocol; Evidence=$evidence; Authentication='Not tested'}
    Start-Sleep -Milliseconds 200
}
if (Get-Command nmap -ErrorAction SilentlyContinue) {
    Write-Output 'Optional (not automatically executed): nmap -n -Pn -sT -p 21,22,23,53,80,443,8080,8443 --max-retries 0 --scan-delay 250ms --max-parallelism 1 --host-timeout 30s 10.0.0.2'
} else { Write-Output 'Nmap not installed; no installation attempted.' }
