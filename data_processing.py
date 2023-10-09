import geopandas as gpd
import folium
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

# Create a base map
m = folium.Map(location=[45.75, 126.65], zoom_start=10)

# Define a color mapping
color_map = {
    "airport-polygon": "yellow",
    "highway-line": "blue",
    "railway-line": "red",
    "water-polygon": "cyan",
    "vegetation-polygon": "green",
    "elevation-line": "brown",
    "nature_reserve-polygon": "lime",
    "land-polygon": "gray"
}

# Overlay features with specified colors
for feature, color in color_map.items():
    if feature in all_data:
        folium.GeoJson(
            all_data[feature],
            name=feature.split('-')[0].capitalize(),
            style_function=lambda feature, color=color: {
                'fillColor': color,
                'color': color,
                'weight': 1.5,
                'dashArray': '5, 5'
            }
        ).add_to(m)

# Add a layer control
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save("map_output.html")