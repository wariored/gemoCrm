import json
from types import SimpleNamespace as Namespace

import requests
from django.conf import settings

from clients.models import Hacker, JobApplication, JobPosition


def get_hackers():
    url = settings.GREEN_HOUSE_CANDIDATES_URL
    response = requests.get(url, auth=(settings.GREEN_HOUSE_TOKEN, ''))
    return json.loads(response.text, object_hook=lambda d: Namespace(**d))


def insert_hacker(hacker_data):
    email_addresses = hacker_data.email_addresses
    hacker = None
    if email_addresses is not None and len(email_addresses) > 0:
        try:
            hacker = Hacker.objects.get(email=email_addresses[0].value)
        except Hacker.DoesNotExist:
            hacker = Hacker.objects.create(first_name=hacker_data.first_name, last_name=hacker_data.last_name,
                                           email=email_addresses[0].value, country="Morocco")
    return hacker


def get_or_create_job_positions(data):
    positions = []
    for job in data:
        position, _ = JobPosition.objects.get_or_create(name=job.name, external_id=job.id)
        positions.append(position)
    return positions


def insert_hacker_job_applications(applications, hacker):
    for application in applications:
        job_application, _ = JobApplication.objects.get_or_create(external_id=application.id,
                                                                  hacker=hacker)
        job_application.rejected_at = application.rejected_at
        job_application.applied_at = application.applied_at
        job_application.status = application.status
        job_application.source = application.source
        if application.rejection_reason is not None:
            job_application.rejection_reason = application.rejection_reason.name
        positions = get_or_create_job_positions(application.jobs)
        if len(positions) > 0:
            job_application.positions.add(*positions)
        job_application.save()


def store_hackers_data():
    hackers_data = get_hackers()
    for data in hackers_data:
        hacker = None
        if not isinstance(data, str):
            hacker = insert_hacker(data)
        if hacker is not None and len(data.applications) > 0:
            insert_hacker_job_applications(data.applications, hacker)
        else:
            print(data.applications)
