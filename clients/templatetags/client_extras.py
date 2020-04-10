from django import template
from django.contrib.auth.models import User
from django.db.models import Q

from clients.models import Exchange
from gemoCrm.models import Role

register = template.Library()


@register.simple_tag
def exchanges_team_members_details(email: str):
    team_members = User.objects.filter(profile__roles__in=[Role.TALENT_ACQUISITION, Role.SALES])
    team_members_emails = team_members.values('email')
    exchanges = Exchange.objects \
        .filter(Q(from_email__in=team_members_emails) | Q(to_email__in=team_members_emails)) \
        .filter(Q(from_email=email) | Q(to_email=email))
    exchanges_grouped = {team_member.email: {"count": 0, "name": team_member.first_name} for team_member in
                         team_members}
    for exchange in exchanges:
        if exchange.from_email != email:
            exchanges_grouped[exchange.from_email]["count"] += 1
        if exchange.to_email != email:
            exchanges_grouped[exchange.to_email]["count"] += 1
    exchanges_grouped = {x: y for x, y in exchanges_grouped.items() if y["count"] > 0}
    return exchanges_grouped


@register.filter(name="status_class")
def status_class(status: str):
    return {
        "rejected": "text-danger",
        "hired": "text-success"
    }.get(status, "text-primary")
