# *Blastocystis* global analysis
Python-based reproducible pipeline for global analysis of *Blastocystis* subtype diversity based on 18S rRNA sequences.
## Repository structure

```text
data/          Raw and processed datasets used in the analysis
scripts/       Python scripts for data cleaning, integration, analysis, and visualization
results/       Generated tables and figures
docs/          Supplementary material and final figures
```
## Data source

This study is based on publicly available *Blastocystis* 18S rRNA sequences retrieved from GenBank.
Only sequences with clear subtype assignment and associated metadata (host and country of origin)
were included in the analysis. Sequences with ambiguous taxonomy, incomplete metadata, or low
sequence quality were excluded during the curation process.
