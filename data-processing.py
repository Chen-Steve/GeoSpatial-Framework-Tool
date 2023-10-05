import geopandas as gpd
import matplotlib.pyplot as plt
import os

def load_shapefiles(directory):
    shapefiles = {}
    for filename in os.listdir(directory):
        if filename.endswith(".shp"):
            filepath = os.path.join(directory, filename)
            layer_name = filename[:-4]  # Removing the .shp extension
            shapefiles[layer_name] = gpd.read_file(filepath)
    return shapefiles

# Load data
data_folder = "data"
all_data = load_shapefiles(data_folder)

# Visualize specific datasets
all_data["airport"].plot()
plt.title("Airports")
plt.show()