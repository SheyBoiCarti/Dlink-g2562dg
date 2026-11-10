# Reading the research

This repository includes the successful implementation and the investigation that led to it: unsuccessful access attempts, alternative explanations, temporary experiments, and sanitized evidence. Historical files are retained to explain the reasoning; their early conclusions do not describe the final result.

## Choose a starting point

- To reproduce access and SSH restoration, follow [the walkthrough](REPRODUCING.md), then [the operating guide](../automation/README.md).
- To understand the overall method, read [the research explanation](RESEARCH.md).
- To audit the evidence, follow the chronology below and open the linked JSON records from each report. See [publication and redaction notes](PUBLICATION.md) before interpreting them.
- To inspect the actual router changes, read [setup](../scripts/phase6a_setup.sh), [rollback](../scripts/phase6a_rollback.sh), and the controller's [provisioning code](../automation/src/dlink_ssh_restore/router.py).

## Investigation chronology

| Stage | Question and result | Start reading |
| --- | --- | --- |
| Initial research | Which hardware/firmware claims are documented, reported, or unknown? | [Phase 1](../archive/phase-1-reconnaissance/README.md), [sources](../archive/phase-1-reconnaissance/docs/SOURCES.md) |
| Network and web inspection | What is reachable? Open ports and banners did not prove Linux access. | [Phase 2](../archive/phase-history/PHASE2_RESULTS.md), [network reconnaissance](NETWORK_RECON.md), [web interface](WEB_INTERFACE.md) |
| Stock SSH | Could the normal account authenticate? Legacy negotiation worked; the attempted password login failed. | [Phase 3](../archive/phase-history/PHASE3_RESULTS.md), [SSH authentication](SSH_AUTHENTICATION.md) |
| Alternative access | What did Telnet/FTP expose? Was UART supported by actual board evidence? | [Phase 3B](../archive/phase-history/PHASE3B_RESULTS.md), [Phase 4](../archive/phase-history/PHASE4_RESULTS.md), [UART assessment](UART_ACCESS.md) |
| Root discovery | Did a firmware-derived CLI account reach a real Linux shell? Yes: UID 0. | [Root access proof](../findings/ROOT_ACCESS_VERIFIED.md), [configuration-backup limits](../findings/CONFIG_BACKUP_RESULTS.md) |
| Linux and Dropbear analysis | Which account and key path does this actual firmware use? | [Phase 5](../archive/phase-history/PHASE5_RESULTS.md), [environment](LINUX_ENVIRONMENT.md), [Dropbear analysis](DROPBEAR_ANALYSIS.md) |
| Temporary root SSH | Could a second stock daemon authenticate a client key without changing persistent storage? Yes. | [Phase 6A](../archive/phase-history/PHASE6A_RESULTS.md), [reference setup](../scripts/phase6a_setup.sh) |
| Interactive terminal | Was the failed PTY test a router defect? Controlled tests isolated client stdin handling. | [Phase 6B](../archive/phase-history/PHASE6B_RESULTS.md), [PTY diagnostics](SSH_PTY_DIAGNOSTICS.md) |
| Persistence assessment | What survives reboot, and who owns service/host-key startup? | [Phase 7](../archive/phase-history/PHASE7_RESULTS.md), [boot process](BOOT_PROCESS.md), [host keys](SSH_HOST_KEYS.md) |
| External restoration | How can Windows restore the temporary service with strict trust and scoped cleanup? | [Phase 8](../archive/phase-history/PHASE8_RESULTS.md), [controller source](../automation/src/dlink_ssh_restore) |
| Live deployment | Did restore, repeated restore, rollback, reboot recovery, monitoring, and scheduling work? | [Phase 9](../archive/phase-history/PHASE9_RESULTS.md), [live results](../findings/LIVE_TEST_RESULTS.md), [recorded deployment](../findings/DEPLOYMENT_STATUS.md) |

## Resolve apparent contradictions

Some reports contain a latest-result paragraph followed by preserved chronological notes. Read the latest result first, then treat earlier sections as historical. For example, initial documents say no shell was demonstrated, Phase 6A says the interactive terminal test failed, and early host-key notes say reboot rotation was untested. Later evidence establishes root, isolates the PTY test failure to client stdin, and records a changed host key after an owner-performed restart.

The curated walkthrough describes the final intended process. Historical approval gates, local paths, and old key directories are not installation instructions. The historical unencrypted test key is not supplied and is rejected by the final controller, which requires an encrypted key. A report saying a task was running describes the recorded investigation, not the current reader's machine or a fresh device check.

## Tooling and evidence

- [Historical controllers](../research/controllers/README.md) preserve experiment source as non-executable text, with their side effects and missing prerequisites explained.
- [Firmware metadata](../research/firmware/README.md) preserves provenance, node offsets, and a portable file manifest, without redistributing firmware contents.
- [Publication manifest](../research/PUBLICATION_MANIFEST.json) lists imported records. It is an inventory, not proof that historical observations can be repeated on other devices.

The original inline firmware extractor was recovered from local investigation history and is now [distributed with reproduction instructions](../research/firmware/README.md). Its output was verified against all original private artifacts. Only the exact recorded image is accepted; the restoration controller continues to require an existing authorized management credential. Earlier statements that the parser was unavailable describe the initial export and are superseded.
