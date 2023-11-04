import geopandas as gpd
import folium
import os


def load_shapefiles(directory):
    """
    Load shapefiles from a specified directory and return them as a dictionary.
    
    Parameters:
    - directory (str): The path to the directory containing the shapefiles.
    
    Returns:
    - dict: A dictionary where keys are the names of the shapefiles (without the .shp extension) and values are the loaded geospatial dataframes.
    """
    
    # Initialize an empty dictionary to store the loaded shapefiles
    shapefiles = {}
    
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory):
        
        # Check if the current file is a shapefile (i.e., has a .shp extension)
        if filename.endswith(".shp"):
            
            # Construct the full path to the shapefile
            filepath = os.path.join(directory, filename)
            
            # Extract the name of the shapefile without its .shp extension
            layer_name = filename[:-4]
            
            # Load the shapefile into a geospatial dataframe and store it in the dictionary
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
m = folium.Map(
    location=[45.75, 126.65], 
    zoom_start=10,
    tiles=None  # This is a less detailed, artistic-like base map
)

#---------------------------------------------
feature_location = [45.75, 126.65]  # Replace with the location you want

# Create a Popup object with HTML content
popup_html = """
<div>
    <h4>Harbin</h4>
        <p>Information about the Harbin...</p>
    <a href="#" onclick="window.parent.openSidebar('harbin');">More details...</a>
</div>
"""
popup = folium.Popup(html=popup_html, max_width=300)

# Create a Marker or another feature and add it to the map
folium.Marker(
    location=feature_location,
    popup=popup,
    tooltip='Click me for more info'
).add_to(m)
#---------------------------------------------
feature_location_saint_sophia = [45.771132, 126.627410] 

popup_html_saint_sophia = """
<div>
    <h4>Saint Sophia Cathedral</h4>
    <p>Chinese: 圣索菲亚教堂; pinyin: Shèng suǒfēiyà jiàotáng</p>
    <a href="#" onclick="window.parent.openSidebar('saint-sophia');">More details...</a>
</div>
"""
popup_saint_sophia = folium.Popup(html=popup_html_saint_sophia, max_width=300)

folium.Marker(
    location=feature_location_saint_sophia,
    popup=popup_saint_sophia,
    tooltip='Click me for more info'
).add_to(m)
#---------------------------------------------
feature_location_stalin_park = [45.78213, 126.61989]  

popup_html_stalin_park = """
<div>
    <h4>Harbin Stalin Park</h4>
    <p>Chinese: 哈尔滨市斯大林公园; pinyin: Hā'ěrbīn shì sīdàlín gōngyuán</p>
    <a href="#" onclick="window.parent.openSidebar('stalin-park');">More details...</a>
</div>
"""
popup_stalin_park = folium.Popup(html=popup_html_stalin_park, max_width=300)

folium.Marker(
    location=feature_location_stalin_park,
    popup=popup_stalin_park,
    tooltip='Click me for more info'
).add_to(m)
#---------------------------------------------
feature_location_volga_manor = [45.68227, 126.90797] 

popup_html_volga_manor = """
<div>
    <h4>Volga Manor</h4>
    <p>Chinese: 伏尔加庄园; pinyin: Fú'ěrjiā Zhuāngyuán</p>
    <a href="#" onclick="window.parent.openSidebar('volga-manor');">More details...</a>
</div>
"""
popup_volga_manor = folium.Popup(html=popup_html_volga_manor, max_width=300)

folium.Marker(
    location=feature_location_volga_manor,
    popup=popup_volga_manor,
    tooltip='Click me for more info'
).add_to(m)
#---------------------------------------------

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