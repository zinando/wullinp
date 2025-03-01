from django.contrib.auth.models import User


def fetch_user(user_id):
    """This function fetches a single user"""
    user = User.objects.get(id=user_id)
    return user

def fetch_all_users():
    """This function fetches all users"""
    users = User.objects.all()
    return users