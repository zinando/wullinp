from django.shortcuts import render

# Create your views here.
def user_login(request):
    message = ''
    errors = []
    if request.method == 'GET' and request.GET.get('message'):
        message = request.GET.get('message')
        
    return render(request, 'user_login.html', {'error_messages': errors, 'success_message': message})