from django.shortcuts import render

def contact_page(request):
    # Mengambil file contacts.html di dalam folder templates/contacts/ 
    return render(request, 'contacts/contacts.html')