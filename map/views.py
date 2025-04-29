from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import MuongXen
from .forms import DateTimeSearchForm, MxMap

# Create your views here.
def say_hello(request):
    # return HttpResponse('Hello World')
    data = MuongXen.objects.all()
    template = loader.get_template('hello3.html')
    context = {'data': data}
    return render(request, 'hello3.html',context)

# Good
# def get_mx_data(request):
#     if request.method == 'POST':
#         form = MxMap(request.POST)
#         print('d')
#         # if form.is_valid():
#         search_dt = form.cleaned_data['date_time']
#         print(search_dt)
#             # entry = form.save(commit=False)
#             # entry.data = "Sample data"
#             # entry.save()

#             #?????
#             # form.save()
#             # return redirect('get_mx_data')
#     else:
#         form = MxMap()

#     # entries = MuongXen.objects.all().order_by('-date_time')
#     entries = MuongXen.objects.get(date_time=search_dt)
#     if entries == None:
#         return render(request, 'hello3.html', {
#             'form': form
#         })
#     return render(request, 'hello3.html', {
#         'form': form,
#         'entries': entries
#     })

def get_mx_data(request):
    if request.method == 'POST':
        form = DateTimeSearchForm(request.POST)
        if form.is_valid():
            search_dt = form.cleaned_data['date_time']
            try:
                entry = MuongXen.objects.get(date_time=search_dt)
                return render(request, 'map.html', {'entry': entry})
            except MuongXen.DoesNotExist:
                return HttpResponse("No data found for this datetime")
    else:
        form = DateTimeSearchForm()
    
    return render(request, 'map.html', {'form': form})


# def get_mx_data(request):
#     form = MxMap()
#     datas = MuongXen.objects.get('data')
#     print(datas)
#     query_dict = request.GET
#     query = query_dict.get("q")
#     t_query = query.replace('T',' ')
#     print(type(t_query))
    
#     if form.is_valid():
#         print("form hop le")
#         date_time = form.cleaned_data.get('date_time')
#         if date_time:  
#             data = MuongXen.objects.filter(date_time=t_query)
#     print(data)
#     return render(request, 'hello3.html',{'rain_data': data})
