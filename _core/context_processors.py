from datetime import datetime
from vendor_register.models import Vendor

def site_name(request):
    # return the current year
    year = datetime.now().year
    return {'SITE_NAME_SHORT': 'WULLINP', 'SITE_NAME_FULL': 'WULLINP MALL', 'CURRENT_YEAR': year}

def vendor_processor(request):
    """
    Adds the vendor object to the template context if the user is a Vendor.
    """
    if request.user.is_authenticated and isinstance(request.user, Vendor):
        return {"vendor": request.user}
    return {"vendor": None}
