from django.urls import reverse

from clients.models import Hacker, Startup, JobApplication, JobPosition


def get_search_result_reverse(search: str):
    if search.startswith('hacker:'):
        result = Hacker.objects.filter(email=extract_query(search, "hacker:"))
        if result:
            return result.first().get_absolute_url()
    elif search.startswith('startup:'):
        result = Startup.objects.filter(email=extract_query(search, "startup:"))
        if result:
            return result.first().get_absolute_url()
    elif search.startswith('application:'):
        result = JobApplication.objects.filter(external_id=extract_query(search, "application:"))
        if result:
            return result.first().get_absolute_url()
    elif search.startswith('position:'):
        result = JobPosition.objects.filter(external_id=extract_query(search, "position:"))
        if result:
            return result.first().get_absolute_url()
    return None


def extract_query(search, starter):
    search_split = search.split(starter)
    return search_split[1] if len(search_split) > 0 else ""
