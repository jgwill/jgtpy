# Command Line Reference

This page documents all command line interfaces provided by **jgtpy**.
Run any command with `--help` to see the full set of options.

| Command | Module | Purpose |
|---------|--------|---------|
| `jgtcli` | `jgtpy.jgtcli:main` | General tool for fetching and processing IDS/CDS/ADS data. |
| `cdscli` | `jgtpy.cdscli:main` | Manage Chaos Data Service files and related indicators. |
| `pds2cds` | `jgtpy.pds2cds:main` | Convert a PDS file to a CDS file. |
| `jgtmksg` (`mkscli`) | `jgtpy.JGTMKSG:main` | Generate market snapshots and charts. |
| `jgtads` (`adscli`) | `jgtpy.JGTADS:main` | Plot ADS analytics from CDS or PDS data. |
| `jgtids` (`idscli`) | `jgtpy.jgtapycli:main` | Create Indicator Data Service files. |
| `adsfromcds` | `jgtpy.adsfromcdsfile:main` | Plot ADS charts directly from cached CDS data. |
| `guidecli_jgtpy` | `jgtpy.jgtpy_guide_for_agent:main` | Display packaged guidance snippets for agents. |

Each command exposes numerous options for controlling data retrieval,
chart generation, and file management. Consult the project README for
installation instructions and see the examples in this repository for
usage patterns.
