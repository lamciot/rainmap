from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import MuongXen
from .forms import DateTimeSearchForm, MxMap
import base64
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Patch
from matplotlib.collections import PatchCollection
import shapefile
from django.http import HttpResponse
import io
import numpy as np

# def generate_map(request):
#     # if request.method == 'POST':
#     #     form = DateTimeSearchForm(request.POST)
#     #     if form.is_valid():
#     #         search_dt = form.cleaned_data['date_time']
#     #         try:
#     #             entry = MuongXen.objects.get(date_time=search_dt)
#     #             return render(request, 'map.html', {'entry': entry})
#     #         except MuongXen.DoesNotExist:
#     #             return HttpResponse("No data found for this datetime")
#     # else:
#     #     form = DateTimeSearchForm()

#     # Create a figure
#     fig, ax = plt.subplots(figsize=(10, 8))
    
#     # Set the bounds for your specific region (latitude: 19-20, longitude: 107-104)
#     min_lat, max_lat = 19, 22.08
#     min_lon, max_lon = 104, 109.1
    
#     # Create a simple basemap (for demonstration)
#     # In a real application, you would use proper map data
#     ax.set_xlim(min_lon, max_lon)
#     ax.set_ylim(min_lat, max_lat)
#     ax.set_xlabel('Longitude')
#     ax.set_ylabel('Latitude')
#     ax.set_title('Lượng mưa trong khu vực')
    
#     # Draw grid lines
#     ax.grid(True, linestyle='--', alpha=0.7)
    
#     # If you have a shapefile, you can load and plot it like this:
    
#     # Example shapefile loading (replace with your actual shapefile path)
#     sf = shapefile.Reader("map/vn_shp.zip/vn.shp")
    
#     for shape in sf.shapeRecords():
#         points = shape.shape.points
#         parts = shape.shape.parts
        
#         patches = []
#         for i in range(len(parts)):
#             start = parts[i]
#             if i == len(parts) - 1:
#                 end = len(points)
#             else:
#                 end = parts[i + 1]
#             polygon = Polygon(points[start:end])
#             patches.append(polygon)
        
#         pc = PatchCollection(patches, facecolor='lightblue', edgecolor='black', alpha=0.8)
#         ax.add_collection(pc)
#     # except:
#     #     # Fallback simple rectangle if shapefile not found
#     #     ax.add_patch(plt.Rectangle((min_lon, min_lat), 
#     #                               max_lon-min_lon, max_lat-min_lat,
#     #                               fill=False, edgecolor='blue', linewidth=2))
#     #     print("shape file not found")
    
#     if request.method == 'POST':
#         date_time = request.POST.get('date_time')
#         print("DATETIME received!" + date_time)
#         # data_file = MuongXen.objects.values_list('data').filter(date_time = date_time)
#         # print(data_file)
#         data_file = "map/test-square000.txt"
#         with open(data_file, 'r') as f:
#             data = np.array([[float(x) for x in line.strip().split()] for line in f.readlines()[::-1]])
#     else:
#         print("Not yet POST")
#         form = DateTimeSearchForm()
#     try:
#         # Load and process your data file
#         # data_file = "map/test-square000.txt"
#         # data = np.array([[float(x) for x in line.strip().split()] for line in data_file.readlines()[::-1]])
#         # with open(data_file, 'r') as f:
#         #     data = np.array([[float(x) for x in line.strip().split()] for line in f.readlines()[::-1]])
        
#         # Create grid
#         lons = np.arange(min_lon, max_lon, 0.1)
#         lats = np.arange(min_lat, max_lat, 0.1)
        
#         # Plot each cell with higher zorder
#         for i in range(len(lats)-1):
#             for j in range(len(lons)-1):
#                 value = data[i, j]
#                 color = 'white'  # default
#                 if value > 2.0:
#                     color = 'red'
#                 elif value > 1.5:
#                     color = 'orange'
#                 elif value > 1.0:
#                     color = 'yellow'
#                 elif value > 0.5:
#                     color = 'dodgerblue'
#                 elif value > 0.2:
#                     color = 'blue'
#                 else:
#                     color = (0,0,0,0)
                
#                 # Create rectangle with higher zorder (foreground)
#                 rect = Rectangle((lons[j], lats[i]), 0.1, 0.1,
#                                 facecolor=color,
#                                 linewidth=0, # Slightly transparent
#                                 zorder=2)  # Higher zorder = foreground
#                 ax.add_patch(rect)
    
#     except Exception as e:
#         ax.text(0.5, 0.5, f"Data Error: {str(e)}", 
#                ha='center', va='center', transform=ax.transAxes,
#                zorder=3)

#     legend_elements= [
#     Patch(facecolor='red', label=' > 2.0'),
#     Patch(facecolor='orange', label=' > 1.5'),
#     Patch(facecolor='yellow', label=' > 1.0'),
#     Patch(facecolor='dodgerblue', label=' > 0.5'),
#     Patch(facecolor='blue', label=' > 0.2')
#     ]
#     ax.legend(handles=legend_elements, loc='upper right')
    
#     # Convert plot to PNG image
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
#     plt.close(fig)
#     buffer.seek(0)
    
#     # Return the image as HTTP response
#     return HttpResponse(buffer.getvalue(), content_type='image/html')
    # return render(buffer.getvalue(),'base.html',content_type='image/png')

# def base(request):
#     form = DateTimeSearchForm()
#     generate_map(request)
#     return render(request, ['map.html'],{'form':form})

def generate_map(request):
    if request.method == 'POST':
        selected_datetime = request.POST.get('datetime')
        request.session['selected_datetime'] = selected_datetime

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
    ax.set_title('Lượng mưa trong khu vực')
    
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
    
    if request.method == 'POST':
        date_time = request.POST.get('date_time')
        print("DATETIME received!" + date_time)
        # data_file = MuongXen.objects.values_list('data').filter(date_time = date_time)
        # print(data_file)
        data_file = "map/test-square000.txt"
        with open(data_file, 'r') as f:
            data = np.array([[float(x) for x in line.strip().split()] for line in f.readlines()[::-1]])
    else:
        print("Not yet POST")
        form = DateTimeSearchForm()
    try:
        # Load and process your data file
        data_file = "map/test-square000.txt"
        # data = np.array([[float(x) for x in line.strip().split()] for line in data_file.readlines()[::-1]])
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
                elif value > 0.5:
                    color = 'dodgerblue'
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
    Patch(facecolor='red', label=' > 2.0'),
    Patch(facecolor='orange', label=' > 1.5'),
    Patch(facecolor='yellow', label=' > 1.0'),
    Patch(facecolor='dodgerblue', label=' > 0.5'),
    Patch(facecolor='blue', label=' > 0.2')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Convert plot to PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    try:
    # Return the image as HTTP response
        request.session['map_image'] = base64.b64encode(buffer.getvalue()).decode('utf-8')
        request.session['image_generated'] = True
        return redirect('base')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=400)

    # return HttpResponse(buffer.getvalue(), content_type='image/png')


def base(request):
    image_generated = request.session.pop('image_generated', False)
    return render(request, ['map.html'],{'image_generated': image_generated,
                                        'selected_datetime': request.session.get('selected_datetime')})
def get_map_image(request):
    if 'map_image' in request.session:
        image_data = base64.b64decode(request.session['map_image'])
        # image_data = request.session['map_image']
        return HttpResponse(image_data, content_type='image/png')
    return HttpResponse(status=404)