from django.contrib.auth.backends import ModelBackend
from vendor_register.models import Vendor  # Import your Vendor model
#from django.contrib.auth.models import User

class VendorBackend(ModelBackend):
    """
    Custom authentication backend to authenticate Vendors
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        #Vendor.objects.all().delete()
        #User.objects.all().delete()
        # try:
        #     vendor = Vendor.objects.get(username=username)  # Adjust if using email instead
        # except Vendor.DoesNotExist:
        #     return None
        
        # if vendor.check_password(password):
        #     return vendor
        # return None
        pass
