"""Member repository."""

from apps.members.models import Member


class MemberRepository:
    @staticmethod
    def get_by_id(member_id, church_id):
        return Member.objects.filter(id=member_id, church_id=church_id).first()

    @staticmethod
    def list_for_church(church_id, status=None, ministry_id=None):
        qs = Member.objects.filter(church_id=church_id)
        if status:
            qs = qs.filter(status=status)
        if ministry_id:
            qs = qs.filter(ministry_id=ministry_id)
        return qs.order_by("last_name", "first_name")
