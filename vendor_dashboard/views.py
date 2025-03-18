from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='vendor_login')
def vendor_dashboard(request):
    return render(request, 'vendor_dashboard.html')


# route for managing orders
@login_required(login_url='vendor_login')
def orders(request):
    action = request.GET.get('action')
    if action == 'get-pending-orders':
        return render(request, 'orders/pending_orders.html')
    return render(request, '404.html')