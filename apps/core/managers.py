"""
Custom managers for multi-tenant filtering.
TenantManager filters querysets by church_id from thread-local context.
"""
from django.db import models


def get_current_church_id():
    """Get church_id from thread-local. Set by TenantContextMiddleware."""
    from middleware.tenant_context import get_church_id
    return get_church_id()


class TenantManager(models.Manager):
    """
    Manager that automatically filters by church_id.
    Use for models inheriting from TenantModel.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        church_id = get_current_church_id()
        if church_id is not None:
            return qs.filter(church_id=church_id)
        return qs
