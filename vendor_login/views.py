from django.shortcuts import render
from vendor_register.models import Vendor
from _core.utils.helpers import check_if_username_is_phone_or_email

# Create your views here.
def vendor_login(request):
    if request.method == 'POST':
        user_id = request.POST['username']
        password = request.POST['password']
        username_type = check_if_username_is_phone_or_email(user_id)

        if username_type == 'email':
            email = user_id
        else:
            email = user_id[-10:]
        try:
            vendor = Vendor.objects.get(email=email)
            if vendor.password == password:
                return render(request, 'vendor_home.html', {'vendor': vendor})
            else:
                return render(request, 'vendor_login.html', {'error': 'Invalid Password'})
        except Vendor.DoesNotExist:
            return render(request, 'vendor_login.html', {'error': 'Vendor not found'})
    else:
        pass
    return render(request, 'vendor_login.html')


def fetch_username_with_email(email):
    user = Vendor.objects.filter(email=email).first()
    return user.username