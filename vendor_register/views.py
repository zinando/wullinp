from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from user_register.models import Profile

# Create your views here.
def vendor_register(request):
    """
    Registers a vendor in the Use table, then updates the Profile table or the User
    """
    message = ''
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        contact_number = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        logo = request.FILES.get('logo')
        email = request.POST.get('email') 

        # check if business_name already exists
        if business_name_exists(business_name):
            message = 'Business name already exists.'

        # check if contact_number already exists
        
        elif phone_exists(contact_number) and Profile.objects.filter(phone=contact_number).user_type == 'vendor':
            message = 'Another business account is linked with this number.'
        # check if email already exists
        elif email_exists(email) and User.objects.filter(email=email).profile.user.user_type == 'vendor':
            message = 'Email already exists.'
        else:
            # create user
            user = User.objects.create_user(
                username=contact_number[-10:], 
                email=email, 
                password=password, first_name=business_name, last_name=business_name)
            user.save() 

            # The signal will create the Profile automatically
            # Now, update the Profile with the form data
            profile = user.profile
            profile.phone = contact_number
            profile.business_name = business_name
            profile.address = address
            profile.logo = logo
            profile.user_type = 'vendor'
            profile.save()
            
            messages.success(request, 'Account created successfully.', extra_tags='alert alert-success')
            return redirect('vendor_login')
    return render(request, 'vendor_register.html', {'error_message': message})

def phone_exists(phone):
    return Profile.objects.filter(phone=phone).exists()
def email_exists(email):
    return User.objects.filter(email=email).exists()
def business_name_exists(business_name):
    return Profile.objects.filter(business_name=business_name).exists()