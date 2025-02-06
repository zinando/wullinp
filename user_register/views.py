from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.
def user_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = format_phone_number(request.POST.get('phone'))
        username = generate_username_from_phone_number(phone)

        # delete existing user data
        # if Profile.objects.filter(phone=phone).exists():
        #     Profile.objects.filter(phone=phone).delete()
        # if User.objects.filter(email=email).exists():
        #     User.objects.filter(email=email).delete()

        # check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'user_signup.html', {'error_message': 'User already exists'})
        # check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'user_signup.html', {'error_message': 'Email already exists'})

        # create user
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save() 

        # The signal will create the Profile automatically
        # Now, update the Profile with the form data
        profile = user.profile
        profile.phone = phone
        profile.save()
        
        # redirect user to login page with a success message
        base_url = reverse('user_login')
        query_param = '?message=Registration successful. Please login to continue'

        return redirect(f'{base_url}{query_param}')
    return render(request, 'user_signup.html')


def generate_username_from_phone_number(phone)->str:
    # username should be phone number without country code
    return f'{phone[-10:]}'

def format_phone_number(phone)->str:
    # phone number should be 11 digits starting with 0
    return f'0{phone[-10:]}'