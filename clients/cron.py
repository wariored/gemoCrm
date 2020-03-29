import kronos

from clients.utils.client_helper import store_hackers_data


@kronos.register('* * * * *')
def import_hackers_data():
    store_hackers_data()
