import geopandas as gpd
import os

# Read GADM Level-1 shapefile (provinces)
gdf = gpd.read_file("data/gadm_belgium/gadm41_BEL_2.shp")

# Check available fields
print(" Columns:", gdf.columns.tolist())

# Print unique province names (should be 10 + Brussels)
print(" Provinces (NAME_2):", gdf["NAME_2"].unique())

# Save GeoJSON with just the NAME_2 and geometry
gdf[["NAME_2", "geometry"]].rename(columns={"NAME_2": "name"}).to_file("data/belgium_provinces.geojson", driver="GeoJSON")
print(" Saved cleaned GeoJSON to data/belgium_provinces.geojson")
