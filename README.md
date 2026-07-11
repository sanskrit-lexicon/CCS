# CCS — Cappeller *Sanskrit-Wörterbuch* (1887)

_Created: 16-05-2026 · Last updated: 11-07-2026_

Development and correction repository for **Carl Cappeller's *Sanskrit-Wörterbuch***, a Sanskrit→German dictionary, part of the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) (CDSL). The canonical source text lives in [`csl-orig/v02/ccs/ccs.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/ccs/ccs.txt) (28,751 entries); this repository holds the development, correction, and enrichment work.

Based largely on the Petersburg Wörterbuch (CCS ⊆ PW ≈ 0.945 by headword containment); same author as CAE.

## Documentation

- [CLAUDE.md](https://github.com/sanskrit-lexicon/CCS/blob/main/CLAUDE.md) — repository guide and data-format reference.
- [DATA_DICTIONARY.md](https://github.com/sanskrit-lexicon/CCS/blob/main/DATA_DICTIONARY.md) — markup tag reference.
- [CONTRIBUTING.md](https://github.com/sanskrit-lexicon/CCS/blob/main/CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](https://github.com/sanskrit-lexicon/CCS/blob/main/CODE_OF_CONDUCT.md)
- Corrections follow the canonical CDSL workflow — see [`csl-corrections/docs/correction-workflow.md`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).

## Contents

| Path | Purpose |
|---|---|
| [`verbs01/`](https://github.com/sanskrit-lexicon/CCS/tree/main/verbs01) | Verb identification: maps verb entries to MW roots, with Devanāgarī renderings |
| [`prefaces/`](https://github.com/sanskrit-lexicon/CCS/tree/main/prefaces) | Front-matter OCR + English and Russian translations of the 1887 *Vorrede* |

## Usage example

A real entry from [`csl-orig/v02/ccs/ccs.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/ccs/ccs.txt) — line 88, the "akaRwaka" entry:

```
88:{#akaRwaka#}¦ dornen-, feindlos.
```

To correct the German gloss (e.g. `dornen-, feindlos` → `dornenlos, feindlos`, a compound-hyphenation fix), write a paired-line change file and apply it with `updateByLine.py` (full workflow: [`csl-corrections/docs/correction-workflow.md`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)):

```
; issueNNN: fix compound hyphenation in "akaRwaka" gloss
88 old {#akaRwaka#}¦ dornen-, feindlos.
88 new {#akaRwaka#}¦ dornenlos, feindlos.
```

```sh
python updateByLine.py ccs.txt change_88.txt ccs_corrected.txt
```

(Illustrative — no actual defect at this line; the workflow above is exact, only the fictitious hyphenation fix is invented to demonstrate the change-file mechanics.)

## Projects & Milestones

| Milestone | Open | Closed | Total |
|---|---|---|---|
| Dictionary to Book | 0 | 0 | 0 |
| Digitization Quality | 1 | 0 | 1 |
| Structured Data | 0 | 1 | 1 |
| Major Enhancements | 1 | 0 | 1 |
| **Total** | **2** | **1** | **3** |

```mermaid
pie showData
  title CCS issues by milestone
  "Digitization Quality" : 1
  "Structured Data" : 1
  "Major Enhancements" : 1
```

## Issues

```mermaid
pie showData
  title CCS issues by type
  "markup" : 1
  "scan-quality" : 1
  "content-enhancement" : 1
```

### Open

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| [1](https://github.com/sanskrit-lexicon/CCS/issues/1) | verbs01 | content-enhancement | medium | Major Enhancements |
| [2](https://github.com/sanskrit-lexicon/CCS/issues/2) | New CCS Scan | scan-quality | minor | Digitization Quality |

### Solved

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| [3](https://github.com/sanskrit-lexicon/CCS/issues/3) | [markup] Minor ccs.txt Markup Oddities | markup | minor | Structured Data |

## Labels

### Type labels

| Label | Meaning |
|---|---|
| `link-target` | Click-throughs from `<ls>` abbreviations to scanned PDF pages |
| `link-splitting` | Splitting combined `SOURCE N,N` refs into per-page links |
| `markup` | Normalising XML tag content |
| `text-correction` | Corrections to German/Sanskrit definitions or headwords |
| `content-enhancement` | New material or structural additions beyond correction |
| `encoding` | SLP1/IAST transcoding, character normalisation |
| `scan-quality` | Replacing blurry/skewed/missing scan pages |
| `bug` | Broken links, XML errors, broken downloads |
| `question` | Scholarly questions requiring research |

### Severity labels

| Label | Meaning |
|---|---|
| `minor` | Targeted fix — a handful of lines or a single file |
| `medium` | Standard unit of work — one batch of corrections |
| `hard` | Large effort spanning many sources or files |

Full label colours and the type→milestone mapping live in the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md).

## Contributors

| Contributor | Commits |
|---|---|
| [gasyoun (Mārcis Gasūns)](https://github.com/gasyoun) | 28 |
| [funderburkjim](https://github.com/funderburkjim) | 3 |

_Commit counts per the GitHub contributors API; excludes automated (Dependabot) commits._

## Source

- **Author**: Cappeller, Carl
- **Title**: *Sanskrit-Wörterbuch*
- **Place / Publisher**: Strassburg: Karl J. Trübner
- **Year(s)**: 1887
- **Language pair**: Sanskrit → German
- **Size (CDSL headword index)**: 28,751 entries
- **License (digital edition)**: CC BY-SA 4.0
- See [CITATION.cff](https://github.com/sanskrit-lexicon/CCS/blob/main/CITATION.cff) for machine-readable citation.

## Encoding

- UTF-8 (NFC) throughout.
- Sanskrit text in SLP1 transliteration, wrapped in `{#…#}`; German gloss / italic display text in `{%…%}`.
- Devanāgarī and IAST display forms are generated at display time, not stored in the source.

## How it works

```mermaid
flowchart LR
  S["Print scan"] -->|keyboarding| O["csl-orig/v02/ccs/ccs.txt"]
  O -->|updateByLine.py| C["change_*.txt corrections"]
  C --> O
  O --> V["verbs01/ verb identification"]
  O -->|csl-pywork build| X["ccs.xml"]
  X --> A["csl-app web display"]
```

## Front matter (`prefaces/`)

OCR transcription + English and Russian translations of the dictionary's front matter (title page, dedication, and the four-page *Vorrede*) of **Carl Cappeller**, *Sanskrit-Wörterbuch nach den Petersburger Wörterbüchern bearbeitet* (Strassburg 1887, Verlag von Karl J. Trübner).

- **Source language:** German (1887 orthography preserved verbatim). The preface is signed *Jena, 3 July 1887* by Carl Cappeller and the dictionary is dedicated to Otto Böhtlingk and Rudolph Roth.
- **Source:** Cologne csldoc scans — [CCS front-matter index](https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/ccspref.html). Digitizer running-header/footer stamps are omitted.
- Per-page files `ccsprefNN.md` (German) + `.en.md` / `.ru.md`; consolidated single-file editions [`ccspref_all.de.md`](https://github.com/sanskrit-lexicon/CCS/blob/main/prefaces/ccspref_all.de.md), [`ccspref_all.en.md`](https://github.com/sanskrit-lexicon/CCS/blob/main/prefaces/ccspref_all.en.md), [`ccspref_all.ru.md`](https://github.com/sanskrit-lexicon/CCS/blob/main/prefaces/ccspref_all.ru.md) built by [`build_combined.py`](https://github.com/sanskrit-lexicon/CCS/blob/main/prefaces/build_combined.py).
- Folder index: [`prefaces/README.md`](https://github.com/sanskrit-lexicon/CCS/blob/main/prefaces/README.md).
- Five Devanāgarī example words in the Vorrede (p. VII) are transcribed verbatim with their printed accent marks: अनन्यमानस, चतुर्धा, इष्टि, स्वयुज्, कथावशेष.

> **OCR run notes (2026-06-22)** — process retrospective, not part of the deliverable.
>
> Produced by the `/cologne-preface-ocr` skill (vision OCR + translation, single agent, synchronous).
>
> **Cost.** All work done in one foreground agent — no OCR/translation subagents were spawned. The cost is dominated by ~40 native-resolution crop reads (title/dedication bands, four dense single-column preface pages cut into 4–6 bands each, plus 3× zoom tiles to verify the five Devanāgarī words on p. VII). Main thread ≈ 0.6–0.8 M tokens total.
>
> **Time.** Wall-clock ≈ 15 min. Gated mainly by the gentle one-at-a-time scan download (server was recently throttling) and the iterative Devanāgarī word-tile zooming.
>
> **Technical lessons (reusable):**
> 1. 6 scans, all single embedded `_images/ccs_Page_0NN_Image_0002.png`; toctree order = filename order here (no swap).
> 2. Pages 03–06 are single-column dense prose (not two-column) — full-width native bands of ~780 px tall scale cleanly to ≤1900 px.
> 3. The five Devanāgarī example words on p. VII needed individual 3× tiles to pin the accent strokes (udātta vertical bar over इ in इष्टि and over यु in स्वयुज्); band-level reads were not enough.
> 4. Cappeller uses the long-ſ ligature in *Maſsstabe / bloſs / auſser / groſsen*; transcribed with `ſ`/`ſs` where printed.

## Timeline

| Period | Activity |
|---|---|
| 2020 | Repository activity begins (first tracked issues) |
| 2021 | Ongoing corrections, markup, and comparison work |
| 2026-05 | Issue taxonomy, citation metadata, documentation |
| 2026-06 | Front-matter OCR + EN/RU translation of the preface (`prefaces/`) |

---
*Issue taxonomy and documentation per the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md).*

_Dr. Mārcis Gasūns_
