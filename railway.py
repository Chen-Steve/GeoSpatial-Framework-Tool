import geopandas as gpd

def print_column_names(shapefile_path):
    try:
        # Load the shapefile into a GeoDataFrame
        gdf = gpd.read_file(shapefile_path)
        
        # Print the column names
        print(f"Column names for {shapefile_path}:")
        for column in gdf.columns:
            print(column)
        print("\n")
    except Exception as e:
        print(f"Error reading {shapefile_path}: {e}")

# Print column names for the specified shapefiles
print_column_names("data/railway-station-point.shp")
print_column_names("data/railway-line.shp")
print_column_names("data/building-polygon.shp")