import json
from types import SimpleNamespace as Namespace

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from faker import Faker

from clients.models import Hacker, JobApplication, JobPosition, Exchange, Startup


def get_hackers():
    page = 1
    final_result = []
    while True:
        url = settings.GREEN_HOUSE_CANDIDATES_URL + f"?page={page}&per_page=500"
        response = requests.get(url, auth=(settings.GREEN_HOUSE_TOKEN, ''))
        result = json.loads(response.text, object_hook=lambda d: Namespace(**d))
        print(len(response.text))
        if len(result) == 0:
            break
        final_result = final_result + result
        page += 1
        print(response)
    print("out")
    return final_result


def insert_hacker(hacker_data):
    email_addresses = hacker_data.email_addresses
    hacker = None
    if email_addresses is not None and len(email_addresses) > 0:
        try:
            hacker = Hacker.objects.get(email=email_addresses[0].value)
        except Hacker.DoesNotExist:
            try:
                hacker = Hacker.objects.create(first_name=hacker_data.first_name, last_name=hacker_data.last_name,
                                               email=email_addresses[0].value, country="Morocco")
            except IntegrityError as e:
                print(e)

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
        if application.source is not None:
            job_application.source = application.source.public_name
        if application.rejection_reason is not None:
            job_application.rejection_reason = application.rejection_reason.name
        positions = get_or_create_job_positions(application.jobs)
        if len(positions) > 0:
            job_application.positions.add(*positions)
        job_application.save()


def store_hackers_data():
    """
    store hackers in the database
    * get data from external resources
    * insert data in database
    """
    hackers_data = get_hackers()
    for data in hackers_data:
        hacker = None
        if not isinstance(data, str):
            hacker = insert_hacker(data)
        if hacker is not None and len(data.applications) > 0:
            insert_hacker_job_applications(data.applications, hacker)


def simulate_send_message(from_email, to_email, from_type, to_type, message):
    Exchange.objects.create(message=message, from_email=from_email, to_email=to_email,
                            from_type=from_type, to_type=to_type)


def push_user_client_exchanges(fake, user, client, client_type):
    message = fake.sentence()
    simulate_send_message(from_email=user.email, to_email=client.email, from_type=Exchange.TEAM_MEMBER_TYPE,
                          to_type=client_type, message=message)
    message = fake.sentence()
    simulate_send_message(from_email=client.email, to_email=user.email, from_type=client_type,
                          to_type=Exchange.TEAM_MEMBER_TYPE, message=message)


def simulate_exchanges(times=1):
    Exchange.objects.all().delete()
    hackers = Hacker.objects.all()
    startups = Startup.objects.all()
    users = User.objects.all()
    fake = Faker()
    while times > 0:
        for user in users:
            for hacker in hackers:
                push_user_client_exchanges(fake=fake, user=user, client=hacker, client_type=Exchange.HACKER_TYPE)
            for startup in startups:
                push_user_client_exchanges(fake=fake, user=user, client=startup, client_type=Exchange.STARTUP_TYPE)
        times -= 1
