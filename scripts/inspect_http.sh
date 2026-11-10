#!/usr/bin/env bash
# Usage: bash inspect_http.sh [10.0.0.2]. Requires Python 3 standard library.
# Four unauthenticated root GETs; no body, redirects, cookies or secrets printed.
set -euo pipefail
if (( $# > 1 )) || [[ ${1:-10.0.0.2} != 10.0.0.2 ]]; then
  echo 'Only target 10.0.0.2 is allowed.' >&2; exit 2
fi
command -v python3 >/dev/null || { echo 'Python 3 is required.' >&2; exit 1; }
python3 - <<'PY'
import datetime, http.client, json, re, ssl, time

def summarize_headers(status, headers):
    """Only emit constrained protocol metadata; never arbitrary header strings."""
    server = headers.get('Server', '')
    # Only recognizable public server products; never emit unknown banner text.
    products = re.findall(r'(?i)\b(?:nginx|Apache|lighttpd|uhttpd|Boa|GoAhead|RomPager|mini_httpd|thttpd)(?:/[0-9.]+)?\b', server)
    content_type = headers.get('Content-Type', '').split(';', 1)[0].strip().lower()
    if content_type not in ('text/html','text/plain','text/css','application/javascript','application/json','application/xhtml+xml'):
        content_type = 'present (value withheld)' if content_type else 'absent'
    challenge = headers.get('WWW-Authenticate', '').split(' ', 1)[0]
    if challenge not in ('Basic', 'Digest', 'Bearer', 'Negotiate'):
        challenge = 'present (scheme unrecognized)' if challenge else 'absent'
    return dict(status=status, server_products=products, server_header_present=bool(server),
                content_type=content_type, auth_challenge=challenge,
                cookie_header_present=bool(headers.get('Set-Cookie')),
                redirect_present=bool(headers.get('Location')))

def main():
    print('UTC ' + datetime.datetime.now(datetime.timezone.utc).isoformat() + ' target=10.0.0.2')
    for scheme, port in (('http',80),('https',443),('http',8080),('https',8443)):
        conn = (http.client.HTTPSConnection('10.0.0.2', port, timeout=3, context=ssl.create_default_context())
                if scheme == 'https' else http.client.HTTPConnection('10.0.0.2', port, timeout=3))
        result = dict(scheme=scheme,port=port)
        try:
            conn.request('GET', '/', headers={'User-Agent':'Owner-Phase2-ReadOnly','Connection':'close'})
            response = conn.getresponse()
            result.update(summarize_headers(response.status, response.headers))
            result['authentication'] = ('HTTP challenge observed' if response.status == 401 else
                'Forbidden; reason unknown' if response.status == 403 else 'Unknown; a login form or redirect may require authentication')
        except ssl.SSLCertVerificationError:
            result['error'] = 'TLS certificate verification failed; no insecure retry'
        except (OSError, http.client.HTTPException) as exc:
            result['error'] = type(exc).__name__  # Never print raw exceptions/URLs/headers.
        finally:
            conn.close()
        print(json.dumps(result))
        time.sleep(.2)

if __name__ == '__main__':
    main()
PY
