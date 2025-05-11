from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import MuongXen
from .forms import DateTimeSearchForm, MxMap

import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Patch
from matplotlib.collections import PatchCollection
import shapefile
from django.http import HttpResponse
import io
import numpy as np

def generate_map(request):
    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Set the bounds for your specific region (latitude: 19-20, longitude: 107-104)
    min_lat, max_lat = 19, 22.08
    min_lon, max_lon = 104, 109.1
    
    # Create a simple basemap (for demonstration)
    # In a real application, you would use proper map data
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Lượng mưa trong khu vực (Lat: 19-20, Lon: 104-107)')
    
    # Draw grid lines
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # If you have a shapefile, you can load and plot it like this:
    
    # Example shapefile loading (replace with your actual shapefile path)
    sf = shapefile.Reader("map/vn_shp.zip/vn.shp")
    
    for shape in sf.shapeRecords():
        points = shape.shape.points
        parts = shape.shape.parts
        
        patches = []
        for i in range(len(parts)):
            start = parts[i]
            if i == len(parts) - 1:
                end = len(points)
            else:
                end = parts[i + 1]
            polygon = Polygon(points[start:end])
            patches.append(polygon)
        
        pc = PatchCollection(patches, facecolor='lightblue', edgecolor='black', alpha=0.8)
        ax.add_collection(pc)
    # except:
    #     # Fallback simple rectangle if shapefile not found
    #     ax.add_patch(plt.Rectangle((min_lon, min_lat), 
    #                               max_lon-min_lon, max_lat-min_lat,
    #                               fill=False, edgecolor='blue', linewidth=2))
    #     print("shape file not found")
    
    try:
        # Load and process your data file
        data_file = "map/test-square000.txt"
        with open(data_file, 'r') as f:
            data = np.array([[float(x) for x in line.strip().split()] for line in f.readlines()[::-1]])
        
        # Create grid
        lons = np.arange(min_lon, max_lon, 0.1)
        lats = np.arange(min_lat, max_lat, 0.1)
        
        # Plot each cell with higher zorder
        for i in range(len(lats)-1):
            for j in range(len(lons)-1):
                value = data[i, j]
                color = 'white'  # default
                if value > 2.0:
                    color = 'red'
                elif value > 1.5:
                    color = 'orange'
                elif value > 1.0:
                    color = 'yellow'
                elif value > 0.2:
                    color = 'blue'
                else:
                    color = (0,0,0,0)
                
                # Create rectangle with higher zorder (foreground)
                rect = Rectangle((lons[j], lats[i]), 0.1, 0.1,
                                facecolor=color,
                                linewidth=0, # Slightly transparent
                                zorder=2)  # Higher zorder = foreground
                ax.add_patch(rect)
    
    except Exception as e:
        ax.text(0.5, 0.5, f"Data Error: {str(e)}", 
               ha='center', va='center', transform=ax.transAxes,
               zorder=3)

    legend_elements= [
    Patch(facecolor='red', label='Value > 2.0'),
    Patch(facecolor='orange', label='Value > 1.5'),
    Patch(facecolor='yellow', label='Value > 1.0'),
    Patch(facecolor='blue', label='Value > 0.5'),
    Patch(facecolor='white', label='Value ≤ 0.5')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Convert plot to PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    
    # Return the image as HTTP response
    return HttpResponse(buffer.getvalue(), content_type='image/png')

def main(request):
    return render(request, 'main.html')

# def generate_map(request):
#     # Create figure
#     fig, ax = plt.subplots(figsize=(10, 8))
    
#     # Your specified region (latitude: 19-20, longitude: 104-107)
#     min_lat, max_lat = 19, 22.08
#     min_lon, max_lon = 104, 109.1
    
#     # Create grid for 0.1×0.1 degree cells
#     lons = np.arange(min_lon, max_lon, 0.1)
#     lats = np.arange(min_lat, max_lat, 0.1)
    
#     # Load data from text file (replace with your actual file path)
#     data_file = "map/test-square000.txt"
    
#     try:
#         # Read data from file (space-separated values)
#         with open(data_file, 'r') as f:
#             data = []
#             for line in f:
#                 row = [float(x) for x in line.strip().split()]
#                 data.append(row)
#         data = np.array(data)
        
#         # Verify data dimensions match our grid
#         expected_rows = len(lats) - 1
#         expected_cols = len(lons) - 1
#         if data.shape != (expected_rows, expected_cols):
#             raise ValueError(f"Data shape {data.shape} doesn't match expected grid {expected_rows}x{expected_cols}")
        
#         # Plot each cell with appropriate color
#         for i in range(len(lats)-1):
#             for j in range(len(lons)-1):
#                 value = data[i, j]
#                 lat1, lat2 = lats[i], lats[i+1]
#                 lon1, lon2 = lons[j], lons[j+1]
                
#                 # Determine color based on value
#                 if value > 1.0:
#                     color = 'yellow'
#                 elif value > 0.5:
#                     color = 'blue'
#                 else:
#                     color = 'white'  # or whatever default color you prefer
                
#                 # Draw rectangle
#                 rect = plt.Rectangle((lon1, lat1), 
#                                    lon2-lon1, lat2-lat1,
#                                    facecolor=color, edgecolor='black', linewidth=0.5)
#                 ax.add_patch(rect)
                
#                 # Optional: Add value text
#                 # ax.text(lon1 + 0.05, lat1 + 0.05, f"{value:.1f}", 
#                 #        fontsize=6, color='black')
    
#     except Exception as e:
#         # Fallback if file loading fails
#         ax.text(0.5, 0.5, f"Error loading data: {str(e)}", 
#                ha='center', va='center', transform=ax.transAxes)
    
#     # Set plot properties
#     ax.set_xlim(min_lon, max_lon)
#     ax.set_ylim(min_lat, max_lat)
#     ax.set_xlabel('Longitude')
#     ax.set_ylabel('Latitude')
#     ax.set_title('Data Visualization (0.1×0.1 degree cells)')
    
#     # Add colorbar legend
#     from matplotlib.patches import Patch
#     legend_elements= [
#     Patch(facecolor='yellow', label='Value > 1.0'),
#     Patch(facecolor='blue', label='Value > 0.5'),
#     Patch(facecolor='white', label='Value ≤ 0.5')
#     ]
#     ax.legend(handles=legend_elements, loc='upper right')
    
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
#     plt.close(fig)
#     buffer.seek(0)
    
#     # Return the image as HTTP response
#     return HttpResponse(buffer.getvalue(), content_type='image/png')
