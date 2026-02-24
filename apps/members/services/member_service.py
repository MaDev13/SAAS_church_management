"""Member service."""

from apps.members.models import Member
from apps.members.repositories import MemberRepository
from middleware.tenant_context import get_church_id


class MemberService:
    def __init__(self):
        self.repo = MemberRepository()

    def list(self, status=None, ministry_id=None):
        church_id = get_church_id()
        if not church_id:
            return Member.objects.none()
        return self.repo.list_for_church(church_id, status=status, ministry_id=ministry_id)

    def get(self, member_id):
        church_id = get_church_id()
        if not church_id:
            return None
        return self.repo.get_by_id(member_id, church_id)

    def create(self, **kwargs):
        church_id = get_church_id()
        if not church_id:
            raise ValueError("Church context required")
        kwargs["church_id"] = church_id
        return Member.objects.create(**kwargs)
