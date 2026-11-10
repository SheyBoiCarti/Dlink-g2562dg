# Core Findings & Validated Capabilities

This directory contains the confirmed technical capabilities, access methods, and live deployment statuses established on the target device (**D-Link DSL-G2562DG**, firmware `TK_1.00TK_V1.2.12ak_20221018`).

For raw logs and phase-by-phase investigation history, refer to [`archive/`](../archive/).

---

## Documents

| Document | Description |
|---|---|
| [`ROOT_ACCESS_VERIFIED.md`](ROOT_ACCESS_VERIFIED.md) | Verification and technical proof of `uid=0(admin)` root execution via CLI escape. |
| [`LIVE_TEST_RESULTS.md`](LIVE_TEST_RESULTS.md) | Verified live execution results for provisioning, rollback, and restart tolerance. |
| [`DEPLOYMENT_STATUS.md`](DEPLOYMENT_STATUS.md) | Baseline service status, socket listeners, and runtime verification metrics. |
| [`ACCESS_METHODS.md`](ACCESS_METHODS.md) | Evaluated device interfaces (SSH, Telnet CLI, Web GUI, UART) and ranking. |
| [`AUTHENTICATED_FOLLOWUP.md`](AUTHENTICATED_FOLLOWUP.md) | Post-authentication boundary tests and interface behavior analysis. |
| [`CONFIG_BACKUP_RESULTS.md`](CONFIG_BACKUP_RESULTS.md) | Web GUI backup encryption, decryption limits, and configuration inspection. |
| [`VERIFIED_COMMAND_OUTPUT.md`](VERIFIED_COMMAND_OUTPUT.md) | Sanitized command output and system information gathered under root privileges. |
