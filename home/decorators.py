from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def custom_login_required(view_func):
    """
    Custom decorator that checks if the user is logged in and if they have set a password.
    If the user's password is still set to the default (default_password=True),
    they will be redirected to the change password page.
    """

    @login_required()  # Ensure user is logged in first
    def _wrapped_view(request, *args, **kwargs):
        if request.user.default_password:  # Check if the user needs to change their password
            return redirect('change-password')  # Redirect to change password page
        return view_func(request, *args, **kwargs)

    return _wrapped_view
