"""
Tenant context middleware - injects church_id from JWT into request context.
Thread-safe using contextvars. Used by TenantManager and services.
"""
from contextvars import ContextVar
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

_church_id_var: ContextVar = ContextVar("church_id", default=None)
_user_var: ContextVar = ContextVar("user", default=None)


def get_church_id():
    """Get church_id for current request. Used by TenantManager and services."""
    return _church_id_var.get()


def get_current_user():
    """Get authenticated user for current request."""
    return _user_var.get()


def set_tenant_context(church_id, user):
    """Set tenant context (internal use by middleware)."""
    _church_id_var.set(church_id)
    _user_var.set(user)


def clear_tenant_context():
    """Clear tenant context (internal use by middleware)."""
    try:
        _church_id_var.set(None)
        _user_var.set(None)
    except LookupError:
        pass


class TenantContextMiddleware(MiddlewareMixin):
    """
    Extracts church_id and user from JWT and sets request.church_id, request.user.
    For API requests with Bearer token, validates JWT and loads user+church.
    For other requests (e.g. admin), does not set church_id.
    """

    def process_request(self, request):
        clear_tenant_context()
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        try:
            auth = JWTAuthentication()
            header = auth.get_header(request)
            if header is None:
                return None
            raw_token = auth.get_raw_token(header)
            validated_token = auth.get_validated_token(raw_token)
            user = auth.get_user(validated_token)
            if user and hasattr(user, "church_id"):
                church_id = user.church_id
            else:
                church_id = None
            request.church_id = church_id
            request.user = user
            set_tenant_context(church_id, user)
        except (AuthenticationFailed, Exception):
            request.church_id = None
            request.user = None
            set_tenant_context(None, None)
        return None

    def process_response(self, request, response):
        clear_tenant_context()
        return response
