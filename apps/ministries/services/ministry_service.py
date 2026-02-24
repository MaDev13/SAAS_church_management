"""Ministry service."""

from apps.ministries.models import Ministry
from apps.ministries.repositories import MinistryRepository
from middleware.tenant_context import get_church_id


class MinistryService:
    def __init__(self):
        self.repo = MinistryRepository()

    def list(self):
        church_id = get_church_id()
        if not church_id:
            return Ministry.objects.none()
        return self.repo.list_for_church(church_id)

    def get(self, ministry_id):
        church_id = get_church_id()
        if not church_id:
            return None
        return self.repo.get_by_id(ministry_id, church_id)

    def create(self, name, description=""):
        church_id = get_church_id()
        if not church_id:
            raise ValueError("Church context required")
        from apps.churches.models import Church
        return Ministry.objects.create(church_id=church_id, name=name, description=description)
