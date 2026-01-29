from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def role_required(role):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.profile.role != role:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator