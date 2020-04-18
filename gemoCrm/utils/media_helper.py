import os
import uuid


def get_deal_file_path(instance, filename):
    return generate_or_get_file_path("deals", filename)


def get_contact_file_path(instance, filename):
    return generate_or_get_file_path("contacts", filename)


def generate_or_get_file_path(file_folder, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(f'{file_folder}/', filename)
