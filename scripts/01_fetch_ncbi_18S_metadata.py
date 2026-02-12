"""
Script: 01_fetch_ncbi_18S_metadata.py
Author: Juan Esteban Montealegre
Description:
    Retrieves publicly available Blastocystis 18S rRNA records from GenBank
    and extracts accession number, organism name, host, and geographic origin.

Output:
    blastocystis_18S_metadata.csv

Note:
    This script uses the NCBI Entrez API via Biopython.
"""
# Importar bibliotecas necesarias
from Bio import Entrez, SeqIO
import pandas as pd

# Configurar tu correo electrónico (requerido por NCBI)
Entrez.email = "***@***.com"  # ¡Reemplaza con tu correo real!

# Función para buscar y extraer metadatos
def fetch_blastocystis_18S_metadata(max_records=3000):
    # Término de búsqueda: Blastocystis y gen 18S
    query = "(Blastocystis[Organism]) AND 18S[Title]"

    try:
        # Buscar en la base de datos Nucleotide
        handle = Entrez.esearch(db="nucleotide", term=query, retmax=max_records)
        record = Entrez.read(handle)
        handle.close()
        id_list = record["IdList"]

        if not id_list:
            print("No se encontraron secuencias para la búsqueda.")
            return None

        # Descargar archivos GenBank
        handle = Entrez.efetch(db="nucleotide", id=id_list, rettype="gb", retmode="text")
        records = list(SeqIO.parse(handle, "genbank"))
        handle.close()

        # Lista para almacenar metadatos
        metadata = []

        # Extraer metadatos de cada secuencia
        for seq_record in records:
            accession = seq_record.id
            organism = seq_record.annotations.get("organism", "N/A")
            host = "N/A"
            geo_loc = "N/A"

            # Buscar en las características (features) la información de source
            for feature in seq_record.features:
                if feature.type == "source":
                    host = feature.qualifiers.get("host", ["N/A"])[0]
                    geo_loc = feature.qualifiers.get("geo_loc_name", ["N/A"])[0]

            # Guardar los metadatos en la lista
            metadata.append({
                "Accession": accession,
                "Organism": organism,
                "Host": host,
                "Geo_loc_name": geo_loc
            })

        # Crear un DataFrame con pandas
        df = pd.DataFrame(metadata)
        return df

    except Exception as e:
        print(f"Error al acceder al NCBI: {e}")
        return None

# Ejecutar la función y mostrar resultados
if __name__ == "__main__":
    max_records = 3000  # Cambia este número para obtener más o menos resultados
    df = fetch_blastocystis_18S_metadata(max_records)

    if df is not None and not df.empty:
        print(df.head())  # Muestra las primeras filas en consola
        df.to_csv("blastocystis_18S_metadata.csv", index=False)
        print("Los metadatos se han guardado en 'blastocystis_18S_metadata.csv'")
    else:
        print("No se encontraron datos para mostrar.")