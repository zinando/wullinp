"""functions that are useful for the rest of the codebase"""

def check_if_username_is_phone_or_email(username):
    if '@' in username:
        return 'email'
    else:
        return 'phone'
