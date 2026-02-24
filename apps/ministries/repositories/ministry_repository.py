"""Ministry repository."""

from apps.ministries.models import Ministry


class MinistryRepository:
    @staticmethod
    def get_by_id(ministry_id, church_id):
        return Ministry.objects.filter(id=ministry_id, church_id=church_id).first()

    @staticmethod
    def list_for_church(church_id):
        return Ministry.objects.filter(church_id=church_id).order_by("name")
