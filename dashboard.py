import geopandas as gpd
import folium
from folium.plugins import Search
from data_processing import load_shapefiles

# Load the data
all_data = load_shapefiles("data")

# Initialize the map
m = folium.Map(location=[45.75, 126.65], zoom_start=10)  # Coordinates for Harbin

# List of features to add to the map
features = [
    {"name": "airport", "geom_type": "Point", "color": "blue"},
    {"name": "subway_entrance", "geom_type": "Point", "color": "red"},
    {"name": "buildings", "geom_type": "Polygon", "color": "green"},
    # Add more features as needed
]

for feature in features:
    feature_key = f"{feature['name']}-polygon" if feature['geom_type'] == "Polygon" else f"{feature['name']}-point"
    if feature_key in all_data:
        geojson_data = all_data[feature_key].to_json()
        folium.GeoJson(geojson_data, name=feature['name'], style_function=lambda x: {'fillColor': feature['color']}).add_to(m)
        
        # Add search functionality for each feature
        search = Search(
            layer=folium.GeoJson(geojson_data),
            geom_type=feature['geom_type'],
            placeholder=f"Search for {feature['name']}",
            collapsed=False,
        ).add_to(m)

# Add layer control to toggle on/off
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save("map.html")