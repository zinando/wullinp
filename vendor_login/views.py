from django.shortcuts import render

# Create your views here.
def vendor_login(request):
    return render(request, 'vendor_login.html')
