import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

def load_shapefiles(directory):
    shapefiles = {}
    for filename in os.listdir(directory):
        if filename.endswith(".shp"):
            filepath = os.path.join(directory, filename)
            layer_name = filename[:-4]  # Removing the .shp extension
            shapefiles[layer_name] = gpd.read_file(filepath)
    return shapefiles

def query_by_feature_type(feature_type, all_data):
    """
    Query the dataset by feature type and return the corresponding GeoDataFrame.

    Parameters:
    - feature_type (str): The type of feature to query (e.g., 'airport', 'parking', etc.)

    Returns:
    - GeoDataFrame: A GeoDataFrame containing the queried features.
    """
    feature_map = {
        'ports': 'ports-point',
        'parking': 'parking-polygon',
        'buildings': 'buildings-polygon',
        'airport': 'airport-polygon',
        'subway_entrances': 'subway_entrance-point',
        'settlements': 'settlements-polygon',
        'public_transport': 'public_transport-line'
    }

    if feature_type in feature_map:
        return all_data[feature_map[feature_type]]
    else:
        print(f"Feature type '{feature_type}' not found.")
        return None

# Load data
data_folder = "data"
all_data = load_shapefiles(data_folder)

# Testing the query_by_feature_type function
airports = query_by_feature_type('airport', all_data)
print(airports.head())  # Print the first few rows of the airports data

boundary_data = gpd.read_file(os.path.join(data_folder, 'boundary-polygon.shp'))

# Base Layer: Boundary of Harbin City
ax = boundary_data.plot(figsize=(15, 15), color='lightgray', edgecolor='black')

# Overlay Airports (if available in the dataset)
if "airport-polygon" in all_data:
    all_data["airport-polygon"].plot(ax=ax, color='yellow', label='Airports')

# Overlay Highways (if available in the dataset)
if "highway-line" in all_data:
    all_data["highway-line"].plot(ax=ax, color='blue', label='Highways', linewidth=0.5)

# Overlay Railways (if available in the dataset)
if "railway-line" in all_data:
    all_data["railway-line"].plot(ax=ax, color='red', label='Railways', linewidth=1)

#TOPOGRAPHY

# Overlay Water Bodies (if available in the dataset)
if "water-polygon" in all_data:
    all_data["water-polygon"].plot(ax=ax, color='cyan', label='Water Bodies')
    
# Overlay Vegetation
if "vegetation-polygon" in all_data:
    all_data["vegetation-polygon"].plot(ax=ax, color='green', label='Vegetation')

# Overlay Elevation Contours
if "elevation-line" in all_data:
    all_data["elevation-line"].plot(ax=ax, color='brown', label='Elevation Contours', linewidth=0.5)

# Overlay Nature Reserves
if "nature_reserve-polygon" in all_data:
    all_data["nature_reserve-polygon"].plot(ax=ax, color='lime', label='Nature Reserves', alpha=0.7)

# Overlay Landuse
if "land-polygon" in all_data:
    all_data["land-polygon"].plot(ax=ax, cmap='tab20b', label='Land', alpha=0.5)
    
#Custom legend
legend_elements = [
    Line2D([0], [0], color='yellow', lw=2, label='Airports'),
    Line2D([0], [0], color='blue', lw=2, label='Highways'),
    Line2D([0], [0], color='red', lw=2, label='Railways'),
    Line2D([0], [0], color='cyan', lw=2, label='Water Bodies'),
    Line2D([0], [0], color='green', lw=2, label='Vegetation'),
    Line2D([0], [0], color='brown', lw=2, label='Elevation Contours'),
    Line2D([0], [0], color='lime', lw=2, label='Nature Reserves'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10, label='Land')
]

# Set title and legend
plt.title('Harbin City with physical Features')
plt.legend(handles=legend_elements)
plt.show()