from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import MuongXen, User
from .forms import DateTimeSearchForm, LoginForm
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import numpy as np
import folium

def map(time=None):
    lat = 20
    lon = 104
    # Create a Map instance
    bounds = [[19, 102], [22, 108]]
    m = folium.Map(location=[lat, lon], zoom_start=8, min_zoom=7, max_bounds=True)  # [latuddue(vi do), longtitude(kinh do)]
    
    # folium.Rectangle(
    #     bounds=bounds,
    #     color='black',
    #     fill=False,
    #     weight=3
    # ).add_to(m)
    
    # Add bounds control to prevent panning outside ( start zoom+1)
    m.fit_bounds(bounds)
    
    # Add markers
    # folium.Marker(
    #     location=bounds[0],
    #     popup="Limit",
    #     icon=folium.Icon(color="black")
    # ).add_to(m)
    
    if time != None :
        entry = list(MuongXen.objects.filter(date_time=time).values_list('data',flat=True))

        try:
            # str_entry = repr(entry).replace("['", "[[").replace("']","]]")
            data = [num.split() for num in entry[0].split('\n')[::-1]]
            data_array = np.array(data, dtype=float)
            print("readed")
            # Create FeatureGroup for the data layer
            data_layer = folium.FeatureGroup(name='Data Layer', show=True)
            
            # Process each 0.1x0.1 degree cell
            for i in range(data_array.shape[0]):
                for j in range(data_array.shape[1]):
                    value = data_array[i,j]
                    # Calculate cell bounds (0.1x0.1 degree)
                    lat_min = 19 + i * 0.1  # Adjust starting lat as needed
                    lon_min = 102 + j * 0.1  # Adjust starting lon as needed
                    lat_max = lat_min + 0.1
                    lon_max = lon_min + 0.1
                    
                    # Set color based on value
                    # if value <= 1:
                    #     color = 'darkred' 
                    # else:
                    #     color = 'mediumspringgreen'
                    
                    
                    def set_color(value):
                        if value >= 25: return "brown"
                        if value >= 20: return "orangered"
                        if value >= 15: return "darkorange"
                        if value >= 10: return "gold"
                        if value >= 5: return "yellow"
                        if value >= 3: return "greenyellow"
                        if value >= 2: return "springgreen"
                        if value >= 1: return "deepskyblue"
                        if value >= 0.5: return "dodgerblue"
                        if value >= 0.1: return "blue"
                        if value >= 0: return "transparent" # '#FFFFFF00': transparent
                        return "gray"
                    color = set_color(value)
                    fill_color = color

                    # Add rectangle for this cell
                    folium.Rectangle(
                        bounds=[[lat_min, lon_min], [lat_max, lon_max]],
                        color=color,
                        fill=True,
                        fill_color=fill_color,
                        fill_opacity=0.7,
                        weight=0.5
                    ).add_to(data_layer)
                    
            data_layer.add_to(m)
        except Exception as e:
            print(f"Error loading data file: {e}")
    else:
        print("Time doesn't exist or wrong")
        
    # Add boundary rectangle (on top of data layer)
    # folium.Rectangle(
    #     bounds=bounds,
    #     color='#ff7800',
    #     fill=False,
    #     weight=2
    # ).add_to(m)
    
    #Khu vuc quy chau
    folium.Marker(
        location=[19.55722, 105.149253],
        popup="Quỳ Châu",
        icon=folium.Icon(color="blue")
    ).add_to(m)
    
    folium.Rectangle(
        bounds=[[19.5, 104],[20.5, 105.1]],
        color='blue',
        fill=False,
        weight=2
    ).add_to(m)

    #Khu vuc muong lat
    folium.Marker(
        location=[20.52461, 104.514255],
        popup="Mường Lát",
        icon=folium.Icon(color="red")
    ).add_to(m)
    
    folium.Rectangle(
        bounds=[[20.5, 102.4],[21.5, 104.5]],
        color='red',
        fill=False,
        weight=2
    ).add_to(m)

    #Khu vuc xa la
    folium.Marker(
        location=[20.936636, 103.926018],
        popup="Xã Là",
        
        icon=folium.Icon(color="gray")
    ).add_to(m)
    
    folium.Rectangle(
        bounds=[[20.9, 102.4],[21.5, 103.7]],
        color='gray',
        fill=False,
        weight=2
    ).add_to(m)

    #KHu vuc cua dat
    folium.Marker(
        location=[19.872367,105.284464],
        popup="Cửa Đạt",
        
        icon=folium.Icon(color="purple")
    ).add_to(m)

    folium.Rectangle(
        bounds=[[19.7, 104],[20.5, 105.3]],
        color='purple',
        fill=False,
        weight=2
    ).add_to(m)

    #Khu vuc muong xen
    folium.Marker(
        location=[19.4, 104.166667],
        popup="Mường Xén",
        icon=folium.Icon(color="green")
    ).add_to(m)

    folium.Rectangle(
        bounds=[[19, 102],[20.5, 104.2]],
        color='green',
        fill=False,
        weight=2
    ).add_to(m)

    # Define the legend's HTML
    legend_html = '''
    <div style="position: fixed; 
        bottom: 10px; left: 10px; width: 400px; height: 30px; 
        border:2px solid grey; z-index:9999; font-size:14px;
        background-color:white; opacity: 0.85;">
        <img src="../static/color_scale.png" alt="Color Scale">
    </div>
    '''

    # Add the legend to the map
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save the map to an HTML file
    m.save('./map/templates/map.html')

    # Get HTML representation of map
    return m._repr_html_()


