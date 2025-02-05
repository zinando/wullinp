from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vendor

# Create your views here.
def vendor_register(request):
    message = ''
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        contact_number = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        logo = request.FILES.get('logo')
        email = request.POST.get('email')

        # check if business_name already exists
        if Vendor.objects.filter(business_name=business_name).exists():
            message = 'Business name already exists.'
        # check if contact_number already exists
        elif Vendor.objects.filter(contact_number=contact_number).exists():
            message = 'Contact number already exists.'
        # check if email already exists
        elif Vendor.objects.filter(email=email).exists():
            message = 'Email already exists.'
        else:
            user = Vendor.objects.create_user(
                username=contact_number[-10:],
                business_name=business_name.lower(),
                contact_number=contact_number,
                address=address,
                logo=logo,
                email=email,
                password=password
            )
            user.save()
            messages.success(request, 'Account created successfully.', extra_tags='alert alert-success')
            return redirect('vendor_login')
    return render(request, 'vendor_register.html', {'error_message': message})