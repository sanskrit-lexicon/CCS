# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**CCS** is the corrections and research repository for the Cologne digitization of Cappeller's *Sanskrit-Wörterbuch* (German edition, 1887). The canonical source lives in `csl-orig/v02/ccs/ccs.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `verbs01/` | Root identification: maps CCS verb entries to MW root spellings, identifies prefixed verbs |

### Verb root pipeline (`verbs01/`)

Identifies Cappeller (German) verb entries and maps them to their MW equivalents, with preverb (upasarga) resolution. See [CCS issue #1](https://github.com/sanskrit-lexicon/CCS/issues/1).

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/CCS/issues).

## Common Commands

### Apply line-level corrections (standard pattern)
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh ccs ../../CCSScan/2020
sh xmlchk_xampp.sh ccs
```

## Dependencies

- **Python 3**
- **ccs.txt** — in `$BASE/cologne/csl-orig/v02/ccs/ccs.txt`
