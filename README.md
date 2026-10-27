# InfraPilot

InfraPilot is a beginner-friendly, **read-only** Windows infrastructure diagnostic tool. Run one command to collect a simple local report about a computer's operating system, CPU and memory basics, disk free space, network configuration, and selected Windows services.

It is designed for learning and for initial troubleshooting—not as a replacement for monitoring, backups, security tooling, or professional incident response.

## What the first version checks

- Computer name, Windows version, architecture, CPU count, and available memory.
- Free space on mounted drives. A drive below 15% free is marked `WARNING` in the text report.
- Active network adapters, IP addresses, default gateway, and DNS configuration (when Windows networking cmdlets are available).
- The state of a few common services: Server, DNS Client, Remote Desktop Services, and Windows Time.

Every check is local and read-only. InfraPilot does **not** start or stop services, change settings, scan other computers, or send data anywhere.

## Before you start

You need Windows 10/11 or Windows Server, plus [Python 3.10 or newer](https://www.python.org/downloads/). No administrator account or paid service is needed for this MVP.

## Quick start (PowerShell)

1. Open PowerShell in the folder that contains this README.
2. Create a private project environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the project locally:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -e .
   ```

4. Run the diagnostic and save a local JSON report:

   ```powershell
   infrapilot --output reports\infrapilot-report.json
   ```

   Or use the included PowerShell helper:

   ```powershell
   .\scripts\Invoke-InfraPilot.ps1
   ```

`reports/` is intentionally ignored by Git because reports may contain internal hostnames, IP addresses, gateway addresses, DNS servers, and disk information. Review a report before sharing it.

## Example console output

```text
InfraPilot — Local Infrastructure Health Report
================================================
Computer: LAB-SERVER-01
OS: Windows Server (example)
Logical CPUs: 8
Memory: 50% used (16.0 GB available)

Disk space:
  [PASS] C:\ — 20.0% free (100.0 GB)

Selected services:
  [PASS] TermService: RUNNING

Network adapters found: 1

Privacy: this report was collected locally. InfraPilot did not upload it.
```

The JSON shape is shown in [examples/sample-report.json](examples/sample-report.json); it contains fictional data only.

## Custom service checks

Supply service names if your environment needs different checks:

```powershell
infrapilot --services TermService W32Time WinRM --output reports\server.json
```

Use service names, not display names. For example, Remote Desktop Services is `TermService`.

## Running the tests

Install Pytest once in your project environment, then run the test suite:

```powershell
python -m pip install pytest
python -m pytest
```

## Safe MVP plan

1. **Current milestone — collect facts safely.** Keep all checks local and read-only; learn how each value is collected.
2. **Next — explain the report.** Add documented rules such as “disk below 15% free needs attention.” Rules should say *what was observed*, not pretend to know the root cause.
3. **Then — improve reporting.** Add HTML output, timestamps for repeated runs, and a comparison view.
4. **Later — optional AI summary.** See [docs/AI_SUMMARY.md](docs/AI_SUMMARY.md). It must remain opt-in and redact sensitive values by default.

## Limits and safety notes

- The network portion reads Windows configuration; it does not test internet access, ping devices, or scan ports.
- A stopped service is a finding to investigate, not proof of a problem. Some services are intentionally stopped.
- Run on machines you own or are authorised to administer.
- Never commit real reports, passwords, API keys, event logs, customer details, or production IP-address plans.

## Publishing this project to GitHub

Nothing in this folder has been published. When you are ready, follow [docs/PUBLISHING.md](docs/PUBLISHING.md) to create an empty GitHub repository and upload this local project deliberately.

## License

InfraPilot is offered under the [MIT License](LICENSE). This is a practical first choice for a public learning project because it permits broad reuse while preserving the copyright and license notice. If you need a different legal outcome, choose a license before publishing.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Please use fictional or scrubbed examples in issues and pull requests.
