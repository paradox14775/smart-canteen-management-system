from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(allowed_roles=None):
    """
    Decorator for views that checks if the logged-in user belongs to allowed roles.
    If not, redirects to their respective authorized home dashboard.
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            messages.error(
                request,
                f"Access denied. Your role ({user.get_role_display()}) is not authorized for this section."
            )
            return redirect('accounts:dashboard')

        return _wrapped_view

    return decorator


def student_required(view_func):
    return role_required(['STUDENT'])(view_func)


def admin_required(view_func):
    return role_required(['ADMIN'])(view_func)


def kitchen_required(view_func):
    return role_required(['KITCHEN', 'ADMIN'])(view_func)


def management_required(view_func):
    return role_required(['MANAGEMENT', 'ADMIN'])(view_func)

