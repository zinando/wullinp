from django.shortcuts import render

# Create your views here.
def vendor_register(request):
    return render(request, 'vendor_register.html')