"""
Script: 09_generate_host_distribution_figures.py
Author: Juan Esteban Montealegre

Description:
    Generates graphical summaries of Blastocystis 18S rRNA sequence classification
    and host distribution.

    The script produces:
        - Bar plot of sequence counts by classification status (ST, Species, Unclassified)
        - Pie charts showing host distribution for each subtype and species
        - Separate outputs for main figures (n ≥ 10) and supplementary material (n < 10)
        - High-resolution PNG (300 dpi) and TIFF (600 dpi) versions
        - A standalone legend figure for host categories

Input:
    - datos_blastocystis_corregido.csv

Output:
    - grafico_barras_clasificacion.png
    - Pie charts (.png and .tiff)
    - leyenda_hospedadores.png / .tiff

# NOTE:
# This script assumes that host names and classification categories
# have been previously standardized and curated.

"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === 1. Leer datos ===
df = pd.read_csv("datos_blastocystis_corregido.csv", sep=";")
df.columns = df.columns.str.strip()

# === 2. Gráfico de barras: número de secuencias por categoría taxonómica ===
conteo_class = df["Classification"].value_counts()
colores_barras = ['#222222', '#555555', '#999999']  # ST, Unclassified, Species

sns.set(style="white")
plt.figure(figsize=(5, 4))
ax = sns.barplot(x=conteo_class.index, y=conteo_class.values, palette=colores_barras)
ax.set_ylabel("Number of sequences", fontsize=12)
ax.set_xlabel("Classification status", fontsize=12)
ax.set_title("Sequence count by classification status", fontsize=14)

for i, value in enumerate(conteo_class.values):
    ax.text(i, value + 10, str(value), ha='center', fontsize=10)

sns.despine()
plt.tight_layout()
plt.savefig("grafico_barras_clasificacion.png", dpi=300)
plt.close()
print("✅ Gráfico de barras guardado como 'grafico_barras_clasificacion.png'")

# === 3. Colores para hospedadores ===
todos_hospedadores = df['Host'].dropna().unique()

n_hosts = len(todos_hospedadores)
colores_tab20 = sns.color_palette("tab20", 20).as_hex()

if n_hosts > 20:
    extra_colores = sns.color_palette("husl", n_hosts - 20).as_hex()
    colores_paleta = colores_tab20 + extra_colores
else:
    colores_paleta = colores_tab20[:n_hosts]

colores_hospedadores = dict(zip(sorted(todos_hospedadores), colores_paleta))

# === 4. Crear carpetas para salida ===
os.makedirs("graficas", exist_ok=True)
os.makedirs("material_suplementario", exist_ok=True)

# nuevas carpetas para TIFF
os.makedirs("graficas_tiff", exist_ok=True)
os.makedirs("material_suplementario_tiff", exist_ok=True)

# === 5. Función para gráficos de pastel ===
def graficar_pastel_modificado(df_filtrado, etiqueta, n_minimo=10):
    for grupo in df_filtrado['Organism'].unique():
        datos = df_filtrado[df_filtrado['Organism'] == grupo]
        conteo = datos['Host'].value_counts()

        # separar salidas según tamaño
        if conteo.sum() < n_minimo:
            carpeta_png = "material_suplementario"
            carpeta_tiff = "material_suplementario_tiff"
        else:
            carpeta_png = "graficas"
            carpeta_tiff = "graficas_tiff"

        colores = [colores_hospedadores[host] for host in conteo.index]

        # Formatear Species a itálica
        titulo_grupo = grupo
        if etiqueta == "Species" and grupo.startswith("B. "):
            especie = grupo.replace("B. ", "")
            titulo_grupo = r"$\it{" + especie + "}$"

        plt.figure(figsize=(7, 6))
        plt.pie(
            conteo.values,
            labels=None,
            startangle=90,
            textprops={'fontsize': 10},
            colors=colores
        )

        # título principal (aumentado tamaño)
        plt.title(
            rf"Host distribution of $\it{{Blastocystis}}$ {titulo_grupo} (n = {conteo.sum()})",
            fontsize=25
        )

        # leyenda solo para suplemento
        if carpeta_png == "material_suplementario":
            plt.legend(
                labels=conteo.index,
                title="Host",
                loc="center left",
                bbox_to_anchor=(1, 0.5),
                fontsize=10,
                title_fontsize=11
            )

        plt.axis('equal')
        plt.tight_layout()

        # guardar PNG estándar (300ppp)
        plt.savefig(
            os.path.join(carpeta_png, f"{grupo.replace(' ', '_')}.png"),
            dpi=300, bbox_inches='tight'
        )

        # guardar TIFF en 600ppp
        plt.savefig(
            os.path.join(carpeta_tiff, f"{grupo.replace(' ', '_')}.tiff"),
            dpi=600, format='tiff', bbox_inches='tight'
        )

        plt.close()
        print(f"✅ Guardado pastel de {grupo} en {carpeta_png} y {carpeta_tiff}")

print("Clasificaciones únicas:", df['Classification'].unique())
print(df.columns)

# === 6. Filtrar y generar gráficos ===
df_st = df[df['Classification'] == "ST"]
df_species = df[df['Classification'] == "Species"]

if len(df_st) > 0:
    graficar_pastel_modificado(df_st, "ST", n_minimo=10)

if len(df_species) > 0:
    graficar_pastel_modificado(df_species, "Species", n_minimo=10)

# === Crear figura única con la leyenda de hospedadores ===
fig_legend, ax = plt.subplots(figsize=(4, len(todos_hospedadores) * 0.35))

handles = [
    plt.Line2D(
        [0], [0],
        marker='o',
        linestyle='',
        markerfacecolor=colores_hospedadores[h],
        markersize=10
    )
    for h in sorted(todos_hospedadores)
]

# manejo de especie humana como itálica
labels = [
    r"$\it{Homo\ sapiens}$" if h == "Homo sapiens" else h
    for h in sorted(todos_hospedadores)
]

ax.legend(
    handles,
    labels,
    title="Host",
    loc='center',
    fontsize=16,
    title_fontsize=15,
    frameon=False
)

ax.axis('off')
plt.tight_layout()

# guardar PNG
plt.savefig(
    "leyenda_hospedadores.png",
    dpi=300,
    bbox_inches='tight'
)

# guardar TIFF
plt.savefig(
    "leyenda_hospedadores.tiff",
    dpi=600,
    format='tiff',
    bbox_inches='tight'
)

plt.close()
print("✅ Leyenda general guardada en PNG y TIFF")
