from typing import Optional

from django.contrib.auth.models import User


def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    authenticate the user by checking if the email and password
    are correct
    """
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None
