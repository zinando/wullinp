from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView

# Create your views here.
@login_required(login_url='user_login')
def wishlist(request):
    return render(request, 'wishlist.html')

# create CBV for wishlist
class WishlistView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass