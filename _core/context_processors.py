from datetime import datetime

def site_name(request):
    # return the current year
    year = datetime.now().year
    return {'SITE_NAME_SHORT': 'WULLINP', 'SITE_NAME_FULL': 'WULLINP MALL', 'CURRENT_YEAR': year}
