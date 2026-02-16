# Blastocystis global 18S rRNA analysis

Python-based semi-reproducible pipeline for the global analysis of *Blastocystis* subtype diversity based on publicly available 18S rRNA sequences.

---

## Study design

This study was conducted as an in silico descriptive and comparative analysis using publicly available nucleotide sequences retrieved from GenBank.

The analytical workflow integrates sequence curation, phylogenetic reconstruction, and comparative metadata analysis to evaluate global subtype distribution and host associations.

---

## Workflow overview

The analytical workflow consisted of the following steps:

1. Retrieval of publicly available *Blastocystis* 18S rRNA records and associated metadata from GenBank.
2. Removal of duplicate sequences and synchronization of metadata.
3. Multiple sequence alignment using MAFFT.
4. Post-alignment filtering to retain sequences with ≥300 non-gap nucleotide positions.
5. Manual trimming of poorly aligned regions.
6. Phylogenetic reconstruction under the Maximum Likelihood framework.
7. Manual metadata curation and taxonomic classification.
8. Generation of global distribution maps and host association visualizations.

---

## Phylogenetic analysis

- Alignment performed with MAFFT v7 (`--auto`).
- Model selection conducted in MEGA v12 using BIC.
- Maximum Likelihood tree constructed under T92+G.
- Node support evaluated using Adaptive Bootstrap.
- Final tree visualized and annotated in iTOL.

---

## Metadata curation

Metadata fields (host, country, taxonomic classification) were manually curated and standardized prior to comparative analyses. Country names were harmonized to match Natural Earth administrative boundaries for spatial visualization.

---

## Repository structure

data/
- sequence.fasta
- blastocystis_18S_metadata.csv
- blastocystis_18S_noDuplicados.fasta → Sequences after duplicate removal
- blastocystis_18S_aligned.fasta → MAFFT alignment output
- blastocystis_18S_aligned_300bp.fasta → Alignment filtered (≥300 bp)
- blastocystis_18S_aligned_Trimed.fasta → Final manually trimmed alignment
- datos_blastocystis_corregido.csv → Manually curated metadata table
- blastocystis_tree.newick → Final Maximum Likelihood phylogenetic tree

scripts/ → Python scripts used in the study

figures/ → Main and supplementary figures

---

## Requirements

Python 3.9+

Install dependencies:

pip install -r requirements.txt

Required packages:

- biopython
- pandas
- matplotlib
- seaborn
- geopandas

---

## Reproducibility note

Sequence alignment, trimming, and phylogenetic reconstruction were performed using MAFFT, AliView, and MEGA, respectively. These steps are documented but were executed outside Python.

---

## Author

Juan Esteban Montealegre  
Undergraduate Researcher in Biology
