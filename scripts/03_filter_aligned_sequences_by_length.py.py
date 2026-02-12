"""
Script: 03_filter_aligned_sequences_by_length.py
Author: Juan Esteban Montealegre

Description:
    Filters aligned Blastocystis 18S rRNA sequences to retain only those
    with ≥ 300 non-gap nucleotide positions (A, T, G, C).

Input:
    - blastocystis_18S_aligned.fasta

Output:
    - blastocystis_18S_aligned_300bp.fasta
    - eliminated_ids.txt
"""
from Bio import SeqIO

def base_count(seq):
    return sum(1 for base in seq if base.upper() in "ATGC")

# Cargar archivo alineado
records = list(SeqIO.parse("blastocystis_18S_aligned.fasta", "fasta"))

# Separar las secuencias filtradas y eliminadas
filtered = []
removed = []

for record in records:
    if base_count(record.seq) >= 300:
        filtered.append(record)
    else:
        removed.append(record)

# Guardar secuencias filtradas
SeqIO.write(filtered, "blastocystis_18S_aligned_300bp.fasta", "fasta")

# Guardar los IDs eliminados
with open("eliminated_ids.txt", "w") as f:
    for r in removed:
        f.write(r.id + "\n")

# Imprimir resumen
print(f"Se conservaron {len(filtered)} secuencias con >= 300 bp.")
print(f"Se eliminaron {len(removed)} secuencias por ser demasiado cortas.")