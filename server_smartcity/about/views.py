from django.shortcuts import render

def about_page(request):
    # Mengambil file about.html di dalam folder templates/about/ 
    return render(request, 'about/about.html')