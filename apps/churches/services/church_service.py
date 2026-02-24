"""
Church service - business logic layer.
"""
from apps.churches.repositories import ChurchRepository


class ChurchService:
    """Service for Church operations."""

    def __init__(self):
        self.repo = ChurchRepository()

    def get_church(self, church_id):
        return self.repo.get_by_id(church_id)

    def create_church(self, name, city="", country=""):
        return self.repo.create(name=name, city=city, country=country)
