"""
Script: 04_generate_geographic_distribution_map.py
Author: Juan Esteban Montealegre

Description:
    Generates a global map showing the geographic distribution of
    Blastocystis 18S rRNA records by country based on curated metadata.

    The script:
        - Standardizes country names
        - Aggregates detected taxa by country
        - Merges metadata with a Natural Earth world shapefile
        - Assigns unique colors per country
        - Produces a publication-quality map with formatted taxon names

Input:
    - datos_blastocystis_corregido.csv

Output:
    - Figure_1_Blastocystis_distribution.pdf
    - Figure_1_Blastocystis_distribution.png (600 dpi)
    - Figure_1_Blastocystis_distribution.tiff (600 dpi)

# NOTE:
# This script assumes that metadata have been manually curated
# and that country names are consistent with Natural Earth standards.
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------
# 1. Cargar datos
# ---------------------------
df = pd.read_csv("datos_blastocystis_corregido.csv", sep=";")
df = df[['Organism', 'Country']].dropna()

# Limpieza fuerte
df['Country'] = (
    df['Country']
    .str.strip()
    .replace({
        "USA": "United States of America",
        "United States": "United States of America",
        "U.S.A.": "United States of America",
        "Czech Republic": "Czechia",
        "Iran, Islamic Republic of": "Iran",
        "Russian Federation": "Russia",
        "Republic of Korea": "South Korea"
    })
)
country_st = (
    df.groupby('Country')['Organism']
    .apply(lambda x: sorted(set(x)))
    .reset_index()
)

# ---------------------------
# 2. Cargar mapa mundial
world = gpd.read_file(
    "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
)

world['name'] = world['NAME'].str.strip()

world = world.merge(
    country_st,
    how='left',
    left_on='name',
    right_on='Country'
)

# ---------------------------
# 3. Asignar colores (MISMA PALETA)
# ---------------------------
countries_with_data = world.loc[world['Organism'].notna(), 'name'].unique()

import itertools

# Paleta base
base_colors = list(plt.get_cmap("tab20").colors)

# Eliminar grises (colores R≈G≈B)
base_colors = [
    c for c in base_colors
    if not (abs(c[0] - c[1]) < 0.02 and abs(c[1] - c[2]) < 0.02)
]

# Ciclo de colores
color_cycle = itertools.cycle(base_colors)

# Diccionario país → color
color_dict = {
    country: next(color_cycle)
    for country in sorted(countries_with_data)
}

# Asignar color al mapa
world['color'] = world['name'].map(color_dict)

# ---------------------------
# 4. Crear figura (MAPA MÁS PEQUEÑO)
# ---------------------------
fig, ax = plt.subplots(figsize=(10, 4.8))  # <- aquí se reduce el tamaño

# Países sin datos
world[world['Organism'].isna()].plot(
    ax=ax,
    color='lightgrey',
    edgecolor='black',
    linewidth=0.3
)

# Países con datos
world[world['Organism'].notna()].plot(
    ax=ax,
    color=world.loc[world['Organism'].notna(), 'color'],
    edgecolor='black',
    linewidth=0.3
)

# ---------------------------
def format_taxa(text):
    text = text.replace("Blastocystis spp.", r"$\it{Blastocystis}$ spp.")
    text = text.replace("Blastocystis sp.", r"$\it{Blastocystis}$ sp.")
    text = text.replace("B. hominis", r"$\it{B. hominis}$")
    text = text.replace("B. cycluri", r"$\it{B. cycluri}$")
    return text


# ---------------------------
# 5. Título
# ---------------------------
ax.set_title(
    "Geographic distribution of $\it{Blastocystis}$ spp. by country",
    fontsize=11
)

ax.axis("off")


# ---------------------------
# 6. Leyenda (lista de países + ST)
# ---------------------------
legend_patches = []

world_with_data = world[world['Organism'].notna()]

for _, row in world_with_data.iterrows():
    label = f"{row['name']}: {', '.join(row['Organism'])}"
    label = format_taxa(label)   # 👈 ESTA ES LA LÍNEA CLAVE
    legend_patches.append(
        mpatches.Patch(
            color=row['color'],
            label=label
        )
    )

ax.legend(
    handles=legend_patches,
    loc='center left',
    bbox_to_anchor=(1.02, 0.5),
    frameon=False,
    fontsize=8
)
import os

output_dir = "figuras_finales"
os.makedirs(output_dir, exist_ok=True)
# ---------------------------
# 7. Guardar en 3 formatos a 600 ppp
# ---------------------------

fig.savefig(
    os.path.join(output_dir, "Figure_1_Blastocystis_distribution.pdf"),
    bbox_inches="tight"
)

fig.savefig(
    os.path.join(output_dir, "Figure_1_Blastocystis_distribution.png"),
    dpi=600,
    bbox_inches="tight"
)

fig.savefig(
    os.path.join(output_dir, "Figure_1_Blastocystis_distribution.tiff"),
    dpi=600,
    bbox_inches="tight"
)

plt.show()