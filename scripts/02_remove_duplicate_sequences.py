"""
Script: 02_remove_duplicate_sequences.py
Author: Juan Esteban Montealegre

Description:
    Removes duplicate Blastocystis 18S rRNA sequences based on sequence identity
    and synchronizes the associated metadata table accordingly.

Input:
    - sequence.fasta
    - blastocystis_18S_metadata.csv

Output:
    - blastocystis_18S_clean.fasta
    - blastocystis_18S_metadata_clean.csv
"""
from Bio import SeqIO
from collections import defaultdict
import pandas as pd

# Cargar todas las secuencias desde el archivo original
records = list(SeqIO.parse("sequence.fasta", "fasta"))

# Crear diccionario para detectar duplicados por secuencia
unique_seqs = {}
duplicates = []

for record in records:
    seq_str = str(record.seq).upper()  # normalizar a mayúsculas
    if seq_str not in unique_seqs:
        unique_seqs[seq_str] = record
    else:
        duplicates.append(record.id)

# Guardar solo las secuencias únicas en nuevo archivo FASTA
SeqIO.write(unique_seqs.values(), "blastocystis_18S_clean.fasta", "fasta")
print(f"Se eliminaron {len(duplicates)} secuencias duplicadas por contenido.")

# Cargar tabla de metadatos original
df = pd.read_csv("blastocystis_18S_metadata.csv")

# Obtener los IDs (accession) de las secuencias que quedaron
kept_ids = [record.id for record in unique_seqs.values()]

# Filtrar la tabla para conservar solo los que están en el archivo FASTA limpio
df_filtered = df[df["Accession"].isin(kept_ids)]

# Guardar la tabla sincronizada
df_filtered.to_csv("blastocystis_18S_metadata_clean.csv", index=False)
print("Tabla de metadatos filtrada y sincronizada con archivo FASTA.")