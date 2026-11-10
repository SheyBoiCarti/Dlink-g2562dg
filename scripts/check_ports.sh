#!/usr/bin/env bash
# Usage: bash check_ports.sh [10.0.0.2]. Requires Python 3. No sudo needed.
set -euo pipefail
if (( $# > 1 )) || [[ ${1:-10.0.0.2} != 10.0.0.2 ]]; then
  echo 'Only target 10.0.0.2 is allowed.' >&2; exit 2
fi
command -v python3 >/dev/null || { echo 'Python 3 is required.' >&2; exit 1; }
python3 - <<'PY'
import datetime, errno, json, re, socket, time
print('UTC ' + datetime.datetime.now(datetime.timezone.utc).isoformat() + ' target=10.0.0.2')
labels = {21:'FTP candidate',22:'SSH candidate',23:'Telnet candidate',53:'DNS candidate (TCP only)',80:'HTTP candidate',443:'HTTPS candidate',8080:'HTTP candidate',8443:'HTTPS candidate'}
for port, protocol in labels.items():
    state, evidence = 'unknown', ''
    try:
        with socket.create_connection(('10.0.0.2', port), timeout=2) as conn:
            state, evidence = 'open', 'TCP connection completed from this host'
            if port in (21,22,23):
                conn.settimeout(2)
                try:
                    banner = conn.recv(512)
                    if re.search(rb'(?m)^SSH-[12]\.[0-9]+-[A-Za-z0-9_.-]+', banner):
                        protocol = 'SSH'; evidence += '; SSH identification received (value withheld)'
                    elif port == 21 and re.match(rb'^220[ -]', banner):
                        protocol = 'FTP greeting'; evidence += '; 220 greeting (text withheld)'
                    elif banner:
                        evidence += '; greeting/negotiation bytes received; contents withheld'
                    else:
                        evidence += '; peer closed without greeting'
                except OSError:
                    evidence += '; no readable greeting within 2s'
    except (TimeoutError, socket.timeout):
        state, evidence = 'timeout', 'No TCP completion within 2s; filtering vs loss unknown'
    except OSError as exc:
        state = 'closed' if exc.errno == errno.ECONNREFUSED else 'error'
        evidence = 'errno=' + str(exc.errno)
    print(json.dumps(dict(port=port,state=state,protocol=protocol,evidence=evidence,authentication='Not tested')))
    time.sleep(.2)
PY
if command -v nmap >/dev/null; then
  echo 'Optional (not executed): nmap -n -Pn -sT -p 21,22,23,53,80,443,8080,8443 --max-retries 0 --scan-delay 250ms --max-parallelism 1 --host-timeout 30s 10.0.0.2'
else
  echo 'Nmap not installed; no installation attempted.'
fi
