"""
Church repository - data access layer.
"""
from apps.churches.models import Church


class ChurchRepository:
    """Repository for Church CRUD operations."""

    @staticmethod
    def get_by_id(church_id):
        return Church.objects.filter(id=church_id).first()

    @staticmethod
    def create(name, city="", country=""):
        return Church.objects.create(name=name, city=city, country=country)

    @staticmethod
    def update(church, **kwargs):
        for key, value in kwargs.items():
            if hasattr(church, key):
                setattr(church, key, value)
        church.save()
        return church