def show_map(request):
    if request.method == 'POST':
        date_time = request.POST.get('date_time')
        # print("Datetime recieved! " + date_time)
        entry = list(MuongXen.objects.filter(date_time=date_time).values_list('data',flat=True))
        map_html = map(date_time)
 
    else:
        print("Not yet Post")
        date_time = None
        entry = None
        map_html = map()
 
        # return render(request, ['base.html'], {'date_time': date_time, 'entry':entry})

    return render(request, ['base.html'], {'map': map_html, 'date_time': date_time, 'entry':entry})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            search_username = User.objects.filter(username=username)
            if search_username is not None:
                search_password = list(search_username.values_list('password',flat=True))[0]
                if password == search_password:
                    
                    # return render(request, ['login-base.html'], context)
                    return redirect('login_base')
                else:
                    print("Sai pass")
            else:
                print("Invalid username or password")
        else:
            form = LoginForm()
            print("form not valid")
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')

def login_base(request):
    map_html = map()
    date_time = None
    context = {
        'map': map_html, 'date_time': date_time,
        'st_xala': None,
        'st_muonglat': None,
        'st_cuadat': None,
        'st_muongxen': None,
        'st_quychau':None 
    }
    if request.method == "POST":
        date_time = request.POST.get('date_time')
        search_entry = MuongXen.objects.filter(date_time=date_time)
        entry = list(search_entry.values_list('data',flat=True))
        if search_entry:
                context = {
                    'map': map_html, 'date_time': date_time, 'entry':entry,
                    'st_xala': list(search_entry.values_list('st_xa_la', flat=True))[0],
                    'st_muonglat': list(search_entry.values_list('st_muong_lat', flat=True))[0],
                    'st_cuadat': list(search_entry.values_list('st_cua_dat', flat=True))[0],
                    'st_muongxen': list(search_entry.values_list('st_muong_xen', flat=True))[0],
                    'st_quychau': list(search_entry.values_list('st_quy_chau', flat=True))[0]
                }
        else:
            print("No data found!")
        return render(request, 'login-base.html', context)
    return render(request, 'login-base.html', context)

def add_form(request):
    return render(request, 'add-form.html')